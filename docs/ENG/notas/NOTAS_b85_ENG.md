# b85 (base b84, md5 426988a7344009ffd63ad6e8f34e609b; b84 intact)

ROM: `wwf_b85.bin`, md5 `0477ea3fbf29e81b98a79ca1d574abf0`. Local SGDK build.
Only the complete arcade punch sequence/combo (FD70+FD7C) for Duggan and Warrior. No AI, no other moves.

## What Emilio asked for
b84 only did FD70 (one punch: 0x150–0x152). A combo **is** the sequence: FD7C (0x153–0x155) must be ported too, identical to the arcade.

## Arcade (citations, prog.bin)
| Addr | What |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 steps; with button 1 at the end it does `eori #$1,$c0` and repeats |
| 0xFD70 | Healthy punch: `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Combo alternative: `0x153`×4, `0x154`×3, `0x155`×3 (10 f) — used with +0xC0 bit0 |
| 0xFD88/0xFD94 | Variant id 7 (André) — does not apply to Duggan/Warrior |

Content (public version, no byte dump): FD70 = poses 0x150, 0x151, 0x152 with waits 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 with waits 4, 3, 3.

## b85 fix
1. **New poses** (`tools/gen85_punch.py`, same method/cmap as gen76/gen84):
   - Duggan bank 3: 793=`0x153`, 795=`0x154`, 797=`0x155` (792=`0x152` already in b84)
   - Warrior bank 0: 794=`0x153`, 796=`0x154`, 798=`0x155` (658/657/765 = 0x150/151/152 already in b84)
2. **Motors** 169/170/171 → xl_w/xl_d to those poses.
3. **`move_seq`**: `[0..9]=FD70` (41×4,40×3,168×3); `[10..19]=FD7C` (169×4,170×3,171×3); kick still at 33.
4. **`main.c`**: `pAlt` (= +0xC0 bit0). Half L=10; `so = pAlt?10:0`. At the end of the half, if A is still held (`joyHeld`) → `pAlt^=1; mk=0` (chains). Otherwise → idle and `pAlt=0`. A short tap = FD70 only.

## MAME Genesis verification
| Mode | Result |
|------|-----------|
| tap A (2 f) | motors 41→40→168; no 169–171; final pAlt 0 |
| holdD | 41×4,40×3,168×3 → 169×4,170×3,171×3 → alternates while A |
| holdW (ctl=1) | Warrior poses 658→657→765→794→796→798 (0x150–0x155) |

## Captures
- `shots/b85/{duggan,warrior}_{150..155}.png`
- `shots/b85/{duggan,warrior}_combo_*.png` (hold)
- `test/t85_pun.lua`, `test/t85_tap.lua`

## Caveats
- The CPU path 0x15878 (40 f / durations ×6) is not ported.
- André (FD88/FD94) out of scope.
- Palette of new poses via cmap (may differ by 1–2 indices from the canonical MD).
- One hold frame of the last pose when chaining (like the arcade's `$8=1` reset).

## Reproduce
```sh
cd /workspace/b85
python3 tools/gen85_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b85.bin && md5sum wwf_b85.bin
T85=holdD mame genesis -cart wwf_b85.bin -autoboot_script test/t85_pun.lua ...
```
(The comment means: if the assets need regenerating.)
