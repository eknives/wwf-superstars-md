# b83 (base b82, md5 b6c57f8cb194c7c7805b5a75b3775dc8; b82 intact)

ROM: `wwf_b83.bin`, md5 `028b1ee1de56104bb26ab5fc56810c80`. Local SGDK build.
Only Warrior's finisher on a downed opponent (zone + animation + 7D layers). Nothing invented: `/workspace/wwf_sgdk/analisis` + arcade ROM in MAME.

## b82 bug (what Emilio saw)
1. **Invented zone:** b82 used `X = ox±48` and `b7 = !vface`. From the **torso** (same X as the opponent) it launched the jump; in the arcade it does **not**.
2. **Wrong target:** `ox±16` instead of `±0x20` (table 0x111D0 / 0x159AC).
3. **Wrong orientation:** `p1face = vface` instead of copying bit7 and mapping `p1face = !bit7` (0x10A6C).
4. **7D baked wrong:** `native82` did a second mirror and `+4` in the bitmap → leg/fist **duplicated** to one side.
5. **Phase 0:** 4 invented ticks; arcade `0x112F0[0]=0` → 1 tick of pose 0x61.

## Arcade (citations)
| Addr | What |
|------|-----|
| 0xC706 / 0xC798–0xC8A8 | Selection: anchor = rival.x ±0x28 depending on bit7; front `<0x20` → sub 0x0C; behind `<0x30` → A sub5 / B sub6 |
| 0xC928–0xC95A | Pin only if d4==0 and d\<0x20; otherwise B → sub1 |
| 0xCB3C | Warrior: sub-action table by zone (B in front = 0x0C); byte dump omitted in the public version |
| 0xCB1A[0xB] | 0xFF → downed branch |
| 0x10A5E / 0x10A6C | Jump; copies the opponent's orientation |
| 0x111D0 / 0x159AC | Trajectory dx=0xFFE0 (−32), mirrored if bit7; vz=0x500 g=0x50 |
| 0x112F0 | Timers `0, 8, 4, FFFF` |
| 0x112FA | Poses `61 62 7A 7B 7B` (+ variant `61 62 76 77 77`) |
| 0x10D9E / 0x10F04 | Impact: z=floor, y=rival−1+0xA |
| 0x1152A | Object 1C0AB2 pose **0x7D**: y−0xA, x∓4, z+0xA, **opposite orientation** |

## b83 fix
- `warriorGroundZone`: `X = fd[o].ox`, `b7 = vface` (fsStart already copies bit7 → vface). **No ±48.**
- Target: `ox ± 0x20`; `p1face = !vface`.
- Phase 0: 1 tick.
- 7D: tiles without mirror/+4; in `drawF` the aux layer uses the **opposite flip** and **dx = fl ? −4 : +4** (1152A). Sort y−10.

## MAME Genesis + arcade tests
| Case | Result |
|------|-----------|
| diveL / headL | 712→727 impact y=309 pose787 — **same as arcade log** |
| diveR / headR | 808→793 |
| feetL/R, **torsoR** | **does not jump** (gs=0) |
| front31 / front32 | 12 / 0 |
| behind47 / behind48 | 13 / 0 |
| stompR, pinL/R | OK |
| Arcade MAME `shots/arcade/k063` | aux 7D at x=723 (=727−4), y=299 (=309−10) |

## Captures
- `shots/arcade/` — MAME wwfsstar floor (not corner).
- `shots/FINAL_b83/compare_arcade_vs_b83.png` — arcade vs port.
- `shots/FINAL_b83/port_diveL_pose_*.png`

## Reproduce
```sh
cd /workspace/b83
python3 tools/native82.py
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b83.bin && md5sum wwf_b83.bin
./test/run83.sh diveL
```
