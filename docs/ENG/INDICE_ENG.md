# Superstars — master index of findings

**Recommended entry point:** **b95**, `docs/notas/NOTAS_b95.md` (running by arcade tick W28/D27, the same on PAL/NTSC; background by queued DMA with no frames lost next to the posts; rope crash 9E78/9F02; base b94). Move inventory: `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`. Duggan's Elbow and the post Knee cadences remain LOW, "polish at the end". Translated notes: same paths under `docs/ENG/` with the `_ENG` suffix.

Paths relative to the repository root. Addresses are arcade 68000 addresses unless stated otherwise. **(np)** = not published: it exists only in the project's private backup because it contains arcade data (disassembly, screenshots, dumps, bulky RAM traces) or is internal material; it is cited so that people know it exists and how it was obtained. The per-version notes are kept verbatim: their paths `/workspace/...` and `01_port_sgdk/…`, `02_arcade_decompilado/…`, `03_roms/…`, `04_herramientas/…`, `05_referencias/…` belong to the private backup. An old note is neither the current state nor a new verification.

## General recipe for moves per wrestler

**[PATRON_MOVIMIENTOS_ENG.md](PATRON_MOVIMIENTOS_ENG.md)** — selector→routine→tables per id/pair→physics/contact→energy/reaction/end; catalogue of the slots of the eight wrestlers, exceptions and real mapping to b92. It is a study, not an implementation; unconfirmed contents are marked U. Visible cadence of Duggan's floor/post Elbow and Warrior's post Knee: **LOW, "polish at the end"**. Sections §6–§10: lying opponent orientation (b93), pin (b94), research on running/posts/ropes, and b95.

- **Flip of the lying opponent in Knee/Elbow (b92):** the arcade never changes the victim's `+A`; b92 used `vface` as bit7 in zones/target/box/A2 while drawing the lying wrestler with `vface^1` → mirrored on contact. Cause and proposal: `docs/PATRON_MOVIMIENTOS.md` §6; **fixed in b93** (`docs/notas/NOTAS_b93.md`).
- **Warrior pin (cover) b93 vs arcade:** `11A72`/`BD10`/`BEF2`: X=Xv∓32 by the opponent's bit7, Y=Yv+1, Z=203, orientation = opponent^0x80. Proposal in §7, **implemented in b94** (§8).

## Search before researching again

- Per-version notes: `docs/notas/NOTAS_b49.md` … `NOTAS_b95.md`; summary in `docs/CHANGELOG.md`.
- Annotated arcade routines (address, name, deduction): `docs/analisis/rutinas.md`.
- Example: `grep -rn -i '10a5e\|stomp\|AF66' docs/`.
- (np) Backup indexes: `DESCUBRIMIENTOS.csv` (topic, summary, addresses, path and line), `DOCUMENTOS.csv`, `RUTINAS_DESENSAMBLADO.csv` (lines of `arc_rec.dis`), `HERRAMIENTAS.csv`, `PROCEDENCIA.csv`, `INVENTARIO_TOTAL.csv`.

## Sources, general map and quality

| Topic / address | What is known | Where to look |
|---|---|---|
| General decompilation | `arc_rec.dis` (np) is the preferred aligned one; the linear `arc.dis` (np) has misaligned targets. They are regenerated from your own ROM with `tools/analisis/rdis.py`. | `docs/analisis/INDICE.md`; `docs/analisis/auditoria.md` |
| Annotated routines | Table of address, name and deduction, including branches and exceptions. | `docs/analisis/rutinas.md`; `tools/analisis/anot2.py` |
| RAM/hardware | Actor structures, shared memory, video/sound registers. | `docs/analisis/ram.md`; `docs/analisis/sistemas/luchadores.md` |
| ROM tables | Dispatches, poses, boxes, energy, AI, maps and geometry by address (addresses and description only). | `docs/analisis/tablas.md` |
| Uncertainties | Audit and historical discrepancies; "100 % read" does not guarantee full correctness. | `docs/analisis/sistemas/sin_confirmar.md`, `discrepancias_s66.md`, `cotejo_s66_wip19.md`; `docs/ESTUDIAR.md` |
| Reference ROM | MAME set `wwfsstar`; not included. Everyone uses their own legal copy. | `README.md`; `tools/extractor/README.md` |

## Clock, movement and animation

| Topic / address | Summary | Path |
|---|---|---|
| 1508–1510 / 155A–157C | Actor logic every 2 refreshes; MAME 57.444852941 Hz, tick 34.816 ms. The MD converts it to 50/60 Hz (`arcTick`, 28.72 Hz). | `docs/estudios/KNEEDROP_arcade.md` §2; `docs/analisis/sistemas/reloj.md`; `docs/notas/NOTAS_b90.md` |
| 3DCE–3E20 | Integration of velocities and height; position 16.16, velocities 8.8. | `docs/estudios/KNEEDROP_arcade.md` §3; `docs/estudios/DUGGAN_SUELO_arcade.md` §2 |
| 156FA / 159AC–15B3E | Table-driven jump solver, limits/truncation/target; there is no universal fixed trajectory. | `docs/estudios/KNEEDROP_arcade.md`; `TABLAS_DUGGAN.txt` (np) |
| 6CD8 / 7FE2 | Graphics bank ≠ selector slot: W0, Hogan1, Macho2, Duggan3, Bossman4, Honky5, DiBiase6, André7. | `docs/analisis/INDICE.md`; `docs/analisis/sprites/BANCOS.md` |
| 1761E / 172FA / 1636C | Boxes/damage by pose and id, reaction by pose and filter by action. | `docs/estudios/ENERGIA_arcade.md`; `docs/analisis/tablas.md` |
| Pose→tiles / 46A0 | b88 fixed the throw direction and the palette bank of borrowed blocks. | `docs/notas/NOTAS_b88.md` |
| Running 93EE/945C/94CE, 0x95BC, 3DF0 | vel/4 px per tick (W 7 / D 6.75), poses 10–15 × 2 ticks; W 201.1 and D 193.9 px/s. Implemented in b95. | `docs/PATRON_MOVIMIENTOS.md` §9–§10; `docs/notas/NOTAS_b95.md` |

## Attacks — Duggan and Warrior

| Topic / address | Summary | Path |
|---|---|---|
| W combo FC84, FD70/FD7C | Poses 150..155, waits and press window; do not take a table duration as 60 Hz frames. | `docs/notas/NOTAS_b87.md`; `NOTAS_b86.md` as background |
| D combo FC4E→FC70→FDA0 / FE88 | Duggan's human dispatch is different; b89 uses FD70/FD7C for both. Damage 1 per hit. | `docs/estudios/ENERGIA_arcade.md` |
| Kick FF3A / 188AB / 188C7 | Damage 4 for humans, CPU exception 0, bonus against running depending on the path. | `docs/estudios/ENERGIA_arcade.md` |
| Clothesline CD14 / 12E7A / 1302E | Entry while running, poses 1D0–1DB and proximity 16634; contact/subtractions 4 or 2. | `docs/notas/NOTAS_b87.md`; `src/cl87.h`; `src/main.c` |
| Clothesline fall 9B9A | Action 8/sub 17; travel direction/flip and palette reviewed in b88. | `docs/notas/NOTAS_b88.md` |
| Knee W C706 / 10A5E | Exact input K on the head; zones, variants, solver, impact and end. | `docs/estudios/KNEEDROP_arcade.md` |
| Knee W 112F0 / 112FA / 10F54 | Poses 61/62/7A: 8/18/10 refreshes; variant 76/77, not 7D. | Same study §§2–3; `src/knee90.h`; `docs/notas/NOTAS_b90.md` |
| Knee W A554 / 28EC | The victim's A2 with arc 4/7/9/10/10/9/7/4/0; not a generic fall. | Knee study §4; `docs/notas/NOTAS_b90.md` |
| Knee W outside AB1E→ACA4 / 21ED0 | b91 normalises only the Knee: contact 528.75/309/128, not 540.125. | `docs/notas/NOTAS_b91.md` |
| Knee W post F35A/F636/F6E6 | P or K→sub 2C; trajectory checked, final cadence irregular (**PENDIENTES, LOW**). | `docs/notas/NOTAS_b91.md` |
| **Duggan Stomp CB75 / 1173A / 118BC** | **P body, 159×14/15A×10 visible refreshes; impact on entering 15A; damage 1. Not an "elbow".** | **`docs/estudios/DUGGAN_SUELO_arcade.md` §1** |
| **Duggan Elbow CB72 / 10A5E / 11372** | **K head, 61/62/1CB/1CC; variant 1CD/1CE; 8/18/10; offset −64, impact point ±8,+4; damage 5.** | **Same study §2** |
| **Duggan post Elbow F6EF / FC14** | **P/K→sub 2F; same holds, trajectory 399/−462 in a fixture; damage 10. Visible cadence pending.** | **Same study §3** |
| Miss 10C6A / 9FCC | −2 to the human attacker, action 8/sub 5, 1CF→16→17→1A; not a penalty for every fall. | Knee/Duggan and energy studies |
| D floor b92 | Independent Duggan engine instead of the old gs5/gs11 activations; Elbow cadence pending. | `src/duggan92.h`; `docs/notas/NOTAS_b92.md` |
| Remaining moves | Techniques done/partial/missing. | `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md` |

## Energy, floor, pin and referee

| Address / topic | Summary | Path |
|---|---|---|
| 7EE6→7F76 / 7FEC | Humans 48; CPU 8190/progression/DIP different; HUD ceil(E/4) up to 12. | `docs/estudios/ENERGIA_arcade.md` § Initial energy |
| +3C/+3E / 16488–1649A | Energy/damage separate; saturated subtraction to 0; no passive regeneration; 0 is not a KO. | Same study § Common rules; `src/main.c` |
| 1698A / 1642A / 16418 | CPU punch/kick 0, bonus against action 1/15/16 and F9.0 duplication. | Energy study; do not confuse the CPU with an uncontrolled opponent |
| 162BC–162DA | The FFFE clothesline exception skips bonus and duplication. | Energy study; `docs/notas/NOTAS_b90.md` |
| 117E0 / 10DC0 / 10DCC | Stomp 1, drop 5 floor / 10 post. Do not use the FAQ's 2/3 scale as RAM. | Energy, Knee and Duggan studies |
| AF66 / AF6A / AA00 | Floor waits 112/82/54/22 ticks, inputs 24/10/6/3, get-up 8..40 ticks by index/flags. | Energy study; Knee study §4; `docs/analisis/sistemas/pin_cuenta.md` |
| AD12 / ADEA / AE7E / AF72 | Getting up/kick-out read energy; E0 restricts escape but does not give an immediate win. Integration into the port pending. | Energy study |
| Grapple / 14CFC / 2209C | Holds/whip/ordinary bounce with no damage of their own; special outside crash 5 with conditions. | Energy study; `docs/analisis/sistemas/cuerdas.md` |
| Referee / counts | 3/20 counts and animations; b89 restarts the match without going back to the selection. | `docs/analisis/sistemas/arbitro.md`, `pin_cuenta.md`; `docs/notas/NOTAS_b89.md` |
| W/D pin BD10/11A72/BEF2, B012/B0A0 | Covers at Xv∓32 (W) / Xv∓36 (D); kicking out next to the rope = arcade since b95. | `docs/PATRON_MOVIMIENTOS.md` §7–§10; `docs/notas/NOTAS_b94.md`, `NOTAS_b95.md` |

## Selection, graphics, stage and sound

| Topic / addresses | Summary | Path |
|---|---|---|
| SELECT 704E / 7240 / 729C | 2×3 Savage/Hogan/Warrior / Honky/Duggan/Bossman, WWF in the centre, choose a partner; 1P/VS/COOP. | `docs/estudios/SELECCION_arcade.md` |
| 749E/74F2/7552 / 7098/72A4 | Navigation without wrap, button 1 confirms, internal timer 384 refreshes; autoplay/flash separate. | Selection study; `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| 2034A / 20404 / 210A8 / 2FAE | Scene/map/portraits/cursors and palettes converted from arcade data. | Selection study; `src/gen/select89_data.h` and `res/` (generated, np) |
| b91 flicker | 896 overlay tiles delayed HINT; now only dirty cells are published in VBlank. | `docs/notas/NOTAS_b91.md` |
| C=A+B / Y | Normalisation before edge detection; Y switches the controlled wrestler (6-button pad). | `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| Ring 21E5A/21ED0 / 221B2 | Inner/outer limits and plane; do not confuse world coordinates with screen coordinates. | `docs/analisis/sistemas/cuerdas.md`; `docs/notas/NOTAS_b91.md` |
| Ropes / palettes / HUD | Historical cases and discrepancies; preserve the corner posts/logo edited by Emilio (not published). | `docs/analisis/sistemas/cuerdas.md`; `src/gen/ropes.h`, `src/gen/hud.h` (np); `docs/REGLAS.md` |
| Background streaming | b95: columns/rows through a DMA queue with a budget; no frames lost next to the posts. | `docs/notas/NOTAS_b95.md`; `docs/ARQUITECTURA.md` |
| Crowd 23170 | Animation/camera tables and crowd resources; choppy audio reported, no certified cause. | `docs/analisis/sistemas/publico.md` |
| Sound 25E6 / OKI / Z80 | Driver, IDs and bell; decoded WAVs (np). | `docs/analisis/sistemas/sonido.md` |
| AI 18F16 onwards | Arcade reference only, **not an authorisation for AI in the port**. | `docs/analisis/sistemas/ia.md`; `docs/analisis/rutinas.md`; `docs/REGLAS.md` |

## Current code, deliveries and tools

- Building: `docs/COMPILAR.md`. With the real resources, the b95 ROM gives MD5 **7be789d70d892c1efb86af8630b296a6**.
- Architecture of `main.c`: `docs/ARQUITECTURA.md`.
- Current MAME tests (b95): `tools/mame/`. Analysis tools: `tools/analisis/`. Resource extractor: **PENDING**, `tools/extractor/README.md`.
- ROMs b48–b95, earlier code copies, screenshots and traces: (np), in the private backup; the MD5 of each ROM is in `docs/CHANGELOG.md`.

## Latest versions

| Version | Summary | Path |
|---|---|---|
| b92 | Duggan's Stomp/Elbow/post Elbow; Elbow cadence not closed. | `docs/notas/NOTAS_b92.md`; `src/duggan92.h`, `src/duggan92_poses.h` |
| b93 | `oriVictima=vface^1` in zones, target, post, box, outside; A2 without mirroring. | `docs/notas/NOTAS_b93.md`; `docs/PATRON_MOVIMIENTOS.md` §6 |
| b94 | Lying wrestler without ±32; covers at Xv∓32/∓36; Warrior faces opposite to the lying wrestler; Duggan's pin by body zone. | `docs/notas/NOTAS_b94.md`; §7–§8 |
| Research 2026-11-09 | Running, slowdown next to the posts and ropes (no changes to the port). | `docs/PATRON_MOVIMIENTOS.md` §9 |
| b95 | Running W28/D27 by arcTick, pose every 2 ticks; background by queued DMA; rope crash 16 px ahead → sub 2 → inward bounce and lying; soilNudge with vface^1. | `docs/notas/NOTAS_b95.md`; §10 |
