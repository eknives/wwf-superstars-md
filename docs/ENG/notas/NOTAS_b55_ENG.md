# b55 (from b54)

ROM: wwf_b55.bin  md5 e00cc84cccd7180ed7822ff219e3c978

Only one change over b54 (b54 intact):

1. **Right ring limit:** `RING_XR` 920 → 917. Taken from Emilio's state/screenshot (Duggan ox=917, oy=232): he cannot get closer to the right corner post (if he does, he overlaps the rope). Left limit (`RING_XL` 616) not touched. From now on this limit is not adjusted again.

Checked in MAME: in the back-right corner, b55 ox=917 / b54 ox=920 (oy=234, no climb). Shot: shots/b55_right_clamp.png.

Not touched: HUD, UP/DOWN, rope art, camera, priority, sound, corner post tiles.
