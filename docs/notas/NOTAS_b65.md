# b65 (desde b64) — md5 ae934feebe83857623862ca7123f43b3
b64 intacta. Solo se añade **Ultimate Warrior**:
- Aparece de pie dentro del ring (660,262), pose idle arcade 6.
- **START solo** (pulsar y soltar sin A/B/C) = Warrior te sigue; otra vez START = se queda quieto. START+A/B/C sigue siendo el público como antes.
- Al seguir **camina con la animación arcade** (poses 69-72, move_seq 704, 8 f cada una), velocidad ~2,5 px/f; quieto = pose 6. Mira hacia Duggan (H-flip arcade).
- Distancia de seguir: 40 px en X / 20 en Y. Clamp dentro del ring (margen 8).
- Sin pelea, sin IA, sin colisión (puede solaparse con el árbitro/Duggan).
- Orden de sprites por pies entre Duggan, árbitro y Warrior; prioridad: ALTA, troceado LOW bajo la cuerda delantera (como el árbitro).
- Paleta: línea 2 (la de Duggan, que ya es la paleta compartida Duggan+Warrior del port). Línea 3 (Macho/Hogan) sin tocar → Hogan igual.
- VRAM: Warrior en tile 1680 (0xD200, hueco libre de la window), 44 tiles.
Sin tocar: Duggan, Macho, Hogan, árbitro, cuerdas, cámara, HUD, sonido.
Shots: shots/b65_sigue_andando1/2.png, b65_sigue_arriba.png, b65_contact.png. MAME OK.
