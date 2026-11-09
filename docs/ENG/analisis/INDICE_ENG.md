# WWF Superstars (arcade) analysis — INDEX
Status (31-10-2026): 100 % read, AUDITED by sample (auditoria.md). Sample of 32 routines: 12.5 % wrong and 12.5 % incomplete, corrected. Re-reading the second half is recommended. UNCONFIRMED: 2 (0x1F86, 0x7E4A; 0x6BA0 confirmed by Emilio). Discrepancies with s66: sistemas/discrepancias_s66.md (compared and re-verified); discrepancias.md is obsolete.
- arc_rec.dis: recursive disassembly with routine headers (the good one). arc.dis: the linear one (misaligned at 94 targets).
- rutinas.md: table of annotated routines. ram.md: RAM and hardware map. tablas.md: ROM tables.
- sistemas/: main loop, wrestlers, ropes, crowd, daze, RNG and discrepancies. The AI, referee, sound and pin/count sections are only sketched.
- Tools: tools/rdis.py, rd.py, dump.py, sig.py, anot.py, cg.py.

> In this English version the files are under `docs/ENG/analisis/` with the `_ENG` suffix (e.g. `sistemas/arbitro_ENG.md`). The `.dis` disassemblies and the analysis tools are not published.

## Added (100 %)
- sistemas/sonido.md: Z80 driver, OKI, bell 0x20/0x21 and IDs (with sonido_ids_llamadas.txt).
- sistemas/arbitro.md, sistemas/pin_cuenta.md and sistemas/reloj.md.
- sistemas/discrepancias_s66.md: comparison with wip19, read-only.
- Coverage: 100 % of bytes; 50,062/50,062 68K instructions in read routines (not counting data blocks); Z80 with 1,200 instructions and 2,523 bytes reached, all read.


## Bank names (+0x2B / index of 0x6CD8)
Verified in MAME 31-10-2026 (attract demo, /workspace/idp): +0x2B = bank (+3, copied in 0x7F44); the caption of each exhibition matches the id of object 1 (Hogan 1, Warrior 0, Macho 2, Duggan 3, Bossman 4, Honky 5). The selection slot is NOT the id: 0x7FE2 converts slot→bank (0→2,1→1,2→0,3→5,4→3,5→4,6→6,7→7).
| Bank | Content |
|---|---|
| 0 | Ultimate Warrior |
| 1 | Hulk Hogan |
| 2 | Macho Man |
| 3 | Jim Duggan |
| 4 | Big Bossman |
| 5 | Honky Tonk Man |
| 6 | Ted DiBiase |
| 7 | André the Giant |
| 8 | table |
| 9 | referee |
| 0x0A | posts |
| 0x0F | chair (UNCONFIRMED) |
| 0x10 | effects |
| 0x11 | texts |

Note: 0x4D4C and 0x5F54 put "bank 0x10" in wrestler objects; there the value may be another field and not the graphics bank (UNCONFIRMED).
