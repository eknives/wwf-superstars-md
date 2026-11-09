# b91 — PARTIAL delivery

**ROM:** `/workspace/b91/wwf_b91.bin` — **MD5 1f7f183b0ef6fe6367d62360697935c6**.
b90 base copied in full. **Points 2 and 3 fixed/verified; point 1 NOT resolved. Do not present this ROM as complete fulfilment.**

## 1. Knee from the post — pending, not considered fixed

New MAME run confirms `arc_corner_frames.csv`: **61×8 / 62×18 / 7A×10 refreshes**, P and K. These are **4/9/5 ticks** (`10F54/10FB2`, `112F0/112FA`; clock `1508–1510`, 57.44485 Hz). MD needs a time conversion, not forcing those numbers literally at 60 Hz.

A separate clock with shared phase, bounded DMA transfer and a SAT prepared before VBlank were tried. **The repetitions did not maintain per-refresh equivalence**, although the per-tick trajectory matched. ALL those changes were withdrawn: the final ROM keeps b90's render, clock, crowd and post cadence. Final trial: loaded pose registers K **11/19/7**, P **5/19/14**; it is not claimed that these are atomic visual counters nor that they match the arcade. There are consecutive PNGs `post_corner*_f*.png` and per-refresh CSVs.

Discarded experiment: `tools/experimental_post91.c.txt`, evidence in `shots91/experimental_post/`; **it is not compiled into the delivered ROM**. The profile showed scroll work and SAT building crossing refreshes; there is no definitive CPU/DMA attribution for all the pauses. SGDK documentation consulted: [SYS/VBlank](https://stephane-d.github.io/SGDK/sys_8h.html), which warns that missing the start can postpone the process by one refresh. The scope was not extended nor was pad polling removed to hide it.

## 2. Outside — fixed and verified

Cause: b89 clips the W510 origin to 512 before entering and does not apply the **`AB1E→ACA4`** adjustment to the lying victim, two tests with offsets ±48 and ±8. Its outside limit is at **`21ED0/22140`**, table **`221B2`**: floor 128, Y192..456, X488..1040, slope /6, inner margin 48 (`21F2A/21F54`).

**Only when starting the outside Knee** is the pre-clipping origin recovered, if it still corresponds to the same position; it is limited as in the arcade and the victim is normalised. Walking and the other moves keep their original limits; the solver was not changed.

Case W510/R558/Y300: origin W510, victim R546, **Vx150**; MD and MAME contact **(528,75;309;128)**, energy 48→43 and A2. The previous difference MD540,125/Vx225 has been eliminated.

Quick regression against MAME: floor **(727;309;187)**; variant **(727;299,375;187)**; post P/K **(725,59375;309,8125;187,5)**, damage 10. **88 stable trajectory states match**; A2 keeps heights 4/7/9/10/10/9/7/4/0. Readings captured between instructions are discarded when comparing states; they are not confused with an already completed contact.

## 3. Selection — fixed and verified visually

Cause: `selDraw89` wrote the **896 overlay tiles** via CPU with interrupts blocked, delaying the HINT palette changes. Now it prepares only the cells that differ and publishes them during VBlank; there is no bulk writing during active display. Navigation/confirmation and the native confirmation flash remain unchanged (`749E/74F2/7552`, `1F5C/1F86`).

**74 consecutive PNGs per version**, four cursor changes: b90 alters up to **2799 pixels unrelated to the cursor in 4 frames**; b91 **0 pixels, 0 frames**. It is also checked that the cursor does NOT freeze: Savage→Hogan→Duggan→Honky→Savage, four distinct visual positions (258 green pixels). MAME reference also recaptured. Evidence: `select_b90/`, `select_b91/`, `select_arcade/`, `validation91.json`.

## Files and limits

- Comparisons: `comparativa91_seleccion_secuencia.png`; `comparativa91_exterior_{vuelo,impacto,reaccion}.png`; `comparativa91_poste_K_{vuelo,impacto,reaccion}.png`; equivalent floor/variant. They are comparable phases, not the same refresh/camera: MAME keeps a fixed camera in the fixtures.
- `trajectory91_compare.csv`, `pose91_refreshes.csv`, Lua and `tools/validate91.py`; NTSC and PAL run. RAM fixtures + inputs, not a full game, exhaustive four corners/outside geometries nor Everdrive. MAME keeps the CRC warning of the background chip 24j6-0.112; CPU MD5 4bd7c20fe4dbaf1b7ee8225e0e5d7359.
- Full audit: b90 intact (`b90_manifest91.json`). **Only `src/main.c` (outside Knee normalisation) and `src/select89.h` (cursor) change**. All graphics resources, corner posts, logo, Hogan, energy and other moves are identical. Diffs `source91_main.diff`/`source91_select.diff`.
- **Out of scope in the ROM: nothing. Main pending item: truly resolve point 1.**
