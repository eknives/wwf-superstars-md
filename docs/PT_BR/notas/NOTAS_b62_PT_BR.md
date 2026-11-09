# b62 (a partir da b61): o árbitro anda como no arcade

ROM: `wwf_b62.bin`  md5 `6c4316bb90496df914dd0e75e6b536d8`
b61 intacta (`080a39c45570498fe8dab0dec0c8b4b8`); b58/b59/b60 também.

## Fonte do arcade
0xD8F4 seguir → 0xDA38 anim_8dir, tabela 0xDAC4: banco 9, frente 2-5 / costas 6-9, 4 frames × 8 ticks, flip se ref x ≥ objetivo x. Sem walk lateral.
Todas têm cabeça. 510-512 sem cabeça = falha de captura da s41 (rgrp), já não são usadas.

## Dados
`tools_rf62.py` (a partir da ROM do arcade, render_obj de analisis): poses do arcade 2-9 → MD **618-625** (frente 618-621, costas 622-625).
3 peças 32×24/32×32/32×24 (como a pose 8), 40 tiles cada (limite 41), acrescentados no final de spr_tiles/spr_tab.
Cor: linha 0, índices da pose 8 (2,4,6,7,8,10,11,13,15) pela cor mais próxima; pernas preto 15 + costura 10.

## Código (`rfStep`)
- Movendo: base = 622 se o Duggan está mais ao fundo (oy > rfy), senão 618; pose = base + ((rfPh>>3)&3).
- Flip = Duggan à esquerda (a arte do arcade olha para +x).
- Parado: congela o último frame e o flip (arcade). Antes do primeiro passo, idle 8.
- Seguimento, refAvoid, clamp e 1 px/f sem mudanças.

## Teste
`t62.lua` (esq., dir., cima, baixo; snap a cada 8 f). `shots/b62_walk_contact.png`, `shots/b62_walk_zoom.png`, `shots/b62_hoja_poses.png`, `shots/walk/`.
