# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versionado semántico.

## [1.0.0] - 2026-11-03
### Agregado
- Método de diseño de SLA en 6 pasos (`docs/metodo.md`).
- Normas de referencia y su uso por paso (`docs/normas.md`) y glosario (`docs/glosario.md`).
- Plantillas: SLA en blanco, checklist de requisitos del cliente e informe de cumplimiento.
- Fórmulas con variables, unidades, norma y ejemplo: disponibilidad, caída permitida, serie, paralelo, throughput y eficiencia, pérdida, jitter, latencia por distancia y crédito de servicio.
- Calculadora `herramientas/calc_sla.py`: lee CSV + YAML, veredicto por métrica (cumple / no cumple / evidencia insuficiente), crédito de servicio e informe en Markdown.
- Datos de ejemplo e informe del caso de enlace dedicado de Internet.
- README con uso, requisitos y flujo de trabajo Git.

## [Sin publicar]
### Planificado
- Cálculo de MTTR/MTBF, salida JSON, calculadora serie/paralelo en CLI.
