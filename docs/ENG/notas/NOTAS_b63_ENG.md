# b63 (from b62) — md5 c4e24dd1024eced745681c0bd9c0ef7d
Only rfStep changes (src/main.c):
- refAvoid limited to 2 px/frame per axis towards its target (it no longer jumps).
- Any real movement after rfClamp+refAvoid animates: advances rfPh, walking pose (front/back according to oy>rfy), flip by ox<rfx. Still = freezes.
Test: push f1008-1020 now 2 px/f and pose 619→620 (frozen before).
Remaining: 28 px jump at f62 (initial rfClamp, before the match).
Shots: shots/b63_empuje_contact.png, shots/b63_000*.png (Duggan walks into the referee).
