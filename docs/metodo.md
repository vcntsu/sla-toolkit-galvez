# Método de diseño de un SLA en 6 pasos

Base: **ITIL 4 – Service Level Management** (proceso) + **ITU-T E.860** (estructura del SLA de telecomunicaciones).

> **Regla base:** no se compromete un objetivo que la infraestructura no pueda cumplir ni que no se pueda medir.

```
1 Servicio → 2 Requisitos (SLR) → 3 Métricas (SLI) → 4 Objetivos (SLO) → 5 Operación y medición → 6 Consecuencias y revisión
                                                                                                          │
                                                                    mejora continua (PDCA) ◄──────────────┘
```

## Resumen

| # | Paso | Norma principal | Qué produce | Archivo del toolkit |
|---|------|-----------------|-------------|---------------------|
| 1 | Definir el servicio | ITU-T E.860 (ISO/IEC 19086-1 si es cloud) | Descripción, partes, alcance, demarcación | `plantillas/plantilla-sla.md` §1–3 |
| 2 | Levantar requisitos (SLR) | ITIL 4 SLM | Checklist completado y SLR priorizados | `plantillas/checklist-requisitos.md` |
| 3 | Elegir métricas (SLI) | Y.1540, MEF 10.4, RFC 7679/7680/3393/5357/6349 | Tabla de SLI con método de medición normado | `plantillas/plantilla-sla.md` §5 |
| 4 | Fijar objetivos (SLO) | Y.1540/Y.1541, G.114, MEF 10.4 | SLO viables con memoria de cálculo | `formulas/formulas.md` |
| 5 | Definir operación y medición | ITIL 4, E.860, RFC 5357 | Período, herramienta, exclusiones, MTTR, escalamiento, reportes | `herramientas/objetivos.yaml`, `datos/*.csv` |
| 6 | Definir consecuencias y revisión | ISO/IEC 20000-1 (PDCA), ITIL 4 | Créditos, tope, ciclo de revisión | `plantillas/informe-cumplimiento.md`, `CHANGELOG.md` |

---

## Paso 1 — Definir el servicio
- **Qué se hace:** describir qué se entrega, a quién, el alcance (incluido y excluido), los roles de cada parte y el **punto de demarcación** (dónde termina la responsabilidad del proveedor).
- **Norma:** ITU-T E.860 (partes que debe tener un SLA de telecomunicaciones). ISO/IEC 19086-1 para servicios cloud.
- **Produce:** secciones de partes, servicio, alcance y demarcación del SLA.

## Paso 2 — Levantar los requisitos del cliente (SLR)
- **Qué se hace:** entrevistar al cliente y traducir su necesidad de negocio a requisitos en *su* lenguaje (ej.: "las videollamadas no pueden cortarse en horario laboral"). Se registran criticidad, horarios y costo de una caída.
- **Norma:** ITIL 4 – Service Level Management.
- **Produce:** checklist completado + lista priorizada de SLR.

## Paso 3 — Elegir las métricas (SLI)
- **Qué se hace:** convertir cada SLR en un indicador medible: disponibilidad, latencia, jitter, pérdida y throughput. Cada uno con definición, punto de medición, unidad y método normado.
- **Norma:** ITU-T Y.1540 (IP), MEF 10.4 (Ethernet), RFC 7679/7680 (retardo/pérdida), RFC 3393 (jitter), RFC 5357 TWAMP (medición activa), RFC 6349 (throughput TCP).
- **Produce:** tabla de SLI (métrica · definición · norma · método · punto de medición · unidad).

## Paso 4 — Fijar objetivos viables (SLO)
- **Qué se hace:** calcular qué puede entregar la infraestructura **antes** de comprometerse: disponibilidad en serie/paralelo de la cadena, latencia mínima física por distancia, capacidad vs. throughput esperado. Fijar el objetivo con margen y contrastarlo con el SLR (voz: ≤ 150 ms, G.114). Revisar los OLA/contratos de soporte con terceros.
- **Norma:** Y.1540 / Y.1541, G.114, MEF 10.4.
- **Produce:** tabla de SLO + memoria de cálculo que demuestre la viabilidad (regla base).

## Paso 5 — Definir operación y medición
- **Qué se hace:** período de medición, herramienta y frecuencia de muestreo, **mínimo de muestras** para que haya evidencia, agregación (promedio, p95), exclusiones (mantención programada, fuerza mayor, causas del cliente), horarios de soporte, tiempos de respuesta y MTTR, escalamiento y formato de reportes.
- **Norma:** ITIL 4, ITU-T E.860, RFC 5357, ISO/IEC 20000-1.
- **Produce:** sección de operación del SLA, `objetivos.yaml` y plan de recolección de mediciones (CSV).

## Paso 6 — Definir consecuencias y revisión
- **Qué se hace:** créditos escalonados por incumplimiento, tope, procedimiento de reclamo y revisión periódica del SLA (ciclo **PDCA**: Planificar, Hacer, Verificar, Actuar).
- **Norma:** ISO/IEC 20000-1 (PDCA), ITIL 4, ITU-T E.860.
- **Produce:** tabla de créditos, calendario de revisión e informe de cumplimiento periódico.

---

## Cómo se usa en la práctica
1. Copiar `plantillas/checklist-requisitos.md` y completarlo con el cliente (paso 2).
2. Copiar `plantillas/plantilla-sla.md` y completar los pasos 1, 3, 4, 5 y 6; verificar viabilidad con `formulas/formulas.md`.
3. Traspasar los objetivos a `herramientas/objetivos.yaml`.
4. Recolectar mediciones en CSV y ejecutar `herramientas/calc_sla.py`.
5. Entregar el informe y revisar el SLA según el ciclo definido (paso 6).
