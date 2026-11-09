# b82 (base b81, md5 ffa3e48e22aee99750cd82af10d6ab31; b81 intact)

ROM: `wwf_b82.bin`, md5 `b6c57f8cb194c7c7805b5a75b3775dc8`. Local SGDK build.
Only Warrior's finisher on the floor is touched (jump onto the downed opponent). The ropes have not been touched.

## 1. Where it is launched from (arcade 0xC706 / 0xC798–0xC8A8 / 0xC928–0xC95A)
- At CB1A[action 0xB] = 0xFF the opponent is down, so the anchor branch is used. Anchor = rival.x ± 0x28 (+ with bit7).
- Warrior's row in 0xCB3C: in front of the anchor (<0x20) → A = sub 4, **B = sub 0x0C (jump)**. Towards the body (<0x30) → A = sub 5 (stomp), B = sub 6 (pin). At 0xC928 the pin is only valid if the distance is <0x20 and propio.y ≥ rival.y; otherwise B gives a normal strike (sub 1).
- **Checked in arcade MAME** (`test/probe.lua`, `test/warrior_probe.txt`) with Warrior id 0 and the opponent down at x=760:
  - without bit7 (head to the left): jump at dx −64..−40; stomp at −32..0; pin at −32..−16.
  - with bit7: jump at +48..+64; stomp at 0..+40; pin at +16..+40.
  - **From the feet side he never jumps.**
- Arcade pose 0x17 occupies x−48..x+16, with the head at x−48. That is, **the jump only comes out from beyond the head**.
- **b81 bug:** it confused the port's orientation with the arcade's bit7 and took ox as if it were the arcade x. That is why he jumped from the feet, as in your capture.
- **Fix:** bit7 = !vface and X = ox ± 48. With that, the selection is exactly that of 0xC798, including the pin restriction at 0xC928.

## 2. Trajectory
- 0x10A6C: Warrior takes the opponent's orientation. Target according to 0x111D0: rival.x − 0x20, mirrored with bit7.
- In the arcade (MAME) he goes from x 712 to 727 with the opponent at 760. Before, he went towards the centre of the body and faced the wrong way.

## 3. Duplicated leg and fist
- 0x1152A: object 7D (1C0AB2) is **another sprite** placed at y−10, z+10, with the opposite orientation and x±4.
- Warrior stays at y = rival+9, **behind** the opponent, and the 7D (knee and fist) at y−10, **in front**.
- b81 put everything into a single sprite on top of everything, which is why two knees and two fists were visible.
- Now poses 787/788 carry the body and the 7D in separate pieces (`tools/native82.py`) and each is sorted with its own depth. It is the same two-layer mechanism as pin 778.
- Result: the opponent's legs cover Warrior's body, as in `shots/arcade_MAME_impacto_7D.png`.

## Tests (MAME Genesis, `test/b82.lua`)
- headL/headR (from the head, B): jumps (gs=12). feetL/feetR (from the feet, B): **does not jump**.
- stompL/stompR: stomp. pinL/pinR: pin.

## Captures (`shots/`)
- Arcade: `arcade_MAME_salto_desde_cabeza.png`, `arcade_MAME_impacto_7D.png`.
- b82: `b82_salto_cabeza_R.png`, `b82_salto_cabeza_L.png`, `b82_impacto_capas.png`, `b82_pies_B_no_salta.png`.

## Out of scope / pending
- A in front of the anchor = sub 4 in the arcade (grab of the downed opponent). Not implemented; the port gives a punch.
