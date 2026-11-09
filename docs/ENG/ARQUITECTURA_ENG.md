# Architecture of `src/main.c` (b95)

`main.c` (~1600 lines) is a single C module for SGDK. Each block carries a `bNN:` comment with the version that introduced it and the arcade addresses it reproduces. Line numbers are approximate for b95.

## Files

| File | Content |
|---|---|
| `src/main.c` | Whole engine: main loop, wrestlers, camera, background, ropes, crowd, referee, pin, sprites. |
| `src/select89.h` | Title screen and wrestler selection (arcade 704E/7240/749E…); `joy89()` normalises C = A+B. |
| `src/duggan92.h`, `duggan92_poses.h` | Duggan's floor attacks (Stomp, Elbow, Elbow from the post; C79E/CB6C). |
| `src/knee90.h`, `native81.h`, `cl87.h` | Port pose indices for the Knee Drop, Warrior's native bank and the clothesline fall. |
| `src/gen/*.h` | **Generated from the ROM** (not published): rope maps and palettes (`ropes.h`), floor tracks (`gs69.h`), HUD frame (`hud.h`), selection navigation (`select89_data.h`). |
| `res/res.res` | Binary resources linked by `rescomp` (see `tools/extractor/README_ENG.md`). |

## Clock

- The arcade's actor logic advances every 2 refreshes at 57.44 Hz, i.e. one tick at 28.72 Hz.
- On the MD, the main loop accumulates `arcClock += 3125·Δvtimer` and sets `arcTick` when it exceeds `arcDen` (5440 on PAL, 6528 on NTSC). There is at most 1 tick per loop.
- Since b95, running and some floor attacks advance by `arcTick`. The rest (walking, `fs` falls, bounce, braking) still advances per loop or MD frame: it is listed in PENDIENTES.

## Main loop (`main()`, ~l. 1434)

1. **Start-up:** VDP 256×224, 64×32 planes, palettes, HUD, ropes and initial poses are loaded; `selectScreen89()` (only once); initial background fill.
2. **Each loop:**
   1. `arcTick` clock;
   2. pad (`joy89`, edges, START = follow; Y = switch control);
   3. `grStep` (grapple) and `pinAdvance`;
   4. **for each wrestler** `f = 0, 1`, with `ctxLoad(f)`/`ctxSave(f)`, which copy the wrestler's context into global variables (`ox`, `oy`, `z0`, `rn`, `sx`…). State priority, from highest to lowest:
      - `kvPhase90` (Knee victim);
      - `clHeld` (caught by a clothesline);
      - `fs` (action 8 fall: flight, rope crash 9F02, landing);
      - kicking out of a pin (`pnS==2`);
      - the wrestler covering in the pin (`pinStepA`);
      - grapple or throw (`gr`, `tr` with `trStep`);
      - victim of a hit (`vh` with `victimStep`);
      - otherwise `engine()` (normal control).
   5. `grTry`, `countStep` (counts), `matchReset` when needed;
   6. `camera()`;
   7. crowd (`caLogic`/`caDraw`/`caApply`);
   8. rope vibration (`ropeDraw`, steps 0x21324/0x213A4);
   9. **background streaming** (`stCol`/`stRow`: DMA queue with the `ST_BUD` budget, since b95);
   10. `sqTick` (sound sequences);
   11. referee (`rfStep`, `refPinStep`, count-out).
3. **VBlank:** `SYS_doVBlankProcess()` flushes the DMA queue. Then come `fLoad` (wrestler pose tiles), `rfLoad` (referee), count digits, `buildSat()` (sprite table), scroll and the SAT DMA.

## Modules inside `main.c`

| Block | Functions (approx. line) | What it does |
|---|---|---|
| Background and VRAM | `acq`, `rel`, `put` (~196), `acqQ`, `stCol`, `stRow` (~219–238) | 88×68-cell world (`W`), reference-counted tile pool, new columns and rows through the DMA queue (b95). |
| Ropes | `ropeA`, `ropeDraw` (~204–248), constants from `gen/ropes.h` | Ropes drawn on the planes; vibration by arcade phases (0x213A4/0x213AC/0x2146E). |
| Crowd | `caLogic`, `caDraw`, `caApply` (~249–290) | Crowd animation by zones (23170). |
| Sound | `smpPlay`, `sndCmd`, `sqTick` (~291–300) | PCM4 samples (2 OKI WAVs) and sequences. |
| HUD | `hudInit` (~302) | HUD frame (`gen/hud.h`). |
| Movement and camera | `walkStep`, `camera` (~308–368) | Walking, ring limits, camera with margins. |
| Referee | `rfLoadEx`, `rfColumn`, `rfClamp`, `rfExtPose`, `refAvoid`, `rfStep` (~369–480) | Referee who walks, avoids and counts (DD4E/DFE0/DECC). |
| Context | `ctxLoad`, `ctxSave` (~481–497) | Switches the active wrestler. |
| Knee (victim) | `kneeVictimStep90`, `kneeVictimStart90` (~498–534) | The victim's A2 reaction (A554/28EC). |
| Falls, action 8 | `fsStart`, `clFallStart`, `fsStep`, `fsAir`, `arcRope` (~530–600) | Flight, rope crash 9E78/9CD0/9F02 (b95), landing 9C3C/9C94. |
| Victim | `victimStep`, `bounceRope`, `soilNudge` (~600–676) | Reaction to hits, rope bounce, nudge when lying down (ACA4). |
| Warrior floor | `groundOK`, `warriorGroundZone/Start/Step/End` (~677–805) | Knee Drop and floor finishers (C706/10A5E/112F0). |
| Clothesline | `clStep87` (~806) | Running clothesline (CD14/12E7A). |
| Control | `engine` (~845–1100) | States of the controlled wrestler: `rn` (1 run, 2 bounce, 3 clothesline; braking per `mvOffR`), `sx` (leaving/entering the ring), `bx`, `climb` (post), `gs` (5/11/12 floor tracks, 14/15 Duggan), punch combo and kick, Duggan's pin. |
| Grapple and throw | `grTry`, `trStart`, `grStep`, `trCF`, `trStep` (~1101–1175) | Grapple and throw into the ropes (`sp_trk` tracks). |
| Pin and counts | `pinAdvance`, `pinStart`, `pinStepA`, `refPinStep`, `countStep` (~1176–1258) | Pin (BD10/11A72/B012/B0A0), 3-count and 20-count; when one ends, the match restarts. |
| Match | `fighterInit`, `matchReset` (~1259–1274) | Initial state. |
| Drawing | `fLoad`, `drawF`, `buildSat` (~1275–1433) | Loads pose tiles (`spr_tab` table) and composes sprites with priorities. |

## Resource data used by the code

- `spr_tab` is a table of `Pose { u16 n, t0, nt; Piece p[12]; }` with `Piece { s16 dx, dy; u16 sz, line, toff; }`, 126 bytes per pose, and `spr_tiles` holds their tiles.
- `xl_w`/`xl_d` translate the logical pose into the port pose for Warrior and Duggan.
- `move_seq`, `sx_seq`, `bx_seq`, `climb_pose`, `run_pos`, `sp_trk` are animation and position tracks.
- `camtab` is the camera table; `crowd_b52` + `crowd_b49_tiles` are the crowd; `bgb_tiles` + `bgb_map52` + `ex52_tiles` are the background.
- The full list with sizes is in `tools/extractor/README_ENG.md`.
