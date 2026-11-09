# b74 (base b73, md5 684b4b738f4255cb231fa286d401fdef; b71/b72/b73 intact)

ROM: `wwf_b74.bin`, md5 `715494ea2b1a1f41ac0b4013ae7b7a0b`

## Arcade evidence (read BEFORE touching code)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc_rec.dis`, `rutinas.md`): y = opponent.y−1 (+2 if id 0/4); x = opponent.x ± BEF2[id][opponent]; z = 0xBB − BEF2[id][opponent+8]. Sign of dx: `btst #7,+0xA(opponent)` → if clear, `neg.w d1`.
- **Table 0xBEF2** (`prog.bin`): per attacker `id*0x10`, dx byte at `[opponent]`, dz at `[opponent+8]`.
  - Duggan(0)→Warrior(1): dx=**32**, dz=13
  - Warrior(1)→Duggan(0): dx=**36**, dz=13
- **0x1190C / 0x11A72**: cover only if opponent in action 0xB, **inside** (`+0x19==0`) and attacker not outside. There is no "near the rope" veto.
- **0xACA4**: on lying down it tests ±0x30/±8 + clamp 0x21E5A (pushes the body inside).
- **s41 track** (`sp_trk` PT_PIN@2731): at the settle (frame 28) dx=**36**, dy=0 (the track already has the arcade's visual offset). Origin of the track = the opponent's arcade x (= centre of the body).
- **Emilio's visual reference (arcade MAME)**: covering wrestler lying torso-over-torso; referee below the pin counting.

## Why b73 ended up worse
- Lying pose **114/626**: the sprite's torso is ~28 px to one side of the origin.
- `lyo` (±32) corrects that when drawing (`bodyX = ox+lyo`).
- b73 **switched off lyo** during the pin and set `pnX=ox`. The metric `err=0` compared the cover with `ox+36` (the formula itself), not with the visible torso → visual gap ~60 px (Emilio: "it's worse").
- With lyo ON and `pnX=ox` the gap was ~28 px; with **`pnX = ox − lyo`** the cover/torso centroids are ~4 px apart.

## Changes (only what was authorised)
1. **Centring:** `pnX = fd[v].ox - lyoOf(114, fl)` and **lyo ON** while being covered. Same s41 track (`ox = pnX + pnM * q[1]`). Referee/RPIN use the same `pnX`.
2. **Pin next to the ropes OK; on/outside them NO.** `groundOK` = rule 0x1190C: attacker `ropeIn(m=0)`, opponent not outside (`sx/bx!=2`), opponent's `ox` inside. The veto by sprite extents (lyo) that blocked the pin next to the rope is removed. `soilNudge` 0xACA4 is kept.

## Not touched
No AI (the other one only chases with START). Same controls. Top corner posts, WWF logo and palettes intact. b72 ring-out figures/gestures intact.

## MAME tests (`test/t73.lua`)
- **pinC** (centre 780/720): `CENTER ox=720 lyo=32 pnX=688 cover=724 expect=724 err=0`
- **pinSide** (next to the left rope): pin OK, `err=0`
- **pinOn** (ox forced outside the limit): `RESULT blocked_ok`
Captures in `shots/` (`hoja_b74.png`).

## Known limits
- The centring uses the bias of the port's pose 114 (±lyo); if those poses are changed it must be recalibrated.
- The big pin figure is still anchored to a fixed screen position (not requested in b74).
- Warrior WPIN (track dx=32) uses the same `ox-lyo` formula; the track was not re-recorded.
