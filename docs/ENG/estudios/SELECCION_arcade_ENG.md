# Arcade selection — study, no changes to the port

**Method:** MAME `wwfsstar`, local ROM; coin + start + joystick/button through `observe.lua`. Inputs, RAM reads and captures only: no RAM writes, no port edits and no ROM build. Four short runs: 1P, versus, cooperative and waiting without choosing. Evidence: `1P.log`, `VS.log`, `COOP.log`, `TIMEOUT.log`; original 256×240 views, without the MAME interface. `RESUMEN_seleccion.png` gathers six states.

## Observed look and controls

- Blue background with a WWF pattern; **SELECT PLAYERS** at the top and the WWF logo in the centre. Six portraits in two rows of three, with the central ones shifted vertically. Names under the portraits:

| Selection ID | Top | ID | Bottom |
|---|---|---|---|
| 0 | RANDY SAVAGE, left | 3 | HONKY TONK MAN, left |
| 1 | HULK HOGAN, centre | 4 | HACKSAW JIM DUGGAN, centre |
| 2 | ULTIMATE WARRIOR, right | 5 | BIG BOSS MAN, right |

- 1P starts on Savage: green frame and **1P** label. 2P starts on Warrior: yellow frame and **2P**. Right from Savage goes to Hogan; down from Hogan goes to Duggan. Movement is by new presses, not continuous movement by holding the direction. Table `0x74F2` connects grid neighbours: the edges **do not wrap**.
- The player's **Button 1** confirms. Do not confuse it with the cabinet's three start buttons. Code: read/edges `0x7240–0x729A`; dispatch `0x749E` (0 = move, 1 = confirm, 2/3 = return without selection). Confirmation `0x7552`: blocks duplicates through bits in `0x1C0069` and flashes the portrait background; green/magenta changes are visible. Test: P2 tried to confirm Duggan, already chosen by P1, and its counter stayed at zero.

## Teams and transition, verified

- **Start A — 1P VS CPU:** on the same screen you choose a wrestler and then a partner; there is no other partner screen. Test: Duggan and Honky; both appear in the match HUD (`08_1P_combate.png`). The two CPU opponents are drawn at random from the rest (`0x71E8`).
- **Start B — 1P VS 2P:** each player chooses two, without repeats between teams. Manual confirmation verified: Duggan/Honky against Big Boss Man/Warrior (`10` and `11`).
- **Start C — 1P/2P VS CPU:** each player chooses one and they form the same team. Verified Duggan + Big Boss Man, together in the left HUD (`13`). Joining code: `0x7392–0x73A6`; closing conditions `0x72DA–0x731E`.
- On confirming, the cursors are removed and the chosen wrestlers flash. Then there is a transition: in 1P the message **THREE MORE VICTORIES TO GET TO THE TITLE MATCH!!** was captured, the presentation **WWF Live from NEW YORK**, the entrance and the match. The loop `0x704E–0x71B2` waits `0x40` refreshes on closing, or `0x70` in versus.

## Time and sound

- **No numeric counter is visible** in the selection captures, not even just before the limit. There is an internal time: `0x7098` loads `0x180` = 384 into `0x1C006A`; `0x72A4` subtracts one per refresh. In the log: 383 at frame 602 and 363 at 622. About 6.68 s with the refresh rate configured in this MAME (~57.44 Hz; not a board measurement).
- Without choosing, when it runs out an animated random draw starts that fills the free places: `0x7328`, `0x73E8`. In `TIMEOUT.log`, first automatic choice at frame 1049 and second at 1113. This does not mean the whole screen lasts only 384 frames: the draw and closing add time.
- `0x705E–0x7066` prepares music command **0x0A**, sent through `0x25E6`. **Name of the tune and SFX not identified**: the tests were run without audio output.

## Quick graphics location, from code/driver

- Scene 4: `0x7078 → 0x1F434 → 0x2034A`. Base map in CPU ROM `0x210A8`, written to BG RAM `0x0C0000`; decompressor `0x203C2`. Portraits: `0x2035A–0x203B0`, blocks of 4×4 16×16 tiles through `0x20404`:

| Portrait | BG tiles inclusive | BG colour bank |
|---|---|---|
| Savage | 0x383–0x392 | 0 |
| Hogan | 0x393–0x3A2 | 1 |
| Warrior | 0x3A3–0x3B2 | 2 |
| Honky | 0x3D3–0x3E2 | 3 |
| Duggan | 0x3C3–0x3D2 | 4 |
| Big Boss Man | 0x3B3–0x3C2 | 5 |

- Driver region `bgtiles`: `24j7-0.113` at 0x00000 and `24j6-0.112` at 0x40000; plane format `tiles16x16_layout`. They are not linear offsets of complete images. Text/cursor: FG RAM `0x080000`, region `fgtiles`, ROM `24aa-0.58`; cursor update `0x75B6`, tables `0x7686` and `0x782A`.
- Selection palette: selector **4** at `0x706C`; loading `0x29F6`. BG: table `0x2F0A`, entry 4 → `0x2FAE`, eight pointers to colours: `0x3416/3434/3452/3470/348E/34AC/34CA/34CA`, destination `0x140200`. Flashing: `0x1F5C/0x1F86`. References checked against `analisis/tools/prog.bin` and `wwfsstar.cpp`; no graphics were extracted or modified.

## Main captures (in this folder)

`01_1P_inicial.png`, `02_1P_cursor_hogan.png`, `03_1P_cursor_duggan.png`, `04_1P_primero_confirmado.png`, `05_1P_elegir_companero.png`, `06_1P_equipo_confirmado.png`, `07_1P_transicion.png`, `08_1P_combate.png`, `09_2P_versus_inicial.png`, `10_2P_versus_equipos.png`, `11_2P_versus_combate.png`, `12_2P_coop_inicial.png`, `13_2P_coop_combate.png`, `14_limite_sin_contador_visible.png`, `15_timeout_sorteo.png`.

**Limits:** observation of the local set in MAME, not a physical board or other revisions/regions. Sound not identified; no full extraction of all texts/tiles was done.
