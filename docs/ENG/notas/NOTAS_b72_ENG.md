# b72 (base b71, md5 dbfe401359b8f726186dd01e82cd5b2c; b71 intact)

ROM: `wwf_b72.bin`, md5 `74c37dc8839ec8780a122eabfc71a58d`

## What I looked at in the arcade
- 0xBD10 / table 0xBEF2: the covering wrestler is placed at the opponent's x ± d (Duggan over Warrior 36, Warrior over Duggan 32), with the opponent's y −1. The b71 tracks already ended at 36 and 32, so the placement in the centre of the ring was the arcade's. The problem in the capture was **the rope**.
- 0xACA4 + 0x21E5A: on falling, the arcade checks the lying body (from x−8 to x+48) against the ring limits. 0x1190C and 0x11A72 only cover if the opponent is lying **inside** and the covering wrestler is not outside.
- 0xDEE4 + 0xDA38 + table 0xDB04: in the outside count, the referee faces whoever is outside and uses the counting poses 0xA-0x11, 4 poses of 8 ticks. He adds 1 on each round (64 f).

## Changes
1. **Ropes: neither pin nor jump.** You can only cover (B close) or jump (B further away) if three things hold: the attacker is not against the ropes; the lying body, with its real pixels (pose 114 with lyo), is entirely inside; and the spot where the covering wrestler is placed is also inside. If not, B is the normal kick.
2. **The referee does not count through the ropes.** The pin only starts if the referee's positions on the track (when dropping and when slapping) fall inside the ring with their margin. If there is no room behind, he goes in front of the body.
3. **Outside count as in the arcade.** The referee makes the counting gesture: arcade poses 0xA-0x11 imported as 757-764 (757-760 facing front, 761-764 from the back), one pose every 16 f and facing whoever is outside. The figures are **big and red**, 16×40, in the style of the 3 count. 1, 2 and 3 are the original ones; the rest have been composed from their segments (`tools_dig72.py` → `res/big_dig.bin`). With two figures, the tens go in tiles 1779 and the units in 1525.

## Not touched
There is no AI: the other one only chases with START. The controls are the same (C switches, START chases, A/B as in b71). The top corner posts, the WWF logo and the palettes have not been touched either.

## Limits
- The shape of the figures 0 and 4-9 is a reconstruction with the segments of 2 and 3, not an arcade capture.
- Referee pose 764 is missing 2 lines of the hand: the referee has a limit of 41 tiles.
- I do not do the arcade push that moves the body away from the ropes on falling (0xACA4). Here, near the ropes, you simply cannot cover.
- There are still no voices in the count (in the arcade, the outside count is silent).

## Tests (MAME, test/t72.lua; T72X=780 puts the match in the centre)
pinC: pin in the centre (count 1, 2, 3 and reset). pinR: next to the left rope it does not cover. ro: gestures and big 1/2/10/20, and reset. jumpC/jumpR: Warrior's jump. Captures in shots/ (hoja_b72.png).
