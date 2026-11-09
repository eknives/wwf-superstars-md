# b78 — base b77 preserved

ROM: `wwf_b78.bin` (1,572,864 bytes).
Base intact: `/workspace/b77/wwf_b77.bin`, MD5 `947bdf6ccc66d33c7d9ecc526e3e8e97`.

**Only change:** the rope vibration on **crashing and falling** uses the arcade's short sequence (it starts at step 2 / frame 3). The running bounce (long sequence) is not touched.

## Arcade

Sources: `analisis/arc_rec.dis`, `analisis/rutinas.md`, `analisis/tools/prog.bin`.

- **0x9700 `marcar_cuerda`**: sets bit15 and the low nibble = `d0` in `1C1898` / `1C189A` (side).
- **0x21324 `cuerda_vibrar`**: if bit15, starts sound 0x2A and bit14=vibrating.
  - nibble `d0 == 0` → step **0**, frame **1** (long sequence).
  - nibble `d0 != 0` → step **2**, frame **3** (short sequence).
  - Advances up to step 8 with durations **0x213A4** = `10 08 06 04 03 02 02 01` (42 ticks) and frames **0x213AC** = `01 02 03 02 03 02 03 00` (&3).
- Who asks for what:
  - **0x960A** running bounce: `moveq #0,d0` → `0x9700` → long.
  - **0x9F02** crash and fall: `moveq #1,d0` → `0x9700` → short.
  - **0xF9B0** fall during a hold stuck to the rope: `move.w #1,d0` → `0x9700` → short.

From step 2: `6+4+3+2+2+1 = 18` ticks. Steps 0+1: `16+8 = 24` ticks.

## Port

`bounceRope` used to always set `rk[sd]=0` (long). Now:

- `fall==0` (running / whip contact): `rk=0` (same as b77).
- `fall==1` (0x9F02 and 0xF9B0): `rk=48`.

`sc0`/`sc1` have `NS=84 = 2×42`. Skipping steps 0+1 = `2×(0x10+0x08) = 48`; `2×18 = 36` frames of short vibration remain. Tiles, maps and the long animation have not been changed.

Calls:
- `bounceRope(..., 1)`: `fs` fall against the rope (0x9F02) and fall during a hold 0xF9B0.
- `bounceRope(..., 0)`: running bounce and the victim's contact in the whip.

## Build

- Local SGDK, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`.
- `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` in `/workspace/b78`.
- Only `src/main.c` was rebuilt; resources identical to b77.
- b77 has not been overwritten.

## Limits

The fall physics, the lock-up, the referee and the pin kick-out have not been touched. Only the start of the rope animation in the crash-and-fall routes.
