# b95 — running per arcade tick, background streaming via DMA, crash against the rope (base b94)

ROM `wwf_b95.bin`, MD5 **7be789d70d892c1efb86af8630b296a6** (b94 b2a8ff5d4453067ad3d2bf8762239413 intact). Only the 3 authorised points (9-11-2026 9:32).

## Changes
1. **Running** (`main.c` 192, 866–871, 878):
   - Per-wrestler speed from table `0x95BC` (`945C` → +0x21): Warrior 28, Duggan 27. `3DF0`: speed/4 px per tick.
   - One step per `arcTick` (arcade clock 28.72 Hz, NTSC and PAL), previously `tick&1`.
   - Pose every 2 `arcTick` (`94CE`, table `0x95C4`).
   - Untouched: walking, rn 2 bounce (48 f track), braking, clothesline and the 3-frame start (noted in PENDIENTES).
2. **Background via queued DMA** (`main.c` 211–240, 1553–1584):
   - Tile ROM→VRAM, BG_B and BG_A of each column/row go to the DMA queue. They are flushed in the vblank (`SYS_doVBlankProcess`) before the new scroll, so the column appears complete on the same frame as in b94.
   - Budget `ST_BUD` of 40 tiles/frame. If it is exceeded (camera jump), the queue is flushed without losing order.
   - The crowd (`caApply`, CPU) and the ropes (`ropeDraw`) are computed before the streaming, with the same result.
   - Splitting a column over several frames was not needed: the cost was in CPU writes to the VDP during active display (measured ~870 cycles per BG_A cell and ~0.2 frame for the tiles).
3. **Crash against the rope** (`main.c` 530–595, 669–672):
   - **9E78**: every tick it tests X±0x10 in the direction of flight, with the limits of `21E5A`/`22140` (left X ≤ 616+e, right X > 920−e). If it touches, X = limit ∓ 0x10; with z ≥ 0xDB it does not clip (`21E7A`).
   - **9CD0**: the `cmpi.b #$1c,$44` compares the high byte, so any contact goes to sub 2. Arcade bug copied.
   - If the contact happens on the same tick as the landing: `9C94`, sub 0xC without ∓0x20 (case Xv728 → 643).
   - **9F02**, on the next tick:
     - marks the rope (vibrates, `9700` d0=1);
     - z ≥ 0xCB and pose 0x16;
     - `27D2` index 0x11 (table 0x2934: vx 0x100, vz 0, g 0x10), with Vx inwards;
     - lands when z < 0xBB → downed (action 0xB).
   - Sound 0x29 of the landing (`25E6`) does not exist in the port and is not added. The "0x11" of 9F02 is a movement parameter, not a sound.
   - `9C5A` ∓0x20 without clamp.
   - **soilNudge** uses `oriVictima` (vface^1) as the bit7 of `ACA4`.
     - Calls 875/893 (takedown by strikes): reviewed; they set `vface = attacker to the right`, the b93 convention, so `oriVictima` is the arcade bit7.
     - The landing call (fs) also fits the convention.

## Verified (MAME 0.276; genesis = NTSC, megadriv = PAL; arcade wwfsstar)
- **Running** px/s, there and back (`shots95/md/b95_{genesis,megadriv}_run.csv`):

  | | Warrior | Duggan |
  |---|---|---|
  | arcade | 201,1 | 193,9 |
  | b95 NTSC | 200,5 / 200,6 | 194,0 / 193,9 |
  | b95 PAL | 199,7 / 200,1 | 192,6 / 193,0 |
  | b94 PAL | 167,7 | 167,7 |
  | b94 NTSC | 201,5 / 202,3 | 199,7 / 196,7 |

  - Pose changes: b95 14.0–14.8/s on NTSC and 14.1–14.3 on PAL (arcade 14.36; b94 PAL 12.1–12.4).
  - Bounce on reaching the rope (906/627) and return: OK on NTSC and PAL.
- **Lost frames walking diagonally towards each post** (580 frames; `b9x_post.csv`):

  | | upper left | upper right | lower left | lower right |
  |---|---|---|---|---|
  | b94 | 20 | 14 | 18 | 19 |
  | b95 | 3 | 2 | 1 | 0 |
  | b94, max in 59 frames | 10 | 6 | 12 | 10 |
  | b95, max in 59 frames | 2 | 1 | 1 | 0 |

  - This script measures 10/59 and 12/59 in b94; the "8/59" from the investigation was a different window.
  - **Background**: every frame the VRAM (BG_B nametable + tile) of the edge columns and rows is read, and the whole window every 16 frames. It is compared with W/ROM: 0 errors in about 100,000 cells per case, in b94 and in b95.
  - Negative control (b95 without tile DMA): 67,667 errors, so the check does detect failures.
  - The visible area always stays inside the loaded window.
  - 6 static captures (centre and 4 posts) pixel-for-pixel identical to b94, ropes included.
- **Kicking out of the pin near the rope** (final X of the covering wrestler):

  | Xv | arcade | b94 | b95 |
  |---|---|---|---|
  | 760 | 642 | 675 | 642 |
  | 728 | 643 | 675 | 643 |
  | 708 | 677 | 675 | 677 |
  | 693 | 677 | 675 | 677 |
  | 832 | 859 | 858 | 859 |

  - b95 = arcade in all 5. Crash with the rope vibrating, pose 0x16, 17 ticks and +2 px/tick as in the arcade.
  - Capture: `shots95/clave1_choque_cuerda_arcade_b94_b95.png`.
- **Regression**:
  - **Leaving the ring**: sx 0→1→2 at the same X as b94, W and D, both sides.
  - **Clothesline** DR/DL/WR/WL: contact, catch, flight, bounce and downed, with 0 tile errors. The victim ends the same as in b94 (746/784); the attacker makes contact 6–8 px further away because running now goes per tick.
  - **Pin**: 26 covering states identical to b94 in 6 cases; kickout in 4 cases; the count of 3 works.
  - **Sub 1 against the rope** (port fixture): bounces inwards (W 627→659, D 906→874). In b94 it jumped 48 px.

## Not verified / limits
- Real console / Everdrive. DMA from ROM with the Z80 PCM active is the same pattern as `fLoad`.
- Sub 1 against the rope (throws, clothesline into the rope) and takedown by strikes next to the rope: not measured in arcade MAME. Only the code of 9F02/ACA4 was followed.
- `arcTick` gives at most 1 tick per loop: with lost frames running loses ~0.3–0.7 %.
- The action 8 fall (fs) still advances every 2 loops (`fsTick`), not by `arcTick`: with lost frames it lasts longer (Xv708: 17 ticks in 40 frames).
- Running between ropes there remain 40/580 lost frames (b94: 55). Cause not investigated; it is not the streaming.
- The right limit of 9E78 uses 920−e (arcade); the port's global `RING_XR` 917 does not change.
