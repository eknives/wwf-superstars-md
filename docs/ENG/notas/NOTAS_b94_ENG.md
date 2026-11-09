# b94 — downed wrestler at the arcade X + adjusted pin (base b93)

ROM `wwf_b94.bin`, MD5 **b2a8ff5d4453067ad3d2bf8762239413** (b93 a89af7ed95159c0899430bf0e81f6441 intact).

## Changes (only the 2 authorised points)
1. **Downed without `lyoOf` ±32** (main.c:487 `bodyX=ox`; drawing main.c:1491 `dLyo=0`). Pose 114/626 without lyo occupies the same as the native arcade 0x17 at Xv (±6 px). Zones C798/C706 untouched.
2. **Pin**:
   - `pinStart`: `pnX=pnVX=Xv`, `pnM = oriVictima?+1:−1` (BD10/11A72, `neg` if bit7=0), `pnKD=pnM`. The tracks already carry BEF2: Warrior Xv∓32, Y+1, Z203; Duggan Xv∓36, Y−1, Z174.
   - Warrior faces the opposite way to the downed wrestler (11A8A `+A = rival^0x80`): `dFlip=(pnM<0)` for 514/778, which were converted mirrored (match69 flip1), and inverted for 513, which is arc pose 2 unmirrored.
   - Duggan: the flip stays the same (it already matches the arcade).
   - Referee: `rfX/rfM` leave him in the same place relative to the visible body as in b77, without any change of choreography.
   - Duggan's pin entry = body zone C706/CB75 (`dugZone==2`, B, like the Stomp). The `bodyX±PIN_ZONE` block from b69 is removed.
   - Kicking out (B012/B0A0) stays in arcade absolute terms: downed Xv∓8, the covering wrestler Xv∓48, Y−1, Z+4.
   - Cadence and sliding unchanged.

## Verified (MAME 0.276, genesis NTSC vs arcade wwfsstar, RAM fixtures, Xv=760)
- **B sweep** d=−88..+88, step 8, W and D, both orientations. All 4 rows are IDENTICAL to the arcade (`shots94/md/sweep_cmp94.txt`):
  - W o0: K −64..−40, P −32..−16. W o1: P +16..+40, K +48..+64.
  - D o0: K −64..−40, P −32..0. D o1: P 0..+40, K +48..+64.
  - In b93 Duggan did not match.
  - With the downed wrestler at Xv, the P band falls on the visible torso and the K on the head (`shots94/clave1_zonas_b93_b94_arcade.png`).
- **Who covers** (W 778 / D 499):
  - W X−Xv = −32/+32, Y301, Z203 (arcade −32/+32, 301, 203). D −36/+36, Y299, Z174 (arcade −36/+36.97, 299, 174.5).
  - Ring side 680/860: also ∓32.
  - Orientation by silhouette against an arcade capture: W sitting and approach 514 match directly in b94 (0.79/0.72, versus 0.69/0.55 mirrored); in b93 they came out mirrored. Duggan covering: face/arms on the same side as the arcade (visual).
  - Capture: `shots94/clave2_cubriendo_arcade_b93_b94.png`.
- **No jump downed→reaction:**
  - 16 cases md94/reg94 (`shots94/validation94.json`): contacts = arcade (16/16); dX and flip constant with lyo 0 in 114/752→A2→wait. b93 went from lyo 32 to 0.
  - Getting up 114→115: no longer jumps either (b93 jumped 32).
- **Clothesline** DL/DR/WL/WR: trace and 144 captures pixel-for-pixel identical b93 vs b94; 0 tile errors.
- **Kickout** (1st pin, W and D, both orientations): works, positions according to formula B012/B0A0.
- **Count of 3** (2nd pin): reaches "3" (pnS 3, winK 117).
- **Native fall of the covering wrestler on kickout:** at the end of the fall, 114 stays at the same dX without lyo (b93 jumped −32).

## Side effects / NOT verified
- **Kickout near the rope:**
  - The covering wrestler now leaves from Xv∓48 (arcade), 32 px further out than in b93. His falling flight (unchanged, 70 px) can go past the limit.
  - With Xv=760 o0 he lands at 642 and the ACA4 push puts him at 675: a 33 px jump. In b93 this only happened near the rope.
  - It has not been measured in the arcade: the arcade fixture does not count, because there is no referee. Left in PENDIENTES.
- **Kickout/count vs arcade:** only compared with the code (B012/B0A0), not with arcade MAME.
- **Pose 513:** the flip comes from the conversion convention (flip0), not from a measured silhouette. It is 4 frames.
- **Approach:** still follows the 513/514 sliding (the arcade places 7E fixed). Duggan's jump has not been measured.
- An occasional one-frame delay of the counter during the pin (emulation lag; also happens in b93).
- Natural takedown in a game, PAL and Everdrive: not tested.
