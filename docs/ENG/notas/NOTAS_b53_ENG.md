# b53 (from b52)

ROM: wwf_b53.bin  md5 61a87b67e3fbb6df3b64dd7362789db2

- Base b52 intact in visuals: map 88×68, background on low B, ropes (sides + front horizontals) on high A, crowd, bounce A/B. Choppy sound: not touched.
- Controllable Duggan (walk / run A+B / rope bounce / exit-enter at the sides and bottom / climb posts). The pad moves Duggan; the camera follows him (arcade→scroll b52: cx≈camx+96, cy≈camy+32). No fighting or AI (dormant stub).
- Empty HUD boxes: bake −4 px to the left (tile-bake; the RGB CRT eats the left edge). Same window.
- Sprite priority (Emilio's s49 colour scheme; HIGH almost always):
  - GREEN: HIGH by default inside the ring / front apron.
  - PURPLE: LOW inside, at the height of the bottom horizontal ropes (splits the piece if it crosses rl=ROPE_FRONT_R0).
  - ORANGE: HIGH if inside; LOW if outside next to the sides (rope in front).
  - Posts: wall; climbing = HIGH. Crossing sx: inside according to x vs rope.
  - Background on low B; low plane A empty. Future SAT order: player, opponent, partner P, partner O, referee.
- Palettes: PAL2 = spr_pal (Duggan); PAL3 = palR3 (remapped ropes + HUD). VRAM: tile pool 16..1015, sprites at 1016 (72 slots), ropes 1120+.
- Controls: D-pad walk; A+B run; hold against a side = leave/enter; DOWN at the bottom post = climb; UP at the back post = climb; A/B+START crowd trigger (b52).
- Shots: shots/b53_walk.png, b53_side.png, b53_run.png, b53_mat.png (+ series 0000–0009). MAME smoke OK; not tested on hardware.
