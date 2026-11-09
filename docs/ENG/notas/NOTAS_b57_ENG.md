# b57 (from b56)

ROM: wwf_b57.bin  md5 8651e4ef71af09be6260350b1489e20d

Only palette distribution + visible referee (b56 intact):

| Line | b56 | b57 |
|---|---|---|
| 0 | background + crowd | background + crowd + **ropes** (380 tiles) + referee (pieces 0-1) |
| 1 | background + crowd | background + crowd + **ropes** (11 tiles) + **HUD** + referee (piece 2) |
| 2 | Duggan + Macho/Hogan remapped | **Duggan only** |
| 3 | ropes + HUD (palR3) | **partners** (spr_pal 16..31, as in s35) |

- Partners: original tiles of poses 449/450 (no remap to Duggan's; part_tiles is no longer used), line 3.
- Ropes: each tile remapped to the closest colour of line 0 or 1 (whichever gives less error); palette bits of map A changed. Almost all tones exist exactly in line 0; 0x00A, 0xAAA, 0x222, 0x444 are missing → approximated.
- HUD: line 1. Light blue E44 → A00, dark blue 822 → 442, black → index 7 (000). It is not perfect.
- Referee: arcade pose 8, (768,352), static, HIGH priority, no interaction. Its pieces already came in lines 0/1 (original palette). VRAM 1088 (28 t) and 1512 (9 t), free gaps. At the back centre the head ends up under the HUD window.
- Not touched: positions, priority, clamps, corner posts, logo, controls, sound.

Shots: shots/b57_companeros.png, shots/b57_arbitro.png. MAME boots OK; not tested on hardware.
