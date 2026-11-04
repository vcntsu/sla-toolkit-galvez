#!/usr/bin/env python3
"""
calc_sla.py — Calculadora de cumplimiento de SLA y crédito de servicio.

Lee un CSV de mediciones (fecha,metrica,valor,unidad) y un archivo de objetivos (YAML),
entrega un veredicto por métrica (CUMPLE / NO CUMPLE / EVIDENCIA INSUFICIENTE) y calcula
el crédito de servicio.

Uso:
    python herramientas/calc_sla.py \
        --mediciones datos/mediciones-ejemplo.csv \
        --objetivos  herramientas/objetivos.yaml \
        [--salida ejemplos/enlace-dedicado/informe.md] [--fecha-emision AAAA-MM-DD]

Sin argumentos usa los archivos de ejemplo del repositorio.

Métricas esperadas en el CSV:
    caida (min), mantenimiento (min), latencia (ms), jitter (ms), perdida (%), throughput (Mbps)
La disponibilidad se calcula a partir de caida y mantenimiento.

Códigos de salida: 0 todo cumple · 1 hay incumplimientos · 2 sin incumplimientos pero con
evidencia insuficiente · 3 error en los archivos de entrada.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Falta PyYAML. Instálalo con:  pip install pyyaml")

CUMPLE = "CUMPLE"
NO_CUMPLE = "NO CUMPLE"
INSUFICIENTE = "EVIDENCIA INSUFICIENTE"
MIN_POR_DIA = 1440
COLUMNAS = ("fecha", "metrica", "valor", "unidad")
AUXILIARES = {"caida", "mantenimiento"}  # métricas de apoyo para disponibilidad
OPERADORES = (">=", "<=")


class ErrorEntrada(Exception):
    """Problema en los archivos de entrada."""


@dataclass
class Resultado:
    metrica: str
    descripcion: str
    objetivo: float
    operador: str
    unidad: str
    agregacion: str
    muestras: int
    min_muestras: int
    valor: float | None
    veredicto: str
    detalle: str = ""


# ----------------------------------------------------------------------------- carga
def cargar_objetivos(ruta: Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ErrorEntrada("El archivo de objetivos está vacío o no es válido.")
    for clave in ("servicio", "periodo", "metricas"):
        if clave not in cfg:
            raise ErrorEntrada(f"Falta la clave '{clave}' en el archivo de objetivos.")
    if "dias" not in cfg["periodo"]:
        raise ErrorEntrada("Falta 'periodo.dias' en el archivo de objetivos.")
    for nombre, m in cfg["metricas"].items():
        for k in ("objetivo", "operador", "unidad", "min_muestras"):
            if k not in m:
                raise ErrorEntrada(f"Métrica '{nombre}': falta '{k}'.")
        if m["operador"] not in OPERADORES:
            raise ErrorEntrada(f"Métrica '{nombre}': operador debe ser '>=' o '<='.")
        if nombre != "disponibilidad":
            m.setdefault("agregacion", "promedio")
            if not re.fullmatch(r"promedio|p\d{1,3}(\.\d+)?", str(m["agregacion"])):
                raise ErrorEntrada(f"Métrica '{nombre}': agregación inválida ({m['agregacion']}).")
    return cfg


def cargar_mediciones(ruta: Path) -> tuple[dict, list[str]]:
    datos: dict[str, list[tuple[str, float, str]]] = defaultdict(list)
    avisos: list[str] = []
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        faltan = set(COLUMNAS) - set(lector.fieldnames or [])
        if faltan:
            raise ErrorEntrada(f"Al CSV le faltan columnas: {', '.join(sorted(faltan))}.")
        for n, fila in enumerate(lector, start=2):
            try:
                valor = float(fila["valor"])
                if math.isnan(valor) or math.isinf(valor):
                    raise ValueError
            except (TypeError, ValueError):
                avisos.append(f"Línea {n}: valor no numérico ({fila['valor']!r}); se ignora.")
                continue
            datos[fila["metrica"].strip()].append((fila["fecha"].strip(), valor, fila["unidad"].strip()))
    return datos, avisos


# ----------------------------------------------------------------------------- cálculo
def percentil(valores: list[float], p: float) -> float:
    """Percentil por rango más cercano (nearest-rank)."""
    s = sorted(valores)
    k = max(1, math.ceil(p / 100 * len(s)))
    return s[k - 1]


def agregar(valores: list[float], modo: str) -> float:
    if modo == "promedio":
        return sum(valores) / len(valores)
    return percentil(valores, float(modo[1:]))


def _filtrar_unidad(filas, unidad, metrica, avisos):
    ok = [(f, v) for (f, v, u) in filas if u == unidad]
    descartadas = len(filas) - len(ok)
    if descartadas:
        avisos.append(f"{metrica}: {descartadas} medición(es) con unidad distinta de '{unidad}' se ignoraron.")
    return ok


def _cumple(valor: float, objetivo: float, operador: str) -> bool:
    eps = 1e-9
    return valor >= objetivo - eps if operador == ">=" else valor <= objetivo + eps


def evaluar_disponibilidad(cfg: dict, datos: dict, avisos: list[str]) -> Resultado:
    m = cfg["metricas"]["disponibilidad"]
    t_total = cfg["periodo"]["dias"] * MIN_POR_DIA
    caidas = _filtrar_unidad(datos.get("caida", []), "min", "caida", avisos)
    mant = _filtrar_unidad(datos.get("mantenimiento", []), "min", "mantenimiento", avisos)
    muestras = len({f for f, _ in caidas})
    mant_min = sum(v for _, v in mant)
    caida_min = sum(v for _, v in caidas)
    t_ef = t_total - mant_min
    permitida = t_ef * (1 - m["objetivo"] / 100)
    detalle = (f"T efectivo {t_ef:.0f} min (período {t_total} − mantención {mant_min:.0f}); "
               f"caída acumulada {caida_min:.1f} min; caída permitida {permitida:.2f} min.")
    r = Resultado("disponibilidad", m.get("descripcion", "Disponibilidad"), m["objetivo"], m["operador"],
                  m["unidad"], "acumulado", muestras, m["min_muestras"], None, INSUFICIENTE, detalle)
    if muestras < m["min_muestras"]:
        r.detalle = f"Solo {muestras} día(s) con registro de caídas; se requieren {m['min_muestras']}. " + detalle
        return r
    if t_ef <= 0:
        raise ErrorEntrada("La mantención excluida es mayor o igual al período.")
    r.valor = (t_ef - caida_min) / t_ef * 100
    r.veredicto = CUMPLE if _cumple(r.valor, m["objetivo"], m["operador"]) else NO_CUMPLE
    return r


def evaluar_metrica(nombre: str, m: dict, datos: dict, avisos: list[str]) -> Resultado:
    valores = [v for _, v in _filtrar_unidad(datos.get(nombre, []), m["unidad"], nombre, avisos)]
    r = Resultado(nombre, m.get("descripcion", nombre), m["objetivo"], m["operador"], m["unidad"],
                  m["agregacion"], len(valores), m["min_muestras"], None, INSUFICIENTE)
    if len(valores) < m["min_muestras"]:
        r.detalle = f"{len(valores)} muestra(s) válidas; se requieren {m['min_muestras']}."
        return r
    r.valor = agregar(valores, m["agregacion"])
    r.veredicto = CUMPLE if _cumple(r.valor, m["objetivo"], m["operador"]) else NO_CUMPLE
    return r


def evaluar(cfg: dict, datos: dict, avisos: list[str]) -> list[Resultado]:
    resultados = []
    for nombre, m in cfg["metricas"].items():
        if nombre == "disponibilidad":
            resultados.append(evaluar_disponibilidad(cfg, datos, avisos))
        else:
            resultados.append(evaluar_metrica(nombre, m, datos, avisos))
    conocidas = set(cfg["metricas"]) | AUXILIARES
    for extra in sorted(set(datos) - conocidas):
        avisos.append(f"La métrica '{extra}' del CSV no tiene objetivo definido; se ignoró.")
    return resultados


def calcular_credito(resultados: list[Resultado], cfg: dict) -> dict:
    c = cfg.get("creditos") or {}
    tope = c.get("tope_pct", 100)
    por_metrica = c.get("por_metrica_incumplida_pct", 0)
    lineas: list[tuple[str, float]] = []
    for r in resultados:
        if r.metrica == "disponibilidad" and r.veredicto == NO_CUMPLE:
            for e in sorted(c.get("escalones_disponibilidad", []), key=lambda e: e["menor_a"]):
                if r.valor < e["menor_a"]:
                    lineas.append((f"Disponibilidad {r.valor:.3f} % < {e['menor_a']:g} %", e["credito_pct"]))
                    break
        elif r.metrica != "disponibilidad" and r.veredicto == NO_CUMPLE and por_metrica:
            lineas.append((f"{r.metrica.capitalize()} no cumple", por_metrica))
    bruto = sum(p for _, p in lineas)
    total = min(bruto, tope)
    cuota = c.get("cuota_mensual", 0)
    return {"lineas": lineas, "bruto": bruto, "tope": tope, "total_pct": total,
            "cuota": cuota, "monto": cuota * total / 100, "moneda": c.get("moneda", "")}


def veredicto_global(resultados: list[Resultado]) -> str:
    if any(r.veredicto == NO_CUMPLE for r in resultados):
        return NO_CUMPLE
    if any(r.veredicto == INSUFICIENTE for r in resultados):
        return INSUFICIENTE
    return CUMPLE


# ----------------------------------------------------------------------------- salida
def _medido(r: Resultado) -> str:
    if r.valor is None:
        return "—"
    dec = 3 if r.metrica == "disponibilidad" else 2
    return f"{r.valor:.{dec}f} {r.unidad}"


def _objetivo(r: Resultado) -> str:
    return f"{r.operador} {r.objetivo:g} {r.unidad}"


def imprimir_consola(cfg, resultados, credito, avisos) -> None:
    p = cfg["periodo"]
    print(f"SLA: {cfg['servicio']}  |  Período: {p.get('etiqueta', '')} ({p['dias']} días)\n")
    print(f"{'Métrica':<16}{'Objetivo':<16}{'Medido':<16}{'Muestras':<14}{'Veredicto'}")
    print("-" * 78)
    for r in resultados:
        print(f"{r.metrica:<16}{_objetivo(r):<16}{_medido(r):<16}{f'{r.muestras} (mín {r.min_muestras})':<14}{r.veredicto}")
    print(f"\nVeredicto global: {veredicto_global(resultados)}")
    print(f"Crédito de servicio: {credito['total_pct']:g} %  =  {credito['monto']:,.0f} {credito['moneda']}")
    for texto, pct in credito["lineas"]:
        print(f"  - {texto}: {pct:g} %")
    for r in resultados:
        if r.veredicto == INSUFICIENTE:
            print(f"  ! {r.metrica}: {r.detalle}")
    for a in avisos:
        print(f"  aviso: {a}")


def generar_informe(cfg, resultados, credito, avisos, args, sha) -> str:
    p = cfg["periodo"]
    disp = next((r for r in resultados if r.metrica == "disponibilidad"), None)
    L = ["# Informe de cumplimiento de SLA", "",
         f"> Generado automáticamente con `herramientas/calc_sla.py`.", "",
         "## 1. Identificación", "",
         "| Campo | Valor |", "|-------|-------|",
         f"| Servicio | {cfg['servicio']} |",
         f"| Cliente / Proveedor | {cfg.get('cliente', '—')} / {cfg.get('proveedor', '—')} |",
         f"| Período evaluado | {p.get('etiqueta', '')} ({p.get('inicio', '')}, {p['dias']} días) |",
         f"| Fecha de emisión | {args.fecha_emision} |", "",
         "## 2. Resumen", "",
         f"- **Veredicto global:** {veredicto_global(resultados)}",
         f"- **Crédito de servicio:** {credito['total_pct']:g} % = {credito['monto']:,.0f} {credito['moneda']}", "",
         "## 3. Resultados por métrica", "",
         "| Métrica | Objetivo | Medido | Muestras (mín.) | Agregación | Veredicto |",
         "|---------|----------|--------|-----------------|------------|-----------|"]
    for r in resultados:
        L.append(f"| {r.metrica.capitalize()} | {_objetivo(r)} | {_medido(r)} | {r.muestras} ({r.min_muestras}) | {r.agregacion} | **{r.veredicto}** |")
    if disp:
        L += ["", "## 4. Detalle de disponibilidad", "", f"- {disp.detalle}"]
    L += ["", "## 5. Crédito de servicio", "", "| Concepto | % |", "|----------|---|"]
    for texto, pct in credito["lineas"]:
        L.append(f"| {texto} | {pct:g} |")
    if not credito["lineas"]:
        L.append("| Sin incumplimientos | 0 |")
    L.append(f"| **Total (tope {credito['tope']:g} %)** | **{credito['total_pct']:g}** |")
    L += ["", f"Cuota mensual: {credito['cuota']} {credito['moneda']} → crédito **{credito['monto']:,.0f} {credito['moneda']}**.", "",
          "## 6. Observaciones", ""]
    insuf = [r for r in resultados if r.veredicto == INSUFICIENTE]
    for r in insuf:
        L.append(f"- **{r.metrica.capitalize()}**: evidencia insuficiente. {r.detalle} No genera crédito hasta completar las mediciones.")
    for a in avisos:
        L.append(f"- Aviso: {a}")
    if not insuf and not avisos:
        L.append("- Sin observaciones.")
    L += ["", "## 7. Reproducibilidad", "",
          f"- Mediciones: `{args.mediciones}` (SHA-256 `{sha[:16]}…`)",
          f"- Objetivos: `{args.objetivos}`",
          f"- Comando: `python herramientas/calc_sla.py --mediciones {args.mediciones} --objetivos {args.objetivos} --salida {args.salida or '<informe.md>'}`", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    raiz = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Verifica el cumplimiento de un SLA y calcula el crédito de servicio.")
    ap.add_argument("--mediciones", default=str(raiz / "datos" / "mediciones-ejemplo.csv"), help="CSV: fecha,metrica,valor,unidad")
    ap.add_argument("--objetivos", default=str(raiz / "herramientas" / "objetivos.yaml"), help="YAML con los objetivos del SLA")
    ap.add_argument("--salida", help="Ruta del informe en Markdown (opcional)")
    ap.add_argument("--fecha-emision", default=date.today().isoformat(), help="Fecha del informe (AAAA-MM-DD)")
    args = ap.parse_args(argv)
    try:
        cfg = cargar_objetivos(Path(args.objetivos))
        datos, avisos = cargar_mediciones(Path(args.mediciones))
        resultados = evaluar(cfg, datos, avisos)
        credito = calcular_credito(resultados, cfg)
        sha = hashlib.sha256(Path(args.mediciones).read_bytes()).hexdigest()
    except (ErrorEntrada, OSError, yaml.YAMLError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3
    imprimir_consola(cfg, resultados, credito, avisos)
    if args.salida:
        Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
        Path(args.salida).write_text(generar_informe(cfg, resultados, credito, avisos, args, sha), encoding="utf-8")
        print(f"\nInforme escrito en {args.salida}")
    g = veredicto_global(resultados)
    return {CUMPLE: 0, NO_CUMPLE: 1, INSUFICIENTE: 2}[g]


if __name__ == "__main__":
    sys.exit(main())