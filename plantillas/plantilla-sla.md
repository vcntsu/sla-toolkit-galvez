# SLA — [Nombre del servicio]

> Plantilla basada en ITU-T E.860 e ITIL 4 SLM. Reemplaza todo lo que esté entre `[corchetes]`. Borra las notas en cursiva al terminar.

## 0. Control de versiones
| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [AAAA-MM-DD] | [nombre] | Versión inicial |

## 1. Partes
| Rol | Nombre | Contacto |
|-----|--------|----------|
| Proveedor | [empresa] | [responsable, correo, teléfono] |
| Cliente | [empresa] | [responsable, correo, teléfono] |

## 2. Descripción del servicio y alcance
- **Servicio:** [qué se entrega: tipo, capacidad, interfaz]
- **Ubicaciones / sitios:** [direcciones o nodos]
- **Incluido:** [...]
- **No incluido:** [...]
- **Horario del servicio:** [24x7 / lunes a viernes 08:00–18:00]

## 3. Punto de demarcación
[Dónde termina la responsabilidad del proveedor: ej. puerto Ethernet del equipo terminal en el sitio del cliente.]

## 4. Requisitos del cliente (SLR)
| ID | Requisito (lenguaje del cliente) | Prioridad |
|----|----------------------------------|-----------|
| SLR-1 | [ej. videollamadas sin cortes en horario laboral] | [Alta/Media/Baja] |

## 5. Indicadores (SLI) y objetivos (SLO)
| Métrica | Definición | Norma | Método / punto de medición | Agregación | Objetivo (SLO) | Mín. muestras |
|---------|-----------|-------|----------------------------|------------|----------------|---------------|
| Disponibilidad | [...] | [Y.1540 / MEF 10.4] | [...] | [mensual] | [≥ __ %] | [__] |
| Latencia | [...] | [Y.1540 / RFC 7679] | [TWAMP] | [p95] | [≤ __ ms] | [__] |
| Jitter | [...] | [RFC 3393] | [TWAMP] | [p95] | [≤ __ ms] | [__] |
| Pérdida | [...] | [RFC 7680] | [TWAMP] | [promedio] | [≤ __ %] | [__] |
| Throughput | [...] | [RFC 6349] | [iperf3] | [promedio] | [≥ __ Mbps] | [__] |

### 5.1 Verificación de viabilidad (regla base)
- [ ] Disponibilidad calculada en serie/paralelo ≥ objetivo (ver `formulas/formulas.md`): [__ %]
- [ ] Latencia física mínima (distancia) < objetivo: [__ ms]
- [ ] Capacidad contratada ≥ throughput objetivo
- [ ] Cada objetivo tiene método de medición y herramienta disponibles
- [ ] OLA / contratos de soporte (UC) respaldan los tiempos de reparación

## 6. Operación y medición
- **Período de medición:** [mensual, del día 1 al último]
- **Herramienta de medición:** [...]
- **Frecuencia de muestreo:** [...]
- **Exclusiones:** [mantención programada (aviso ≥ __ días, máx. __ h/mes), fuerza mayor, causas del cliente]

## 7. Soporte, MTTR y escalamiento
| Severidad | Descripción | Respuesta | MTTR objetivo | Escalamiento |
|-----------|-------------|-----------|---------------|--------------|
| 1 | Sin servicio | [__ min] | [__ h] | [nivel 2 a los __ min] |
| 2 | Servicio degradado | [__ h] | [__ h] | [...] |
| 3 | Consulta / solicitud | [__ h] | [__ días] | [...] |

## 8. Reportes
[Contenido, frecuencia (mensual), formato (informe generado con `calc_sla.py`), plazo de entrega.]

## 9. Créditos de servicio
| Condición | Crédito (% de la cuota mensual) |
|-----------|---------------------------------|
| Disponibilidad < [__ %] | [__ %] |
| Disponibilidad < [__ %] | [__ %] |
| Otra métrica incumplida | [__ % por métrica] |
| **Tope mensual** | [__ %] |

*Procedimiento de reclamo:* [plazo y forma].

## 10. Responsabilidades del cliente
[Energía y espacio en sitio, acceso para técnicos, no manipular equipos del proveedor, etc.]

## 11. Revisión (PDCA)
- **Frecuencia de revisión:** [semestral / anual]
- **Responsables:** [...]
- **Gestión de cambios al SLA:** [cómo se propone, aprueba y versiona]

## 12. Vigencia y firmas
Vigencia: [desde] — [hasta].

| Proveedor | Cliente |
|-----------|---------|
| Nombre: | Nombre: |
| Firma: | Firma: |
| Fecha: | Fecha: |
