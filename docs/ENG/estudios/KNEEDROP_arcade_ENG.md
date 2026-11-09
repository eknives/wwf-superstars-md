# Ultimate Warrior's Knee Drop — STUDY ONLY

**b89 has not been changed and no ROM has been built.** Its ROM still has MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`.

## 1. How it is done

- **Floor: press Kick, arcade button 2, by the head of the lying opponent; no direction required.** Supplied GameFAQs, lines 167–171 of `GameFAQs_text.txt`: "Knee Drop = K (By head,2)". In b89 it corresponds to **B**. Punch+Kick is not that input: Warrior head row `04,0C,04` for P/K/P+K (`0xCB3C+6`).
- Human route: `0x8F9E` / outside `0x904A` → `0xC706` → action `0x0C`, subaction `0x0C` → table `0xFB58+0x30` → **`0x10A5E`**. New inputs are at `+0x114`; `0x4066–0x40B6` accumulates them in `+0x116`, cleared every four refreshes. `0xC70A` consumes that small buffer, not an auto-repeating held button.
- Normal case: opponent in action **B**, same plane **byte `+0x19`** (0 inside, 1 outside), `abs(Ya−Yv)<24`. **The Z height is not compared to choose the zone.** Sources: `0xC79E–0xC7EE`, table `0xCB1A`. The selector also classifies `0x1E` as floor and admits the exception action 8/sub D (`0xC82A–0xC836`); those exceptions were not tested with input in MAME. The impact, on the other hand, requires B.
- Coordinates: **X=`+0x0C`, Y=`+0x10`, Z/height=`+0x14`**, 16.16 format. They are not screen coordinates or the visual centre of the sprite. Head anchor: `Xv−40` if bit7 of the opponent's `+0xA`=0; `Xv+40` if =1 (`0xC83E–0xC85C`). For a normal opponent, not André:

| Opponent orientation | Attacker X that selects Knee Drop | Y |
|---|---|---|
| bit7=0 | `Xv−71 … Xv−40`, both included | `Yv−23 … Yv+23` |
| bit7=1 | `Xv+41 … Xv+71`, both included | same |

Derivation: front side of the anchor and distance **strictly <32**, `0xC860–0xC88E`. Behind it another row is selected: for example K on the torso → sub 6, pin, not Knee Drop. The attacker's initial orientation is not a requirement: `0x10A6C`, `0x10BB2–0x10BD8` copy/orient; Warrior ends with bit7 according to the sign of Vx.

**Ropes/outside:** there is no generic "near the ropes" veto in this selection. The normal walking limits apply (`0x21E5A` / `0x21ED0`). Also, `0x240B6` clears `+0x9E` and its list **`0x240F0` does not contain 0C or 2C**: the generic cancellation `0xF9B0` must not be attributed to those jumps. Impacts tested with attacker X=640 and X=896, Y=300, next to both sides. **It also works outside**, with both on plane 1; the outside table `0xCBBC+7` keeps sub 0C. MAME confirmed it with floor Z=128 and damage 5.

**From the corner post:** **P or K**, with the opponent lying (GameFAQs 176–177). Action `0x0F`/post state 2 → `0xF35A`, reading of the `+0x114` edge at `0xF38A/0xF3B6/0xF3EA/0xF41E` → `0xF636`; Warrior table `0xF6E6=2C,20,2C` → **sub 2C**, also `0x10A5E`. Button 1 and Button 2 confirmed separately from the bottom-left corner. It does not require standing in the small head zone of the floor attack.

## 2. Poses and real time

A wrestler tick is **two refreshes**, checked at `0x1508–0x1510`, loop `0x155A–0x157C` and in the MAME log. This driver uses **57.444852941 Hz**: 17.408 ms/refresh, **34.816 ms/tick**, not exactly 60 Hz (`wwfsstar.cpp:632`; its video totals are marked as estimated).

Warrior pose table **`0x112FA`**:
- Normal: **61 → 62 → 7A → 7B → 7B**.
- Variant `Ya+2<Yv`, flag `+0x5C=1`: **61 → 62 → 76 → 77 → 77** (`0x10B36–0x10B5C`).
- The corner post block uses the same two sequences.

| Phase | Pose | Real duration | Source |
|---|---|---|---|
| Prepare | 61 | **4 ticks = 8 refreshes** | **`0x10F54`, hardcoded counter `0x10FB2–0x10FC6`** |
| Rise | 62 | **9 ticks = 18 refreshes** | `0x10D2C–0x10D4C`, `0x112F0[1]=8`; advances when counter >8 |
| Descend | 7A / 76 | **5 ticks = 10 refreshes** | same comparator, table=4 |
| Seek contact | 7B / 77 | until collision/floor; variable | `0x10BF2–0x10CBC`, table=FFFF |
| After impact | 7B / 77 | counter up to **12 ticks** | `0x10D58–0x10EA6` |
| Get up | 1A | normally **8 ticks / 16 refreshes** | action 5, `0xA90E`, `0xAA00[0]=8` |

**The first duration is NOT 1 tick even though `0x112F0[0]=0`: that phase jumps to `0x10F54`, which waits four.** The note/comment inherited from b83 in b89 is incorrect.

Measured in RAM every refresh, normal floor case: **61×8, 62×18, 7A×10, 7B×26, 1A×16**. The 26 of 7B include 2 before the impact and 24 from it: on switching to action 5 it keeps that pose one tick before loading 1A. Auxiliary 7D is active for **22** refreshes, not the full 24 (`0x10E9A`). In the tested corner, the flight extends 7B to **34** refreshes. They are not universal durations for any trajectory.

## 3. Trajectory and impact

**Warrior parameters:** pointers `0x11150` → record **`0x111D0`** (normal), eight words:
`0, −32, 0, 0, 0x500, 0x50, 0x2000, 0x2000`.
`0x156FA`, `0x108B0`, `0x159AC–0x15B3E` solve the trajectory. Initial Vz **0x500**, gravity **0x50**, velocities 8.8. Normal target: `(Xv±32,Yv)`; outside, the −32 offset becomes **−16** before the mirror (`0x15A52–0x15A5A`). The last values limit |Vx|/|Vy|. The solver simulates simple steps and divides the displacement by their number, truncating towards zero: **34 steps** from floor to floor in these cases.

During phase 0 there is no integration. Per flight tick, **`0x3DCE→0x3E20`**:
`X += 2*Vx/256; Y += 2*Vy/256; Z += 2*Vz/256; Vz -= 0xA0`, descending limit −0x800. There is no universal fixed displacement in X/Y.

MAME example: attacker `(712,300,187)`, opponent `(760,300,187)`, bit7=0: **Vx=0x78, Vy=0**, maximum rise **Z=232**; contact on the 16th movement tick, `(727,309,187)` after adjustment. Mirror: starts X=808, Vx=−0x78 and contacts X=793. Variant initial Y=290: Vy=0x4B, ends Y=**299.375**, not 309.

Corner post tested: native origin **`(632,374,233)`** (`0xF280`, table `0xF6CE`), **Vx=599, Vy=−462**, solver 41 steps; contact on the 20th movement tick, `(725,59375;309,8125;187,5)`. `0x10B5E–0x10B6C`/`0x110E4` can replace Vx with ±0x200 if the horizontal distance to `Xv±64` is ≥96, and Vy with ±0x100 if |dy|≥80 inside /112 outside. A fixed floor flight must not be reused for any corner.

**Impact window:** after integrating, Vz<0, opponent action B, same `+0x19`, integer Z ≤floor+16 (`0x10BF8–0x10C3C`). `0x10FCC` compares the Warrior point **`(Xa,Ya+4)`**, table `0x110A4`, with:
- opponent bit7=0: **`Xv−64 < Xa ≤ Xv`**;
- opponent bit7=1: **`Xv < Xa ≤ Xv+64`**;
- in both: **`Yv < Ya+4 ≤ Yv+16`**.

Sources: rectangle `0x11084` = (−48,+8), construction/comparisons `0x10FD6–0x11060`. Phase 4 is set and its impact runs on that same tick (`0x11062`, `0x10CBC`).

**Placement/layers:** `0x10D9E–0x10DB0` writes the integer words Z=floor and Y=Yv−1, **keeping fractions**. In the normal variant Warrior adds 10 to Y and creates **7D**, attacker's bank, orientation XOR80, X=attacker∓4, Y−10, Z+10 (`0x10F04–0x10F1A`, `0x1152A`). **In variant 1 it does not add those 10 or create 7D.**

## 4. Damage, reaction and end

- `0x10DB4–0x10DD2`: victim **action 8/sub D**, energy damage **5 on the floor /10 from the post**. `0x161C8→0x16488` subtracts it with saturation. Confirmed **100→95** and **100→90**. The "2/3" of GameFAQs is its author's scale; its equivalence with those internal values has not been shown.
- Real reaction: `0x99BE→0x9A48→0xA554`, **pose A2 from the victim's bank**, not a generic fall. `0x27D2[8]→0x28EC`: **Vx=0,Vy=0,Vz=0x200,g=0x40**. In the test the relative height goes through **4,7,9,10,10,9,7,4,0**: nine ticks. A2 lasts **18 refreshes**. The literal `A20004` at `0xA566` does NOT mean that this reaction lasts four ticks: the exit depends on the landing (`0xA5DA–0xA610`).
- On landing: action B with bit1 and pose 17 on its next update; then its normal get-up (`0xAB1E`). For a human that bit keeps the remaining floor counter `+0x38` (`0xAB7A–0xABBC`); do not invent a new fixed wait. For the CPU there is a calculation by energy/table `0xAF66`. Warrior ends in action 5/1A and returns to 0; **it does not chain an automatic pin**. `0xAA00` contains 8,12,16,32,20,24,28,40 ticks according to `+0xF0&7`; the tests used index 0.
- **Miss:** `0x10C4A–0x10CB2`: action 8/sub 5, pose **1CF**, moves X **−24** if bit7=0 /+24 if =1, opposite drawing flip; loses **2 energy if human**. Then `0x9FCC` (`0x27D2[0x19]`: Vz=0x300,g=0x40), poses **1CF→16→17→1A→0**. Verified by moving the opponent during the flight: attacker's energy **100→98**, not the opponent's. The later floor waits depend on the state.

## 5. Concrete differences against b89

Source: `/workspace/b89/src/main.c` and `native81.h`, plus running **the existing ROM without rebuilding**.

1. **Preparation too short:** lines 647–648 wait 1 tick, arcade 4. Measured by refreshes: b89 normal **4/22/10/2** for 61/62/7A/7B before contact; arcade **8/18/10/2**. b89 variant: **3/21/11/3**. The contact at +38 refreshes matches by compensation in these fixtures, not because the distribution is correct.
2. **Incorrect/unstable clock:** lines 638–640 count every two **iterations**, not `arcTick`. The logs show iterations that do not advance on every refresh, hence lengthened/variable poses. It has not been profiled to attribute the cost to CPU or DMA. PAL is not tested either.
3. **Variant 1 misplaced and with an undue layer:** lines 663–685 always Yv+9 and combined pose 788=77+7D; arcade Yv−1 keeping the fraction, **without 7D**. Measured: b89 Y=309 against MAME 299.375.
4. **Reaction/damage not reproduced:** line 685 only `vjolt=10,vk=14,vlast=180` and effect; it does not subtract the 5 or run A2 with physics. In b89 the victim stayed at Z=187 and generic pose 752; in the arcade it does the small A2 arc. `vlast=180` is a timer of the hit accumulator, **not** the arcade fall duration.
5. **End/layers not identical:** the combined pose keeps 7D until loading 1A; the arcade removes it one tick earlier. b89 recovery observed **15 refreshes**, arcade **16**; immediate exit at the eighth counter at line 661 versus the native dispatch that keeps the pose.
6. **Outside and ropes:** lines 585–594/898 veto the attack outside; the arcade allows it. Lines 669–673 add a rope crash during the flight that is not justified for sub 0C by `0x240B6` (list without 0C). Crossing all rope geometries was not tested.
7. **Simplified selector:** `lyingNow` requires a specific phase of the generic knockdown; it does not represent the action table `0xCB1A`, its exceptions, or the four-refresh press buffer.
8. **The corner post is not connected to this technique:** the `climb` branch, lines 843–856, discards `pendBtn`; it does not implement the P/K→sub 2C input or the post flight/damage.
9. **Incomplete miss:** lines 689–692 do not apply the −2 energy and erase the X fraction. The normal left/right orientation must not be declared incorrect just because of `p1face=!vface`: that is another port convention; no audit of each tile/flip has been done here.

## 6. Verification and files

**Verified in MAME:** real Button 2 input from lying fixtures; both directions; variants 0/1; X limit −71 valid/−72 not, |dy| 23 valid/24 not; torso→pin; near both sides; outside; A2 reaction and damage 5; miss/−2; Button 1 and 2 from a corner, same sequence and damage 10. **b89 compared** in two fixtures with B: durations, variant placement and absence of A2 physics.

It was started with coins/start and normal selection of Warrior/Duggan. **Positions/knockdowns/energy were prepared in RAM, not a full natural match**; the Knee Drop subaction was not forced. In the miss test the opponent was moved; in the corner tests its floor counter was extended so that it would not get up earlier. The pose counters come from RAM every refresh, not a certification of every video pixel. The PNGs are taken two refreshes after the observed change to avoid capturing the previous bitmap of the drawing pipeline.

- **Visual summary:** `RESUMEN_KNEEDROP.png`.
- MAME, normal sequence: `arc_headL_01_preparacion.png`, `arc_headL_02_salto.png`, `arc_headL_03_vuelo.png`, `arc_headL_04_impacto.png`, `arc_headL_05_reaccion_apice.png`, `arc_headL_06_recuperacion.png`.
- Mirror/variant/corner: `arc_headR_04_impacto.png`, `arc_aboveL_04_impacto.png`, `arc_cornerK_04_impacto.png`.
- b89 intact: `md89_headL_impacto.png`, `md89_aboveL_impacto.png`.
- Data/reproduction: `arc_frames.csv`, `arc_corner_frames.csv`, `md89_frames.csv`, their `.lua` scripts, `AUDITORIA.txt`, `audit_knee.py`, `ROM_tables.txt` and the text extracted from the MHT.

**Limits:** no hardware/PAL, not all corners/opponents/exceptional states, no tile-by-tile graphics audit. MAME warns of a different CRC in **24j6-0.112, background tiles**, not CPU/sprites; the CPU rebuilt from the ZIP is identical to `analisis/tools/prog.bin` (MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`). Physical board frequency not measured.
