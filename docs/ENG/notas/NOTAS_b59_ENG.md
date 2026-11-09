# b59 (from b58)

ROM: `wwf_b59.bin`  md5 `9147ee11d533442397987e165520be45`

b58 intact (md5 `cbe3a2b0976a142ceb25068edc660869`). Only partner colours change (PAL3).

## Changes

1. `res/spr_pal.bin` PAL3:
   - idx 7 (off 0x2E): `0006` → `0024` — Macho's beard dark brown.
   - idx 4 (off 0x28): `02C8` → `00CE` — Hogan warm yellow (hair, trunks, boots).
2. `res/spr_tiles.bin`: pose 449 (Macho), tiles 14254..14296 (43): nibble 4 → 13 (maroon `0228`), 96 px = trunks. No other pose uses that range. Hogan's tiles (450) untouched.
3. Rest the same as b58 (referee, clamps, walk, HUD). ROM diff vs b58: 66 bytes.

## Test

Boot OK. Shots (t56.lua): `shots/b59_macho_izq.png`, `shots/b59_hogan_dcha.png`.
Offline preview: `/workspace/tmp/pal3_preview_hogan_calido_macho13.png`.
