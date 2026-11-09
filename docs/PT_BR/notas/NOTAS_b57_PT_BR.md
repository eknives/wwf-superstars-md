# b57 (a partir da b56)

ROM: wwf_b57.bin  md5 8651e4ef71af09be6260350b1489e20d

Só distribuição de paletas + árbitro visível (b56 intacta):

| Linha | b56 | b57 |
|---|---|---|
| 0 | fundo + público | fundo + público + **cordas** (380 tiles) + árbitro (peças 0-1) |
| 1 | fundo + público | fundo + público + **cordas** (11 tiles) + **HUD** + árbitro (peça 2) |
| 2 | Duggan + Macho/Hogan remapeados | **só Duggan** |
| 3 | cordas + HUD (palR3) | **parceiros** (spr_pal 16..31, como na s35) |

- Parceiros: tiles originais das poses 449/450 (sem remap para a do Duggan; part_tiles já não é usado), linha 3.
- Cordas: cada tile remapeado para a cor mais próxima da linha 0 ou 1 (a que der menos erro); bits de paleta do mapa A alterados. Quase todos os tons existem exatos na 0; faltam 0x00A, 0xAAA, 0x222, 0x444 → aproximados.
- HUD: linha 1. Azul claro E44 → A00, azul escuro 822 → 442, preto → índice 7 (000). Não fica perfeito.
- Árbitro: pose 8 do arcade, (768,352), estático, prioridade ALTA, sem interação. Suas peças já vinham nas linhas 0/1 (paleta original). VRAM 1088 (28 t) e 1512 (9 t), espaços livres. No centro-fundo a cabeça fica sob a janela do HUD.
- Sem mexer: posições, prioridade, clamps, córneres, logo, controles, som.

Shots: shots/b57_companeros.png, shots/b57_arbitro.png. O MAME inicia OK; não testado em hardware.
