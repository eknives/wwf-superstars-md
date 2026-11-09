# WWF Superstars energy: feasibility for b89

Study only, 6-11-2026 (Europe/Madrid). **b89 has not been modified, no ROM built and no b90 created.**

## Conclusion before implementing

**Yes: independent energy can be added for Duggan and Warrior and subtracted at the already existing contacts.** Drawing a bar or reusing `vdmg` is not enough: the latter is a temporary knockdown accumulator that b89 clears when `vlast` expires (`main.c:1357`), not the arcade energy. Full fidelity has pending parts: identity/zones of Duggan's floor tracks, human/CPU mode, clothesline variants and energy-dependent pin/getting up.

The uncontrolled opponent in b89 **has no AI** (inventory, line 96). It must not be considered a CPU simply because it is not `ctl`: the arcade explicitly distinguishes that role and changes punch/kick damage. That data distinction can be implemented without changing AI, but the mode has to be defined.

## Sources, units and method

- Big-endian CPU ROM `analisis/tools/prog.bin`, MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; checked against the two CPU chips of the local ZIP. Addresses in this document: **arcade 68000 addresses**, except the RAM and port lines expressly indicated.
- Disassembly `analisis/arc.dis`, tables read directly from the binary and aligned disassembly of the routines. The b89 inventory keeps old references to b83: checked against the current `b89/src/main.c`. The FAQ is used for names/inputs, **it does not turn its "1 after 3 / after 2" into exact RAM points**.
- MAME `wwfsstar`, local ROM `/workspace/wwf/mame/roms/wwfsstar.zip`. Real coins/START/selection; then RAM fixtures to isolate actions, initial energy, positions and, where appropriate, prevent evasion/AI until contact. The native routine runs: CPU code was not patched. **They are not all matches played from start to finish nor verifications of the inputs of every hold.** Scripts `arc_energy*.lua`, per-refresh CSV and logs kept.
- Arcade CPU/video: 57.444852941 refreshes/s; actor logic every **2 refreshes**, `0x1508–0x1510`. Tick = 34.816 ms. Energy points are not scaled by PAL/NTSC.
- MAME warns of a different CRC for `24j6-0.112`: **background** chip, not CPU/sprite code. Warning kept; the set has not been fixed or replaced.

## Representation and common rules

Actor: energy **word `+0x3C`**, pending damage **word `+0x3E`**; `+0x2A` byte bit 3 = CPU; `+0x2B` id (Warrior 0, Duggan 3). Main actors RAM `0x1C0100` and `0x1C0334`.

Subtraction at **`0x16488`**: `0x16492` subtracts `+3E`, `0x16496–0x16498` saturates at **0** on borrow; `0x1649A` writes `+3C`. It does not contain a universal maximum of 48. Wrappers for other victim references: `0x161C8/161DA/161EC/161FE`.

Hits with a box: `0x1672C` looks up `0x1761E[pose]` and then `[id]`; header byte **+1** is the damage. `0x1697E–0x16984` copies it to `+3E`.

1. **CPU victim and attacker sub 0/1 (punch/kick): base damage is forced to 0**, `0x1698A–0x169A2`. Do not confuse "loses no energy" with "is not hit": there is contact, reaction and combo/dizziness accumulator.
2. In the common path `0x16304–0x16328`, if the victim was in action **1, 0x15 or 0x16** (running/automatic paths, **not stun**), `0x1638E–0x163C6` adds `0x1642A[sub] & 0x7F`: punch +0, kick +2, clothesline +1.
3. In that same path, the attacker's flag **`+F9.0`** doubles the result, `0x16418–0x16420`. Activation `0x1CCE8–0x1CD28`, dizziness threshold `+F6` at `0x1CD48`; duration `0x1CD6C`, switch-off `0x1CD50`. There is no complete equivalent in b89.
4. **Important exception**: a victim with pending reaction `+40=0xFFFE` (clothesline link/grab) goes through `0x162BC–0x162DA` directly to the subtraction `0x16328`; **it skips bonus and doubling**. Do not apply rules 2–3 indiscriminately to all hits. The direct stomp/drop subtractions do not go through `0x1638E` either.
5. `+48` combo / `+46` window and `+F6` dizziness are different from energy: `0x16D4C–0x16D92`, table `0x17590`. Do not add that counter to the bar.

## Damage per move and possibility of hooking it now

H/C = **human/CPU victim**, except the miss column, which distinguishes the attacker. Values in internal points, not HUD segments. W=Warrior, D=Duggan.

| Existing or partial attack | Confirmed arcade damage and address | Add subtraction in b89? |
|---|---|---|
| W punch | **1 H / 0 C per hit**, not 1/2/3 by combo number. Active poses 0x152/0x155: header 0x18810, byte **0x18811=1**; FD70/FD7C. | **Yes**, contact `main.c:799`; one subtraction per hit, separate from the knockdown. |
| D punch | **1 H / 0 C per hit**; active poses 0x150/0x153, byte **0x187F5=1**. | **Yes for energy** at the same contact; animation not identical, see below. |
| W/D kick | **4 H / 0 C**. Pose 0x158; bytes **0x188AB=4 (W)** / **0x188C7=4 (D)**; sequence FF3A. Against a victim in action 1/15/16: **6 H / 2 C**, bonus **0x1642B=2**. | **Yes**, `main.c:816`; identify running/whip, do not add 2 just for being hurt. |
| W/D clothesline | Contact pose **0x1D1: 4**, byte **0x1890D**; contact **0x1DA: 2**, byte **0x18929**. Both victims H/C. Sequence 12E7A/1302E. Common path: +1 against a runner and ×2 with F9.0; **linked path FFFE: without both**. | **Yes** for 4/2: `clStep87`, line 729, already distinguishes those values for `vdmg`. Full equality of variants **partial**: not all links/reactions are represented. |
| W stomp | **1 H/C**, write **0x117E0**, call `0x117F4→161DA`; routine 1173A/1179A. The 3 at 117EE is for id 7, not W/D. | **Yes**, `warriorGroundStep`, `gs=13`, contact at 638–698. |
| D "Stomp/elbow" `gs=5` | Native stomp sub 5 is **1 H/C** (117E0). **The graphic equivalence of the MD track `gs5P` with that stomp is not shown here**: the inventory and the comment call it an elbow. | **Partial**: there is a contact at 782–784, but do not label it as an exact arcade stomp or pick another elbow's damage because of the alias. |
| W Knee Drop `gs=12`, sub 0x0C | **5 H/C from the floor**, **10 H/C from the post**: **0x10DC0=5**, if +34 active **0x10DCC=10**; sub 0x0C/0x2C in FB58 → 10A5E. | **Yes for the subtraction** in `warriorGroundStep`; movement/zone/animation still partial according to the Knee Drop study. |
| D Elbow/jump `gs=11`, sub 0x11 | Sub **0x11 of FB58 also points to 0x10A5E**: **5 floor / 10 post H/C**, same writes. | **Partial** for full equivalence: contact at 782–784 allows subtracting 5, but the port's track/input/zone are generic, not a fully verified arcade elbow. |
| Drop miss W 0x0C / D 0x11 | **2 to the human attacker; 0 to the CPU attacker**, **0x10C6A** and earlier CPU check. Only if that jump misses, not for any fall. | **Partial**: impact/miss must be distinguished and applied at the native landing event; currently no energy or real penalty. |
| W/D grapple / reverse | **No subtraction of its own** in B1D0/B48C/B670. | **Yes: 0**. Do not charge energy for each press or for deciding the winner. |
| `trStart` called Irish Whip W/D | Tracks S_1E/W1E: sub **0x1E → 0x14CFC**, counter-hold that releases the victim into action 0x15; **no subtraction of its own**. | **Yes: 0** on release, running and normal bounce. Do not assign Body Slam's 8 to this track. |
| Running, inner rope / attacker's fall on the whip return | **No energy damage by itself**. Inner limit **0x21E5A**, bounce 960A/96AA, hold crash F94C/F9B0; action 8 sub 1 does not receive the 5 from 2209C. | **Yes: 0**, including `trStep:1021–1023` and `fsStart`. |
| Crashing into the post/ring limit from outside W/D | **5 to whoever crashes H/C**, **0x2209C→220A2**. **Outer** limit **21ED0→21FA8→22040**, first contact by bitmask 22016; list **220BE = 08,01,14,15,16,FF**. In action 8 it only subtracts if the reaction sub is **0x0A** (2208C–2209A). | **Partial**: the port has limits/exits/reactions, but the outside condition and anti-repetition must be reproduced. **Do not subtract 5 on every inner bounce.** |
| Pin/kick-out, climbing/descending the post, entering/leaving W/D | No attack subtraction of its own in the studied routes B012/AB1E/AD12/ADEA/AE7E and EC12. The pin uses the energy that was left. | **Yes: 0** damage; adapting pin/getup to energy is another integration, currently not arcade. |

**Important differences from the inventory:**
- Human Duggan does not dispatch the native combo through FC84: **FC4E→FC70→FDA0**, sequence **FE88** (hits 150/150/153 if chained). W uses FC84/FD70/FD7C. b89 uses FD70/FD7C for both: the unit damage can be added without touching that, but it does not allow claiming that D's whole sequence is exact. Nothing was changed.
- The alias `gs=11` is decimal 17 = **sub 0x11**, not sub 0x0B. The latter is 132C8 (bulldog), **not** the D track dealt with here.
- **Gorilla Press, Body Slam, Headlock, Bulldog, Back Suplex, Atomic Drop and attacks from the post are not implemented** (inventory and code); there are no corresponding contacts to add damage to yet. "Warrior finisher" here may refer to the partial Knee Drop; **there is no Gorilla Press hidden in `trStart`**.
- Another elbow/aerial finisher **125F0** has damage **12** at 126B8, **8** if sub 0x35 at 126C6 and human miss **4** at 1274E. **Do not confuse it with gs11/10A5E**. Values from code only; that variant was not tested and is not an attack available in b89.
- Special mutual crash `+40=FFFC` can subtract **1** through **17202→1720A** (selector 17136/1715C). It is not automatic "grapple damage"; no equivalent branch has been identified in `grStep`. **Partial/do not add to all holds.**

## Initial energy, maximum, refill

- **Human W and D: 48**. Table **7FEC**, eight words 48; initialisation **7EE6→7F76**. HUD **7CF2–7D14** shows `min(12, ceil(E/4))`. One internal point is not one visible cell.
- CPU: table **8190**, row `1C0028 & 0xFF`, column `(word +2A)&7`; initialisation **7FFC/8066/8110**, difficulty bonus **80A6–80B4**: **8×(1C004A & 3)**. First row W=45, D=43; internal difficulty 1 → **53/51**. Not all opponents start at 48.
- CPU bases by progression index 0..9, W/D: **45/43, 60/58, 68/66, 72/70, 40/40, 76/74, 76/74, 76/74, 86/86, 64/68**. Initial maximum W/D in these ten rows and four difficulties: **110**, not a global cap of the subtractor. Full data in `energia_inicial.csv`.
- **No passive regeneration during the match was found** among the +3C writes reviewed. Short idle sample with no change; it is not presented as a dynamic test of all possible states.
- Between matches, **2060→20C2**: with a non-negative +40 counter, consumes 4 from the counter; if DIP **180002 bit7=0**, adds 4 to energy (20D6); **20DC–20E4** limits to 48 even when it does not add. **20EC** restores 48 to members of the eliminated team for the later flow. It is not regeneration during a jump/fall.
- Power Up with credit/START in the allowed modes: **6F64**, **6FEE/701E**, writes **7000/7014/7030/7044**: **restores to table 7FEC (48), does not add 48 on top**. Refill and Power Up: checked by code, not run as an energy-purchase test.

## Low or zero energy: not an automatic KO

- Quarter index **1CE9C**: divides by `max(1, initial_reference >> 2)`, limits 0..3. Human: bands **0–11 / 12–23 / 24–35 / 36+**. CPU uses base 8190 without adding the difficulty bonus in this calculation. `1CEF4` computes thirds 0..2 for other uses.
- Lying time **AB1E→AB82–ABAA**, table **AF66 bytes**: **112/82/54/22 ticks** from lower to higher energy = **224/164/108/44 refreshes** of full logic. CPU can halve it with F9.0 or if **1CD80** returns CS. Flag +33.0 adds 32 ticks (ABB6). Do not convert these times into "60 Hz frames" without keeping real time.
- Bringing forward the human's exit from the floor **AD12**: new inputs `+116 != 0` increment +34; thresholds **AF6A bytes = 24/10/6/3**, exit to action 0x19. At E=0 it can still get up; it takes longer. Do not read that table as words.
- Human pin **ADEA**: AF72=6/6/6/6 controls the window relative to the referee; **AE24–AE40** adds to +34 each tick with `+114 != 0` and compares against **48−E**. **AE36 with E=0 prevents this exit by input**. There are also referee phase conditions leading to AE42: it is not simply a single press counter.
- CPU pin **AE7E/AF26**: indices **0/1/2/3/4/5/6** for **E≥54 / ≥48 / ≥36 / ≥25 / ≥14 / >0 / =0**. Each level changes the escape phase/time; index 6 does not exit through that routine (**AE8E–AE92**). **129A4** does not ask for the partner's rescue either when energy=0.
- **0 does not end the match by itself**: it requires a pin/count or the corresponding victory condition. MAME: victim E=0 stays standing and, when lying, returns to action 0 keeping **E=0**. In b89 the "first pin" pin/kick-out is deterministic, it does not read energy (`pinAdvance` 1040+); adding the bar does not fix this automatically.

## MAME verification — valid results and limits

Primary evidence: `mame_energy2..5_frames.csv` (RAM per refresh), logs of the same name; summary `mame_resumen.csv`. They are internal before/after readings, not bar estimates by pixels. Letters W/D in case names indicate the attacker; both were tested except where specified.

| Test | Observed result |
|---|---|
| VS start, W and D human | **48/48**, line NATURAL_START_ENERGY in logs. |
| Natural 1P start before hits | `natural_cpu_final.log`: human W **48**, CPU ids 4 and 2 **55/55** = 47+8, progression 0/difficulty 1. CPU formula confirmed with those columns; all W/D rows only by table. |
| W/D punch to human / CPU | **48→47 / 48→48**, with pending hit/reaction even on the CPU (energy2). FD7C W pose 155 also **48→47**. A full three-hit combo against each type was not measured. |
| W/D kick to human / CPU | **48→44 / 48→48**, contacts recorded (energy2). |
| Kick to a runner action 15 | **48→42 human / 48→46 CPU**, both attackers (energy2). |
| Clothesline pose 1D1 | **48→44 human and CPU**, both attackers (energy4). |
| Clothesline pose 1DA | **48→46**, linked human (energy2/3) and CPU on late contact (energy3), both attackers. The CPU link is not considered verified with that fixture. Do not confuse a test's early name with the real pose: the CSV shows which one touched. |
| Active clothesline 1D1 against a runner | **48→43**, both (energy5; the fixture starts in the active phase to isolate this case). |
| F9.0, punch / early clothesline / late linked | Punch **48→46** (energy3), 1D1 **48→40** (energy4), linked 1DA **48→46**, **does not double** (energy5). Both attackers. |
| Native stomp sub 5, W/D, H/C | **48→47**, energy2. Native D verified, not identity of the MD gs5 track. |
| Drop W 0C / D 11, floor, H/C | **48→43**, energy2; CPU victim immobilised to prevent it dodging before contact. |
| Drop from the post W/D sub 2C | **48→38**, energy2; fixture at post position/height, not a test of the full climbing input. Attack not available in the port today. |
| Drop miss, human / CPU attacker | Attacker **48→46 / 48→48**, victim without damage, energy2; the `miss_attackerCPU` cases are a CPU attacker. The old `drop_miss_cpu` were frozen badly and do NOT verify a miss. |
| Saturation | Drop with victim E=3: **3→0**, not negative (energy2, W_saturate3). |
| Counter-hold S/W1E, running, inner rope and crash on return | **48→48** for both actors, even though there is bounce and fall (energy2, counter_whip). |
| Running outside, limit/post impact | Attacker **48→43**, both, energy3 `post_outside`. No exact visual comparison of which physical post it was is claimed. |
| Idle and zero | Idle **48→48**; standing **0→0** without end of match (energy2). Short sample, not all states. |
| Getting up by energy | `levantarse_mame.csv`: initial table values minus the tick already consumed: E48=21, E24=53, E12=81, E0=111; until action 5 from k21: **42/106/162/222 refreshes**; E0 returns to action 0 at k259 with E0. Matches **22/54/82/112 ticks** in total. |

**Not verified dynamically**: full progression/difficulty matrices W/D, refill between matches, Power Up, all the pin/teammate/kick-out logic, full triple combo, all back/rope/link variants. Their values above are distinguished as direct deduction from the code. The comparison of D's floor art and the full equivalence of each branch with b89 remain pending; the port was not changed to make the tests easier.

The first tests are also kept (`arc_energy.lua`, log/CSV without a number), but some fixtures allowed evasion or did not move the clothesline. **Their absence of damage is not used as proof of zero damage**. `mame_resumen.csv` flags tests without contact and badly isolated misses.

## Files and preservation

- `ENERGIA_ataques.csv`: decision per wrestler/move, values and addresses.
- `energia_inicial.csv`, `cabeceras_poses.csv`, `TABLAS.txt`: extraction of tables/headers; empty box expressly distinguished from active damage.
- `mame_resumen.csv`, `levantarse_mame.csv` and the CSV/log/Lua of each test: reproduction and audit.
- Optional MAME PNGs: `W_drop_antes.png`, `W_drop_despues.png`, `W_clothes_antes.png`, `W_clothes_despues.png`. The RAM reading is the numerical evidence; the bar rounds in steps of four.
- b89 ROM still **MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`**. Nothing written inside b89; all the new work stays in this directory.
