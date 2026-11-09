# b90 — internal energy + Knee Drop

ROM: `/workspace/b90/wwf_b90.bin` — MD5 **24759dec91fa996dc6e7a2f227e30f45**.
b89 base copied; its files still match `b89_manifest90.json`. Local SGDK build with the requested command. **I do not present the Knee Drop as 100 % identical: there are two verified pending differences below.**

## 1. Energy — verified

- Two humans, initial **48** (`7EE6→7F76`, table `7FEC`); `energy90[]` independent of `vdmg/vlast`, no HUD, regeneration or KO at zero. Saturated subtraction (`16488–1649A`). `fighterInit` restores both to 48 on match restart.
- MAME Genesis, final binary: **20 RAM fixtures** with real inputs after preparing the state. Both attackers: punch **48→47**, kick **→44**, early clothesline **→44**/late **→46**, stomp **→47**, drop **→43**; miss **48→46 to the attacker**. Zero stays zero without ending the match; **1→0** saturates. The pin count/ring-out branches restart **48/48**, keeping selection phase 4. The final count phase was forced; a full count was not played.
- Evidence: `shots90/md90_energy_frames.csv`, `md90_energy.log`, `validation90.json`.

## 2. Damage of existing attacks — verified in those contacts

Punch W/D: `18811/187F5=1`; kick `188AB/188C7=4`; clothesline `1890D=4`, `18929=2`; stomp `117E0=1`; floor/post drops `10DC0=5`, `10DCC=10`; human miss `10C6A=2`. Duggan's `gs5` uses MD522/523 = bank 3 poses **159/15A**, compared with `b69/tools69/match69.pkl`: stomp 1 is applied, not an invented "elbow" damage.

Kick incorporates +2 from `1642B` for running/whip when the contact allows it; the b89 collision filter normally excludes those states, **it was not extended and that bonus is not verified on MD**. The chained b89 Clothesline follows the FFFE exception (`162BC–162DA`), with no bonus or duplication. F9.0 has no complete equivalent; it was not invented. Holds/whip/inner bounce still have no damage of their own. Missing moves were not added, nor the special outside crash of `2209C`, whose condition/anti-repeat does not exist in full in b89. Pin/kickout and pick-ups unrelated to the Knee were not changed.

## 3. Warrior Knee Drop — partial verification

- Entry `C706/C79E–C88E`; post P **or** K `F35A/F636/F6E6`, sub2C→`10A5E`. Wind-up `10F54/10FB2`: **4 ticks**; `112F0/112FA`: **9/5 ticks** of flight. Arcade `1508–1510`: tick=2 refreshes at 57.44485 Hz → **61×8 / 62×18 / 7A×10**. `arcTick` is used, not loop parity. Existing clock: NTSC 3125/6528, PAL 3125/5440.
- Solver `159AC–15B3E`: Vz500, g50, target Xv±32 (±16 outside), velocities capped at 2000; division by integer word coordinates `15A6C/15AD8`. Post keeps initial height and rules `10B5E/110E4`. Asymmetric impact `10FCC/11084/110A4`, descent and Z≤floor+16. Variant `10B36–10B5C`: **76/77**, Yv−1 with the fraction preserved, without 7D. Normal Yv+9 and auxiliary hands; withdrawal `10E9A`. The false generic crash was removed: `240F0` does not enumerate sub0C/2C.
- Reaction `A554`, table `27D2[8]→28EC`: A2, Vz200/g40; relative heights **4,7,9,10,10,9,7,4,0**. Floor/getup 17/1A; table AF66 for the human wait of this reaction. Only six poses A2/17/1A from banks 3/0 (`6CD8`) are added, without overwriting previous graphics. Flip of the Knee and A2 compared visually; native orientation `10BB2`. Miss `9FCC`, vz300/g40 and −2.
- Against arcade MAME: **88 trajectory states by phase/timer match exactly** (X/Y/Z). Contacts: floor left **(727,309,187)**; right **(793,309,187)**; variant **(727;299,375;187)**; post P/K **(725,59375;309,8125;187,5)**. Damage **5/10**, nine-tick A2 curve and variant without 7D checked. Fractions are compared in CSV, not by pixels.
- PAL tested on the floor: visible holds **7/16/9** refreshes; NTSC floor **8–9/19/10–11**. These are real-time conversions; 8/18/10 are not forced at 60 Hz.

### Pending issues found, not hidden

1. **Post: irregular visible cadence**, although trajectory/logical timers match. In the final measurement K: **9/18/8**, P: **10/19/8** refreshes for 61/62/7A; 7A should be around 10–11 NTSC. Irregularity observed during camera movement; **there is no CPU/DMA profile that allows the cause to be definitively attributed**. Neither the clock nor the global scroll was changed so as not to affect other moves.
2. **Outside connects, A2 and damage 5 work, but position NOT identical**. Initial fixture W510/R558: b89 limits W to 512 and keeps R558; arcade moves R to 546 (`AB1E→ACA4/21ED0`). MD contact **(540,125;309;128)** versus arcade **(528,75;309;128)**; Vx225 vs 150. The general outside limits of b89 were not altered. The fixture with R546/W510 from the general CSV does not select the Knee; the valid MD outside test is in **`md_ext_knee_frames.csv`**, arcade reference in **`arc_frames.csv`, outside case**. The isolated trial `arc_outside_frames.csv` did not execute sub0C and **is not used as validation**.
3. The fixtures prepare RAM: they do not demonstrate all natural gameplay cases, four corners, fractional combinations, remaining time on the floor until getting up, nor Everdrive. The victim's remaining wait is not compared byte by byte: the arcade fixture initially keeps 200 ticks and MD uses AF66. The MAME set warns of a different CRC on `24j6-0.112` (background); CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`.

## Captures and preservation

`shots90/comparativa90_{suelo,variante,poste,exterior}_{vuelo,impacto,reaccion}.png` (12 PNGs). They are comparable phases, **not an exact per-refresh synchronisation**. Originals `arc_*.png`, `md90_*.png`, `md_ext_*.png` and PAL; numbers in `trajectory90_compare.csv`, `pose90_refreshes.csv`, `validation90.json`. Reproducible: `tools/validate90.py`, test Lua and `source90.diff`.

Audit: b89 intact; original resources preserved as an exact prefix. Only `spr_tab.bin` (+756 bytes) and `spr_tiles.bin` (+6880) grow, with lengths regenerated in `res.h`. Corner posts, ring logo, Hogan, HUD, AI and other timings/animations intact. **No deliberate change outside the scope**; the pending differences are delivered explicitly, not assumed resolved.
