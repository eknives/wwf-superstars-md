# Pin y cuenta

## Inicio
- Cubrir = acción 0x17 (0xBD10). La ponen 0x1190C, 0x11A72 y 0x12972.
- Al mismo tiempo marcan al rival con +0x18 bit5, y eso pasa al árbitro al estado 2.
- Al acabar la cuenta, el cubierto pasa a la acción 0x19 (rodar, 0x12B00).

## Tiempo en el suelo: acción 0xB (0xAB1E)
- +0x38 = tabla 0xAF66[banda] = 112 / 82 / 54 / 22 ticks. Cada tick son 2 frames, así que dura 224 / 164 / 108 / 44 frames.
- Banda (0x1CE9C) = energía / (máxima/4), limitada a 3:
  - Humano: máxima 48 (0x7FEC).
  - CPU: máxima de la tabla 0x8190[nivel*8 + hueco].
- CPU: el tiempo se divide entre 2 si 0x1CD80 da CS (+0xF6 >= 0x1CD48[id], medidor alto) o si +0xF9 bit0.
- +0x20 si venía de fuera del ring.
- Machacar botones (0xAD12, umbral 0xAF6A = 24 / 10 / 6 / 3) → acción 0x19.

## Salida del pin: kick-out propio, acción 0x1E
- **Humano (0xADEA):** el umbral es AF72[energía]/2; las pulsaciones durante la cuenta lo libran.
- **CPU (0xAE7E):** nivel d1 de 0xAF26:

  | Energía | d1 |
  |---|---|
  | ≥ 0x36 | 0 |
  | ≥ 0x30 | 1 |
  | ≥ 0x24 | 2 |
  | ≥ 0x19 | 3 |
  | ≥ 0xE | 4 |
  | > 0 | 5 |
  | 0 | 6: nunca sale |

  Sale cuando cuenta*2 + paridad ≥ d1 (más condiciones de los frames del árbitro).
- **Kick-out inmediato (0x11BC6):** tirada contra la tabla 0x11C30[dificultad*3 + 0x1CEF4].

## Salvamento del compañero (0x129A4)
- No hay salvamento si el cubierto tiene energía 0, o si el compañero no puede (3/16 de probabilidad).
- La CPU acude con el estado 0xF (0x1B486).
