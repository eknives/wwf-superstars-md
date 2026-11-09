# b66 (from b65) — md5 037a4213d712fd0e7124bbe5322e1080
b65 intact. New:

**Duggan's basic hits (arcade, move_seq sequences from port s05-s07)**
- **A = punch** (33 f, poses 40-41), **B = kick** (31 f, poses 42-43). A+B is still running (as before).
- Impact on the arcade frame: punch f24, kick f18. Reach 40 / 42 px in X and 7 px in Y, only if Warrior is in front.
- When hitting, if Warrior is close (±64 X, ±24 Y), Duggan turns towards him. Facing left the hits use H-flip.
- Only from the normal floor (not on corner posts, outside the ring, running or bouncing).

**Warrior takes hits (does not hit yet)**
- Punch → arcade reaction (pose 44, 13 f). Kick → doubled over (pose 45, 41 f).
- Accumulated damage: punch 1, kick 4; on reaching 8 → **knockdown**: doubled over → lying (111/112, ~74 f) → kneeling (115) → **dazed** (116/117, ~96 f) → standing.
- The accumulated damage is lost after 3 s without being hit. Lying, he does not take hits.

**Warrior's orientation**
- Standing: always faces Duggan (like b65).
- Taking a hit / lying / kneeling / dazed: **does not turn** (stays as he fell) and does not move or follow.
- Corner posts: Warrior does not climb the corner posts yet, so the corner post rule does not apply yet (ready for when he climbs).

**START**: same as b65 (follow / stop, walking with animation). During a hit/knockdown he does not move; when he gets up he follows again if he was in follow mode.

Warrior VRAM extended to 48 tiles (1680-1727; 44 before) for pose 44.
Not touched: Macho, Hogan, referee, ropes, camera, HUD, sound.
Shots: shots/b66_punetazo_reaccion.png, b66_patada_derribo.png, b66_tumbado.png, b66_atontado.png, b66_contact.png. MAME test: test/t66.lua.
