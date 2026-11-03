# Informe de cumplimiento de SLA

> Plantilla del informe técnico de verificación. `herramientas/calc_sla.py --salida` genera este mismo formato ya completado.

## 1. Identificación
| Campo | Valor |
|-------|-------|
| Servicio | [...] |
| Cliente / Proveedor | [...] / [...] |
| Período evaluado | [...] |
| Fecha de emisión | [...] |
| Versión del SLA | [...] |

## 2. Resumen
- **Veredicto global:** [CUMPLE / NO CUMPLE / EVIDENCIA INSUFICIENTE]
- **Crédito de servicio:** [__ % = __ CLP]

## 3. Resultados por métrica
| Métrica | Objetivo | Medido | Muestras (mín.) | Agregación | Veredicto |
|---------|----------|--------|-----------------|------------|-----------|
| Disponibilidad | | | | | |
| Latencia | | | | | |
| Jitter | | | | | |
| Pérdida | | | | | |
| Throughput | | | | | |

## 4. Detalle de disponibilidad
- Tiempo del período (T): [__ min] · Mantención excluida: [__ min]
- Caída acumulada: [__ min] · Caída permitida: [__ min]

## 5. Incidentes del período
| Fecha | Duración | Causa | Severidad | MTTR |
|-------|----------|-------|-----------|------|

## 6. Crédito de servicio
| Concepto | % |
|----------|---|
| | |
| **Total (con tope)** | |

## 7. Observaciones y acciones
- [Métricas sin evidencia suficiente, hallazgos, acciones correctivas, recomendaciones para la revisión del SLA]

## 8. Reproducibilidad
- Archivo de mediciones: [ruta] (SHA-256: [...])
- Archivo de objetivos: [ruta]
- Comando: `[...]`
