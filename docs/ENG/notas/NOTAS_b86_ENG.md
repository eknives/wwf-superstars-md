# b86 (base b85, md5 0477ea3fbf29e81b98a79ca1d574abf0; b85 intact)

ROM: `wwf_b86.bin`. Local SGDK build (`PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`).
Only: (1) arcade punch timing, (2) combo by **presses** (not hold), (3) Clothesline with hit + opponent reaction. No AI, no other moves.

## What Emilio asked for
b85 chained FD70↔FD7C with **hold** (`joyHeld`) and it looked too fast. In the arcade A is not held: it is several presses. In addition, both wrestlers' Clotheslines had no collision or reaction.

## Arcade (citations)

### Punches — `sub_combo_golpes` 0xFC84
| Addr | What |
|------|-----|
| 0xFC84 | Three steps; at steps `+0x36==0xB/0xC` it does `OR +0x114 → +0x22` (**newly pressed**, not hold) |
| 0xFD2E | At the end: if `+0x22 & 3 == 1` (button 1 only) → `eori #$1,+0xC0` and repeats; otherwise → action 0 |
| 0xFD70 | Healthy punch: `0x150`×4, `0x151`×3, `0x152`×3 |
| 0xFD7C | Alternative: `0x153`×4, `0x154`×3, `0x155`×3 |
| 0xFD48 | When chaining: `$8=1` (loads the 1st pose of the other half on the next frame) |

Content (public version, no byte dump): FD70 = poses 0x150, 0x151, 0x152 with waits 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 with waits 4, 3, 3.

GameFAQs: `Punch = P (1 after 3 Punches)` → after the 3 poses of a half, another P press continues.

### Clothesline — running A → sub 0x14
| Addr | What |
|------|-----|
| 0x93EE | `acc_correr`: 0xCC26 can launch a running strike |
| 0xCD14 | A while running: Warrior/Duggan → sub **0x14** |
| 0xFB58+0x14*4 | → `0x12E7A` `sub_carrera_hombro` |
| 0x1302E | Charge poses: `0x1D0`×6, `0x1D1`×4, `0x1DA`×4, `0x1DB`×6, … |
| 0x12E7A | Connects before step 0x10 (+0xC9 bit3); at step 0xC the opponent → action **8** sub **0x17** |
| 0x9B9A | `rec_lanzado_20` (impulse 0x20) |
| 0x16634 | Collision proximity filter: \|dx\|<0x60, \|dy\|<8 |

GameFAQs: `Clothesline = P (2)` while running.

## b86 fix
1. **Combo by presses:** `pAcc` (= +0x22). During the last pose (mk 10..12 = 0x152/0x155) the A edge is accumulated (`pendBtn`, already +0x114). At the end of the half: only if `(pAcc & (A|B)) == A` → `pAlt^=1; mk=2` (equiv. `$8=1`). Hold **no longer** chains.
2. **Timing:** the FD70/FD7C durations (4+3+3) are kept in `move_seq`; no multipliers are invented. The perceived pace drops because you have to press again between halves.
3. **Clothesline hit:** at `rn==3`, if `rnk∈[1,20]` and the opponent is at ≤0x60/≤8: `vdmg+=2`, `fsStart(o,1,…)` = thrown fall (action 8 / `rec_lanzado_20`). `rnW` prevents multi-hit. Both wrestlers (same engine).

## Caveats
- The CPU path 0x15878 and André (FD88/FD94) are not ported.
- The attacking Clothesline animation is still the MD track `atkR/atkL` (already in b83+); arcade poses 0x1D0–0x1DB are not regenerated.
- `fsStart(...,1,...)` uses the port's impulse (thrown); arcade sub 0x17 is exactly 0x20 in A74A parameters — an approximation using the already-ported fall system.
- One overlap frame when chaining (like the arcade's `$8=1`).

## Reproduce
```sh
cd /workspace/b86
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b86.bin && md5sum wwf_b86.bin
```

Manual test: one tap of A = FD70 only (0x150–152). A second tap of A during the last pose → FD7C. Holding without releasing must not chain. A+B while running → run; A alone while running → Clothesline; on connecting, the opponent flies/falls.
