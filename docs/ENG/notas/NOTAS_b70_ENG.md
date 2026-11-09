# b70 (base b69, md5 b3d460cb3f2bd3bc97338e499f1c2046; b69 intact)

ROM: `wwf_b70.bin` — md5 `24854415d3674c5e784b99ea9f7cc8da`

## 1. Slower getting up
- `wrDown`: lying face up (pose 114) lasts 140 frames (68 before) and the get-up animation (115) lasts 30 (18 before).
- Measured in MAME: he is lying from frame +14 to +154 (about 2.3 s, 1.1 s before), so there is more time to test the floor hits (elbow A / jump B).

## 2. Arcade grapple (both wrestlers)
- **How it starts:** when both are free, closer than 32 px in X and 16 in Y, and one of them walks, they lock up. Both come together at the midpoint and use the arcade grapple poses (move_seq 118 for Duggan and 343 for Warrior, looping). Each wrestler always uses **his own** poses, so the sprites do not get mixed.
- **Struggle 1 (basic):** the wrestler you control (C) presses A or B before the counter reaches 17 → wins and throws the opponent against the ropes.
- **Struggle 2 (reversing the hold):** if you press nothing before 16, the hold is reversed and the other wrestler wins (whether driven by the AI or standing still without START) when the counter reaches 32. In that case he throws you.
- **Throw against the ropes:** the arcade tracks `sp_trk` are used (S_1E when Duggan throws, W1E when Warrior throws). The victim runs to the **real** rope: if the rope is closer it jumps to the contact frame, and if it is further it repeats the running steps. He bounces (with the rope flexing), runs back to the opposite rope, bounces again and ends up standing. The thrower is released after 25 frames and can already move.
- After each grapple there is a 40-frame wait before being able to lock up again.
- While the grapple or the throw lasts, no hits can be given.
- C still only switches the controller and START only the chase (same as b69).

## Pending / limitations
- A and B do the same thing (the throw to the ropes). The arcade hold 0x26 on A remains pending.
- There is nothing yet on returning from the ropes (clothesline, etc.): the victim bounces and stays standing.
- As the grapple distance (32) is smaller than the punch reach (40), if you walk until you are stuck to the opponent you lock up, the same as in the arcade.

## Tests (MAME, test/t70.lua and test/t70g.lua) — captures in shots/b70
- 01-04: Duggan grapples, presses B and wins; Warrior runs, bounces on the right rope (x=912) and on the left one (x=621).
- 05-08: nothing is pressed, the hold is reversed (blk=1, c2 reaches 32), Warrior throws Duggan and Duggan bounces on the right rope.
- 09-11: after C (you control Warrior) you press A and Warrior throws Duggan.
- 12-13: Warrior on the floor (the test data confirm that he stays lying until frame +154).
