# Comparison with the s66 port (wip19/main.c, read-only)

File compared: s66/wip19/main.c, sha256 3d216c78…, unmodified.

States:
- **C** = discrepancy confirmed by the arcade code.
- **=** = matches.
- **V** = MAME needed to decide.

## Pin and floor

| # | Port (line) | Arcade | State |
|---|---|---|---|
| 1 | 292 and 396: «kick-outs are ALWAYS the partner coming in»; the first pin always ends in a kick-out. | Own kick-out, action 0x1E: the human mashing (0xADEA, threshold AF72/2) and the CPU according to energy and count (0xAE7E/0xAF26). There is also an immediate kick-out with a roll (0x11BC6). The partner save (0x129A4) is one more route, not the only one. | C |
| 2 | 294 and 397: with energy 0, 13/16 → count of 3. | The CPU with energy 0 (d1=6) never gets out and the partner cannot save it (0x129A4) → the count of 3 is certain (16/16). A human with energy 0 needs 0x30 presses. The arcade's 3/16 is the probability that the partner cannot save, not that of the count. | C |
| 3 | 365: lieTab {180,120,64,0} + 44 base. | 2×AF66 = 224/164/108/44 frames. | = (exact) |
| 4 | 365: mashTab {24,10,6,3}. | AF6A = 24/10/6/3. | = |
| 5 | 366: lieBand = e/12 also for the CPU. | The CPU uses the maximum from 0x8190[level*8 + slot]/4, not 12. | C. The effect depends on that maximum: with 48 it matches. |
| 6 | 76: the CPU starts with 55 (MAME demo). | 55 does not appear in table 0x8190. Where the CPU's energy is initialised in demo mode has not been read. | V |
| 7 | 396: the CPU only covers with P1's energy < 16. | The CPU's covering decision (planner 0x1D1A8 → subs 0x1190C/0x11A72) has not been compared rule by rule. | V |
| 8 | The downed CPU does not halve its time. | 0xAB1E: the CPU uses /2 if 0x1CD80 gives CS, and +0x20 if coming from outside. | C |

## Systems missing from the port

| # | System | State |
|---|---|---|
| 9 | Clock 30:00, hurry at 5:00 (music 8) and TIME UP (0x2626E). | C (missing) |
| 10 | Count-out outside the ring up to 20 and double disqualification (0xDEE4). | C (missing) |
| 11 | Sound: there is no driver; the count voices 0x3D–0x3F and the bell 0x20/0x21 are missing. | C (missing) |
| 12 | RNG: the port uses random(); the arcade uses 0x450A. | C |

## Corrected with respect to discrepancias.md
- The barrier/crowd 1C1854 (old discrepancy #1) is already implemented in wip19, lines 788–811. The condition matches 0x22462; it has not been compared line by line.
- The old #4 («lieTab is an approximation») is withdrawn: the values are exactly 2×AF66.
