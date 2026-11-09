# b94 — tumbado en la X arcade + pin ajustado (base b93)

ROM `wwf_b94.bin`, MD5 **b2a8ff5d4453067ad3d2bf8762239413** (b93 a89af7ed95159c0899430bf0e81f6441 intacta).

## Cambios (sólo los 2 puntos autorizados)
1. **Tumbado sin `lyoOf` ±32** (main.c:487 `bodyX=ox`; dibujo main.c:1491 `dLyo=0`). La pose 114/626 sin lyo ocupa lo mismo que la nativa arcade 0x17 en Xv (±6 px). Zonas C798/C706 sin tocar.
2. **Pin**:
   - `pinStart`: `pnX=pnVX=Xv`, `pnM = oriVictima?+1:−1` (BD10/11A72, `neg` si bit7=0), `pnKD=pnM`. Las pistas ya llevan BEF2: Warrior Xv∓32, Y+1, Z203; Duggan Xv∓36, Y−1, Z174.
   - Warrior mira al revés que el tumbado (11A8A `+A = rival^0x80`): `dFlip=(pnM<0)` para 514/778, que se convirtieron espejadas (match69 flip1), e invertido para 513, que es la arc pose 2 sin espejar.
   - Duggan: el flip se mantiene igual (ya coincide con el arcade).
   - Árbitro: `rfX/rfM` lo dejan en el mismo sitio respecto al cuerpo visible que en b77, sin cambio de coreografía.
   - Entrada del pin de Duggan = zona cuerpo C706/CB75 (`dugZone==2`, B, como el Stomp). Se quita el bloque `bodyX±PIN_ZONE` de b69.
   - Zafarse (B012/B0A0) queda en absoluto arcade: tumbado Xv∓8, el que cubre Xv∓48, Y−1, Z+4.
   - Cadencia y deslizamiento sin cambios.

## Verificado (MAME 0.276, genesis NTSC vs arcade wwfsstar, fixtures RAM, Xv=760)
- **Barrido B** d=−88..+88, paso 8, W y D, ambas orientaciones. Las 4 filas son IGUALES al arcade (`shots94/md/sweep_cmp94.txt`):
  - W o0: K −64..−40, P −32..−16. W o1: P +16..+40, K +48..+64.
  - D o0: K −64..−40, P −32..0. D o1: P 0..+40, K +48..+64.
  - En b93 Duggan no coincidía.
  - Con el tumbado en Xv, la banda P cae sobre el torso visible y la K sobre la cabeza (`shots94/clave1_zonas_b93_b94_arcade.png`).
- **Quién cubre** (W 778 / D 499):
  - W X−Xv = −32/+32, Y301, Z203 (arcade −32/+32, 301, 203). D −36/+36, Y299, Z174 (arcade −36/+36.97, 299, 174.5).
  - Lado del ring 680/860: también ∓32.
  - Orientación por silueta contra captura arcade: asiento W y aproximación 514 coinciden directos en b94 (0,79/0,72, contra 0,69/0,55 espejado); en b93 salían espejados. Duggan cubriendo: cara/brazos al mismo lado que el arcade (visual).
  - Captura: `shots94/clave2_cubriendo_arcade_b93_b94.png`.
- **Sin salto tumbado→reacción:**
  - 16 casos md94/reg94 (`shots94/validation94.json`): contactos = arcade (16/16); dX y flip constantes con lyo 0 en 114/752→A2→espera. b93 pasaba de lyo 32 a 0.
  - Levantarse 114→115: tampoco salta ya (b93 saltaba 32).
- **Clothesline** DL/DR/WL/WR: traza y 144 capturas idénticas pixel a pixel b93 vs b94; 0 errores de tiles.
- **Zafar** (1.er pin, W y D, ambas orientaciones): funciona, posiciones según fórmula B012/B0A0.
- **Cuenta de 3** (2.º pin): llega a "3" (pnS 3, winK 117).
- **Caída nativa del que cubre al zafarse:** al acabar la caída, 114 queda en la misma dX sin lyo (b93 saltaba −32).

## Efectos colaterales / NO verificado
- **Zafar cerca de la cuerda:**
  - El que cubre sale ahora de Xv∓48 (arcade), 32 px más fuera que en b93. Su vuelo de caída (sin cambios, 70 px) puede pasar el límite.
  - Con Xv=760 o0 aterriza en 642 y el empuje ACA4 lo pone en 675: un salto de 33 px. En b93 pasaba sólo cerca de la cuerda.
  - En el arcade no se ha medido: el fixture arcade no cuenta, porque no hay árbitro. Queda en PENDIENTES.
- **Zafar/cuenta vs arcade:** sólo contrastado con el código (B012/B0A0), no con MAME arcade.
- **Pose 513:** el volteo sale de la convención de conversión (flip0), no de silueta medida. Son 4 frames.
- **Aproximación:** sigue el deslizamiento 513/514 (el arcade coloca 7E fijo). El salto de Duggan no se ha medido.
- Un frame de retraso puntual del contador durante el pin (lag de emulación; también ocurre en b93).
- Derribo natural en partida, PAL y Everdrive: sin probar.
