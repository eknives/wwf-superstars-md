# Duggan: Stomp and Elbow Drop — STUDY ONLY

6-11-2026, Europe/Madrid. No new ROM, no b92, b91 not modified. MAME 0.276, set `wwfsstar`; CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`. The CRC warning for the background chip `24j6-0.112` remains, not CPU/sprites.

## Inputs and zones

Nominal source: local GameFAQs, Duggan section, lines 245–253 of `study_kneedrop/GameFAQs_text.txt` (copy in the backup). P=Button 1, K=Button 2 (A/B in the port). New press, no mandatory direction. Human route `8F9E/904A → C706`, buffer `+116 & 3`, accumulated by `4066–40B6` over four refreshes. Common conditions `C79E–C8A8`: same plane `+19`, `abs(Ya−Yv)<24`; opponent lying in action B. `CB1A` covers other actions/exception 8/subD: not tested here.

Anchor H=`Xv−40` with the victim's orientation bit7=0; H=`Xv+40` with bit7=1 (`C83E–C85C`; André uses 56). X/Y/Z are 16.16 world coordinates at `+0C/+10/+14`, not screen. For a normal victim:

| Technique | Input/floor zone | Dispatch |
|---|---|---|
| Stomp | P next to the body: victim orientation 0, `H<Xa<H+48`; orientation 1, `H−48<Xa≤H`. Same Y ±23. | `CADE+3*4=CAEA → CB6C`; body row `CB75=05,06,06` for P/K/P+K. `FB6C → 1173A`. |
| Elbow Drop | K next to the head: orientation 0, `H−31≤Xa≤H`; orientation 1, `H<Xa≤H+31`. Same Y ±23. | Head row `CB72=04,11,04`; `FB9C → 10A5E`. |
| Post Elbow | P **or K** from action F, state `+B8=2`, opponent B; no small head zone. | `F35A → F636`, Duggan table `F6EF=2F,20,20`, choice by lying opponent; `FC14 → 10A5E`. |

The attacker's initial orientation does not block: `10A6C/10BB2` copies the opponent's. From the post, the preparation drawing and phase 1 are oriented by Vx (`10F90–10FAC`, `10D02–10D26`). Selection cells are NOT banks: Duggan=3, Warrior=0 (`6CD8`, `7FE2`).

Outside, by code: `CAFE+12=CB0A → CBEC`, head keeps `04,11,04`, body `05,05,05` (outside, K on the body does not ask for a pin). Not tested dynamically in this study. **Ropes:** `240B6` clears `+9E`; list `240F0` does contain 11 and 2F, but their entries `24102→24322` and `24106→24324` are RTS: do not impose a generic rope cancellation on these jumps. Not all ring limits were verified.

## 1. Stomp, not an "elbow"

`1173A`: table **118BC = (159,8),(15A,4)**. The first counter is already decremented on initialisation (`11750→1175C`): **159 lasts 7 ticks/14 refreshes**, not 16. On switching to step 4 (`1177A/11782/11786`) it hits; 15A has 4 ticks and one tick is kept on returning to action 0: **10 visible refreshes in RAM**, then pose 0. MAME: k25..38=159; k39..48=15A; action 0 from k47, pose 0 from k49.

X/Y/Z constant: case (744,300,187). No jump or velocity. **Contact only once on entering 15A**, `1179A`: checks plane and action B, **does not measure the X/Y distance again**. The zone was decided in C706. `1185A` can make the victim get up at random in certain modes/CPU (`118B6`), before that contact; it can then miss. That evasion was not tested separately.

Damage **1**, `117E0→117F4→161DA→16488`; the 3 at `117EE` is André, not Duggan. Victim action 8/subD, A2; `+BF` increments up to 4 (`117F8–11806`). If it is no longer B, `117B8` returns: no energy penalty for the attacker in this routine. There is a special branch for a victim in action 17 (pin), `1180E`, not tested. Attacker ends in action 0 (`1176E`), not the 1A get-up.

## 2. Elbow Drop, floor

It shares **10A5E** with Warrior's Knee, but **does NOT share offsets or final poses**. Duggan pose table **11372 = 112FA+3*40**:
- Normal: **61 → 62 → 1CB → 1CC → 1CC**.
- Variant `Ya+2<Yv`, `+5C=1` (`10B36–10B5C`): **61 → 62 → 1CD → 1CE → 1CE**.
- Durations: **61×8 /62×18 /1CB or 1CD×10 refreshes** (`10F54/10FB2`, `112F0=0,8,4,FFFF,0`, strict comparator `10D42`). Then 1CC/1CE variable until contact +12 recovery ticks (`10D58–10EA6`); on the floor tested **26 refreshes** in total, then **1A×16** (`A90E/AA00`, index 0). Tick=2 refreshes (`1508–1510`), MAME video 57.444852941 Hz; they are not 60 Hz frames.

Duggan physics `11180/11188 →111F0`: words **0,−64,0,0,500,50,2000,2000** (hex except −64 decimal). Against André, `11184/1118C →11200`: offset −80. Target Xv±64 normal; outside, the solver divides the offset by 2 (`15A52–15A5A`). Vz=0x500, g=0x50; velocities 8.8, coordinates 16.16. Common solver `156FA→159AC–15B3E`: divides with truncated word coordinates, |Vx|/|Vy|≤0x2000. Per flight tick `3DCE→3E20`: ΔX=2Vx/256, ΔY=2Vy/256, ΔZ=2Vz/256, Vz−=0xA0 (limit −0x800). It does not integrate during the preparation.

MAME, attacker (712,300,187), victim (760,300,187), orientation 0: **Vx=−120, Vy=0**, apex 232; contact **(697,299,187)**. Mirror (808,300): Vx=+120, contact **(823,299,187)**. Variant Ya 290: Vy 75; contact **(697;299,375;187)** and poses 1CD/1CE.

Window `10BF8–10C3C`: descending Vz<0, victim B, same plane, Zword≤floor+16. `10FCC` uses the victim rectangle `11084[id]`: normal (−48,+8), asymmetric widths 16/48. Victim orientation 0: `Xv−64 < Xhit ≤Xv`; orientation 1: `Xv < Xhit ≤Xv+64`; `Yv<Yhit≤Yv+16`. **Duggan point `110BC=110A4+3*8`: (Xa±8,Ya+4)**, X sign by attacker orientation; same point on the post (`110C0`). It is different from Warrior (Xa,Ya+4). It is not a generic |dx|≤48 box.

The impact sets step 4 and applies the damage on that same tick (`11062→10D58`). `10D9E–10DB0`: Zword=floor and Yword=Yv−1, **keeps fractions**. Duggan does not add Y+10 or auxiliary 7D: `10F04` only does it for Warrior; **auxiliary=0 in all these tests**. Damage **5**, `10DC0`; A2 reaction described below. After 12 ticks: action 5, removes auxiliaries (`10E8A–10EA0`), get-up 1A and action 0; no automatic pin.

## 3. Elbow Drop from the post

Sub **2F**, not 11 or Knee 2C. Same poses and **8/18/10 refreshes**, both P and K. Same Duggan physics record 111F0; `+34=1/2` according to height/side (`10B12–10B30`). `110E4` can limit Vx to ±0x200 if the horizontal distance to Xv±64 ≥96 and Vy to ±0x100 if |dy|≥80 inside/112 outside; not a fixed flight.

Native bottom-left post case (632,374,233), victim (760,300,187): **Vx 399, Vy −462**, apex 278; impact **(694,34375;299,8125;187,5)**. P and K give the same results. 1CC is seen for **34 refreshes** in total (10 before +24 from contact), 1A 16. **Damage 10**, `10DCC`, not 5. Table F6CE provides the initial post position. The other three corners were not tested.

## Shared reaction and miss

Victim: `10DB4/117BA` → action 8/subD → `99BE/9A48/A554`, **pose A2**, `27D2[8]→28EC`: Vx=Vy=0, Vz 0x200, g 0x40. MAME: relative heights **4,7,9,10,10,9,7,4,0**, A2 **18 refreshes**; then B/pose 17 and normal get-up according to energy/remaining counter (`A5DA–A610`, `AB1E`, `AF66`, `AA00`). The literal A20004 does not fix the duration at 4 ticks. Do not assign a new universal wait.

Elbow miss (floor or post), `10C4A–10CB2`: lands, action 8/sub 5, **1CF**, Xword−24 if orientation 0 /+24 if 1, keeps the fraction; **−2 to the human attacker**, 0 CPU (`10C62/10C6A`). Routine `9FCC`, Vz 0x300, g 0x40; 1CF→16→17→1A→0. MAME miss test: victim moved during the flight; attacker 100→98, victim 100; 1CF 20/16×8/17×44/1A×16 refreshes in that case. Floor waits depend on state/energy; do not turn that sample into a constant.

## Concrete differences against b91 (inspection, without rebuilding)

- **Stomp already uses the correct track**, despite the "elbow" comment: `gs69.h` 522/523 correspond to bank 3 poses 159/15A (earlier confirmation `b90/NOTAS_b90.md`, comparison `b69/tools69/match69.pkl`). Track 14/10 iterations, with rest poses before/after; `main.c:838` advances per iteration, **not by arcTick or a stable refresh**. The cadence of the MD ROM was not measured here.
- D zones `main.c:984–987`: uses `bodyX`, |dy|≤16, P≤40, B between PIN_ZONE and 100; not the head/body zones C706/CB6C or |dy|<24. P hits at `GS5_K=16`, one index BEFORE the first 523 at index 17; the arcade hits on entering 15A. Also the port filters |dx|≤48/|dy|≤16 again on impact; the arcade Stomp does not.
- D Elbow still uses `gs=11` (the **port's decimal state 11**, not a native subaction number; the arcade routine is **sub 0x11=decimal 17**: clarification of the ambiguous sentence in the energy study), **track of 83 iterations** (`gs69.h`), X interpolated towards `bodyX` with `gD*gs11X/7`, erasing the fraction; no 111F0 solver, no native displacement towards Xv±64, no variants 1CD/1CE. `gs11Z` exists in the header but is not consulted in main.c; old resources may incorporate a visual displacement: **no pixel audit of their composed poses is claimed here**.
- Generic contact at index 40 and a box centred on the body (`main.c:844–847`), not descending/Z≤floor+16 or D point ±8. Y is not repositioned to Yv−1 with fraction. Current damage 1/5 and miss −2 already correct (`hurt90`), but reaction `vjolt=10,vk=14,vlast=180`, **no physical A2 for these two Duggan attacks**. The A2/Knee branch is only connected to Warrior.
- **Duggan's post Elbow does not exist**: `main.c:906–915` authorises the jump only with `curF` (Warrior); therefore sub 2F, trajectory, damage 10 and its miss are missing for D. Changing the Knee's sprite id is not enough.

## Verification and files

**Verified in MAME:** P body→sub 5, K head→sub 11, mirror, variant, P and K post→sub 2F; poses and RAM holds above, positions/contacts, energy 100→99/95/90, A2 reaction, miss 100→98. Data per refresh: `arc_frames.csv`; summarised in `RESUMEN_RAM.json` and `poses_refrescos.csv`; extracted sources/values `TABLAS_DUGGAN.txt`. Script `arc_duggan.lua`, log `MAME.log`. Captures `arc_stomp_*`, `arc_elbow_*`, `arc_cornerP_*`; summary `RESUMEN_DUGGAN_SUELO.png`.

Boot with coins/start and selection; then fixtures of positions, bank 3 Duggan/bank 0 Warrior, energy 100 and lying opponent in RAM, **without forcing the attack subaction**. Real button inputs; for the post, action F/state 2 is prepared and the opponent's floor time is extended. PNG two refreshes after the logical state, not perfect pixel synchronisation. Not a test of all boundaries, corners, opponents, evasions or the outside; the b91 ROM was not run or changed. The energy→wait link depends on more flags: these samples do not certify it exhaustively.
