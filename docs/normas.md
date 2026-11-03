# Normas de referencia

Qué define cada norma y en qué paso del método (`docs/metodo.md`) se aplica. Verifica siempre la versión vigente de cada documento.

| Ámbito | Norma | Qué define | Pasos |
|--------|-------|-----------|-------|
| Gestión del SLA | **ITIL 4 – Service Level Management** | Práctica de gestión: captar requisitos, acordar niveles, monitorear, informar y revisar. | 2, 5, 6 |
| Gestión del SLA | **ISO/IEC 20000-1** | Requisitos certificables de un sistema de gestión de servicios; mejora continua con ciclo PDCA. | 5, 6 |
| Estructura del SLA | **ITU-T E.860** | Marco para un SLA entre operador y cliente: partes, servicio, parámetros, responsabilidades. | 1, 4, 5 |
| Estructura del SLA | **ISO/IEC 19086-1** | Marco de SLA para servicios cloud (visión general y conceptos). | 1, 3 |
| Métricas IP | **ITU-T Y.1540** | Parámetros de transferencia de paquetes IP: retardo (IPTD), variación de retardo (IPDV), pérdida (IPLR) y disponibilidad. | 3, 4 |
| Métricas IP | **ITU-T Y.1541** | Objetivos de desempeño de red IP y **clases de QoS**. | 4 |
| Métricas Ethernet | **MEF 10.4** | Atributos de servicio Ethernet (E-Line, E-LAN) y objetivos de desempeño: retardo, rango/variación de retardo, pérdida y disponibilidad. | 3, 4 |
| Medición | **RFC 7679** | Métrica de retardo unidireccional (One-Way Delay, IPPM). | 3, 5 |
| Medición | **RFC 7680** | Métrica de pérdida unidireccional (One-Way Loss, IPPM). | 3, 5 |
| Medición | **RFC 3393** | Variación de retardo de paquetes IP (IPDV, base del jitter). | 3, 5 |
| Medición | **RFC 5357 (TWAMP)** | Protocolo de medición activa bidireccional (ida y vuelta). | 5 |
| Medición | **RFC 6349** | Marco de pruebas de throughput TCP (BDP, ventana, eficiencia TCP). | 3, 5 |
| Voz | **ITU-T G.114** | Tiempo de transmisión unidireccional recomendado: ≤ 150 ms para voz interactiva. | 4 |

## Uso por métrica

| Métrica (SLI) | Definición | Medición |
|---------------|-----------|----------|
| Disponibilidad | Y.1540 / MEF 10.4 | Registro de caídas (monitoreo activo); exclusiones según SLA |
| Latencia | Y.1540, RFC 7679 | TWAMP (RFC 5357), ping/OWAMP |
| Jitter | RFC 3393, Y.1540 | TWAMP / OWAMP |
| Pérdida | RFC 7680, Y.1540 | TWAMP / OWAMP |
| Throughput | RFC 6349 | Pruebas TCP (iperf3, herramientas RFC 6349) |
