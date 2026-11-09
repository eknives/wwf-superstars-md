# b59 (a partir da b58)

ROM: `wwf_b59.bin`  md5 `9147ee11d533442397987e165520be45`

b58 intacta (md5 `cbe3a2b0976a142ceb25068edc660869`). Só mudam as cores dos parceiros (PAL3).

## Mudanças

1. `res/spr_pal.bin` PAL3:
   - idx 7 (off 0x2E): `0006` → `0024` — barba do Macho marrom-escura.
   - idx 4 (off 0x28): `02C8` → `00CE` — Hogan amarelo quente (cabelo, calção, botas).
2. `res/spr_tiles.bin`: pose 449 (Macho), tiles 14254..14296 (43): nibble 4 → 13 (grená `0228`), 96 px = calção. Nenhuma outra pose usa essa faixa. Tiles do Hogan (450) sem mexer.
3. Resto igual à b58 (árbitro, clamps, walk, HUD). Diff da ROM vs b58: 66 bytes.

## Teste

Início OK. Shots (t56.lua): `shots/b59_macho_izq.png`, `shots/b59_hogan_dcha.png`.
Preview offline: `/workspace/tmp/pal3_preview_hogan_calido_macho13.png`.
