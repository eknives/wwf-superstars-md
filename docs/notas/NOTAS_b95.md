# b95 — carrera por tick arcade, streaming del fondo por DMA, choque contra cuerda (base b94)

ROM `wwf_b95.bin`, MD5 **7be789d70d892c1efb86af8630b296a6** (b94 b2a8ff5d4453067ad3d2bf8762239413 intacta). Sólo los 3 puntos autorizados (9-11-2026 9:32).

## Cambios
1. **Carrera** (`main.c` 192, 866–871, 878):
   - Velocidad por luchador de la tabla `0x95BC` (`945C` → +0x21): Warrior 28, Duggan 27. `3DF0`: vel/4 px por tick.
   - Un paso por `arcTick` (reloj arcade 28,72 Hz, NTSC y PAL), antes `tick&1`.
   - Pose cada 2 `arcTick` (`94CE`, tabla `0x95C4`).
   - Sin tocar: andar, rebote rn 2 (pista 48 f), freno, clothesline y arranque de 3 frames (apuntado en PENDIENTES).
2. **Fondo por DMA en cola** (`main.c` 211–240, 1553–1584):
   - Tile ROM→VRAM, BG_B y BG_A de cada columna/fila van a la cola DMA. Se vuelcan en el vblank (`SYS_doVBlankProcess`) antes del scroll nuevo, así que la columna aparece completa el mismo frame que en b94.
   - Presupuesto `ST_BUD` de 40 tiles/frame. Si se supera (salto de cámara), se vacía la cola sin perder el orden.
   - El público (`caApply`, CPU) y las cuerdas (`ropeDraw`) se calculan antes del streaming, con el mismo resultado.
   - No hizo falta repartir una columna en varios frames: el coste estaba en las escrituras CPU al VDP en pantalla activa (medido ~870 ciclos por celda BG_A y ~0,2 frame por los tiles).
3. **Choque contra cuerda** (`main.c` 530–595, 669–672):
   - **9E78**: cada tick prueba X±0x10 hacia donde vuela, con los límites de `21E5A`/`22140` (izq X ≤ 616+e, dcha X > 920−e). Si toca, X = límite ∓ 0x10; con z ≥ 0xDB no recorta (`21E7A`).
   - **9CD0**: el `cmpi.b #$1c,$44` compara el byte alto, así que cualquier contacto pasa a sub 2. Fallo arcade copiado.
   - Si el contacto ocurre el mismo tick del aterrizaje: `9C94`, sub 0xC sin ∓0x20 (caso Xv728 → 643).
   - **9F02**, en el tick siguiente:
     - marca la cuerda (vibra, `9700` d0=1);
     - z ≥ 0xCB y pose 0x16;
     - `27D2` índice 0x11 (tabla 0x2934: vx 0x100, vz 0, g 0x10), con Vx hacia dentro;
     - aterriza cuando z < 0xBB → tumbado (acción 0xB).
   - El sonido 0x29 del aterrizaje (`25E6`) no existe en el port y no se añade. El "0x11" de 9F02 es parámetro de movimiento, no un sonido.
   - `9C5A` ∓0x20 sin clamp.
   - **soilNudge** usa `oriVictima` (vface^1) como bit7 de `ACA4`.
     - Llamadas 875/893 (derribo por golpes): revisadas; ponen `vface = atacante a la derecha`, la convención de b93, así que `oriVictima` es el bit7 arcade.
     - La llamada del aterrizaje (fs) también encaja con la convención.

## Verificado (MAME 0.276; genesis = NTSC, megadriv = PAL; arcade wwfsstar)
- **Carrera** px/s, ida y vuelta (`shots95/md/b95_{genesis,megadriv}_run.csv`):

  | | Warrior | Duggan |
  |---|---|---|
  | arcade | 201,1 | 193,9 |
  | b95 NTSC | 200,5 / 200,6 | 194,0 / 193,9 |
  | b95 PAL | 199,7 / 200,1 | 192,6 / 193,0 |
  | b94 PAL | 167,7 | 167,7 |
  | b94 NTSC | 201,5 / 202,3 | 199,7 / 196,7 |

  - Cambios de pose: b95 14,0–14,8/s en NTSC y 14,1–14,3 en PAL (arcade 14,36; b94 PAL 12,1–12,4).
  - Rebote al llegar a la cuerda (906/627) y vuelta: OK en NTSC y PAL.
- **Frames perdidos andando en diagonal hacia cada poste** (580 frames; `b9x_post.csv`):

  | | sup izq | sup der | inf izq | inf der |
  |---|---|---|---|---|
  | b94 | 20 | 14 | 18 | 19 |
  | b95 | 3 | 2 | 1 | 0 |
  | b94, máx en 59 frames | 10 | 6 | 12 | 10 |
  | b95, máx en 59 frames | 2 | 1 | 1 | 0 |

  - Este script mide 10/59 y 12/59 en b94; el "8/59" de la investigación era otra ventana.
  - **Fondo**: cada frame se lee la VRAM (nametable BG_B + tile) de las columnas y filas del borde, y la ventana entera cada 16 frames. Se compara con W/ROM: 0 errores en unas 100.000 celdas por caso, en b94 y en b95.
  - Control negativo (b95 sin DMA de tiles): 67.667 errores, así que el chequeo sí detecta fallos.
  - La zona visible queda siempre dentro de la ventana cargada.
  - 6 capturas estáticas (centro y 4 postes) idénticas píxel a píxel a b94, cuerdas incluidas.
- **Zafarse del pin cerca de la cuerda** (X final del que cubría):

  | Xv | arcade | b94 | b95 |
  |---|---|---|---|
  | 760 | 642 | 675 | 642 |
  | 728 | 643 | 675 | 643 |
  | 708 | 677 | 675 | 677 |
  | 693 | 677 | 675 | 677 |
  | 832 | 859 | 858 | 859 |

  - b95 = arcade en las 5. Choque con cuerda vibrando, pose 0x16, 17 ticks y +2 px/tick como en el arcade.
  - Captura: `shots95/clave1_choque_cuerda_arcade_b94_b95.png`.
- **Regresión**:
  - **Salir del ring**: sx 0→1→2 en las mismas X que b94, W y D, ambos lados.
  - **Clothesline** DR/DL/WR/WL: contacto, agarre, vuelo, bote y tumbado, con 0 errores de tiles. La víctima termina igual que en b94 (746/784); el atacante contacta 6–8 px más lejos porque la carrera va ahora por tick.
  - **Pin**: 26 estados de cubrir iguales a b94 en 6 casos; zafar en 4 casos; la cuenta de 3 funciona.
  - **Sub 1 contra cuerda** (fixture del port): rebota hacia dentro (W 627→659, D 906→874). En b94 saltaba 48 px.

## No verificado / límites
- Consola real / Everdrive. El DMA desde ROM con el Z80 PCM activo es el mismo patrón que `fLoad`.
- Sub 1 contra cuerda (lanzamientos, clothesline en la cuerda) y derribo por golpes junto a la cuerda: no medidos en MAME arcade. Sólo se siguió el código de 9F02/ACA4.
- `arcTick` da como máximo 1 tick por vuelta: con frames perdidos la carrera pierde ~0,3–0,7 %.
- La caída de acción 8 (fs) sigue avanzando cada 2 vueltas (`fsTick`), no por `arcTick`: con frames perdidos dura más (Xv708: 17 ticks en 40 frames).
- Corriendo entre cuerdas quedan 40/580 frames perdidos (b94: 55). Causa no investigada; no es el streaming.
- El límite derecho de 9E78 usa 920−e (arcade); el `RING_XR` 917 global del port no cambia.
