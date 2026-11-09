# b52 (from b51)
ROM: wwf_b52.bin  md5 7c3254185b41c1494120155d126850e7
- Even camera: map 80x68 -> 88x68 (+8 columns = 64 px on the left, taken from the arcade background, same method as the b50 fill; 242 new tiles in ex52_tiles). Limits cx 0..448. Margin from the post to the edge: left 162 px, right 165 px.
- Crowd (crowd_b52.bin) and ropes shifted +8 columns; crowd zones adjusted (camx -64).
- Front horizontal ropes (red/white/blue + posts) from ring_edit/ring_cuerdas_planoA.png, on high plane A, fixed. In the cells of the side ropes they are mixed with each bounce frame.
- The back horizontal ropes were already in the background (plane B); not touched.
- A = left bounce, B = right bounce (same as b51). C = fast.
- Ropes: 391 tiles in VRAM 1120+. Colours of the horizontal ropes adjusted to the rope palette (5 approximate tones).
- Checked: assets in the ROM (byte by byte), MAME boots, shots/b52_test.png (left limit, bounce A, right limit, bounce B).
- Choppy sound: not touched.
