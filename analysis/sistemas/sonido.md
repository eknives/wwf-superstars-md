# Sonido: driver Z80, OKI y campana

Fuente: ROM 24ab-0.12 (Z80, 32 KB) y ROMs OKI 24a9-0.46 + 24j8-0.45.
Herramientas: tools/z80rec.py (listado en /tmp/z80.lst) y tools/oki.py (genera oki/sXX.wav).
Se ha leído todo el código Z80 alcanzado: 1.200 instrucciones y 2.523 bytes, más los manejadores de opcodes del secuenciador 0x468–0x6C0.

## Hardware y flujo
- El 68K escribe en el latch 0x180009. Eso provoca una NMI en el Z80, que mete el byte en la cola 0x8400.
- El YM2151 genera la IRQ de 0x38 con su temporizador. El bucle principal está en 0x100 y el despachador en 0x18F.

## Comandos
- 0 = reset.
- Bit7 activo = parar.
- 0xF0, 0xF1 y 0xF2 cambian el manejador (0x821A).
- 0xFE y 0xFF = reset.
- Tabla 0x1000: 0x67 entradas de 4 bytes.

| Rango | Significado |
|---|---|
| 0x01–0x17 | Música FM. 8 canales en 0x8000 con paso 0x40; tabla de opcodes del secuenciador 0x8CF (C0–EA). El 0x16 es un duplicado del 0x0A. |
| 0x18–0x1F | Entradas de relleno (tocan la muestra 1). |
| 0x20–0x49 | Muestra OKI = comando − 0x1F. Driver en 0xC4B, 4 voces en 0x8310. |
| 0x50 / 0x51 / 0x52 | Secuencias de muestras (0xD79/0xDAA) con datos en 0x1152/0x117A/0x11A2. 0x50 y 0x51 son oleadas de público (muestras 3 y 4); 0x52 es un ritmo con la muestra 5 y el 68K nunca lo envía. |
| 0x55–0x67 | Las «entradas» se solapan con los datos de secuencia: no son comandos reales. |
| > 0x67 | Va a 0x345, que solo escribe 0x821F, y nada lo lee: es un NO-OP. Por eso el aviso 0x70 del reloj no suena. |

Las muestras válidas son 1–0x2A.

## Campana (resuelto)
- **0x20 = campana de inicio.** Muestra 1: 1,5 s, pico espectral en 2.360 Hz y decaimiento exponencial. Solo la envía inicio_combate (0x84A2).
- **0x21 = campana repetida.** Muestra 2: mismo pico (2.350 Hz), sostenida 2,3 s. La envían musica_combate (0x179A) y el fin de tiempo (0x26548 / 0x2657A / 0x2658E).
- El 0x3B (muestra 0x1C), que antes se suponía la campana, **no lo es**.
- Esto se deduce del espectro y del contexto de llamada; nadie lo ha oído.

## Otros IDs identificados

| ID | Muestra | Uso |
|---|---|---|
| 0x22 / 0x23 | 3 / 4 | Público |
| 0x24 | 5 | Pasos |
| 0x29 | 0xA | Golpe sordo |
| 0x32 | — | Rodar fuera del ring |
| 0x33 | 0x14 | Cuerda |
| 0x47 | 0x28 | Poste |
| 0x3D / 0x3E / 0x3F | — | Voces de la cuenta del árbitro: 1, 2, 3 |

La lista completa de qué rutina envía cada ID está en sonido_ids_llamadas.txt.
