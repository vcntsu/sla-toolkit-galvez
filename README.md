# sla-toolkit-galvez

Toolkit para **diseñar, calcular y verificar SLA de servicios de red**. Reúne un método de diseño (ITIL 4 + ITU-T E.860), las normas de medición, plantillas, fórmulas y una calculadora en Python que aplica esas fórmulas a mediciones reales.

> Actividad formativa de Ingeniería en Telecomunicaciones, INACAP sede La Serena. Autor: Vicente Gálvez Pastén.

## Qué incluye

| Componente | Ubicación |
|------------|-----------|
| Método de diseño en 6 pasos | [`docs/metodo.md`](docs/metodo.md) |
| Normas (ITIL 4, ISO 20000-1, E.860, Y.1540/1541, MEF 10.4, RFC…) | [`docs/normas.md`](docs/normas.md) |
| Glosario (SLA, SLI, SLO, SLR, OLA, MTBF, MTTR…) | [`docs/glosario.md`](docs/glosario.md) |
| Plantillas: SLA, checklist de requisitos, informe | [`plantillas/`](plantillas/) |
| Fórmulas con variables, unidades, norma y ejemplo | [`formulas/formulas.md`](formulas/formulas.md) |
| Calculadora de cumplimiento y créditos | [`herramientas/calc_sla.py`](herramientas/calc_sla.py) |
| Caso completo: enlace dedicado de Internet | [`ejemplos/enlace-dedicado/`](ejemplos/enlace-dedicado/) |

## Requisitos
- Python 3.9 o superior
- PyYAML: `pip install pyyaml`
- Git (para versionar tus propios SLA)

## Uso rápido

```bash
git clone https://github.com/<tu-usuario>/sla-toolkit-galvez.git
cd sla-toolkit-galvez
pip install pyyaml

python herramientas/calc_sla.py \
  --mediciones datos/mediciones-ejemplo.csv \
  --objetivos herramientas/objetivos.yaml \
  --salida ejemplos/enlace-dedicado/informe.md
```

Salida del caso de ejemplo (octubre 2026): disponibilidad 99.854 % → **NO CUMPLE** (crédito 10 % = 45 000 CLP); latencia, jitter y pérdida **CUMPLEN**; throughput **EVIDENCIA INSUFICIENTE** (3 de 4 pruebas semanales).

### Para un servicio nuevo
1. Completa `plantillas/checklist-requisitos.md` con el cliente.
2. Copia `plantillas/plantilla-sla.md` y complétala; valida viabilidad con `formulas/formulas.md`.
3. Copia `herramientas/objetivos.yaml` y ajusta objetivos, mínimos de muestras y créditos.
4. Registra mediciones en un CSV y ejecuta `calc_sla.py`.

### Formato del CSV de mediciones
```csv
fecha,metrica,valor,unidad
2026-10-01,caida,0,min
2026-10-01,latencia,9.8,ms
```
Métricas: `caida` (min), `mantenimiento` (min, se excluye del período), `latencia` (ms), `jitter` (ms), `perdida` (%), `throughput` (Mbps). La disponibilidad se calcula con `caida` y `mantenimiento`. Las filas con valor no numérico o unidad distinta se ignoran y se informan como aviso.

### Archivo de objetivos (`objetivos.yaml`)
Define el período, cada métrica (`objetivo`, `operador` `>=`/`<=`, `unidad`, `agregacion` `promedio`/`pNN`, `min_muestras`) y los créditos (escalones de disponibilidad, % por métrica incumplida, tope, cuota mensual).

### Veredictos y código de salida
| Veredicto | Cuándo |
|-----------|--------|
| CUMPLE | Hay muestras suficientes y el valor cumple el objetivo |
| NO CUMPLE | Hay muestras suficientes y el valor no cumple |
| EVIDENCIA INSUFICIENTE | Menos muestras que el mínimo definido |

Salida `0` todo cumple · `1` hay incumplimientos · `2` solo evidencia insuficiente · `3` error de entrada.

## Estructura
```
sla-toolkit-galvez/
├── README.md · LICENSE · CHANGELOG.md
├── docs/            metodo.md · normas.md · glosario.md
├── plantillas/      plantilla-sla.md · checklist-requisitos.md · informe-cumplimiento.md
├── formulas/        formulas.md
├── herramientas/    calc_sla.py · objetivos.yaml
├── datos/           mediciones-ejemplo.csv
└── ejemplos/enlace-dedicado/   sla.md · informe.md
```

## Flujo de trabajo con Git
- Una rama por componente (`docs/metodo`, `feat/calculadora`, `feat/plantillas`…), commits descriptivos (`feat: …`, `docs: …`) e integración a `main` con merge.
- Cada versión se registra en [`CHANGELOG.md`](CHANGELOG.md) y se publica con un tag (`v1.0`, `v1.1`, `v2.0`…).

## Hoja de ruta
- v1.1: cálculo de MTTR/MTBF desde un registro de incidentes y salida en JSON.
- v1.2: calculadora de disponibilidad serie/paralelo desde la línea de comandos.
- v2.0: nuevos casos (Carrier Ethernet MEF, servicio cloud ISO/IEC 19086-1).

## Licencia
MIT — ver [`LICENSE`](LICENSE).
