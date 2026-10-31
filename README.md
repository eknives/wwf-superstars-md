# WWF Superstars (arcade) → Sega Mega Drive fan port

**Free, non-commercial fan project, made with no profit motive. AI-assisted port.**
It must not be sold or distributed for profit. All trademarks, characters, names, graphics,
music and sound belong to their respective owners. This project is not affiliated with or endorsed by them.

This repository contains **no ROM and no copyrighted data**: no graphics, fonts, sound, music,
data tables or disassembly from the original game. Only original code, our own notes and the tools.

## What you need
- Your own legally obtained MAME `wwfsstar` ROM set (zip).
- SGDK, an m68k toolchain, python3 (numpy, pillow).

## Build
```
./build.sh /path/to/wwfsstar.zip
```
1. Verifies the CRC32 of each ROM file (`roms.crc`, take values from `mame -listxml wwfsstar`).
2. Runs the extractors in `tools/` to generate `res/*.bin` and the data headers from **your** ROM.
3. Builds with SGDK.

## Status (WIP)
The game code (`src/main.c`) currently embeds tables taken from the arcade, so it is **not published yet**;
it will be added once those tables are generated at build time by the tools. Until then the build is semi-automatic.

## Layout
- `src/` – original SGDK code (boot, disclaimer, sound interface)
- `res/res.res` – resource list (binaries are generated, not committed)
- `tools/` – extraction/conversion/analysis scripts
- `analysis/` – our own notes on how the arcade works (addresses + descriptions)

---
## Resumen (español)
Port aficionado, gratuito y sin ánimo de lucro, asistido con IA, del arcade WWF Superstars a Mega Drive.
No incluye ROM ni material con copyright. Necesitas tu propio set `wwfsstar` de MAME y ejecutar `./build.sh`.
