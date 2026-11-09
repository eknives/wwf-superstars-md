# Move pattern — documentary recipe from the arcade → port b92

**Study only; no implementation, build or new MAME test.** b92 is already delivered (PARTIAL in visible fidelity). This does not authorise adding characters/moves or touching Hogan. The visible cadence of Duggan's floor/post Elbow and Warrior's post Knee stays **LOW PRIORITY, "polish at the end"**.

Sources relative to this backup: `02_arcade_decompilado/analisis/arc_rec.dis` (aligned instructions), `arc.dis` only for the eight consecutive BRA.W at FC64–FC80; studies `02_arcade_decompilado/estudios/{kneedrop,duggan_suelo,energia}/`; `03_roms/notas/NOTAS_b87.md`, `NOTAS_b88.md`, `NOTAS_b90.md`, `NOTAS_b91.md`, `NOTAS_b92.md`. Port read: `/workspace/b92/src/`, identical to `01_port_sgdk/actual/src/`. The earlier b89/b90 notes are background, not the b92 state.

**Quality:** C=instruction/index confirmed by code; D=value already extracted/documented; M=explicit historical test on D/W; U=content or behaviour not confirmed here. A slot computed from a C stride does NOT imply knowing its pointer/values or having tested that wrestler. prog.bin has not been reopened/processed and MAME has not been run.

## 1. The common pattern: selector → subroutine → tables → reaction

1. **Identity:** byte `actor+2B` is the native id; `word+2A & FF` selects the tables. CPU is bit3 of the BYTE `+2A`, not "the opponent I don't control". Graphics bank and selector cell are different concepts (`6CD8`, selection conversion `7FE2`). Canonical identities: 0 Warrior, 1 Hogan, 2 Macho/Savage, 3 Duggan, 4 Bossman, 5 Honky, 6 DiBiase, 7 André.
2. **Input/selector:** edges `+114`; buffer `+116` maintained by `4066–40B6`. Choose action/sub by state, plane, opponent and zone. Do not deduce a technique from a sprite's name.
3. **Dispatch:** action byte `+2D`, table `8CE2`/dispatch `8C82`; action 0C runs `F94C`, which at `F980–F994` calls the pointer `FB58 + 4*sub` (`word+30 & FF`). Action 0C does not by itself mean Knee or combo.
4. **Clock:** actor every 2 refreshes (`1508–1510`), MAME 57.444852941 Hz. `+6` pose, `+8` timer and `+36` step are usually shared, but each routine decides whether it decrements on entry, uses > or ≥, keeps the drawing on exit or adds a preparation. **Do not convert a table value directly into 60 Hz frames.**
5. **Physics and contact:** world coordinates X/Y/Z `+0C/+10/+14` 16.16; velocities `+24/+26/+28` 8.8. Integration `3DCE/3E20`. Broad-phase, active box and energy are three different things.
6. **End:** change attacker/victim actions, links and auxiliary layers/objects; subtract energy only at the correct event. Do not replace every reaction with a generic fall.

### Current translation (NOT a universal engine)

`main.c`: `FC fd[2]`, `ctxLoad/ctxSave`, `engine`, `pendBtn`, `curPose`, `p1face/dFace`, `sx/bx`, `climb/ck`, `mv/mk`, `rn`, `gs/gk`. **Port slot 0=Duggan native 3; slot 1=Warrior native 0.** `curF`, `f^1`, `ctl` and the `[2]` rows are NOT native ids. There are `if(curF)` and `if(!curF)` branches and private clocks; adding a row or changing the portrait is not enough. b92's `gs14/15` are internal labels, not arcade subs 0E/0F; the old decimal `gs11` does not prove identity with sub 0B either.

`FC.ox/oy`+`oxf/oyf` and the private `w81X/Y/Z`, `dugX/Y/Z92`, `kvZ90`, `fsX/Z` use scale 256: they do not represent every arbitrary 16.16 fraction of the arcade. The documented physics keeps the representable fractions; do not certify universal precision. `arcClock/arcLast/arcTick/arcDen` convert VBlank to ticks (3125/6528 NTSC, 3125/5440 PAL, NOTAS_b87). Per-tick logic does NOT guarantee timely pose publication because of CPU/DMA/SAT.

Graphics: `Pose/Piece`, `poseTab`, `spr_tab`, `spr_tiles`, `xld/xlw`, `dLog/dPose/dLoaded`, `dFlip/dLyo`, `fLoad/drawF/buildSat`. Native pose, sequence alias and converted pose are different indices. Examples: `duggan92_poses.h` appendix 849..860; `native81.h` Warrior 779..791; `knee90.h` A2/17/1A for D and W. Do not reuse tile numbers as native ids or touch the palettes of the ring/partners/referee. The per-block palette banks cited in cl87.h (2 Warrior, 7 Duggan) are NOT the wrestler ids (0 and 3).

## 2. Catalogue by id: slots that ALREADY exist in the arcade

All addresses in the following tables are hexadecimal. They are ENTRY addresses, not their target pointers, unless `→` is explicit. C sources: `4624–463A` (bank), `FC54–FC5E` (combo), `C778–C794` (floor inside/outside), `F63C–F648` (post), `1500E–15020` (hold). Combo targets: eight BRA.W FC64–FC80 read in arc.dis; they are real dispatch instructions, not data pseudo-ops.

|id|Wrestler/bank|bank pointer 6CD8+4i|combo FC64+4i → routine|floor pointer CADE+4i|outside pointer CAFE+4i|post F6E6+3i|hold 15126+3i|
|---|---|---|---|---|---|---|---|
|0|Warrior|6CD8|FC64→FC84|CADE|CAFE|F6E6|15126|
|1|Hogan|6CDC|FC68→FC84|CAE2|CB02|F6E9|15129|
|2|Macho/Savage|6CE0|FC6C→FDA0|CAE6|CB06|F6EC|1512C|
|3|Duggan|6CE4|FC70→FDA0|CAEA|CB0A|F6EF|1512F|
|4|Bossman|6CE8|FC74→FC84|CAEE|CB0E|F6F2|15132|
|5|Honky|6CEC|FC78→FC84|CAF2|CB12|F6F5|15135|
|6|DiBiase|6CF0|FC7C→FDA0|CAF6|CB16|F6F8|15138|
|7|André|6CF4|FC80→FC84|CAFA|CB1A|F6FB|1513B|

Known D content: floor slot CAEA→CB6C; outside CB0A→CBEC. Rows head CB72=`04,11,04`, body CB75=`05,06,06`, columns P/K/P+K; outside body CBF5=`05,05,05` (TABLAS_DUGGAN, base CBEC+9). Warrior uses CB3C inside and CBBC outside (Knee study/main.c). **The targets/bytes of the other floor slots have NOT been confirmed here: do not assume CB3C+16*i.** The groups are chosen at C79E–C8A8; head offset 6, body 9; do not name the other rows without reading their branch.

Post: W F6E6=`2C,20,2C`; D F6EF=`2F,20,20` (studies). `F650–F664` picks column 0 if the opponent is in action B, 1 otherwise: **they are NOT P/K/P+K columns**; the third byte is not consumed in that particular selector. Bytes for the other wrestlers U. Hold 15126 does use button−1 (1501C/15020); contents for other ids U. Having a row does not prove that all techniques are accessed the same way.

### Jump/impact tables: distinguish attacker and victim

C: `10A72–10AB2`: physics `11150+16*attackerId`, four long pointers: +0 normal floor, +4 special floor, +8 normal air/post, +C special air. Special if victim id 7, or attacker id 6/sub 11 (`10A90–10AA8`). `10AB6–10AFA` adds variants by zone for sub 1A; do not extrapolate the D/W solver without those branches.

C: `10CC8–10CF6`/`10F54–10F84`: poses `112FA+40*attackerId +20*post +10*variant +2*step` (bytes). Each block has 20 words: four lists of 5 poses. Timers 112F0 shared, NOT per wrestler. Victim box `11084+4*victimId` (two words; 10FCC–11001A). Attacker point `110A4+8*attackerId +4*post` (two words; 11001E–11004E).

|id|wrestler|base 4 physics pointers|base 20 words poses|victim box|attacker point floor / post|
|---|---|---|---|---|---|
|0|Warrior|11150|112FA|11084|110A4 / 110A8|
|1|Hogan|11160|11322|11088|110AC / 110B0|
|2|Macho/Savage|11170|1134A|1108C|110B4 / 110B8|
|3|Duggan|11180|11372|11090|110BC / 110C0|
|4|Bossman|11190|1139A|11094|110C4 / 110C8|
|5|Honky|111A0|113C2|11098|110CC / 110D0|
|6|DiBiase|111B0|113EA|1109C|110D4 / 110D8|
|7|André|111C0|11412|110A0|110DC / 110E0|

D confirmed: physics 11180/11188→111F0; special 11184/1118C→11200; 111F0 words `(0,−64,0,0,0500,0050,2000,2000)`, special offset −80. Poses 11372=`61,62,1CB,1CC,1CC /61,62,1CD,1CE,1CE`, repeated for the post. Point 110BC/110C0=(8,4). W poses 112FA: 61/62/7A/7B; variant 76/77; point 110A4=(0,4). Other blocks **exist by the C index, contents U**: no invented list of Hogan/Macho poses has been extracted.

### Grappling, pin and energy: other per-character rows

C: grappling B370–B382 uses the **opponent's id** in B46C+4*i (two poses; shared times B468). 14E0A–14E1C uses the opponent in 150F6+6*i (three poses; times 150F0); 150E0+2*i uses its own id at 14DEE–14DF8 for that routine's counter, not energy. Pin BDCC–BE62 uses row BEF2+16*attackerId, dx byte `[victimId]`, dz byte `[8+victimId]`; they are NOT word pairs (dx,dz). There are exceptions for ids 0/4 at BD84–BE84 and an auxiliary object. Values for other characters U.

Human 7FEC+2*i=48 for all eight (TABLAS.txt energy). CPU 8190+16*progression+2*i, not universal values of 48; `1CD48+id` is a dizziness threshold (1CD84...), NOT initial energy. AF66/AF6A/AF72 are energy bands, NOT ids. AA00 uses `+F0&7`, not an id either.

|id|wrestler|grappling B46C|poses 150F6|counter 150E0|pin BEF2|human energy|CPU column row 0|dizziness threshold|
|---|---|---|---|---|---|---|---|---|
|0|Warrior|B46C|150F6|150E0|BEF2|7FEC=48|8190|1CD48|
|1|Hogan|B470|150FC|150E2|BF02|7FEE=48|8192|1CD49|
|2|Macho/Savage|B474|15102|150E4|BF12|7FF0=48|8194|1CD4A|
|3|Duggan|B478|15108|150E6|BF22|7FF2=48|8196|1CD4B|
|4|Bossman|B47C|1510E|150E8|BF32|7FF4=48|8198|1CD4C|
|5|Honky|B480|15114|150EA|BF42|7FF6=48|819A|1CD4D|
|6|DiBiase|B484|1511A|150EC|BF52|7FF8=48|819C|1CD4E|
|7|André|B488|15120|150EE|BF62|7FFA=48|819E|1CD4F|

## 3. Recipes by family: what to reuse and what NOT to clone

### A. Standing punches / combo
- Arcade: sub 0→FC4E→dispatch FC64 by attacker; FC84 for W/Hogan/Bossman/Honky/André, FDA0 for Macho/Duggan/DiBiase. **Same engine does NOT mean same poses**: FDA0 chooses FE88, exception id 2 FEAC (FDA4–FDB2); its full sequences/durations are not re-extracted here.
- FC84: FD70/FD7C poses 150..152/153..155, 4/3/3 **ticks**=8/6/6 refreshes for those steps; preparation FCAC=3 ticks, end/link FD2E/FD48 timer 1. For **attacker id 7 (André)** FD88/FD94 are chosen, own-id check at FCC0–FCE6; do not replace those tables with FD70 automatically. FCFC only accumulates NEW presses in step C (the B comparison exists, but increment 4 does not reach it); it decides on `&3==1`, not on holding P.
- Human damage 1 per hit: W header 18810/byte 18811; D 187F5. `1761E[pose]→[id]` and copy 1697E. Do not hand out 1/2/3 just because it is a combo.
- b92: `engine` branch `mv==1`, `mk/pAlt/pAcc/pEnd`, `move_seq`, `arcTick`; both slots use the FC84 pattern. **Duggan's native FDA0 combo is NOT faithfully ported**. For another character first pick its BRA from FC64 and convert its bank/sequence; do not copy the W combo to everyone. The current `hittable`/reaches are not the whole arcade box engine.

### B. Kick
- Arcade: sub 1→FED0; FF3A normal, FF4A when attacker id 7 (FED6). Advance at FEFc–FF38, special exit C9.2; real durations depend on the decrement and exit, they are not certified here for other ids. Pose 158: W 188AB=4, D 188C7=4. The box engine determines when it is active.
- b92: remaining `mv` branch, `move_seq` offset 33, `MV_HIT_KIK/MV_REACH_KIK/MV_REACH_Y`; damage 4 or 6 against running/whip represented. Generic reaction `victimStep/vh`; it is not a complete native descriptor. Giving a kick to another wrestler: table FF3A/FF4A + bank + boxes + reaction + damage, not just copying `mv=2`.

### C. Running and clothesline
- Arcade: running 93EE, bounce 960A/96AA; A while running CD14→action 0C/sub 14→12E7A. Shared table 1302E: 1D0/1D1/1DA/1DB, capture 1D2+victimId for 8 ticks; stops X at 12F04 and throws at 12FAA, not on first touch. Proximity 16634 (`|dx|<60hex,|dy|<8`, world coordinates X/Y) is NOT the final box; 1672C/16796 and boxes 1761E, case 1890C→18C2A (NOTAS_b87).
- b92: `engine` rn 1/2/3, `clStep87`, `clInit/Step/Timer/Held/Pose`, `rnW`, `rnx`; uses broad-phase + standing intersection, damage 4/2. `clHeld` and release tied to the opponent. Known gaps: runner, back/ropes and links; `hittable` excludes running. Do not declare it a complete arcade engine.
- For another wrestler: convert the attacker's bank including **the eight captures 1D2+victim**, test which box touches, and convert the fall from the victim's bank. Do not confuse `rnd` with H-flip: b92's release calls `clFallStart(o,-rnd)` per 12F16/12F1C and 9BC6/27D2. Movement without impact/ordinary running does not subtract energy just by existing.

### D. Grappling / Irish Whip
- Arcade: B1D0/B48C/B670 and tables B46C/B468; route 14DD6 and 150F6/150F0; human entry 14FEE→15126. Several tables choose by the **opponent's size/id**, not only by the attacking character. Choosing holds by button is different from deciding the winner of the grapple.
- b92: `grTry/grStep`, `gr/grk/grCool`, `lkC*`, `trStart/trStep`, `spT`, `sp_trk`, `trO/N/Pose`, bounce phases `rw*`; tracks S/W1E represent sub 1E→14CFC (counter-hold that releases to action 15). They do not contain Body Slam, Headlock, Gorilla Press or complete finishers.
- Recipe: model two linked actors and their cross tables, entry/reverse/winner, then release and bounce with limits 21E5A/21ED0. Own damage of grapple/whip/inner bounce=0; special outside crash 2209C=5 only with filters 220BE/2208C and anti-repetition. Do not charge Body Slam damage for reusing the whip track.

### E. Floor: Stomp and Knee/Elbow
- Common selection C706/C778–C8A8: same plane, |dy|<24; head Xv±40 (André ±56), strict zones 32/48 (André 40/56), action table CB1A. The buffer/the per-action exceptions are different from the final impact test. Pin/head/body are not chosen only by absolute distance to the centre.
- **Stomp sub 5:** 1173A/118BC `(159,8),(15A,4)`; consumes on entry 11750→1175C: 159×14/15A×10 refreshes including exit. Hits on entering 15A (11782/11786→1179A); only final plane/state, no second XY filter. 117E0 damage 1; exception 117E6 compares graphics bank+3 with 7 and writes 3. b92 D=`dugZone92/dugStart92/dugStep92`, gs14; W=`warriorGround*`, gs13. **The existing W stomp clock is not the newly ported D arcTick** (`if(!(gk&1))`): do not claim universal equality.
- **Common drop 10A5E:** W sub 0C/2C, D 11/2F; selects physics/poses by the §2 tables, solver 156FA→159AC, integration 3DCE/3E20. D/W: 8/18/10 initial refreshes, not 112F0[0]=0 interpreted as 1 tick; 10F54 waits 4 ticks, then comparator 10D42 >8/>4. After that, variable contact/recovery.
- Impact 10BF8–10C3C→10FCC: descending, victim B and same plane, Zword≤floor+16; box 11084 by victim and point 110A4 by attacker/post. Writes Yword=Yv−1 and Zword=floor, keeping fractions; W adds adjustment 1152A and variant 76/77, D NOT that +10 nor 7D. Damage 10DC0=5/10DCC=10, reaction 8/sub D→A2. Outside, the solver offset is divided by 2 (15A52); do not forbid it for being "near the rope"; the D 11/2F handlers at 24102/24106 end in RTS 24322/24324.
- b92 W=`warriorGroundStart/Step/End`, `w81*`, `kneePost90`, gs12; b92 D=`dugStart92/Step92/End92`, `dug*92`, gs15. Shared victim `kneeVictimStart90/Step90`. D keeps fraction, point ±8,+4, A2 and damage 1/5/10; it does not use the old generic aliases gs5/gs11.
- **Other characters are NOT a D/W copy:** Hogan id 1 doubles Vx/Vy on the floor at 10B70–10BAE, clears them when descending and changes gravity at 10C00–10C16; damage +1 at 10DDA and special end/bounce 10E30–10EA8. Sub 1A imposes 11, sub 0F 6; id 7 imposes 12 at the end of that decision 10DFC–10E04. The order of exceptions matters. For DiBiase id 6/sub 11 there is a special selector 10A98/10B42. The commercial names of those techniques are not identified here, and their animations are not considered tested.

### F. Attack from the post
- Arcade: action F, state +B8=2, F35A receives P **or K**, F636 chooses the row F6E6 according to opponent B. W sub 2C/D sub 2F enter the SAME 10A5E, not an independent jump. Flags +34, heights and solver change the trajectory; limits 10B5E/110E4 (horizontal distance ≥96→Vx ±200hex, vertical ≥80 inside/112 outside→Vy ±100hex).
- b92: `climb/ck`, `cPOST/cD0`, `CK` climb* tables, `engine` post branches, `kneePost90` W / `dugPost92` D. Standing opponent/dropkick from the post still absent. Do not change the global input or choose another technique just because it shares a button.
- For another wrestler: test the sub that its row really returns, solve from its corner/height, load the pose list `+20` and point `+4`, damage and end of ITS routine; it may not go to 10A5E. **Visible cadence D floor/post and W post pending LOW "polish at the end"**; it is not considered solved by copying tables.

### G. Pin / counts / restart
- Arcade: covering action 17→BD10, entries 1190C/11A72/12972, victim flag +18.5; matrix BEF2 per pair, poses 65 or 7F depending on id 0/4 and 188 by flag. Referee D7D8: DD4E count of 3 (poses DED4, times DEDC), DEE4 outside count of 20; E02C/E0A8 voices. Those referee tables are not per wrestler.
- Bands AF66/AF6A/AF72 and human pin ADEA/CPU AE7E depend on energy/flags/time, not "the first pin is always escaped". For the human escape the energy study §Low energy prevails over the old simplification in pin_cuenta.md: AE24–AE40 compares an accumulator with 48−E; E0 blocks that exit, not an automatic KO.
- b92: `pinStart/pinStepA/pinAdvance`, `pn*`, `rs*`, `digPin`, `countStep` (RO_TICK/roC), `roC/roT/roDone`, `resetReq→matchReset→fighterInit`. The kick-out model does not yet integrate all the native energy. Authorised port design rule: 3/20 **restarts the match without SELECT**; do not confuse it with the arcade transition that would have to be copied for full teams.

### H. Energy, damage and reactions (common, with data per pose/id)
- Energy +3C separate from pending damage +3E; subtraction 16488–1649A saturates at 0. No passive regeneration identified, 0 is not a KO; there are refills BETWEEN matches 2060–20EC and Power Up 6F64/6FEE (they are not regeneration during the fight). b92=`energy90[2]`, `hurt90`, `fighterInit` 48, no HUD, both HUMAN. `vdmg/vlast` are not energy. Every new wrestler must get independent energy, without turning the uncontrolled one into a CPU.
- Boxes: 1672C→1761E[pose]→[id] (header byte+1 damage), 1697E copy; 1698A CPU victim against sub 0/1 forces 0. 1638E/1642A adds a bonus only against actions 1/15/16; 16418 doubles F9.0; link FFFE 162BC skips both. D/W: punch 1, kick 4, clothesline 4/2, stomp 1, drop 5/10. Do not copy values to Hogan/André ignoring their exceptions or invent contacts for absent holds. Extra damage 1642A/counter 17590/sound 175CE are per SUB, not per id.
- **A2**: reaction action 8/sub 0D (dispatch 99BE/9A14, A554→28EC), Vz 200hex, g 40hex; relative heights 4/7/9/10/10/9/7/4/0 over 9 ticks; pose A2 from the VICTIM's bank, lands 17/state B; wait B kept according to AB7A, get-up 5/1A (AA00). Port `kneeVictim*90`, `kvPhase/Time/Z90`, `ground90`, `kneePose90`; do not add a universal fixed wait.
- **Thrown 0x17**: action 8/sub 17→9B9A, NOT action 17 pin. A8BE/2964: moves ±32, height +24, Vx ±80hex, Vz 100hex, g 30hex; pose 15→16 when descending below 24, bounce 9C94→A4C8 without Vx, ends 17. Port `clFallStart/fsStep`, `koF==3`, `fs*`, `clFallPose` in `cl87.h`. b88 fixed direction/flip and per-block palettes; native pose 15/16/17 is loaded from the victim's bank, NOT the attacker's. The rest of `victimStep/fsStart` is not automatically equivalent to these two reactions.
- **Drop miss**: 10C4A–10CB2/10C6A, human loses 2, CPU 0; recoil ±24 by orientation, +action 8/sub 5; 9FCC flips once and uses 1CF→16→17→1A, AF66/AA00 for the end. b92 D phase 6/7/8 in `dugStep92`; W miss branch `warriorGroundStep`. The jump 125F0/1274E is ANOTHER routine (miss 4); do not universalise −2.

## 4. Step-by-step recipe to give a technique to another wrestler (future work)

1. Identify id/bank, human/CPU role and technique from its selector row; record slot and REAL target. If it is marked U above, read that datum before choosing behaviour. Do not touch Hogan because he is used as an example.
2. Note action/sub, events/flags, admitted opponent, zones/orientations/planes; check whether the table indexes attacker, victim or pair. Consult the exceptions id 1/4/6/7; do not repeat the mistake "same code = same technique".
3. Separate data (poses, times, offsets, boxes, physics, damage) from the controller. A future `descriptorPorId` structure would be a PROPOSED DESIGN: **it does not exist as a generic engine in b92**. Replacing the curF branches will require a specific authorised scope, not just changing assets.
4. Convert from 6CD8 the correct bank with pose→pieces→tiles/palette; respect borrowed blocks (b88), pivots/H-flip/layers/auxiliaries, add without overwriting prefixes or Emilio's resources. References: converters `04_herramientas/scripts/b88/tools/gen88.py`, `b92/gen92.py`; building does not need to regenerate them.
5. Reproduce init/step/hit/recover/miss/end with the native clock and fractions, including victim/reaction/energy. Links between 2 actors are not an isolated animation. Do not apply contact twice or damage on every refresh of an active box.
6. With later implementation authorisation: short MAME/MD tests per tick and per visible REFRESH; record native/converted/loaded pose, world XYZ/fractions/velocities/energy, mirror, floor/post/outside and miss. Do not compare counts at 57.44/60/50 without real time, nor two captures of different phases as synchrony.
7. Keep the controls C=A+B, Y switches, no new AI/START only follows; energy for every new wrestler; regression of Hogan and untouchable resources, rest of the moves. New folder/ROM+MD5 only when authorised, never as a consequence of this guide.

## 5. Reusable evidence and gaps

- D/W floor mechanics: Knee/Duggan studies and `02_arcade_decompilado/notas_historicas/b92/shots92/{validation92.json,trajectory92_compare.csv,pose92_refreshes.csv}`. 88 stable states match, not complete visible equality. The b92 cases are RAM+button fixtures, not all corners/natural play/Everdrive.
- Combo/clothesline/fall: NOTAS_b87/b88 and b88 captures; the runner/back/ropes gaps remain.
- Damage/exceptions: energy study, `ENERGIA_ataques.csv`, `TABLAS.txt`, `cabeceras_poses.csv`; index by pose/id confirmed, headers of other wrestlers not recomputed here.
- Hogan/Macho/Bossman/Honky/DiBiase/André: C entries/strides listed, few exceptions read; **no new tests or certification of their complete techniques**. Pointers/bytes marked U are not completed by visual similarity.
- Official priorities: `PENDIENTES.md`; b92 delivered according to `03_roms/CHANGELOG.md`. Documenting pending items does not reopen the ROM.

## 6. Orientation of the lying opponent in Knee/Elbow (floor and post) — study 9-11-2026

Reading only `arc_rec.dis` + already existing b92 captures; no new MAME, no ROM or port changes.

**Arcade (C):** the opponent NEVER changes orientation. `10A5E` only writes the ATTACKER's `+A`: it copies the opponent's (`10A6C`, again `10BB2–10BB6`); id 0 Warrior or sub 1A replace it with the sign of Vx (`10BC4–10BD8`). From the post (+34≠0, except id 4) the attacker's graphics flag `+4` follows the sign of Vx during preparation/climb (`10F90–10FAC`, `10D02–10D26`). The impact (`10D58–10E0A`: `+2C=8`, `+44=0D`, damage `+3E`, `161C8`, sound `C6CA`) and the A2 (`A554`: `27D2(8)`, pose `A2`, `A56E move.b +A→+4`) draw the victim with its SAME `+A`. `C6CA` only chooses the sound.
- Target: solver `156FA` towards `Xv ± offset` according to the OPPONENT's bit7 (physics table §2); post: `10B5E/110E4` replaces Vx/Vy with ±200/±100 hex if far from `Xv±64`. Box `11084[victimId]` also by the opponent's bit7 (ori0 `Xv−64<X≤Xv`); point `110A4[attackerId]+4·post`. Head: anchor `Xv−40` if bit7=0, `Xv+40` if 1 (`C83E–C858`). The attacker adapts to the opponent, never the other way round.
- Hit `10BF8–10C3C→10FCC`; miss `10C4A–10CB2` (−2 human, ±24, action 8/sub 5, `9FCC` flips ONLY the attacker). Victim landing `A5DA–A60A`: Z=floor, action B, `+AE=0`; orientation intact.

**b92 (C, by code + PNG):** double convention for `vface`.
- Every drawing of the lying victim uses flip `vface^1`: generic pose 114–117/626 by `invFl` (`main.c:462`, `1485`, with `lyoOf` ±32) and native falls 15/16/17 (`main.c:1468`, `dFlip=vface^1`). When getting up from A2, `main.c:473` sets `p1face=!vface`. That is, **the displayed native orientation = `vface^1`**.
- The Knee/Elbow uses `vface` as if it were the native bit7: zones `main.c:649`, `duggan92.h:11–14`; target `main.c:677/685`, `duggan92.h:34/39`; box `main.c:736`, `duggan92.h:82`; attacker D copies `vface` (`duggan92.h:28`); and the A2/wait are drawn with `dFlip=vface` and `dLyo=0` (`kneeVictimStart90 main.c:483`, loop `main.c:1465`).
- Effect: the attacker aims at the side that on screen is the feet and, on contact, the victim is mirrored (and loses the ±32 offset) so that the head ends up under the knee/elbow. Evidence: `05_referencias/capturas/b92/volteo_A2_b92_suelo.png` (refreshes 118→124 of the elbow case: boots on the left → on the right) and `volteo_A2_b92_poste_suelo.png`. It also happens on the floor, not only from the post.
- The b92 tests did not detect it because they fixed `vface=0` against arcade ori0, assuming `vface=bit7`; the coordinates match in that frame of reference, not in the visual one.
- **Cadence 8/18/10:** NO relationship has been shown. The flip does not touch the attacker's timers and the irregular samples of the loaded pose are the attacker's; it remains a LOW pending item of visible publication. (U: not measured whether loading the victim's tiles on the contact refresh adds delay.)
- U: exact position of 114 with `lyoOf` against native pose 17 at the same `ox` (possible 32 px jump even with the correct flip); natural flow (knockdown by hits/clothesline → Knee/Elbow) without fixtures, not tested.

**b93 proposal (base b92) — IMPLEMENTED in b93, see result below:**
1. A single helper `oriVictima(o)=vface[o]^1` (displayed native orientation) used instead of `vface[o]` in `warriorGroundZone`, `dugZone92`, targets/solver/post override, impact box, `kneeOutsideVictim91` and Duggan's orientation copy (`duggan92.h:28`).
2. A2 and wait: `dFlip=oriVictima` at `main.c:483` and `1465`; keep `p1face=!vface` when getting up (already consistent). Check whether `dLyo` is needed so that it does not jump 32 px.
3. Do not touch `vface` or how it is assigned in falls/hits (avoids breaking the b88 clothesline and the pin). Stomp: the body zone is fixed with the same helper (today also inverted with respect to what is shown).
4. Verify: fixtures with arcade ori0 ↔ port `vface=1` (and mirror), same contacts 88 states; PNG per refresh without mirroring on contact; natural case knockdown→Knee/Elbow floor and post, both sides; regression Warrior/Duggan, clothesline and pin.

**b93 result (MD5 a89af7ed95159c0899430bf0e81f6441):** points 1–3 implemented (`oriVictima` at main.c:464; A2/wait main.c:485 and 1467 with `dLyo=0`, which is the arcade placement of the native pose at Xv). MAME: contacts = arcade in all Duggan and Warrior cases; opponent flip constant lying→A2→wait; captures `05_referencias/capturas/b93/shots93/contacto93_*.png`. Clothesline: b88 trace identical b92/b93. Pin: same mechanism; Warrior's pin (zone C798) now lands on the correct visible side. What was U is confirmed: there is a ~32 px jump between the generic lying pose (with `lyoOf`) and the native A2; it remains pending (it is not from the A2). Not tested: natural knockdown, post on the opposite side, PAL.

## 7. Warrior's pin (cover) on Duggan — arcade vs b93 verification (9-11-2026, verification only)

**Arcade, code (`arc_rec.dis`):** Warrior/Bossman (id 0/4) cover through `11A72` (no jump): `11A8A–11A90` orientation of the covering wrestler `+A = +A(victim) XOR 0x80`; pose 0x7E; `Y=Yv+1`; `X = Xv ± BEF2[0][3]` (=32; `btst #7,+A(victim)`: bit7=1 → +32, 0 → −32 with `neg`), `Z=0xBB−16+2·18=207`. After 8 steps (`11B2A–11B60`) action 0x17 → `BD10`: same X, `Y=Yv−1+2`, `Z=0xBB−16+16+16=203`, pose 0x7F with `+4=+A`, auxiliary `1C0AB2` pose 0x80 same X/Z, Y−2. Table `BEF2` row 0=[48,32,32,32,36,32,32,40 | dz 16,13,13,16,13,16,13,18]. Duggan (id 3) uses `1190C` (jump 1C00B4): orientation = sign of Vx (`11992–119A2`), then the SAME `BD10`: `X=Xv±36` (BEF2[3][0]), `Y=Yv−1`, `Z=0xBB−13`, pose 0x65. Duggan trigger: body row `CB75=05,06,06` (K in the body zone = pin, the same zone as the Stomp, between the head and Xv).

**Arcade MAME result (6 cases: ori0 Xv 680/760/880, ori1 640/760/860; inside the ring, no ACA4 push):** always `X−Xv=−32` (ori0) / `+32` (ori1), `Y=301`, `Z=203`, `+A/+4` of the covering wrestler opposite to the victim. B→sub 6 +2 f, pose 7E at the final X at +4 f (Z207, no displacement), 0x17 at +26 f, 7F at +28 f. At the edges the arcade pushes the lying wrestler inwards (ori0 640→675, ori1 880→861).

**b93 (code, `main.c` `pinStart`/`pinStepA`, unchanged since b77):** side by `pnM = oriVictima?−1:+1` and `pnX = Xv − lyoOf(114)`; final X = `pnX + pnM·32 = Xv` (not `Xv∓32`). `Y=Yv+1` and `Z=203` (pose 778 = 7F+80, two layers) correct. Orientation: `p1face=(pnM<0)=oriVictima`; as 778 was already converted mirrored (`gen77_pin.py arc(0,ap,1)`), the sprite comes out MIRRORED with respect to the arcade.

**b93 result (same 6 cases):** X=Xv in all of them (32 px off from the arcade in absolute terms, towards the feet), but relative to the VISIBLE body of the lying wrestler (drawn with `lyoOf` ±32) the position matches the arcade within ≤4 px (measured on captures: Warrior head↔Duggan boots 2/−15 px vs arcade 6/−15). Y/Z exact. Correct body side on both sides of the ring. **Flip:** silhouette of 778 against arcade IoU 1.00 only when mirrored (0.97 unmirrored) in the 4 measured cases; colour error 58 vs 117. Approach: b93 slides 24 f with historical poses 513/514 (Z187) from Xv−35; the arcade places 7E still at the final X. Sitting 778 at +29 f vs 7F at +28 f. b92 has the same placement code (only the trigger zone changed).

**Verdict (b93):** NOT entirely correct (fixed in b94, see §8). Good: body side, Y, Z, relation to the visible body, timing of the sitting. Bad: (1) Warrior covering mirrored in both orientations; (2) different approach (513/514 slide vs fixed 7E); (3) absolute X = Xv instead of Xv∓32 (compensates the `lyoOf` of the generic lying pose; same origin as the 32 px jump). Proposal (NOT implemented): (1) in `pinStart`, for Warrior `p1face=dFace=!oriVictima(v)` (= `+A(victim)^0x80` with the 778 convention), then check the flip of 513/514; (2) optional: replace the approach with the converted pose 7E (fixed at the final X, Z207, 24 f); (3) only together with the fix of the lying pose (lyo): `pnX=Xv`, X=`Xv+(oriVictima?32:−32)`. Duggan: same `BD10` rule (dx36/dz13), same `pinStart`; not measured in MAME here; its trigger (`bodyX±24`, feet side) is not the arcade zone `CB75`.
Evidence: `05_referencias/capturas/b93/pin_warrior/{pin93_comparativa,pin93_zoom_volteo,pin93_cmp_lados}.png`; data `02_arcade_decompilado/notas_historicas/b93/pin_warrior/`.

## 8. b94 — lying wrestler at the arcade X + adjusted pin (9-11-2026, MD5 b2a8ff5d4453067ad3d2bf8762239413)

**Implemented (only 2 points):** (1) `bodyX=ox`, `dLyo=0` for lying 114/626/752 (main.c:487, 1491): the pose without lyo occupies the same as native 0x17 at Xv (fl0 −56..16 vs −54..10). (2) `pinStart`: `pnX=pnVX=Xv`, `pnM=oriVictima?+1:−1` (BD10/11A72), `pnKD=pnM` (B012/B0A0); Warrior `dFlip=(pnM<0)` for 514/778 (converted mirrored, match69 flip1) and inverted for 513 (arc pose 2 flip0) ⇒ faces opposite to the lying wrestler (11A8A); Duggan flip unchanged; referee `rfX=Xv±64`, `rfM=−pnM` (same position relative to the body as b77). Duggan's pin by `dugZone92==2`+B (C706/CB75 body row, 06=cover); removed `bodyX±PIN_ZONE` (b69).

**MAME result (Xv=760):** B sweep d −88..+88 step 8 EQUAL to the arcade for W o0/o1 and D o0/o1 (W: K −64..−40, P −32..−16 / P +16..+40, K +48..+64; D: K −64..−40, P −32..0 / P 0..+40, K +48..+64). Covering wrestler: W X−Xv ∓32, Y301, Z203; D ∓36, Y299, Z174 (arcade ∓36/+36.97, 299, 174.5); ring side 680/860 OK. Silhouette: sitting and 514 direct in b94 (mirrored in b93). Knee/Elbow/Stomp contacts = arcade 16/16, flip/dX constant without lyo; getting up 114→115 without a jump. Clothesline identical to b93. Kick-out: lying Xv∓8, covering Xv∓48, Y−1, Z+4 (= B012/B0A0 formula; not measured in the arcade). 3 count OK.
**Side effect:** landing after kicking out near the rope: ACA4 pushes ~33 px (arcade measurement pending).
Evidence: `05_referencias/capturas/b94/`; data `02_arcade_decompilado/notas_historicas/b94/shots94/`.

## 9. Research 9-11-2026 (study only, no changes): running, slowdown next to the posts, rope crashes

**(b) Running — arcade (code):**
- `93EE` acc_correr → `945C` init: speed byte `0x95BC[id]` → `+0x21` (= [28,28,30,27,24,30,27,20]; Warrior id0 = **28**, Duggan id3 = **27**), angle `+0x1E = (+A&0x80)|0x40`, movement mode `+1 = 1`, no acceleration.
- `3DCE`→`3DF0`: every tick X += speed·2·0x20/256 px = **vel/4 px** (Warrior 7, Duggan 6.75).
- `94CE`: poses `0x95C4[id]` = 10..15, 2 ticks each.
- `953C`: `21E5A`; on touching the rope on the side it runs towards → action 2 (`960A`).
- Arcade MAME: 1 step every 2 refreshes in 65/65 cases (also along the top rope next to the posts). W 201.1 px/s, D 193.9 px/s (57.444 Hz). Poses every 4 refreshes.

**(b) Port b94 (`main.c` 821–832):**
- Advances `27<<6` (8.8 = 6.75 px) when `tick&1`. `tick` counts loop iterations (main.c:1460), not `arcTick` (main.c:1428, which does convert 57.44→60/50).
- Same 27 for both; the arcade gives 28 to Warrior.
- Measured in MAME:
  - NTSC: Warrior 194–202 px/s, with 3 out of 75 frames lost (vs 201.1).
  - **PAL: 167.7 px/s (−16.6 % W, −13.5 % D)**, because it is still 1 step every 2 refreshes, now at 50 Hz.
  - The poses go every 4 MD frames: also 17 % slower on PAL.
- Cause: running (and walking/animations) per MD frame instead of per arcade tick, plus fixed speed 27.

**(a) Slowdown — port b94:**
- Frame losses always coincide with the camera scroll crossing a tile: the loop in `main.c` 1507–1510 calls `put()`/`rel()` (main.c 196–208).
  - `acq` loads each new tile with `VDP_loadTileData(...,CPU)`, and `put` does 2× `VDP_setTileMapXY`.
  - A column is 29 rows (≈490–526 VDP words by CPU) and a row is 33 tiles.
- Frame with streaming: busy 0.83 frame (median) vs 0.25 without it. Any extra load (new pose in `fLoad`, ropes, crowd `caApply`) goes over 1 frame and is lost.
- As the logic advances per iteration (`tick`), every lost frame slows down the game.
- Near the posts the camera (`camera()` 289–332, `camtab` corridor) moves in X and Y at the same time. `main.c:330` prevents a column and a row in the same frame, so they chain up.
- Measured (MAME genesis NTSC, 59-frame windows):
  - diagonal approach to the top-left post: 8/59 frames lost (13.6 %);
  - bottom post: up to 12/59;
  - walking horizontally through the centre: 2.4 %;
  - standing still: 0.
- Sprites in the SAT (`nsat`): 3–20 next to the top posts and 0–39 next to the bottom ones (limit 80). It does not match the lost frames; sprites per line were not measured separately.
- Arcade: hardware scroll, no streaming; the logic does not lose ticks next to the posts. On real hardware (CPU writes to the VDP during active display) it may be worse; not measured.

**Ropes — three arcade cases:**
1. **Bounce** (he runs or is thrown):
   - `953C`→action 2 `960A`: turns, anim 0x10, speed 9 decreasing by 1 per tick, `9700` marks the rope.
   - Thrown: action 8 → `9CD0` → sub 2.
   - Port: rn==2 (48 f track, verified in s66).
2. **Leaving:**
   - `CD2C`→`CD5C/CDF8`: touching the side rope (`+0x18` bit0/1 of `21E5A`), direction 7/3 towards it, and y+z in [0x1E0,0x230), without 1C1898/189A bit6.
   - Team human: 12 ticks (`+0x102`).
   - Action 3, or 6 if not a team member, is inside and +2A bit4/bit1 are 0.
   - Port main.c:1023–1026: 27 frames (`SX_HOLD`) at the rope's X.
3. **Crash:**
   - `9E78` every tick tests X∓0x10 ahead with `21E5A` (undoes it if it touches, except poses 9A/A1).
   - `9CD0` compares the high byte of +0x44, so it **always goes to sub 2** (MAME: sub 0x1C→2 on first contact, not to sub 1).
   - `9F02`: `9700` marks the rope (1C1898/189A = 0x4001: vibrates), z≥0xCB, pose 0x16, `27D2` index 0x11 (flight parameters 0x2934: Vx 0x100, Vz 0, g 0x10; it is not a sound — corrected in b95), **Vx negated**: bounces inwards 2 px/tick until z=0xBB → action 0xB.
   - Without a rope, sub 0x1C falls with an extra −0x20 (`9C5A`).
   - `ACA4` when lying down tests ±0x30 and ∓8 **according to bit7 of +A**.

**Crash when kicking out (B012/B0A0) — arcade MAME vs b94** (S = X of the covering wrestler when the kick-out happens):

| Xv | S | Arcade | b94 |
|---|---|---|---|
| 760 | 712 | 642, no rope, stays | 642 → `soilNudge` → **675** (jump 33) |
| 728 | 680 | 643, stays | 627 → 675 (jump 48) |
| 708 | 660 | crashes: rope vibrates, pose 22, bounces to **677** | crosses to 627 without bouncing → 675 |
| 693 | 645 | crashes → 677 | 627 → 675 |
| 832 (right) | 880 | crashes → **859** | 906 → 858 |

Port causes (`main.c` 498–552, 625–632):
- `fsRope` looks at its own already clipped X, not X∓16 ahead.
- Sub 0x1C goes to fs2 instead of fs3.
- fs3 does not move X (the negated Vx is missing).
- `soilNudge` uses `vface` as bit7, when the b93 convention is `oriVictima = vface^1`; that is why it pushes to the wrong side.

Evidence: `02_arcade_decompilado/notas_historicas/inv95/` (arc_run*.csv, arc_zafar*.csv, port_zafar.csv, b94_*.csv and .lua scripts).

## 10. b95 — running by arcade tick, background by DMA, rope crash (9-11-2026, MD5 7be789d70d892c1efb86af8630b296a6)

**Implemented (only the 3 points of §9):** (1) running: `rnSpd` = byte 0x95BC[id] (945C → +0x21; W 28, D 27), step vel/4 px per `arcTick` (3DF0), pose every 2 `arcTick` (94CE); the rest of the logic still goes per frame (pending). (2) streaming: tiles and BG_B/BG_A cells of columns/rows through a DMA queue (`acqQ`, `stCol`, `stRow`, budget 40 tiles/frame, `DMA_flushQueue` if exceeded), crowd and ropes computed before; they appear in the same vblank as in b94. (3) rope: 9E78 tests X±0x10 every tick with 21E5A/22140 (616+e / 920−e, no clipping with z≥0xDB) → X=limit∓0x10; 9CD0 always sub 2 (`cmpi.b` bug copied); contact on the landing tick → 9C94 without ∓0x20; 9F02 on the next tick: rope vibrates, z≥0xCB, pose 0x16, Vx 0x100 inwards, g 0x10, lands with z<0xBB → lying. `soilNudge` with `oriVictima` (vface^1) as bit7 of ACA4; calls 875/893 reviewed (vface=attacker on the right, b93 convention).
**MAME result:** running W 200.5/D 194.0 px/s NTSC, 199.7–200.1/192.6–193.0 PAL (arcade 201.1/193.9), poses 14.0–14.8/s (arcade 14.36); frames lost towards the top-left/top-right/bottom-left/bottom-right posts 20/14/18/19 → 3/2/1/0 out of 580 (max in 59: 10/6/12/10 → 2/1/1/0), background verified by reading VRAM: 0 errors; static captures identical to b94. Kick-out at Xv 760/728/708/693/832 → 642/643/677/677/859 = arcade (b94 675/675/675/675/858). Running bounce, leaving the ring, clothesline (victim the same, attacker 6–8 px further away because of per-tick running) and pin still fine.
**Not verified:** sub 1 against the rope in throws and knockdowns by hits next to the rope vs arcade; PAL at the posts; real hardware; sound 0x29 does not exist in the port.
Evidence: `05_referencias/capturas/b95/`; data `02_arcade_decompilado/notas_historicas/b95/shots95/`.
