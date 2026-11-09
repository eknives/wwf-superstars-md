# b61 (from b59)

ROM: `wwf_b61.bin`  md5 `080a39c45570498fe8dab0dec0c8b4b8`

b59 (`9147ee11d533442397987e165520be45`) and b60 (`5986c9c1f2a51854b2ebda56407ce6a0`) intact.
Base b59: Macho on the apron (602,338), LOW, pose 449 (not the referee route). Hogan (939,280) LOW. b59 palette (7=0024, 4=00CE, Macho's trunks→13).

## Change: loose strip on the left rope (plane A), removed (it does not go to plane B)

mp0 cells (row,col) (24,24) and (23,25), top-left corner post. Strip pixels = indices 6/8/2/A/F; rope = 5/C/1.
- frame 0: (24,24) `0x8464` (tile 1124, strip only) → `0x0` in `src/ropes.h`.
- tiles cleaned in `res/ropes_tiles.bin` (only 5/C/1 remain):
  - 1123 = (23,25) frame 0
  - 1182 = (24,24) frames 1–4
  - 1280 = (24,24) frame 7
  - 1237 = (23,25) frames 5–6
  Each tile is only used in that cell → edited in place (equivalent to a clean copy, no new tiles).
- Nothing else of the top corner post is redrawn (art pending from Emilio).

## Test

Boot OK (t56.lua). Shots: `shots/b61_macho_apron.png`, `shots/b61_macho_cara_zoom.png`, `shots/b61_hogan_dcha.png`.

## State
Delivered (md5 080a39c45570498fe8dab0dec0c8b4b8): strip removed, Macho on the apron.
