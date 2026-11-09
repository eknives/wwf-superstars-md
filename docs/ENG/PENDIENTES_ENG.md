# Pending implementation — by priority

This does not authorise changes. State as of b95; symptoms reported by Emilio without a new test are marked as such. Unresolved research is kept separately in ESTUDIAR.md.

## HIGH — functional fidelity / Duggan focus

- **Moves still missing (excluding the LOW-priority cadences)** from the inventory `01_port_sgdk/actual/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`: Duggan High Knee, Body Slam, Headlock, Bulldog, Back Suplex, Back Body Drop, Dropkick against a running opponent, Pick Up and Dropkick from the post; Warrior Shoulder Tackle, Body Slam, Headlock, Gorilla Press, Atomic Drop, attacks against a running opponent, Pick Up and Dropkick from the post. The b89 inventory is historical; check b92: Warrior's Knee and energy advanced in b90/91; Duggan's Stomp in b92 passes the tests; floor/post Elbow work, with cadence pending, LOW only.
- **Energy vs pin/kick-out and getting up:** integrate the native rules that b90/91 still does not cover outside the Knee. Zero is not a KO; do not indiscriminately extend AF66 or the escape block at zero. Source: energy study §§ Low energy / Differences; `NOTAS_b90.md`.

## MEDIUM — visual/sound errors and coverage of variants

- **Crowd: choppy sound**, reported by Emilio; review playback/mixing and compare with the arcade before fixing. Not diagnosed again in this backup. See the sound/crowd analysis and historical notes.
- **Green Macho**, reported by Emilio; fix only after checking source/palette/bank. Not presented as an already measured problem or as an authorised change in another version.
- **Clothesline gaps:** back/rope variants and full coverage of links/reactions are missing; b88 fixed the fall direction and palette, not all variants. See the b89 inventory, NOTAS_b87/b88 and the energy study. Do not reopen the already fixed contact without evidence.
- Complete natural coverage of Knee/selection: other corners, limits, opponents, play without fixtures and hardware. The specific outside normalisation and the selection flicker were fixed/verified in b91 and are not listed as open bugs.

## After b93 (lying opponent orientation fixed)
- **Not verified in b93:** natural knockdown in a match→Knee/Elbow (only equivalent fixtures), post from the opposite side (no arcade data), PAL, Everdrive.

## After b94 (lying wrestler at the arcade X + pin)
- **Kick-out/count vs arcade MAME:** only checked against the B012/B0A0 code; the arcade fixture without a referee does not count.
- **Pin approach:** historical 513/514 slide (arcade: 7E fixed at the final X, Z207). Flip of 513 by conversion convention (flip0), not measured by silhouette. Duggan's jump not measured.

## After b95 (running by arcade tick, background by DMA, rope crash)
- **Extend arcTick to the rest of the logic (noted, NOT authorised):** walking, run start (3 frames), rn 2 bounce (48 f track), braking, clothesline and falls (fs advances every 2 loops with `fsTick`) still go per MD frame; on PAL/NTSC or with lost frames their pace differs from the arcade.
- **Frames lost while running between ropes:** 40/580 in b95 (b94 55); it is not the streaming (posts already 0–3/580). Cause not investigated (unmeasured suspicion: CPU `ropeDraw` / sprite loading).
- **Not verified in b95:** rope crash in throws/clothesline (sub 1, port fixture: bounces W 627→659, D 906→874) and knockdown by hits next to the rope (soilNudge 875/893 reviewed in code only) against arcade MAME; lost frames on PAL; real hardware/Everdrive. Sound 0x29 of the 9F02 landing does not exist in the port (not added).
- **Right ring limit:** port `RING_XR` 917 vs arcade 920 (21E5A); only the new crash uses 920−e. Not touched.

## LOW — polish at the end

- **Cadence of the Knee Drop from the post — LOW PRIORITY, "polish at the end".** Arcade **8/18/10 refreshes** against b91 port logs **K11/19/7, P5/19/14**. These are samples of the loaded pose, not an atomic visual certification. b91 did NOT solve this point; it discarded the clock/render experiments. On NTSC/PAL the real time of 57.44485 Hz must be kept, without forcing counts identical at 60/50 Hz. Source `01_port_sgdk/actual/NOTAS_b91.md:6–12`, per-refresh CSV and labelled experiments. It does not block the priorities above.

- **Visible cadence of Duggan's Elbow Drop, floor and post — LOW PRIORITY, "polish at the end".** b92 already delivered. Physics/contact/damage/A2 verified; the visible cadence is still uneven: NTSC floor 10/17/12, post P 9/21/5, K 6/19/12 against the native 8/18/10 before conversion. Do not reopen the ROM or touch Warrior because of this note. Sources NOTAS_b92.md and pose92_refreshes.csv. It sits next to the pending Warrior Knee from the post.

## COMPLETED IN b92 TESTS
Stomp: zones 23/24, damage 1, impact 15A without refiltering, NTSC/PAL conversion. Elbow: physics/contact/A2/damage/miss and post P/K, NOT the visible cadence. Natural/outside/other-corner coverage pending.

## COMPLETED IN b93 TESTS
Lying opponent orientation: no mirroring lying→A2→wait in 16 cases; contacts = arcade (Duggan stomp/elbow/mirror/top/post P/K; Warrior head left/right, top, post K/P, outside). Clothesline trace identical to b92.

## COMPLETED IN b94 TESTS
Lying wrestler without lyoOf: pin zone over the visible torso, Knee/Elbow over the head; B sweep = arcade (W/D, both orientations); no jump lying→A2 or 114→115; Duggan's pin by the CB75 body zone; the covering wrestler at the arcade X/Y/Z and orientation.

## COMPLETED IN b95 TESTS
Running = arcade on NTSC and PAL (W 200.5/199.7–200.1, D 194.0/192.6–193.0 px/s; arcade 201.1/193.9). Slowdown next to the posts solved (20/14/18/19 → 3/2/1/0 lost frames out of 580; 0 background errors). Kick-out next to the rope = arcade at Xv 760/728/708/693/832 (crash 9E78→9CD0→9F02, no soilNudge jump).
