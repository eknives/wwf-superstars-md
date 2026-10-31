# Cotejo con el port s66 (wip19/main.c, solo lectura)

Fichero cotejado: s66/wip19/main.c, sha256 3d216c78…, sin modificar.

Estados:
- **C** = discrepancia confirmada por el código arcade.
- **=** = coincide.
- **V** = hace falta MAME para decidir.

## Pin y suelo

| # | Port (línea) | Arcade | Estado |
|---|---|---|---|
| 1 | 292 y 396: «los kick-outs son SIEMPRE el compañero entrando»; el primer pin siempre acaba en kick-out. | Kick-out propio, acción 0x1E: el humano machacando (0xADEA, umbral AF72/2) y la CPU según la energía y la cuenta (0xAE7E/0xAF26). Además hay un kick-out inmediato con tirada (0x11BC6). El salvamento del compañero (0x129A4) es una vía más, no la única. | C |
| 2 | 294 y 397: con energía 0, 13/16 → cuenta de 3. | La CPU con energía 0 (d1=6) nunca sale y el compañero no puede salvarla (0x129A4) → la cuenta de 3 es segura (16/16). Un humano con energía 0 necesita 0x30 pulsaciones. El 3/16 del arcade es la probabilidad de que el compañero no pueda salvar, no la de la cuenta. | C |
| 3 | 365: lieTab {180,120,64,0} + 44 de base. | 2×AF66 = 224/164/108/44 frames. | = (exacto) |
| 4 | 365: mashTab {24,10,6,3}. | AF6A = 24/10/6/3. | = |
| 5 | 366: lieBand = e/12 también para la CPU. | La CPU usa la máxima de 0x8190[nivel*8 + hueco]/4, no 12. | C. El efecto depende de esa máxima: con 48 coincide. |
| 6 | 76: la CPU empieza con 55 (demo MAME). | 55 no aparece en la tabla 0x8190. No se ha leído dónde se inicializa la energía de la CPU en el modo demo. | V |
| 7 | 396: la CPU solo cubre con la energía de P1 < 16. | La decisión de cubrir de la CPU (planificador 0x1D1A8 → subs 0x1190C/0x11A72) no se ha cotejado regla por regla. | V |
| 8 | La CPU tumbada no reduce su tiempo a la mitad. | 0xAB1E: la CPU usa /2 si 0x1CD80 da CS, y +0x20 si venía de fuera. | C |

## Sistemas que faltan en el port

| # | Sistema | Estado |
|---|---|---|
| 9 | Reloj 30:00, prisa a 5:00 (música 8) y TIME UP (0x2626E). | C (falta) |
| 10 | Cuenta fuera del ring hasta 20 y doble descalificación (0xDEE4). | C (falta) |
| 11 | Sonido: no hay driver; faltan las voces de la cuenta 0x3D–0x3F y la campana 0x20/0x21. | C (falta) |
| 12 | RNG: el port usa random(); el arcade usa 0x450A. | C |

## Corregido respecto a discrepancias.md
- La valla/público 1C1854 (antigua discrepancia #1) ya está implementada en wip19, líneas 788–811. La condición coincide con 0x22462; no se ha cotejado línea por línea.
- La antigua #4 («lieTab es una aproximación») se retira: los valores son exactamente 2×AF66.
