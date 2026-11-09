# b62 (desde b61): árbitro camina como el arcade

ROM: `wwf_b62.bin`  md5 `6c4316bb90496df914dd0e75e6b536d8`
b61 intacta (`080a39c45570498fe8dab0dec0c8b4b8`); b58/b59/b60 también.

## Fuente arcade
0xD8F4 seguir → 0xDA38 anim_8dir, tabla 0xDAC4: banco 9, frente 2-5 / espalda 6-9, 4 frames × 8 ticks, flip si ref x ≥ objetivo x. Sin walk lateral.
Todas llevan cabeza. 510-512 sin cabeza = fallo de captura s41 (rgrp), ya no se usan.

## Datos
`tools_rf62.py` (desde ROM arcade, render_obj de analisis): poses arcade 2-9 → MD **618-625** (frente 618-621, espalda 622-625).
3 piezas 32×24/32×32/32×24 (como pose 8), 40 tiles c/u (límite 41), añadidos al final de spr_tiles/spr_tab.
Color: línea 0, índices de pose 8 (2,4,6,7,8,10,11,13,15) por color más cercano; piernas negro 15 + costura 10.

## Código (`rfStep`)
- Moviendo: base = 622 si Duggan más al fondo (oy > rfy), si no 618; pose = base + ((rfPh>>3)&3).
- Flip = Duggan a la izquierda (arte arcade mira a +x).
- Parado: congela último frame y flip (arcade). Antes del primer paso, idle 8.
- Seguimiento, refAvoid, clamp y 1 px/f sin cambios.

## Test
`t62.lua` (izq, dcha, arriba, abajo; snap cada 8 f). `shots/b62_walk_contact.png`, `shots/b62_walk_zoom.png`, `shots/b62_hoja_poses.png`, `shots/walk/`.
