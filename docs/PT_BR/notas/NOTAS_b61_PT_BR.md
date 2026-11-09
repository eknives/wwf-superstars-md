# b61 (a partir da b59)

ROM: `wwf_b61.bin`  md5 `080a39c45570498fe8dab0dec0c8b4b8`

b59 (`9147ee11d533442397987e165520be45`) e b60 (`5986c9c1f2a51854b2ebda56407ce6a0`) intactas.
Base b59: Macho no avental (602,338), LOW, pose 449 (não pela rota do árbitro). Hogan (939,280) LOW. Paleta b59 (7=0024, 4=00CE, calção do Macho→13).

## Mudança: tira solta na corda esquerda (plano A), eliminada (não vai para o plano B)

Células mp0 (linha,col) (24,24) e (23,25), córner superior esquerdo. Pixels da tira = índices 6/8/2/A/F; corda = 5/C/1.
- frame 0: (24,24) `0x8464` (tile 1124, só tira) → `0x0` em `src/ropes.h`.
- tiles limpos em `res/ropes_tiles.bin` (ficam só 5/C/1):
  - 1123 = (23,25) frame 0
  - 1182 = (24,24) frames 1–4
  - 1280 = (24,24) frame 7
  - 1237 = (23,25) frames 5–6
  Cada tile só é usado nessa célula → editados no lugar (equivale a uma cópia limpa, sem tiles novos).
- Nada mais do córner superior é redesenhado (arte pendente do Emilio).

## Teste

Início OK (t56.lua). Shots: `shots/b61_macho_apron.png`, `shots/b61_macho_cara_zoom.png`, `shots/b61_hogan_dcha.png`.

## Estado
Entregue (md5 080a39c45570498fe8dab0dec0c8b4b8): tira removida, Macho no avental.
