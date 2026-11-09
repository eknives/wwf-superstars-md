# b61 (desde b59)

ROM: `wwf_b61.bin`  md5 `080a39c45570498fe8dab0dec0c8b4b8`

b59 (`9147ee11d533442397987e165520be45`) y b60 (`5986c9c1f2a51854b2ebda56407ce6a0`) intactas.
Base b59: Macho en apron (602,338), LOW, pose 449 (no ruta árbitro). Hogan (939,280) LOW. Paleta b59 (7=0024, 4=00CE, calzón Macho→13).

## Cambio: tira suelta en la cuerda izquierda (plano A), eliminada (no va a plano B)

Celdas mp0 (fila,col) (24,24) y (23,25), esquinero sup. izq. Píxeles de la tira = índices 6/8/2/A/F; cuerda = 5/C/1.
- frame 0: (24,24) `0x8464` (tile 1124, solo tira) → `0x0` en `src/ropes.h`.
- tiles limpiados en `res/ropes_tiles.bin` (se quedan solo 5/C/1):
  - 1123 = (23,25) frame 0
  - 1182 = (24,24) frames 1–4
  - 1280 = (24,24) frame 7
  - 1237 = (23,25) frames 5–6
  Cada tile solo se usa en esa celda → editados en sitio (equivale a copia limpia, sin tiles nuevos).
- No se redibuja nada más del esquinero superior (arte pendiente de Emilio).

## Test

Arranque OK (t56.lua). Shots: `shots/b61_macho_apron.png`, `shots/b61_macho_cara_zoom.png`, `shots/b61_hogan_dcha.png`.

## Estado
Entregada (md5 080a39c45570498fe8dab0dec0c8b4b8): tira quitada, Macho en el apron.
