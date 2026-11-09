# b68 (desde b67) — md5 3a41cd79ddf5d3b669c0475ca56ca20c
b67 intacta (md5 593ceefe80133aeb5b5e737fd1ec7807).

**Error de b67 (reconocido):** las poses 111/112 se copiaron de la 120, que es **Duggan** tumbado (calzón azul, mallas blancas, barba castaña). La captura "boca abajo" mostraba a Duggan dos veces y la etiqueta era falsa.

**Arreglo:**
- Nueva pose MD **626** = Ultimate Warrior **boca abajo REAL**, sacada del banco arcade **0 (Warrior)**, pose 157. Cabeza completa (pelo rubio), espalda, calzón, botas moradas; 4 piezas, 39 tiles, paleta línea 2.
- Colores: mismo mapa arcade→MD que ya usa la pose 114 (Warrior boca arriba, verificado píxel a píxel contra arcade pose 23, coincidencia 100 %).
- Secuencia de derribo: doblado 45 (8 f) → **boca abajo 626 (6 f)** → **hold boca arriba 114 (68 f, Warrior)** → rodillas 115 → atontado 116/117.
- `wrDown` pasa a u16 (626 no cabe en u8). Warrior ya no usa 111/112/120 (Duggan) en ningún momento.

**Verificado a ojo en MAME:**
- `shots/b68_boca_abajo_WARRIOR.png` (+ _x3): tumbado boca abajo = **Warrior** (pelo rubio, botas moradas); de pie = **Duggan** (barba, calzón azul) rematando la patada.
- `shots/b68_boca_arriba_WARRIOR.png` (+ _x3): tumbado boca arriba = **Warrior** (pintura facial, pelo rubio); de pie = Duggan.
- `shots/b68_pose626_vs_114.png`: las dos poses aisladas.
(En la prueba se coloca a Warrior más arriba del ring para que no lo tape la cuerda delantera.)

Sin tocar: golpes A/B, START seguir/parar, orientación, Macho, Hogan, árbitro, cuerdas, cámara, HUD, sonido. Warrior aún no pega.
Prueba MAME: `test/t68.lua`. Herramienta: `tools68/addfd.py`.
