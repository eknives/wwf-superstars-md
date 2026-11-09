# b67 (from b66) — md5 593ceefe80133aeb5b5e737fd1ec7807
b66 intact (md5 037a4213d712fd0e7124bbe5322e1080). New:

**Normal fall = face up (pose 114)**
- The knockdown hold uses arcade pose **114** (face up), not the incomplete face-down substitute.
- Sequence: doubled over (45, 8 f) → brief face down (111, 6 f) → **face-up hold 114 (68 f)** → knees 115 → dazed 116/117.

**Face down with a complete head**
- In b66 poses 111/112 (t0=4080/3832, nt=34) came out **without the head** (a tile/sprite missing).
- In b67, 111 and 112 copy pose **120** from the same Warrior bank (t0=4414, nt=46): same 5 pieces, head included.
- Knockdown/hit/floor poses reviewed (45, 111, 112, 114, 115–117): 114 already had the 5 pieces (nt=49); 111/112 were the incomplete ones.

**Orientation fixed (flip inverted)**
- Idle 6 faces **left** without flip. Before, `wrFl = (ox < wrx)` put him with his back to the player.
- Now `wrFl = (ox > wrx)`: standing, he faces **towards** Duggan / the player.
- Lying / dazed / taking hits: still does not turn (like b66).

**VRAM**
- Warrior extended to **56 tiles** (1680–1735) because pose 114 needs 49.
- Punch bank 0 moved 1728 → **1736** so as not to overlap.

Not touched: Duggan's A/B hits, START follow/stop, Macho, Hogan, referee, ropes, camera, HUD, sound. Warrior does not hit yet.
Shots: `shots/b67_orientacion.png`, `b67_boca_abajo.png`, `b67_boca_arriba.png` (+ k13/hold). MAME test: `test/t67.lua` / `test/run67.sh`.
