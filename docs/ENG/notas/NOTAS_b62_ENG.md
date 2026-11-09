# b62 (from b61): the referee walks like the arcade

ROM: `wwf_b62.bin`  md5 `6c4316bb90496df914dd0e75e6b536d8`
b61 intact (`080a39c45570498fe8dab0dec0c8b4b8`); b58/b59/b60 too.

## Arcade source
0xD8F4 follow → 0xDA38 anim_8dir, table 0xDAC4: bank 9, front 2-5 / back 6-9, 4 frames × 8 ticks, flip if ref x ≥ target x. No sideways walk.
All of them have a head. 510-512 without a head = s41 capture error (rgrp), no longer used.

## Data
`tools_rf62.py` (from the arcade ROM, render_obj from analisis): arcade poses 2-9 → MD **618-625** (front 618-621, back 622-625).
3 pieces 32×24/32×32/32×24 (like pose 8), 40 tiles each (limit 41), added at the end of spr_tiles/spr_tab.
Colour: line 0, pose 8 indices (2,4,6,7,8,10,11,13,15) by closest colour; legs black 15 + seam 10.

## Code (`rfStep`)
- Moving: base = 622 if Duggan is further back (oy > rfy), otherwise 618; pose = base + ((rfPh>>3)&3).
- Flip = Duggan on the left (arcade art faces +x).
- Stopped: freezes the last frame and flip (arcade). Before the first step, idle 8.
- Following, refAvoid, clamp and 1 px/f unchanged.

## Test
`t62.lua` (left, right, up, down; snap every 8 f). `shots/b62_walk_contact.png`, `shots/b62_walk_zoom.png`, `shots/b62_hoja_poses.png`, `shots/walk/`.
