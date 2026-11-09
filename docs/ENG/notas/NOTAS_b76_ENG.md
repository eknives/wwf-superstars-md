# b76 (base b75, md5 b2f37978b626d9bd1a072b1e655e7218; b75 intact)

ROM: `wwf_b76.bin`, md5 `49075e62b6b23d071da6035564adcea8`
Only the 5 fixes requested. The AI, new attacks, HOME, corner posts, logo and crowd sound have not been touched.
All the evidence comes from `/workspace/wwf_sgdk/analisis` (arc_rec.dis, rutinas.md, tools/prog.bin and the arcade sprite banks).

## 1. Warrior's punch complete
- **Arcade:** the punch is move 0x00, at 0xFC84. It uses table 0xFD70 with poses 0x150 (4 f), 0x151 (3 f) and 0x152 (3 f); 0xFD7C is the combo alternative (0x153 to 0x155).
- **Bank 0 (Warrior):** 0x152 is the pose with the arm extended. It matches the MAME reference 01M6PKH6….
- **Cause of the bug:** in the port, `xl_w[41]` pointed to pose 658, which is 0x150 of bank 0 (preparation, no arm). That is why Warrior never stretched his arm.
- **Fix:** new pose 765 is added, converted from 0x152 of bank 0 with `tools/gen76_punch.py` (same method as gen69). Now `xl_w[41]` = 765. Duggan does not change.
- Capture: `shots/b76_01_punetazo_warrior.png`.

## 2. Count and referee
- **Arcade, figures:** fg0 is drawn over the sprites (wwfsstar.cpp: bg0 → sprites → fg0) and the count text goes through 0xE02C/0x2549E. The port's figures already have a transparent background (index 0, checked in pin_glyph.bin), so that is left as it is.
- **Real cause of the referee "disappearing":** `refSideY` (invented in b73) sent him IN FRONT (−73) when there was no room behind. He ended up at y < RING_Y0, outside the ring and covered by the front rope.
- **Arcade:** referee state 2 (0xDD4E) goes towards the pair (0xDFE0) and every frame does `jsr 0x21E5A` (0xDECC), which is the ring limit. He never goes out.
- **Fix:** the referee always goes to the track side (+73) and is limited to the ring with `rfClamp`, both during the count and when getting up.
- Captures: `shots/b75_antes_cuenta_arbitro_fuera.png` (before) and `shots/b76_02_cuenta_arbitro_dentro.png` (after).

## 3. Misaligned lock-up (one higher than the other)
- **Cause:** when Warrior covers, the WPIN/WKO track does not carry Z, so `pinZof` = 174 is used. At the end of the kick-out, `z0` stayed at 174 and Warrior appeared 13 px higher in the next grapple.
- It is reproduced in b75 with the koW test: Warrior's dZ = 174 after the pin. In b76 it goes back to 187.
- **Fix, without touching the pin's sitting z0=174:**
  - z to the floor in the reactions and on the floor (0xAB1E and 0xA90E, "z to the floor").
  - z = 0xBB for both at the start of the grapple (0xB1D0 + 0x16F58 centrar_pareja).
  - The pin exit now goes through action 8, which ends on the floor.
- The pinC regression stays the same: `SETTLE z0=174`, `CENTER err=0`.

## 4. Fall against the rope during a hold (the famous one)
- **Arcade 0xF94C (action 0xC):** if he is inside the ring and touches the rope (+0x9E&3, limit 0x21E5A/0x22140), it calls 0xF9B0.
- **0xF9B0:**
  - Marks the rope (0x9700, d0=1).
  - If the opponent is NO LONGER in 0x10, the one doing the hold goes to action 8 sub 1.
  - If the opponent is still in 0x10, only subs 0x1B/0x21/0x22/07/0x29/0x28 act. The whip is sub 0x1E, so nothing happens there.
- **Action 8 (0x99BE, table 0x9A14 / parameters 0xA74A):**
  - Sub 1 (0x9B7E): impulse 0x10 backwards (0x9BBE), z+0x10 and pose 0x15/0x16 according to height (0x9E4C).
  - With the rope (0x9CD0) it goes to sub 2 (0x9F02): z ≥ 0xCB, pose 0x16, vx negated. On reaching 0xBB it goes to action 0xB (lying).
- **Port:** during the whip, from when the victim leaves action 16 (0x10) on the track, if the thrower is on the edge of the ring's trapezium he falls against the rope and ends up lying. The rope vibrates and then he gets up.
- Capture: `shots/b76_04_caida_cuerda_llave.png` (MAME test `rope`).
- **Important limit:** the grapple places both at the midpoint (the same as the arcade, 0x16F58). That is why the thrower only touches the rope if the grapple starts stuck to it. In the test x=627 is forced (the left rope at y=300). The arcade can also get there by pushing during the grapple (+0xAF mode 2/3), but that movement is not ported and I have not invented it.

## 5. Kicking out of the pin, for both
- **Arcade action 0x1E (0xB012), the covered wrestler's:**
  - x ±8, pose 0x9F for 8 f and 0xA0 for 4 f (table 0xB0EA).
  - The covering wrestler has pose 0x9B at x ±0x28, y−1, z+4.
  - At the end, the covered one goes to action 5 (get up) and the covering one to action 8 sub 0x1C, turned (0xB068–0xB084).
  - Sub 0x1C (0x9B66): impulse 0x10, z+0x18, poses 0x9B/0x9C by height.
  - On touching the floor with +0x45=0x1C (0x9C5A): x ±0x20 and sub 0xC (0xA4C8: pose 0x16, vz 0x100, g 0x30). Then action 0xB.
- **New poses** (tools/gen76_poses.py, banks 0 and 3):
  - Warrior: 766 9F, 767 A0, 768 9B, 769 15, 770 16, 776 9C.
  - Duggan: 771, 772, 773, 774, 775, 777.
- The lying of the wrestler who was covering lasts 44 f, as measured in the inventory: "08 34 + 0B 44 + 05 16". Then he gets up, without being dazed. The covered one gets up (0x5) without being dazed.
- Captures: `shots/b76_05a_zafar_warrior_cubierto.png` and `shots/b76_05b_zafar_duggan_cubierto.png`.

## What could not be taken from the arcade (declared approximations)
- **Gravity of action 8:** sub 1 and 0x1C do not set vz or g. The physics of 0x3E20 is used with g=0x30 (the value set by 0xA4C8) and initial vz 0.
- **Fall sounds** (0x11, 0x29, 0x21): not added.
- **Get-up duration:** the port's pose 115 (30 f) is used instead of action 5's 16 f.

## MAME tests (test/t76.lua, run76.sh)
- `pun`/`punD`: Warrior stretches his arm and hits.
- `ko`/`koW`: complete kick-out in both directions; z0 = 187 at the end (in b75, koW leaves dZ = 174).
- `rope`: fall against the rope.
- `cnt`: referee inside the ring during the count.
- t75 regression `pinC`/`pinSide`: pin_ok, SETTLE z0=174, CENTER err=0.
