# SLA — Enlace dedicado de Internet 100 Mbps simétrico

> Caso de ejemplo ficticio que aplica `plantillas/plantilla-sla.md`. Los valores coinciden con `herramientas/objetivos.yaml`.

## 0. Control de versiones
| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-10-01 | Vicente Gálvez | Versión inicial |

## 1. Partes
| Rol | Nombre | Contacto |
|-----|--------|----------|
| Proveedor | Proveedor Ejemplo Telecom | NOC — noc@proveedor-ejemplo.cl, 24x7 |
| Cliente | Empresa Ejemplo SpA | Jefe de TI — ti@empresa-ejemplo.cl |

## 2. Descripción del servicio y alcance
- **Servicio:** acceso dedicado a Internet (DIA) de 100 Mbps simétrico sobre fibra óptica, con IP pública fija.
- **Sitio:** oficina central del cliente, La Serena.
- **Incluido:** acceso de fibra, equipo terminal (CPE) del proveedor, tránsito IP, monitoreo 24x7.
- **No incluido:** red LAN, firewall y equipos del cliente, servicios de seguridad gestionada.
- **Horario del servicio:** 24x7.

## 3. Punto de demarcación
Puerto Ethernet 1000BASE-T del CPE del proveedor instalado en el sitio del cliente.

## 4. Requisitos del cliente (SLR)
| ID | Requisito (lenguaje del cliente) | Prioridad |
|----|----------------------------------|-----------|
| SLR-1 | La oficina debe poder trabajar en horario laboral sin cortes largos | Alta |
| SLR-2 | Las videollamadas deben verse y oírse fluidas | Alta |
| SLR-3 | Descargas y respaldos a la nube a velocidad cercana a la contratada | Media |
| SLR-4 | Si el proveedor falla, el cliente recibe compensación | Media |

## 5. Indicadores (SLI) y objetivos (SLO)
| Métrica | Definición | Norma | Método / punto de medición | Agregación | Objetivo (SLO) | Mín. muestras |
|---------|-----------|-------|----------------------------|------------|----------------|---------------|
| Disponibilidad | Tiempo con servicio operativo sobre el tiempo del período, sin mantención programada | Y.1540 / MEF 10.4 | Monitoreo activo del CPE; registro diario de caídas | Mensual | ≥ 99.9 % | 28 días |
| Latencia | RTT desde el CPE al nodo de salida del proveedor | Y.1540, RFC 7679 | TWAMP (RFC 5357) | p95 | ≤ 20 ms | 28 |
| Jitter | Variación del retardo entre paquetes | RFC 3393 | TWAMP | p95 | ≤ 10 ms | 28 |
| Pérdida | Paquetes perdidos / enviados | RFC 7680 | TWAMP | Promedio | ≤ 0.1 % | 28 |
| Throughput | Tasa TCP alcanzable extremo a extremo | RFC 6349 | iperf3 semanal hacia servidor del proveedor | Promedio | ≥ 90 Mbps | 4 |

### 5.1 Verificación de viabilidad (regla base)
- [x] **Disponibilidad en serie:** acceso fibra 99.95 % × CPE 99.98 % × red proveedor 99.99 % = **99.92 %** ≥ 99.9 % (margen pequeño; sin redundancia no se ofrece más).
- [x] **Latencia física:** ruta de fibra ≈ 500 km hasta el nodo de salida → RTT mínimo ≈ 5 ms < 20 ms. Referencia de voz G.114 (≤ 150 ms) cumplida con holgura.
- [x] **Capacidad:** 100 Mbps contratados; objetivo TCP 90 Mbps (90 % de utilización). BDP a 20 ms de RTT = 250 000 byte: el cliente debe usar ventanas TCP adecuadas.
- [x] **Medibles:** todas las métricas tienen herramienta (TWAMP, iperf3) y registro diario.
- [x] **Soporte respaldado:** OLA interno de reparación y contrato (UC) con el proveedor de última milla con MTTR ≤ 4 h.

## 6. Operación y medición
- **Período de medición:** mensual (día 1 al último del mes).
- **Herramienta:** TWAMP (latencia, jitter, pérdida) cada 1 min con valor diario agregado; iperf3 una vez por semana; registro de caídas por el NOC.
- **Exclusiones:** mantención programada (aviso ≥ 5 días hábiles, entre 00:00 y 05:00, máx. 4 h/mes), fuerza mayor y causas atribuibles al cliente (energía, equipos propios, desconexión).

## 7. Soporte, MTTR y escalamiento
| Severidad | Descripción | Respuesta | MTTR objetivo | Escalamiento |
|-----------|-------------|-----------|---------------|--------------|
| 1 | Sin servicio | 30 min | 4 h | Nivel 2 a los 60 min; gerencia a las 4 h |
| 2 | Servicio degradado | 2 h | 8 h | Nivel 2 a las 4 h |
| 3 | Consulta / solicitud | 1 día hábil | 3 días hábiles | — |

> `calc_sla.py` v1.0 no calcula MTTR; se revisa manualmente con el registro de incidentes.

## 8. Reportes
Informe mensual de cumplimiento generado con `calc_sla.py`, entregado dentro de los primeros 5 días hábiles del mes siguiente, con el CSV de mediciones adjunto.

## 9. Créditos de servicio
| Condición | Crédito (% de la cuota mensual) |
|-----------|---------------------------------|
| Disponibilidad < 99.9 % | 10 % |
| Disponibilidad < 99.5 % | 25 % |
| Disponibilidad < 99.0 % | 50 % |
| Otra métrica incumplida | 5 % por métrica |
| **Tope mensual** | **60 %** |

Cuota mensual: 450000 CLP. El cliente debe reclamar dentro de 30 días desde la entrega del informe. Las métricas con evidencia insuficiente no generan crédito hasta completar las mediciones.

## 10. Responsabilidades del cliente
Energía eléctrica y espacio en sitio, acceso para técnicos acordado con aviso, no manipular el CPE, informar cambios de contacto.

## 11. Revisión (PDCA)
- **Frecuencia:** semestral.
- **Responsables:** jefe de TI del cliente y gerente de servicio del proveedor.
- **Cambios al SLA:** se proponen por escrito, se aprueban por ambas partes y se versionan (tabla §0).

## 12. Vigencia y firmas
Vigencia: 2026-10-01 a 2027-09-30.

| Proveedor | Cliente |
|-----------|---------|
| Nombre: | Nombre: |
| Firma: | Firma: |
| Fecha: | Fecha: |
