# b76 (base b75, md5 b2f37978b626d9bd1a072b1e655e7218; b75 intacta)

ROM: `wwf_b76.bin`, md5 `49075e62b6b23d071da6035564adcea8`
Solo los 5 arreglos pedidos. No se han tocado la IA, los ataques nuevos, HOME, los esquineros, el logo ni el sonido del público.
Toda la evidencia sale de `/workspace/wwf_sgdk/analisis` (arc_rec.dis, rutinas.md, tools/prog.bin y los bancos de sprites arcade).

## 1. Puñetazo de Warrior completo
- **Arcade:** el puñetazo es el mov 0x00, en 0xFC84. Usa la tabla 0xFD70 con las poses 0x150 (4 f), 0x151 (3 f) y 0x152 (3 f); 0xFD7C es la alternativa del combo (0x153 a 0x155).
- **Banco 0 (Warrior):** 0x152 es la pose con el brazo extendido. Coincide con la referencia MAME 01M6PKH6….
- **Causa del fallo:** en el port, `xl_w[41]` apuntaba a la pose 658, que es la 0x150 del banco 0 (preparación, sin brazo). Por eso Warrior nunca estiraba el brazo.
- **Arreglo:** se añade la pose nueva 765, convertida desde la 0x152 del banco 0 con `tools/gen76_punch.py` (mismo método que gen69). Ahora `xl_w[41]` = 765. Duggan no cambia.
- Captura: `shots/b76_01_punetazo_warrior.png`.

## 2. Cuenta y árbitro
- **Arcade, cifras:** el fg0 se dibuja encima de los sprites (wwfsstar.cpp: bg0 → sprites → fg0) y el texto de la cuenta va por 0xE02C/0x2549E. Las cifras del port ya tienen el fondo transparente (índice 0, comprobado en pin_glyph.bin), así que eso se deja como está.
- **Causa real de que el árbitro "desapareciera":** `refSideY` (inventado en b73) lo mandaba DELANTE (−73) cuando no cabía detrás. Quedaba en y < RING_Y0, fuera del ring y tapado por la cuerda frontal.
- **Arcade:** el estado 2 del árbitro (0xDD4E) va hacia la pareja (0xDFE0) y en cada frame hace `jsr 0x21E5A` (0xDECC), que es el límite del ring. Nunca sale.
- **Arreglo:** el árbitro siempre va al lado de la pista (+73) y se limita al ring con `rfClamp`, tanto en la cuenta como al levantarse.
- Capturas: `shots/b75_antes_cuenta_arbitro_fuera.png` (antes) y `shots/b76_02_cuenta_arbitro_dentro.png` (después).

## 3. Enganche desalineado (uno más alto que el otro)
- **Causa:** cuando Warrior cubre, la pista WPIN/WKO no trae Z, así que se usa `pinZof` = 174. Al acabar el kick-out, `z0` se quedaba en 174 y Warrior se veía 13 px más alto en el siguiente agarre.
- Se reproduce en b75 con el test koW: dZ de Warrior = 174 después del pin. En b76 vuelve a 187.
- **Arreglo, sin tocar el asiento z0=174 del pin:**
  - z al suelo en las reacciones y en el suelo (0xAB1E y 0xA90E, "z al suelo").
  - z = 0xBB para los dos al empezar el forcejeo (0xB1D0 + 0x16F58 centrar_pareja).
  - La salida del pin pasa ahora por la acción 8, que termina en el suelo.
- El regression pinC sigue igual: `SETTLE z0=174`, `CENTER err=0`.

## 4. Caída contra la cuerda en una llave (la famosa)
- **Arcade 0xF94C (acción 0xC):** si está dentro del ring y toca la cuerda (+0x9E&3, límite 0x21E5A/0x22140), llama a 0xF9B0.
- **0xF9B0:**
  - Marca la cuerda (0x9700, d0=1).
  - Si el rival YA NO está en 0x10, el que hace la llave pasa a la acción 8 sub 1.
  - Si el rival sigue en 0x10, solo actúan las subs 0x1B/0x21/0x22/07/0x29/0x28. El whip es la sub 0x1E, así que ahí no pasa nada.
- **Acción 8 (0x99BE, tabla 0x9A14 / parámetros 0xA74A):**
  - Sub 1 (0x9B7E): impulso 0x10 hacia atrás (0x9BBE), z+0x10 y pose 0x15/0x16 según la altura (0x9E4C).
  - Con la cuerda (0x9CD0) pasa a la sub 2 (0x9F02): z ≥ 0xCB, pose 0x16, vx negada. Al llegar a 0xBB pasa a la acción 0xB (tumbado).
- **Port:** durante el whip, desde que la víctima deja la acción 16 (0x10) en la pista, si el lanzador está en el borde del trapecio del ring cae contra la cuerda y queda tumbado. La cuerda vibra y luego se levanta.
- Captura: `shots/b76_04_caida_cuerda_llave.png` (test MAME `rope`).
- **Límite importante:** el forcejeo coloca a los dos en el punto medio (igual que el arcade, 0x16F58). Por eso el lanzador solo toca la cuerda si el agarre empieza pegado a ella. En el test se fuerza x=627 (la cuerda izquierda en y=300). El arcade también puede llegar empujando en el forcejeo (+0xAF modo 2/3), pero ese movimiento no está portado y no lo he inventado.

## 5. Zafarse del pin, para los dos
- **Arcade acción 0x1E (0xB012), la del cubierto:**
  - x ±8, pose 0x9F durante 8 f y 0xA0 durante 4 f (tabla 0xB0EA).
  - El que cubre lleva la pose 0x9B en x ±0x28, y−1, z+4.
  - Al acabar, el cubierto pasa a la acción 5 (levantarse) y el que cubre a la acción 8 sub 0x1C, girado (0xB068–0xB084).
  - Sub 0x1C (0x9B66): impulso 0x10, z+0x18, poses 0x9B/0x9C por altura.
  - Al tocar el suelo con +0x45=0x1C (0x9C5A): x ±0x20 y sub 0xC (0xA4C8: pose 0x16, vz 0x100, g 0x30). Luego la acción 0xB.
- **Poses nuevas** (tools/gen76_poses.py, bancos 0 y 3):
  - Warrior: 766 9F, 767 A0, 768 9B, 769 15, 770 16, 776 9C.
  - Duggan: 771, 772, 773, 774, 775, 777.
- El tumbado del que cubría dura 44 f, como lo medido en el inventario: "08 34 + 0B 44 + 05 16". Después se levanta, sin atontado. El cubierto se levanta (0x5) sin atontado.
- Capturas: `shots/b76_05a_zafar_warrior_cubierto.png` y `shots/b76_05b_zafar_duggan_cubierto.png`.

## Lo que no se ha podido sacar del arcade (aproximaciones declaradas)
- **Gravedad de la acción 8:** la sub 1 y la 0x1C no fijan vz ni g. Se usa la física de 0x3E20 con g=0x30 (el valor que pone 0xA4C8) y vz inicial 0.
- **Sonidos de la caída** (0x11, 0x29, 0x21): no se han añadido.
- **Duración de levantarse:** se usa la pose 115 del port (30 f) en lugar de los 16 f de la acción 5.

## Pruebas MAME (test/t76.lua, run76.sh)
- `pun`/`punD`: Warrior estira el brazo y golpea.
- `ko`/`koW`: zafarse completo en los dos sentidos; z0 = 187 al final (en b75, koW deja dZ = 174).
- `rope`: caída contra la cuerda.
- `cnt`: árbitro dentro del ring durante la cuenta.
- Regresión t75 `pinC`/`pinSide`: pin_ok, SETTLE z0=174, CENTER err=0.
