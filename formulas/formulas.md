# Fórmulas del toolkit

Cada fórmula incluye variables, unidades, norma de origen y un ejemplo resuelto. Los ejemplos usan el caso `ejemplos/enlace-dedicado/`.

## Índice
1. Disponibilidad · 2. Caída permitida · 3. Disponibilidad en serie · 4. Disponibilidad en paralelo · 5. Throughput y eficiencia · 6. Pérdida · 7. Jitter · 8. Latencia por distancia · 9. Crédito de servicio

---

## 1. Disponibilidad

```
A (%) = (T − D) / T × 100
A = MTBF / (MTBF + MTTR)          (forma por confiabilidad)
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| T | Tiempo del período acordado, **sin** mantención programada ni exclusiones | min |
| D | Indisponibilidad acumulada | min |
| MTBF / MTTR | Tiempo medio entre fallas / de reparación | h |

**Norma:** ITU-T Y.1540 (disponibilidad IP), MEF 10.4 (disponibilidad Ethernet); definición contractual según ITU-T E.860.

**Ejemplo:** octubre = 31 d = 44 640 min; mantención programada 120 min → T = 44 520 min; caídas D = 65 min.
`A = (44520 − 65) / 44520 × 100 = 99.854 %`.
Por confiabilidad: MTBF = 1000 h, MTTR = 1 h → `A = 1000/1001 = 99.900 %`.

---

## 2. Caída permitida

```
D_max = T × (1 − A_obj / 100)
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| A_obj | Disponibilidad objetivo | % |
| T | Tiempo del período | min |

**Norma:** derivada de la definición de disponibilidad (Y.1540 / MEF 10.4).

**Ejemplo:** T = 44 520 min, A_obj = 99.9 % → `D_max = 44520 × 0.001 = 44.52 min`.

| Objetivo | Caída permitida / mes (30 d) | / año (365 d) |
|----------|------------------------------|---------------|
| 99 % | 432 min (7.2 h) | 87.6 h |
| 99.9 % | 43.2 min | 8.76 h |
| 99.95 % | 21.6 min | 4.38 h |
| 99.99 % | 4.32 min | 52.6 min |
| 99.999 % | 25.9 s | 5.26 min |

---

## 3. Disponibilidad en serie

Todos los elementos deben funcionar: la cadena es **peor** que su peor eslabón.

```
A_serie = A1 × A2 × … × An        (A en fracción, 99.9 % = 0.999)
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| Ai | Disponibilidad del elemento i | fracción (0–1) |

**Norma:** teoría de confiabilidad; práctica de diseño de SLO en ITIL 4 SLM / ITU-T E.860.

**Ejemplo:** acceso de fibra 99.95 %, equipo del cliente 99.98 %, red del proveedor 99.99 %:
`A = 0.9995 × 0.9998 × 0.9999 = 0.99920 → 99.92 %` (≥ 99.9 % ✔, con poco margen).

---

## 4. Disponibilidad en paralelo

Basta que uno funcione (redundancia).

```
A_paralelo = 1 − [(1 − A1) × (1 − A2) × … × (1 − An)]
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| Ai | Disponibilidad de cada rama redundante | fracción (0–1) |

**Norma:** teoría de confiabilidad (ITIL 4 / E.860 para el diseño de SLO).

**Ejemplo:** dos enlaces de 99.5 % → `1 − (0.005 × 0.005) = 0.999975 → 99.9975 %`.
Mixto: ese par en serie con un switch de 99.99 % → `0.999975 × 0.9999 = 0.999875 → 99.9875 %`.

> Supone fallas independientes. Dos enlaces por el mismo ducto **no** son independientes: la disponibilidad real es menor.

---

## 5. Throughput y eficiencia

```
Throughput (bit/s)   = bits transferidos / tiempo
Utilización (%)      = Throughput_medido / Capacidad × 100
BDP (bit)            = BW × RTT
Throughput_máx TCP   = Ventana / RTT
Eficiencia TCP (%)   = (B_tx − B_retx) / B_tx × 100
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| BW | Ancho de banda del enlace | bit/s |
| RTT | Tiempo de ida y vuelta | s |
| Ventana | Ventana TCP | bit |
| B_tx / B_retx | Bytes transmitidos / retransmitidos | byte |

**Norma:** RFC 6349 (pruebas de throughput TCP: BDP, ventana y eficiencia TCP).

**Ejemplo:**
- 1.125 GB en 100 s → `1.125e9 × 8 / 100 = 90 Mbps` → utilización sobre 100 Mbps = **90 %**.
- BDP con 100 Mbps y RTT 20 ms → `100e6 × 0.02 = 2 000 000 bit = 250 000 byte`.
- Ventana de 64 KB (524 280 bit) con RTT 20 ms → `524280 / 0.02 = 26.2 Mbps` (la ventana limita el enlace).
- B_tx = 1 000 000, B_retx = 5 000 → eficiencia TCP = **99.5 %**.

---

## 6. Pérdida de paquetes

```
Pérdida (%) = (N_enviados − N_recibidos) / N_enviados × 100
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| N_enviados / N_recibidos | Paquetes de prueba enviados / recibidos | paquetes |

**Norma:** RFC 7680 (pérdida unidireccional), ITU-T Y.1540 (IPLR).

**Ejemplo:** 10 000 enviados y 9 995 recibidos → `5 / 10000 × 100 = 0.05 %`.

---

## 7. Jitter (variación del retardo)

```
IPDV_i = D_i − D_(i−1)                          (RFC 3393)
Jitter (promedio) = media de |IPDV_i|
PDV = percentil_alto(D) − D_mín                 (ITU-T Y.1540, p. ej. p99 − mín)
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| D_i | Retardo del paquete i | ms |
| IPDV_i | Variación de retardo entre paquetes consecutivos | ms |

**Norma:** RFC 3393 (IPDV), ITU-T Y.1540 (PDV); MEF 10.4 define el equivalente Ethernet (rango/variación de retardo).

**Ejemplo:** retardos 20.0, 22.0, 19.0, 25.0 ms → IPDV = +2, −3, +6 → `jitter = (2+3+6)/3 = 3.67 ms`; PDV = 25 − 19 = **6 ms**.

---

## 8. Latencia por distancia

```
t_prop (s) = d / v                  v ≈ 2 × 10^8 m/s en fibra  →  ≈ 5 µs por km
RTT_mín    = 2 × t_prop
t_tx (s)   = L / BW
Latencia   = t_prop + t_tx + t_proc + t_cola
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| d | Longitud de la **ruta de fibra** (no la distancia en línea recta) | m |
| v | Velocidad de propagación en fibra (≈ 2/3 de c) | m/s |
| L | Tamaño del paquete | bit |
| BW | Velocidad del enlace | bit/s |
| t_proc, t_cola | Procesamiento y colas en equipos | s |

**Norma:** propagación física; objetivos de referencia en ITU-T G.114 (voz ≤ 150 ms unidireccional) e ITU-T Y.1541 (clases de QoS).

**Ejemplo:** ruta de fibra de 500 km → `t_prop = 500 × 5 µs = 2.5 ms`, `RTT_mín = 5 ms`.
Paquete de 1500 B a 100 Mbps → `t_tx = 12000 / 1e8 = 120 µs`.
Ningún SLO de latencia puede ser menor que 5 ms RTT en esa ruta.

---

## 9. Crédito de servicio

```
p (%)       = min( tope, p_disp + k × m )
Crédito     = Cuota_mensual × p / 100
```

| Variable | Significado | Unidad |
|----------|-------------|--------|
| p_disp | % del escalón de disponibilidad alcanzado (0 si cumple) | % |
| k | % adicional por cada otra métrica incumplida | % |
| m | Número de otras métricas que no cumplen | – |
| tope | Máximo de crédito mensual | % |
| Cuota_mensual | Valor mensual del servicio | CLP |

**Norma:** ITU-T E.860 (consecuencias del incumplimiento en el SLA); práctica ITIL 4 SLM / ISO/IEC 20000-1. Los escalones los fija cada SLA (`objetivos.yaml`).

**Ejemplo:** A = 99.854 % cae bajo 99.9 % → escalón 10 %; las demás métricas cumplen (m = 0); cuota 450000 CLP:
`p = min(60, 10 + 0) = 10 %` → `Crédito = 450000 × 0.10 = 45000 CLP`.
