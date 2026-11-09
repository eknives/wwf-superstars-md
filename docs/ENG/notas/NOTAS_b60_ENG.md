# b60 (from b59)

ROM: `wwf_b60.bin`  md5 `5986c9c1f2a51854b2ebda56407ce6a0`

b59 intact (md5 `9147ee11d533442397987e165520be45`). No palette changes.

## Changes (src/main.c only)

1. Macho inside the ring: `ptX[0]=652`, `ptY[0]=300` (before, apron 602,338). Pose 449 the same.
2. Macho is drawn like the referee: HIGH + zones (purple/orange, splitting at the front rope) + pieces on the HUD → LOW.
   Order by feet of 3 actors (Duggan / referee / Macho, lower = in front; 3-element bubble sort).
   Referee branch generalised (`who==2` → pose 449, tiles `ptT[0]+toff`, no flip).
3. Hogan the same: (939,280), LOW, pose 450, warm yellow from b59. The tag-partner loop only paints q=1.
4. Static Macho: no collision or AI; the referee does not walk around him (refAvoid only looks at Duggan).

## Test

Boot OK. Shots: `shots/b60_idle.png`, `shots/b60_macho_dentro.png`, `shots/b60_hogan_dcha.png`.
