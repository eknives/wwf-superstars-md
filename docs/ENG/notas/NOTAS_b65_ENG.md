# b65 (from b64) — md5 ae934feebe83857623862ca7123f43b3
b64 intact. Only **Ultimate Warrior** is added:
- He appears standing inside the ring (660,262), arcade idle pose 6.
- **START alone** (press and release without A/B/C) = Warrior follows you; START again = he stays still. START+A/B/C is still the crowd as before.
- When following he **walks with the arcade animation** (poses 69-72, move_seq 704, 8 f each), speed ~2.5 px/f; still = pose 6. He faces Duggan (arcade H-flip).
- Follow distance: 40 px in X / 20 in Y. Clamp inside the ring (margin 8).
- No fighting, no AI, no collision (he can overlap the referee/Duggan).
- Sprite order by feet between Duggan, referee and Warrior; priority: HIGH, split LOW under the front rope (like the referee).
- Palette: line 2 (Duggan's, which is already the port's shared Duggan+Warrior palette). Line 3 (Macho/Hogan) untouched → Hogan the same.
- VRAM: Warrior at tile 1680 (0xD200, free gap of the window), 44 tiles.
Not touched: Duggan, Macho, Hogan, referee, ropes, camera, HUD, sound.
Shots: shots/b65_sigue_andando1/2.png, b65_sigue_arriba.png, b65_contact.png. MAME OK.
