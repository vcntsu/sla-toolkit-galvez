# Informe de cumplimiento de SLA

> Generado automáticamente con `herramientas/calc_sla.py`.

## 1. Identificación

| Campo | Valor |
|-------|-------|
| Servicio | Enlace dedicado de Internet 100 Mbps simétrico |
| Cliente / Proveedor | Empresa Ejemplo SpA / Proveedor Ejemplo Telecom |
| Período evaluado | Octubre 2026 (2026-10-01, 31 días) |
| Fecha de emisión | 2026-11-03 |

## 2. Resumen

- **Veredicto global:** NO CUMPLE
- **Crédito de servicio:** 10 % = 45,000 CLP

## 3. Resultados por métrica

| Métrica | Objetivo | Medido | Muestras (mín.) | Agregación | Veredicto |
|---------|----------|--------|-----------------|------------|-----------|
| Disponibilidad | >= 99.9 % | 99.854 % | 31 (28) | acumulado | **NO CUMPLE** |
| Latencia | <= 20 ms | 14.30 ms | 31 (28) | p95 | **CUMPLE** |
| Jitter | <= 10 ms | 3.40 ms | 31 (28) | p95 | **CUMPLE** |
| Perdida | <= 0.1 % | 0.02 % | 31 (28) | promedio | **CUMPLE** |
| Throughput | >= 90 Mbps | — | 3 (4) | promedio | **EVIDENCIA INSUFICIENTE** |

## 4. Detalle de disponibilidad

- T efectivo 44520 min (período 44640 − mantención 120); caída acumulada 65.0 min; caída permitida 44.52 min.

## 5. Crédito de servicio

| Concepto | % |
|----------|---|
| Disponibilidad 99.854 % < 99.9 % | 10 |
| **Total (tope 60 %)** | **10** |

Cuota mensual: 450000 CLP → crédito **45,000 CLP**.

## 6. Observaciones

- **Throughput**: evidencia insuficiente. 3 muestra(s) válidas; se requieren 4. No genera crédito hasta completar las mediciones.

## 7. Reproducibilidad

- Mediciones: `datos/mediciones-ejemplo.csv` (SHA-256 `642d3e2bbef12317…`)
- Objetivos: `herramientas/objetivos.yaml`
- Comando: `python herramientas/calc_sla.py --mediciones datos/mediciones-ejemplo.csv --objetivos herramientas/objetivos.yaml --salida ejemplos/enlace-dedicado/informe.md`
