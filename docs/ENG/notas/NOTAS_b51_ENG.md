# b51 (from b50)
ROM: wwf_b51.bin  md5 328134aa6dde7116b2ac863ecea7eb29
- Side ropes (left and right) from the arcade (frames from b45/b46) on high plane A, in background coordinates (arcade x+32, y+16). Without the bottom horizontal rope.
- A = left rope bounce, B = right rope bounce. Arcade timings from b45 (84 steps, 1 per frame), like b46.
- Background on low plane B (b50: billboard, margins, empty HUD).
- Camera: D-pad; C = fast (A/B no longer speed up). START+A/B/C = crowd as in b49.
- Ropes: 356 tiles in VRAM 1120+, PAL2 + PAL3 (3-9); the background pool goes down to 1100.
- Pending: corner posts incomplete in some states (limitation of b45).
- Shots: shots/0001-0002 = right bouncing, 0003-0005 = left bouncing, 0006 = rest.
