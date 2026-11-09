# b66 (desde b65) — md5 037a4213d712fd0e7124bbe5322e1080
b65 intacta. Novedades:

**Golpes básicos de Duggan (arcade, secuencias move_seq del port s05-s07)**
- **A = puñetazo** (33 f, poses 40-41), **B = patada** (31 f, poses 42-43). A+B sigue siendo correr (como antes).
- Impacto en el frame arcade: puñetazo f24, patada f18. Alcance 40 / 42 px en X y 7 px en Y, solo si Warrior está delante.
- Al pegar, si Warrior está cerca (±64 X, ±24 Y), Duggan se gira hacia él. Mirando a la izquierda los golpes usan H-flip.
- Solo desde suelo normal (no en esquineros, fuera del ring, carrera ni rebote).

**Warrior recibe golpes (no pega todavía)**
- Puñetazo → reacción arcade (pose 44, 13 f). Patada → doblado (pose 45, 41 f).
- Daño acumulado: puñetazo 1, patada 4; al llegar a 8 → **derribo**: doblado → tumbado (111/112, ~74 f) → de rodillas (115) → **atontado** (116/117, ~96 f) → de pie.
- El daño acumulado se pierde a los 3 s sin recibir golpes. Tumbado no recibe golpes.

**Orientación de Warrior**
- De pie: siempre mira a Duggan (como b65).
- Recibiendo golpe / tumbado / de rodillas / atontado: **no se gira** (queda como cayó) y no se mueve ni sigue.
- Esquineros: Warrior todavía no sube a los esquineros, así que la regla de esquineros aún no se aplica (queda lista para cuando suba).

**START**: igual que b65 (sigue / se para, caminando con animación). Durante golpe/derribo no se mueve; al levantarse vuelve a seguir si estaba en modo seguir.

VRAM Warrior ampliada a 48 tiles (1680-1727; antes 44) para la pose 44.
Sin tocar: Macho, Hogan, árbitro, cuerdas, cámara, HUD, sonido.
Shots: shots/b66_punetazo_reaccion.png, b66_patada_derribo.png, b66_tumbado.png, b66_atontado.png, b66_contact.png. Prueba MAME: test/t66.lua.
