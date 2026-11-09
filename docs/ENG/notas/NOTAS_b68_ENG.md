# b68 (from b67) — md5 3a41cd79ddf5d3b669c0475ca56ca20c
b67 intact (md5 593ceefe80133aeb5b5e737fd1ec7807).

**b67 error (acknowledged):** poses 111/112 were copied from 120, which is **Duggan** lying (blue trunks, white tights, brown beard). The "face down" capture showed Duggan twice and the label was false.

**Fix:**
- New MD pose **626** = Ultimate Warrior **REAL face down**, taken from arcade bank **0 (Warrior)**, pose 157. Complete head (blond hair), back, trunks, purple boots; 4 pieces, 39 tiles, palette line 2.
- Colours: the same arcade→MD map already used by pose 114 (Warrior face up, verified pixel by pixel against arcade pose 23, 100 % match).
- Knockdown sequence: doubled over 45 (8 f) → **face down 626 (6 f)** → **face-up hold 114 (68 f, Warrior)** → knees 115 → dazed 116/117.
- `wrDown` becomes u16 (626 does not fit in u8). Warrior no longer uses 111/112/120 (Duggan) at any time.

**Verified by eye in MAME:**
- `shots/b68_boca_abajo_WARRIOR.png` (+ _x3): lying face down = **Warrior** (blond hair, purple boots); standing = **Duggan** (beard, blue trunks) finishing the kick.
- `shots/b68_boca_arriba_WARRIOR.png` (+ _x3): lying face up = **Warrior** (face paint, blond hair); standing = Duggan.
- `shots/b68_pose626_vs_114.png`: the two poses isolated.
(In the test Warrior is placed higher in the ring so that the front rope does not cover him.)

Not touched: A/B hits, START follow/stop, orientation, Macho, Hogan, referee, ropes, camera, HUD, sound. Warrior does not hit yet.
MAME test: `test/t68.lua`. Tool: `tools68/addfd.py`.
