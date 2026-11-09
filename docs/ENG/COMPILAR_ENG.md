# Building the port (b95)

## Environment used and verified

| Component | Version | Notes |
|---|---|---|
| SGDK | **2.11** (April 2025) | `GDK` points to its root (`makefile.gen`, `bin/`, `inc/`, `lib/`). |
| Toolchain | **m68k-elf-gcc 13.1.0** + m68k-elf binutils | On the `PATH` (`m68k-elf-gcc`, `m68k-elf-objcopy`…). |
| Java | **17** | For SGDK's `rescomp.jar` and `sizebnd.jar`. |
| make | GNU make | Linux x86_64 (it should also work on Windows with SGDK; not tested). |
| MAME | **0.276** | Only for testing: `genesis` = NTSC, `megadriv` = PAL, `wwfsstar` = arcade. |

If your SGDK installation does not include `lib/libmd.a`, build it first with `make -f $GDK/makelib.gen`.

## Step by step

1. **Your own ROM.** Legally obtain the MAME set `wwfsstar`. It is not distributed here.
2. **Resources.** Generate the 32 files in `res/` and the 4 headers in `src/gen/` with the extractor. **PENDING**: the specification is in `tools/extractor/README_ENG.md`. The paths expected by `res/res.res` are `res/graficos/...`, `res/datos/...` and `res/sonidos/...`.
3. **Build** in the repository root:
   ```sh
   export PATH=/path/toolchain/bin:/path/jdk17/bin:$PATH
   make clean
   make GDK=/path/to/SGDK-2.11
   md5sum out/rom.bin
   ```
   **Do not use `make -B`**: the SGDK template can overwrite `src/main.c`.
4. **Check.**
   - With the exact b95 resources (including Emilio's edits to the corner posts and logo, which are not published), the MD5 is `7be789d70d892c1efb86af8630b296a6`. Verified on 2026-11-09 with this same layout (`src/gen/`).
   - With resources extracted from the arcade only, the background will be the original one and the MD5 will differ.
5. **Test** in MAME: `mame genesis -cart out/rom.bin` (or `megadriv` for PAL). On real hardware, with a flashcart (Everdrive): not yet verified for b95. The automated tests are in `tools/mame/`.

## Checking only that it builds (without the arcade ROM)

- Create every `res/` file with the size given in the table in `tools/extractor/README_ENG.md`, filled with zeros. The `.wav` files must be valid PCM WAV files containing silence.
- Create the 4 headers with the declarations from that same document, initialised to `{0}`.
- `make` finishes without errors and produces a 1,703,936-byte ROM with no usable graphics or sound. Tested on 2026-11-09: in MAME (`genesis`) the screen is completely black at frames 300 and 900.
- The two `.wav` files must be mono, 16-bit, 8000 Hz, with 32768 samples. Another format still builds, but the ROM changes size.

## Video memory and size

ROM of 1,703,936 bytes (aligned to 128 KB by `sizebnd`). VRAM map, in `main()`: BG_B 0xE000, BG_A 0xC000, Window 0xD000, sprites 0xF000, HScroll 0xF800.
