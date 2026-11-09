# b64 (from b63) — md5 9b3cffff1bd585fc241f684f09ab77a4
Only rfStep:
- The follow step (hx/hy) no longer advances rfPh or sets a pose before the clamp: the animation is decided at the end with the NET movement after rfClamp+refAvoid+rfClamp.
- At the side limit (RF_MARGIN 16, does not touch the ropes), pushes of ±1 px without following in Y do not count as walking: freezes the last frame.
- Net 0 = freezes (like the arcade).
MAME test: referee forced to the right edge (x 887) with Duggan stuck to the rope: fixed pose 618 the whole time.
Note: with b63 in that same test it did not cycle either; I could not reproduce the cycle on the spot. Going down along the diagonal of the edge it does walk (real movement).
Shots: shots/b64_borde_*.png, b64_borde_contact.png.
