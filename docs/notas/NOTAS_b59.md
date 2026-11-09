# b59 (desde b58)

ROM: `wwf_b59.bin`  md5 `9147ee11d533442397987e165520be45`

b58 intacta (md5 `cbe3a2b0976a142ceb25068edc660869`). Solo cambian colores de compañeros (PAL3).

## Cambios

1. `res/spr_pal.bin` PAL3:
   - idx 7 (off 0x2E): `0006` → `0024` — barba Macho marrón oscuro.
   - idx 4 (off 0x28): `02C8` → `00CE` — Hogan amarillo cálido (pelo, calzón, botas).
2. `res/spr_tiles.bin`: pose 449 (Macho), tiles 14254..14296 (43): nibble 4 → 13 (granate `0228`), 96 px = calzón. Ninguna otra pose usa ese rango. Tiles de Hogan (450) sin tocar.
3. Resto igual que b58 (árbitro, clamps, walk, HUD). Diff ROM vs b58: 66 bytes.

## Test

Arranque OK. Shots (t56.lua): `shots/b59_macho_izq.png`, `shots/b59_hogan_dcha.png`.
Preview offline: `/workspace/tmp/pal3_preview_hogan_calido_macho13.png`.
