# b49: Emilio's background + free camera + animated crowd + crowd sound

ROM: `wwf_b49.bin` (also `out/rom.bin`), 524,288 bytes, md5 `6d1b50331b893d52879d7a11eff9f37f`
Base: b42 (`b42_camara`). No earlier ROM has been overwritten.

## What there is
- Emilio's background from b42, unchanged (`bgb_tiles.bin`, `bgb_map.bin` and `pal.bin` are the same).
- The free camera works the same as in b42: D-pad to move; A, B or C to go fast.
- **Crowd: CROWD_ARC from s67**, with the arcade routines 0x22462/0x224E8/0x225B0 (phase cycle {0,1,2,1,2,…,0} at 30 Hz), the barrier 0x23406/0x230FC and the small element 0x232DE/0x2336C.
  - The s67 lists were made on the old background. `tools/remap_crowd.py` moves them to Emilio's background by comparing pixels: it adds 608 new tiles and 10,244 cells come out. None had to be omitted, because the 331 cells where Emilio's background changes do not coincide with crowd cells.
  - The map in RAM uses 13-bit ids, because 3,540 + 608 exceeds 4,095.
- **Sound (SGDK PCM4 driver, original OKI samples 3 and 4):**
  - 0x22 = sample 3 once. 0x23 = sample 4 once.
  - 0x50 / 0x51 = waves: the Z80 sequences 0x1152 / 0x117A copied as they are. Each entry restarts the sample with its OKI attenuation. Times are in 100 Hz ticks (timer B 0xDD), about 9.4 s in total.

## How to test
- On boot 0x22 plays, as in the arcade (0x1010).
- **Automatic demo:** every 8 s there is a crowd reaction with a wave, alternating 0x50 and 0x51. It is disabled by building with `AUTO_DEMO=0`.
- **START + A** = reaction + 0x50. **START + B** = reaction + 0x51. **START + C** = barrier + 0x22.
- The crowd is at the top and bottom: you have to move the camera up or down to see it (in the centre only the ring is visible).

## Checked (minimum)
- It boots. The captures in `shots/` show no broken tiles.
- The crowd changes after the trigger, about 470 frames with changes.
- There is audio output at boot and during the wave.
- The data is inside the ROM: `crowd_b49.bin` at 0x4FBC8 and the tiles at 0x5EC46. `res.h` and `res.rs` were deleted before building.

## Missing / limits
- **Camera flashes (0x6BA0):** not there. They are sprites (object 1C09A6) and go in another step.
- Without wrestlers there are no real triggers. Reactions come from the demo or the buttons.
- The volume is low with PCM4. The samples have not been normalised, so as not to touch the original.
- Corner posts: not applicable.
- **No ropes:** there are no bounce banks or plane A. The ropes are the next step.
