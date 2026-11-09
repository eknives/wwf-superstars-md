# b89 — selection and controls

ROM: `/workspace/b89/wwf_b89.bin`  
MD5: `7c1c5202f5fb27f115278eecd9b9ffb9`  
Base b88 intact: `96371335c6b9cb43b08d158ba73ec488`. Local SGDK build with the requested PATH/make, `BUILD_b89.log`.

## 1. SELECT PLAYERS — verified, with the limits stated below

- Isolated screen before the match, after title/START. Portraits, names, pattern, central logo and cursors decoded from the arcade data, not redrawn. Scene: `0x704E`, `0x1F434 → 0x2034A`; map `0x210A8`; six 4×4 blocks of `0x20404` (tiles `383–392`, `393–3A2`, `3A3–3B2`, `3D3–3E2`, `3C3–3D2`, `3B3–3C2`). Palette 4: `0x706C/0x29F6`, BG table `0x2FAE`.
- Same 2×3 layout and positions. 4-to-3-bit-per-channel conversion specific to MD; the portraits' colours are not reduced. CRAM banks are reused in the vertical gaps: changes at the end of MD lines 95/119/143. The selection keeps the first 224 arcade lines: only the bottom 16 margin lines are omitted, without scaling.
- Green 1P / yellow 2P cursors: native tables `0x7686/0x782A`, drawing `0x75B6`. Movement by edges and without wrapping: table `0x74F2`. **A confirms**, which was already punch/Button 1; B does not confirm, same as dispatch `0x749E/0x7552`. Picking duplicates is not allowed.
- Invisible timer `0x180` = **384 arcade refreshes**, `0x7098/0x72A4`. Clock converted to real time: 6250/6528 per NTSC VBlank, 6250/5440 PAL; test: it reaches zero after **401** NTSC VBlanks and **334** PAL, roughly 6.68 s nominal. Random draw: modulo 6 and filter of picked wrestlers `0x740E–0x742A`; movement `0x747A`; new candidates every 16 and confirmation at phase 63/64 (`0x73E8`). The MD seed does not reproduce the random CPU registers of `0x450A`.
- Flash: colours/pens from `0x2048/0x2054/0x205A`, steps of 2 refreshes and duration `0x40`, engine `0x1F5C/0x1F86`. **81 ticks of flash registers compared with MAME: zero differences** (`flash89_result.txt`). Closing of 64 refreshes, or 112 in versus: `0x7134–0x717A`, checked.
- Adaptation of MD starts: START on pad 1 = solo, you pick two; START on pad 2 = co-op, one per player; both STARTs = versus, two per player. The modes correspond to the closing `0x72DA–0x73DC`. **The result is stored but does not modify the match: it is still Duggan vs Warrior from b88.**
- Graphical evidence: 12 captures compared with MAME, **0/57,344 different pixels** after colour conversion. Another three differ only in the visible phase of the flash, not in the drawings; they are identified as such in the pairs. Initial screen also checked on PAL and three-button pad. Results: `verify89/RESULTADO_b89.txt`.

## 2. Count finished → restart match — verified

The selection is only called once before the fight loop. b88's `countStep/pinAdvance → matchReset` is kept; no restart goes back to the menu. Short tests with RAM fixtures just before the third count strike and the 20 count-out: 3/20 appears, the existing 120-frame wait ends and both wrestlers return to X=736/660, counts at zero, match phase=4 throughout. A full fight was not simulated to reach those positions naturally.

## 3. C=A+B; swap moved to Y — verified

C is normalised to A+B **before computing edges**; no other running logic is added. In two independent runs C and A+B produce **32 identical snapshots of the wrestler's 100 bytes**; C runs without changing `ctl`. Same result with 3- and 6-button pads. Y on the 6-button pad switches `ctl` 0→1→0, once per press. The old START+C shortcut likewise becomes START+Y so that C is truly equivalent to A+B.

## Captures and limits

In `shots89/`: `pareja_C_initial.png`, `pareja_C_partner.png`, `pareja_C_confirmed2.png`, `pareja_COOP_initial.png`; `md_C_C_run.png`, `md_C_Y_swap.png`, `md_C_pin3.png`, `md_C_pin_restarted.png`, `md_C_ringout20.png`, `md_C_ringout_restarted.png`.

b88 had no title/start: a START gate is added with the arcade title **static and reduced to 16 colours**; the attract mode, the later presentation and music 0x0A are not ported. After selecting there is a restore/load of the match; it is not claimed that this transition is identical to the arcade. Nor is frame-by-frame capture synchronisation claimed for the three images with a different flash phase. MAME warns of a different checksum on `24j6-0.112` of the existing local set; the comparisons are against that set. No Everdrive/physical board test.

All pre-existing resources in `res/` remain identical to b88 (except the list/declarations of new resources). **Upper corner posts and ring WWF logo intact; no other move, AI or match timing retouched.**
