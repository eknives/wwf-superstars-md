# b54 (from b53)

ROM: wwf_b54.bin  md5 dad17974aae704c185eaf92d7e869de3

Only two changes over b53 (b53 intact):

1. **Right HUD black:** the tiles of the right edge of the blue frame (3/7/11) had 4 transparent px because of b53's −4 px bake; they are filled with colour 15 (black, PAL3). The black band reaches the right edge of the screen; the left −4 px and the box design are not touched.
2. **Duggan UP/DOWN inverted:** pad UP → towards the back of the ring (oy++); pad DOWN → towards the camera/front (oy--). Before they were reversed on screen. Post climbing / leaving-entering the ring follow the same logic (DOWN at the bottom post, UP at the back post).

Not touched: choppy sound, ropes, camera, s49 priority, AI.

Shots: shots/b54_hud.png (+ zoom), b54_down.png, b54_up.png. MAME smoke OK.
