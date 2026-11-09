# Resource extractor — **PENDING**

This utility **does not exist yet**. Its job will be to read **your own ROM** (MAME set `wwfsstar`, legally obtained) and generate the resources the port needs in order to build, without the repository having to contain any arcade data. Until it exists, the code cannot be built with real content (see `docs/ENG/COMPILAR_ENG.md`).

## Requirements

1. Check the set (CRC32/SHA1 of each file as given by `mame -listxml wwfsstar`) before extracting anything.
2. Generate the 32 files in `res/` and the 4 headers in `src/gen/` listed below, **byte-for-byte identical** to the ones used in b95.
3. The outputs are never committed: `.gitignore` excludes `res/**/*.bin`, `res/**/*.wav` and `src/gen/*.h`.
4. The original converters were written version by version (b42–b92) and are in the project's private backup. They have to be merged into a single reproducible process; each version's notes (`docs/notas/`) describe how every resource was obtained.
5. **Exception:** the upper corner posts and the WWF logo in the background (`bgb_tiles.bin`/`bgb_map52.bin`/`pal.bin`, "Emilio's background" since b42) contain manual edits by Emilio that **are not published**. The extractor will produce the arcade version, so the ROM's MD5 will not match b95 unless those edits are applied some other way.

## Resources in `res/` (32, referenced by `res/res.res`)

| File | Bytes | Content | Origin in the notes |
|---|---:|---|---|
| `graficos/paletas/pal.bin` | 64 | Background palettes (2×16 MD colours) | b42/b49 (Emilio's background) |
| `graficos/fondos_cuerdas_publico/bgb_tiles.bin` | 113280 | Background tiles (ring, floor, stands) | b42/b49 |
| `graficos/mapas/bgb_map52.bin` | 11968 | Background world map (88×68) | b52 |
| `datos/crowd_b52.bin` | 61566 | Crowd animation by zones | b49/b52 |
| `graficos/fondos_cuerdas_publico/crowd_b49_tiles.bin` | 19456 | Crowd tiles | b49 |
| `graficos/fondos_cuerdas_publico/ex52_tiles.bin` | 16160 | Outside filler tiles | b50/b52 |
| `sonidos/oki_s03.wav` | 65580 | Decoded OKI sample 0x03: WAV mono, 16-bit, 8000 Hz, 32768 samples (PCM4 in SGDK) | sound analysis |
| `sonidos/oki_s04.wav` | 65580 | Decoded OKI sample 0x04, same format | sound analysis |
| `graficos/fondos_cuerdas_publico/ropes_tiles.bin` | 12512 | Rope tiles (391 tiles, at VRAM 1120) | b53/b61 |
| `graficos/luchadores/spr_tiles.bin` | 933600 | Tiles of every pose (Duggan, Warrior, referee…) | b55/b56, additions b81–b92 |
| `datos/spr_tab.bin` | 108486 | 861 `Pose` × 126 bytes (see `docs/ENG/ARQUITECTURA_ENG.md`) | b55/b56 and additions |
| `graficos/paletas/spr_pal.bin` | 64 | Sprite palettes | b53 |
| `datos/move_seq.bin` | 1716 | Movement sequences (pose, duration) | b65/b85 |
| `datos/sx_seq.bin` | 1856 | Leaving/entering the ring | — |
| `datos/bx_seq.bin` | 1056 | Outside sequence | — |
| `datos/climb_pose.bin` | 1360 | Climbing the post | — |
| `datos/run_pos.bin` | 436 | Run/bounce positions | — |
| `datos/camtab.bin` | 772 | Camera table | — |
| `graficos/luchadores/part_tiles.bin` | 2752 | Partial tiles remapped to PAL2 | b56 |
| `datos/xl_w.bin` | 1276 | Logical pose → port pose (Warrior) | b76/b84 |
| `datos/xl_d.bin` | 1276 | Logical pose → port pose (Duggan) | b84 |
| `datos/sp_trk.bin` | 48720 | Arcade tracks for throws/flights | b69/b70 |
| `datos/pin_glyph.bin` | 1472 | Pin count digits | b76 |
| `datos/credit_dig.bin` | 320 | Credit digits | — |
| `datos/big_dig.bin` | 3200 | Large count-out digits | b72 |
| `graficos/seleccion/select89_tiles.bin` | 16512 | Selection screen | b89 |
| `graficos/seleccion/select89_map.bin` | 1792 | Selection map | b89 |
| `graficos/seleccion/select89_cursors.bin` | 21504 | Cursors and portraits | b89 |
| `graficos/paletas/select89_pal.bin` | 256 | Selection palettes | b89 |
| `graficos/titulo/title89_tiles.bin` | 21888 | Title screen | b89 |
| `graficos/titulo/title89_map.bin` | 1792 | Title map | b89 |
| `graficos/paletas/title89_pal.bin` | 32 | Title palette | b89 |

"—" = the exact origin still has to be located in the historical notes and scripts of the backup. The backup has 3 more files that `res.res` does not use (`bgb_map50.bin`, `ex50_tiles.bin`, `crowd_b49.bin`) and that are not needed. `res/crowd_b49.h` (3 size constants) is published.

## Headers in `src/gen/` (4)

Declarations the code expects. The values come from the ROM and **are not published**:

```c
/* src/gen/ropes.h — rope tile maps (vibration) and 2 palettes */
#define X0 22
#define Y0 19
#define W0 6
#define H0 27
#define NS0 84
static const u16 mp0[8][162];  static const u8 sc0[84];
#define X1 60
#define Y1 18
#define W1 6
#define H1 28
#define NS1 84
static const u16 mp1[5][168];  static const u8 sc1[84];
#define XH 20
#define YH 39
#define WH 48
#define HH 9
static const u16 mph[432];  static const u16 palR2[16];  static const u16 palR3[16];
#define VT 1120
#define NR 391

/* src/gen/gs69.h — sp_trk tracks 0x05 (floor elbow) and 0x11 (jump onto the lying wrestler) */
#define GS5_N 29
#define GS5_K 16
#define GS11_N 83
#define GS11_K 40
static const u16 gs5P[29];  static const u16 gs11P[83];  static const s8 gs11X[83];  static const s8 gs11Z[83];

/* src/gen/hud.h — HUD frame: 12 4bpp tiles and their map */
static const u32 hudT[12*8];  static const u8 hudMap[4][32];
#define HUD_NT 12

/* src/gen/select89_data.h — selection navigation and colours (747A, 2048, 2054) */
#define SEL89_NT 516
#define TITLE89_NT 684
static const u8 selNav89[96];  static const u8 autoNav89[36];  static const u16 flashColor89[6];  static const u8 flashPen89[6];
```

The `#define` constants are geometry and sizes that the code needs. With these declarations initialised to `{0}` and the `res/` files filled with zeros, the project builds (tested on 2026-11-09) and produces a black ROM.
