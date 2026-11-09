# b84 (base b83, md5 028b1ee1de56104bb26ab5fc56810c80; b83 intact)

ROM: `wwf_b84.bin`, md5 `426988a7344009ffd63ad6e8f34e609b`. Local SGDK build.
Only completing the standing punch sequence (A) for Duggan and Warrior. No AI, no other moves.

## Bug (what Emilio saw)
- **Warrior:** since b76 the impact extended the arm (`xl_w[41]=765` = arcade bank 0 pose `0x152`), but the sequence skipped the wind-up `0x150` and did not follow the FD70 order.
- **Duggan:** `move_seq` did idle → pose 40 (`0x151`) → pose 41 (`0x150`) in 33 f; the third arcade pose `0x152` was missing and the order/timings were not those of FD70.

## Arcade (citations)
| Addr | What |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 table steps |
| 0xFD70 | Healthy punch: pose `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Combo alternative (`0x153`–`0x155`) when holding/chaining A — **not ported in b84** |
| Bank 0 | Warrior: `0x150`/`0x151`/`0x152` |
| Bank 3 | Duggan: same indices in his bank |

## b84 fix
1. **New pose 792** = Duggan bank 3 pose `0x152` (`tools/gen84_punch.py`, same method/cmap as gen76).
2. **Motor 168** (free u8 in `move_seq`): `xl_d[168]=792`, `xl_w[168]=765` (Warrior `0x152`).
3. **`xl_w[41]=658`** (Warrior `0x150`; previously 765). `xl_w[40]=657` (Warrior `0x151`, unchanged).
4. **`move_seq[0..9]`** = `41×4, 40×3, 168×3` (FD70). Rest of the 33 f block = 0 (padding; kick still at offset 33).
5. **`main.c`:** `L` punch = 10; `MV_HIT_PUN` = 10 (first frame of `0x152`).

## MAME Genesis verification (test/t84_pun.lua)
| Mode | dPose sequence | Hit |
|------|-----------------|-----|
| punD (Duggan) | 41 → 40 → 792 | vh Warrior=1 at mk=10 |
| pun (Warrior, C) | 658 → 657 → 765 | vh Duggan=1 on reaching 765 |

## Captures
- `shots/b84/warrior_{150,151,152}.png`
- `shots/b84/duggan_{150,151,152}.png`
- `shots/b84/ref_mame_warrior_punch.jpg` (Emilio's ref)

## Caveat
- The FD7C chaining (`0x153`–`0x155`) and the CPU path 0x15878 (40 f) have not been ported. One A = one FD70 punch.
- Palette of pose 792: cmap via the gen76 cmap (not invented; may differ by 1–2 indices from the canonical MD).

## Reproduce
```sh
cd /workspace/b84
python3 tools/gen84_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b84.bin && md5sum wwf_b84.bin
T84=punD mame genesis -cart wwf_b84.bin -autoboot_script test/t84_pun.lua ...
```
(The comment means: if the assets need regenerating.)
