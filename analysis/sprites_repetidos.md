# Sprites/tiles repetidos de verdad (solo nota, sin optimizar)

Medido sobre `res/spr_tiles.bin` de s65 (31-10-2026). Aquí solo entran los duplicados idénticos píxel a píxel.

- **Tiles 8×8 idénticos exactos:** 4664 de 19073, unos 145 KB.
  - Ojo: en Mega Drive un sprite usa tiles consecutivos. Solo se pueden quitar si coincide la pieza entera, es decir, un bloque contiguo del sprite.
  - Falta medir cuántos de esos tiles forman piezas completas idénticas.
- **Tiles idénticos en espejo H/V:** 315 más.
  - El hardware solo espeja el sprite entero, no tile a tile. Así que no se pueden quitar salvo que coincida una pieza completa espejada.
- **Poses enteras idénticas:** 0. Ya se quitaron en s64 (−6936 tiles).

Árbitro, Macho Man y Hogan: se añadirán al extraerlos.

## s66 wip8 (presa 0x26 de Warrior, MAME p88)
- Pose 8C de la presa = poses 586 (Warrior) y 580 (Duggan) ya existentes: idénticas en píxel y paleta, se reutilizan (no se duplican).
- Poses nuevas 608, 609, 610 y 611: ninguna es idéntica a una pose existente.
