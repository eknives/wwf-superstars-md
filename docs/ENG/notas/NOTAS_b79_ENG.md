# b79 — base b78 preserved

ROM: `wwf_b79.bin` (1,572,864 bytes).
Base intact: `/workspace/b78/wwf_b78.bin`, MD5 `baa09bf2c1316b25c6881ca0ec0a4019`.

**Only change:** **short** rope vibration on crashing and falling, with real tile redraw (arcade). The running bounce (long sequence `sc0`/`sc1`) is not touched.

## Problem in b78

`bounceRope(..., 1)` set `rk=48` inside `sc[]`. That lands in the late phase 6↔7 of the long timeline, **not** at the arcade start of step 2. Emilio: the rope was not animating (as a crash vibration).

## Arcade (analisis)

- **0x9700 `marcar_cuerda`**: bit15 + nibble `d0` in `1C1898`/`1C189A`. Always restarts.
- **0x21324 `cuerda_vibrar`**: if bit15 and nibble≠0 → **step 2**, dur `0x213A4[2]=6`, frame reg=3.
- **0x213A4**: `10 08 06 04 03 02 02 01`.
- **0x2146e** (map index per step): `00 01 02 01 02 01 02 03`.
- **0x213B4 → 0x21412/0x21420**: if vibrating and the index changed, copies the tile block of the struck side.

Short (steps 2..7): maps **2,1,2,1,2,3** and then rest. Ticks 6+4+3+2+2+1=18 (×2 in the port = 36 frames).

Who asks for short: **0x9F02** and **0xF9B0** with `d0=1`. Long: **0x960A** with `d0=0`.

## Port b79

- `rFall`/`rStep`/`rTimer` + tables `ropeDurA` / `ropeMapA`.
- Fall: always restarts (like bit15), initial map 2, immediate `ropeDraw`.
- Short tick: advances steps 2..7; when finished restores map 0 and redraws.
- Fall `bounceRope(..., 0)` / `sc[]` unchanged.

## Validation

MAME test `rope` (x=627): `rcur` goes 2→1→2→1→2→0 on the left side. Caps: `shots/b79_rope_frames_arcade_short.png`, diffs `b79_diff_rest_vs_map2.png`, `b79_diff_map2_vs_map1.png`.

## Build

Local SGDK, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` in `/workspace/b79`. b78 not overwritten.
