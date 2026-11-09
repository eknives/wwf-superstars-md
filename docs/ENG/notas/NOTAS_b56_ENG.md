# b56 (from b55)

ROM: wwf_b56.bin  md5 69171a59c5c65f55f93bfeb09de3d094

Only partners on the apron, to see the ropes (b55 intact):

- **Macho Man** LEFT partner (602,338); **Hogan** RIGHT partner (939,280). Arcade positions (s35).
- Static (fixed pose 449 / 450, the same as s35–s46). No AI, no collision, no tag.
- Sprites with **LOW** priority always (ropes on high plane A in front). In the SAT they go behind Duggan.
- Assets: spr_tab/spr_tiles from b55 (identical to wwf_sgdk). Tiles remapped to PAL2 (PAL3 is used by ropes+HUD) → res/part_tiles.bin. Note: those poses bring a rope painted inside (from s35); it stays under the plane A rope.
- VRAM: Macho at tile 1728 (0xD800), Hogan at 1941 (0xF2A0), free zones; the pool, ropes and Duggan are not touched.

Not touched: ropes, background, HUD, RING_XL/XR, controls, sound, corner posts, logo.
Shots: shots/b56_macho_izq.png, shots/b56_hogan_dcha.png. MAME boots OK.
