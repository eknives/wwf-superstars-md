# Tools

Only the ones current for b95. Earlier versions and the historical converters are in the private backup. No tool contains arcade data: they all read **your own ROM** or the MD ROM you build.

## `tools/mame/` — MAME 0.276 tests used to verify b95

| Script | What it measures |
|---|---|
| `mame95.sh rom.bin script.lua [genesis\|megadriv]` | Launcher with no video or sound. Variables: `MAME`, `ROMPATH`, `SHOTS`. |
| `run95.lua` + `runsum.py` | Running speed (px/s) and pose changes per second, W and D. |
| `post95.lua` + `postsum.py` | Frames lost while walking towards the 4 posts, and background integrity by reading VRAM through the VDP port. |
| `zafar95.lua` + `zsum.py` | Kicking out of a pin next to the rope: final X at Xv 760/728/708/693/832. |
| `kick95.lua` | Kick-out in mid-ring and 3-count. |
| `salir95.lua` | Leaving and entering the ring. |
| `pinvis95.lua` | Sequence of pin states. |
| `fs2_95.lua` | Throw (sub 1) into the rope. |
| `postes95.lua` | Still screenshots of the posts. |
| `cl95_clothesline.lua` | Clothesline (variables `SYM`, `CLD`, `MODE88`). |
| `prof95.lua` | Profiling of lost frames. |

- The scripts read the addresses of the port's variables from `out/symbol.txt` (variable `SYM`) and write CSV to the path in `OUT`.
- Some keep default paths `/workspace/...` from the original machine: adjust them with the variables or by editing the header.
- MAME buttons: `P1 A`/`P1 B`… Wrestler index in the port: 0 = Duggan, 1 = Warrior.

## `tools/analisis/` — analysis of the arcade program

`rdis.py` (disassembler that generates `arc_rec.dis` from your ROM), `anot.py`/`anot2.py` (annotations of the 964 routines that produce `docs/analisis/rutinas.md`), `cg.py` (call graph), `sig.py`, `rd.py`, `dump.py`, `reread.py`, `regen.py`, `audit_sample.py`, `oki.py` (OKI ADPCM decoder), `z80rec.py`, `render_obj.py`, `sheets.py`. Several contain `/workspace/...` paths that need adjusting.

## `tools/extractor/` — **PENDING**

Specification of the resource extractor: `tools/extractor/README_ENG.md`.
