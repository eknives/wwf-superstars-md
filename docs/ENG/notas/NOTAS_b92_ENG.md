# b92 — PARTIAL delivery: Duggan floor attacks

ROM `/workspace/b92/wwf_b92.bin` — **MD5 `d9af08525a0f49f4bdc025ed00499135`**, 1703936 bytes. Base b91 intact. **Stomp verified in the trials; floor/post Elbow functional and physics compared, but the visible cadence is NOT yet identical. Do not consider the whole assignment closed.**

## 1. Stomp — verified in the tested cases
- C706/C79E–C8A8 and CB6C/CB75: P=A on the body, same plane, |dy|<24, head anchor Xv±40 and the original strict limits. 1173A/118BC: 159×14 and 15A×10 arcade refreshes; damage 1 at 117E0 on entering 15A (11782→1179A), with no second XY filter.
- Independent Duggan engine `src/duggan92.h`, existing arcTick clock without modifying it. Keeps 7 ticks of 159 and 5 of 15A counting the exit. MAME 57.444852941 Hz, tick=2 refreshes; MD keeps real time, it does not copy 14/10 literally at 60/50 Hz. NTSC sample 15/11, PAL 13/8; compatible with conversion and quantisation.
- Normal entry, |dy| 23 accepted / 24 rejected and opponent moved to X900 after starting: same damage 48→47 in MD and MAME. Normal impact (744;300;187). A2 reaction compared.

## 2. Elbow to the head — PARTIAL
- CB72, sub11→10A5E via FB9C; tables 11180/11188→111F0, poses 11372: 61/62/1CB/1CC, variant 1CD/1CE. Initial native holds 8/18/10 refreshes. Solver 159AC, integration 3DCE/3E20: Vz0x500, gravity 0x50 per refresh; limits 0x2000. Inner offset 64, outer 32; the victim's orientation, not Warrior's Vx rule.
- 11084/110BC/110C0: descending and height≤floor+16, point Xa±8,Ya+4 against the native rectangle. Impact keeps fractions: Yword=Yv−1, Zword=floor; no 7D nor artificial rope crash (24102→24322, 24106→24324 are RTS). Damage 5 (10DC0), A2 (A554/28EC).
- Exact MD/MAME contacts: normal (697;299;187), mirror (823;299;187), variant (697;299,375;187), energy 48→43. A2: 4/7/9/10/10/9/7/4/0, RAM comparison of both. Miss 10C6A: −2, recoil 24 according to orientation, 1CF→16→17→1A (9FCC/AF66/AA00); miss contact (672,0625;300), 48→46.
- **Pending visible cadence:** NTSC 61/62/1CB=10/17/12 versus the expected conversion 8–9/18–19/10–11. Mirror 10/18/10; variant 9/18/10. PAL also has discrepancies. The logic uses arcTick, but it does not certify visible duration; see `pose92_refreshes.csv` and consecutive PNGs.

## 3. Elbow from the post P/K — PARTIAL
- F6EF=`2F,20,20`, dispatch FC14→10A5E. Same Duggan physics/poses, adjustments 10B5E/110E4. Damage 10 (10DCC); shared native miss, not a new generic jump.
- P and K connect in MD/MAME (694,34375;299,8125;187,5), Vx399, Vy−462, energy 48→38 and A2. **88 stable trajectory states** floor/mirror/variant/post match; 0 without a sample.
- **Visible cadence NOT resolved:** NTSC P 9/21/5 and K 6/19/12; arcade 8/18/10 before converting frequency. PAL P 4/18/7, K 8/18/5. Neither the global render nor Warrior's post was fixed. Private SAT trial discarded: `tools/experimental_sat92*`, NOT compiled. Precise cause CPU/DMA/publication still not isolated; it is not gratuitously attributed to any of them.

## Evidence and limits
- MAME 0.276: arcade `wwfsstar`, MD `genesis` and PAL `megadriv`, ten short cases per region, RAM fixtures + real buttons. `shots92/validation92.json`, `arc_frames.csv`, `md92_knee_frames.csv`, `pal_md92_knee_frames.csv`, `trajectory92_compare.csv`, `pose92_refreshes.csv`. Scripts in `tools/`.
- PNG: `comparativa92_stomp_impacto.png`, `comparativa92_elbow_{vuelo,impacto,reaccion}.png`, `comparativa92_elbow_mirror_impacto.png`, `comparativa92_elbow_above_impacto.png`, `comparativa92_corner{P,K}_{vuelo,impacto,reaccion}.png`, `comparativa92_miss.png`. Comparable phases, cameras/refreshes NOT synchronised; they are not a pixel-by-pixel certification of palettes. Sequences `refresh_{stomp,elbow,cornerP}_f*.png`.
- Warrior regression: same functions/headers and original render, same contacts/energy as b91 on floor, variant, post P/K, outside. The already irregular post cadence remains: samples in `warrior92_refreshes.csv`, visible equality is NOT claimed. Not tested: Everdrive, full game, all corners, Duggan outside nor miss from the post.
- Only main.c changes for Duggan's input/engine, new `duggan92.h`/`duggan92_poses.h`, and appendices to tables/tiles with 12 poses from bank 3 (6CD8/7FE2; converter `tools/gen92.py`). Previous graphics prefix identical. Rest of res intact, Hogan/corner posts/logo/selection/other energy/Warrior not edited. `source92_main.diff`, `b91_manifest92.json`.
- Arcade CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; MAME keeps the background CRC warning 24j6-0.112. The arcade ROM is not packaged in the backup.
- **Out of scope in the ROM: nothing intended. Main pending item b92: visible Elbow cadence; do not replace this limitation with the logical match.**
