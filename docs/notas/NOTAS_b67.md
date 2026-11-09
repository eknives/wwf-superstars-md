# b67 (desde b66) — md5 593ceefe80133aeb5b5e737fd1ec7807
b66 intacta (md5 037a4213d712fd0e7124bbe5322e1080). Novedades:

**Caída normal = boca arriba (pose 114)**
- El hold del derribo usa la pose arcade **114** (boca arriba), no el sustituto incompleto boca abajo.
- Secuencia: doblado (45, 8 f) → boca abajo breve (111, 6 f) → **hold boca arriba 114 (68 f)** → rodillas 115 → atontado 116/117.

**Boca abajo con cabeza completa**
- En b66 las poses 111/112 (t0=4080/3832, nt=34) salían **sin la cabeza** (falta un tile/sprite).
- En b67 111 y 112 copian la pose **120** del mismo banco Warrior (t0=4414, nt=46): mismos 5 trozos, cabeza incluida.
- Revisadas las poses de derribo/golpe/suelo (45, 111, 112, 114, 115–117): 114 ya traía los 5 trozos (nt=49); 111/112 eran las incompletas.

**Orientación corregida (invertir flip)**
- Idle 6 mira a la **izquierda** sin flip. Antes `wrFl = (ox < wrx)` lo ponía de espaldas al jugador.
- Ahora `wrFl = (ox > wrx)`: de pie mira **hacia** Duggan / el jugador.
- Tumbado / atontado / recibiendo: sigue sin girar (como b66).

**VRAM**
- Warrior ampliado a **56 tiles** (1680–1735) porque la pose 114 pide 49.
- Banco de puñetazo 0 movido 1728 → **1736** para no solaparse.

Sin tocar: golpes A/B de Duggan, START seguir/parar, Macho, Hogan, árbitro, cuerdas, cámara, HUD, sonido. Warrior aún no pega.
Shots: `shots/b67_orientacion.png`, `b67_boca_abajo.png`, `b67_boca_arriba.png` (+ k13/hold). Prueba MAME: `test/t67.lua` / `test/run67.sh`.
