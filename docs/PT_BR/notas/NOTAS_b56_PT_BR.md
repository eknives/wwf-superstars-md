# b56 (a partir da b55)

ROM: wwf_b56.bin  md5 69171a59c5c65f55f93bfeb09de3d094

Só parceiros no avental, para ver as cordas (b55 intacta):

- **Macho Man** parceiro ESQUERDO (602,338); **Hogan** parceiro DIREITO (939,280). Posições do arcade (s35).
- Estáticos (pose fixa 449 / 450, as mesmas de s35–s46). Sem IA, sem colisão, sem troca.
- Sprites com prioridade **BAIXA** sempre (cordas no plano A alto na frente). Na SAT vão atrás do Duggan.
- Assets: spr_tab/spr_tiles da b55 (idênticos ao wwf_sgdk). Tiles remapeados para PAL2 (a PAL3 é usada por cordas+HUD) → res/part_tiles.bin. Nota: essas poses trazem uma corda pintada dentro (da s35); fica embaixo da corda do plano A.
- VRAM: Macho no tile 1728 (0xD800), Hogan no 1941 (0xF2A0), zonas livres; não se mexe no pool, nas cordas nem no Duggan.

Sem mexer: cordas, fundo, HUD, RING_XL/XR, controles, som, córneres, logo.
Shots: shots/b56_macho_izq.png, shots/b56_hogan_dcha.png. O MAME inicia OK.
