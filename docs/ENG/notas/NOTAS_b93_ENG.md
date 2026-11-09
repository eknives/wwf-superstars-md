# b93 — orientation of the downed opponent (base b92)

ROM `wwf_b93.bin`, MD5 **a89af7ed95159c0899430bf0e81f6441** (b92 d9af08525a0f49f4bdc025ed00499135 intact; its source recompiles to the same MD5).

## Changes (only the 3 authorised points)
1. `oriVictima(o) = vface[o]^1` (main.c:464): the arcade bit7 of +A of a downed opponent = the flip with which the port draws him. The arcade (10A5E/A554) never changes it. Used in: Warrior zone C798 (`warriorGroundZone`), `kneeOutsideVictim91`, jump target and post adjustment (15A6C / ±64), impact box 10FCC (`warriorGroundStep`), Duggan zone C706 (Stomp/Elbow), Duggan orientation copy 10A6C/10BB2, Duggan solver and post, Duggan box.
2. A2 reaction and floor wait (`kneeVictimStart90` main.c:485 and loop main.c:1467): `dFlip = oriVictima`, `dLyo = 0` (the native A2 pose is placed at Xv as in the arcade: head at Xv∓40).
3. Without touching `vface` assignments in falls/strikes, clothesline b88, pin, `bodyX`, `lyoOf`, cadence 8/18/10.

## Verified (MAME 0.276, genesis NTSC, RAM fixtures: downed opponent vh=3 with the two orientations produced by takedowns)
- Contacts = exact arcade (x,y,z,energy): Duggan stomp/elbow/elbow mirror/elbow above/post P/post K/far stomp/y23 (+y24 and miss −2 identical); Warrior Knee head left/right, above, post K/P, outside. See `shots93/validation93.json`.
- No mirroring: the opponent's flip does not change from downed → A2 (846/847/848, 843/844/845) → wait, in all 16 cases (`flip` in validation93.json). Captures: the elbow/knee lands on the visible head; boots stay on the same side.
- Clothesline: b88 trace (DL/DR/WL/WR, 147 refreshes, incl. flip/poses) byte-for-byte identical b92 vs b93; 0 tile errors.
- Pin: `pinStart`/counter/poses unchanged. Duggan's pin (bodyX) at the same X. Warrior's pin (zone 2 C798) keeps the arcade geometry (torso_pin 744/760 ori0 → pin) and now lands on the correct visible side; that is why in b93 its X relative to `vface` are the symmetric ones of b92 (`shots93/pin93_b92.csv` vs `pin93_b93.csv`).

## NOT verified / pending
- Natural takedown in a game (only equivalent fixtures), PAL, Everdrive.
- Post on the opposite side (no arcade data for that side).
- Visual jump of ~32 px when going from the generic downed pose 114/752 (with the b74 pin `lyoOf`) to the native A2: the A2 is where the arcade has it; the offset belongs to the previous generic pose (out of scope, not touched).
- Duggan's pin uses `bodyX` (b71 invention, feet side) while Warrior's follows the arcade: a previous inconsistency, not touched.
- Cadence 8/18/10 (LOW, unchanged).
