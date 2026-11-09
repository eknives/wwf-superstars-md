# b73 (base b72, md5 74c37dc8839ec8780a122eabfc71a58d; b72 intact)

ROM: `wwf_b73.bin`, md5 `684b4b738f4255cb231fa286d401fdef`

## Arcade evidence used
- **0x1190C / 0x11A72** (`analisis/rutinas.md`, `prog.bin`): cover only if the opponent is in action 0xB, **inside** (`+0x19==0`) and the attacker is not outside. There is no extra "near the ropes" margin.
- **0xACA4** (`suelo_chk_cuerdas`): on lying down it tests ±0x30 and ±8 with the clamp **0x21E5A**; it leaves the body inside (not on the rope).
- **0xBD10 + table 0xBEF2** (`prog.bin`): the covering wrestler at `ox_rival ± dx` (Duggan→Warrior **36**, Warrior→Duggan **32**), and y = opponent−1. Same as s41 (`pinX = ox` of the victim).
- **0x21E5A** (`s66/cuerdas_casos.md`): sloped ring limits (m=0).

## Changes (only what was authorised)
1. **Pin next to the ropes OK; on/outside them NO.** The aggressive b72 block (`m=6/4` + referee veto) is undone. `groundOK` uses the 0x1190C/0x21E5A rule (m=0): body or attacker past the limit = no; inside (even next to the rope) = yes.
2. **0xACA4 on falling** (`soilNudge`): on becoming lying (vh=3) it pushes the body inside with the same 0x30/8 logic + clamp.
3. **Centring of the covering wrestler:** `pnX = ox` of the opponent (arcade/s41/BEF2). During the pin the lying wrestler's `lyo` is switched off so that the sprite shares the track's ox (before, the ±32 lyo misaligned it with respect to the cover).

## Not touched
No AI (the other one only chases with START). Same controls. Top corner posts, WWF logo and palettes intact.

## MAME tests (`test/t73.lua`)
- **pinC**: pin in the centre; `CENTER ox=720 cover=756 expect=756 err=0`.
- **pinSide**: next to the left rope; pin OK.
- **pinOn**: body forced outside the limit; pin blocked (`RESULT blocked_ok`).
Captures in `shots/` (`hoja_b73.png`).
