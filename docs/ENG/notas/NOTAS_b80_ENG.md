# b80 — base b79 preserved

ROM: `wwf_b80.bin` (1,572,864 bytes).
MD5: `d843bac410485579980872341264fda9`
Base intact: `/workspace/b79/wwf_b79.bin`, MD5 `80c22913744ca241ac6a4673d64b7a09`.

**Only change:** when kicking out of the pin near the ropes, the rope vibrates with the arcade's **short** sequence. The running bounce (long) and the b79 short machine are not touched.

## Problem in b79 (Emilio's test)

Count near the ropes → kickout → the thrown wrestler crashes into the rope, but the rope **does not animate**.

Cause: the kickout throw uses action 8 sub **0x1C** (`fs==1`, arcade `0xB012` → `0x9B66`). In b79 the rope was only checked with `fs==2` (sub 1). Sub 0x1C flew, clamped at the edge and on touching the floor went to sub 0xC (`fs==4`) **without** calling `marcar_cuerda`.

## Arcade (analisis)

- **0xB012 `acc_alzar_lanzar`**: after 2 steps the covering wrestler → action 8 sub **0x1C**; the covered → action 5.
- **0x9B66**: init of sub 0x1C (text 0x9B, impulse ±0x10, physics table).
- **0x9CD0** (every frame in the air, after `0x9E78`): if `+0x9E&3` (rope contact):
  - if `+0x44 == 0x1C` → `+0x44 = 1` (goes to sub 1) and restarts action 8;
  - otherwise → `+0x44 = 2` (sub 2 = **0x9F02**).
- **0x9F02**: `moveq #1,d0` → **0x9700 `marcar_cuerda`** (nibble≠0).
- **0x21324 `cuerda_vibrar`**: nibble≠0 → starts at **step 2** (short sequence; b79).

Who already asked for short in the port: **0x9F02** (fall `fs==2→3`) and **0xF9B0** (hold). The **0x9CD0** link was missing for the 0x1C kickout.

## Port b80

In `fsStep`, after moving X of sub 0x1C:

```
if (fs==1 && fsRope) fs=2;          /* 0x9CD0: 0x1C → 1 */
if (fs==2 && fsRope) { fs=3; bounceRope(..., 1); }  /* 0x9CD0 → 0x9F02 */
```

Same short machine as b79 (`rFall` / `ropeMapA` / `ropeDurA`). `bounceRope(..., 0)` (running bounce) intact.

## Validation

Natural MAME test `t80_korope_nat.lua` (pin next to left rope, first kickout, without forcing ox):

| ROM | On throw | Result |
|-----|-----------|-----------|
| b79 | `fs=1 rFall=0 rcur=0` | `FAIL_no_rope_vib` |
| b80 | `fs=3 rFall=1 rcur=2` | `ok_rope_vib` short path 2→1→2→1→2→…→0 |

Captures: `shots/b80_01_kickout_start.png`, `b80_02_kickout_hit_rope_rc2.png`, `b80_03_vib_start_rc2.png`, `b80_ko_df015_rc1.png` (bowed rope), `b80_rope_kickout_strip.png`.

## Build

Local SGDK, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` in `/workspace/b80`. Only `src/main.c` changes. b79 not overwritten.
