# b88 — only fall direction and Clothesline graphics review
ROM: `wwf_b88.bin` — MD5 `96371335c6b9cb43b08d158ba73ec488`. Base b87 intact.

## 1. Fall — YES, verified in MAME
**Bug:** b87 called `clFallStart(o,rnd)`: it threw the opponent in the same direction and chose the opposite mirror. Now it uses `-rnd`.
Arcade: 12F16/12F1C copies the attacker's orientation to the opponent and flips bit7; 9B9A/9BC6 applies ±32 px; 27D2/2964 applies vx=±0x80. Result: attacker →, opponent ← (and vice versa), 32 initial px + 1 px/tick. 9E4C/A8BE and ABBC: 15→16→17, fall **face up**, head towards the attacker. It is not changed to a face-down pose.
Tested Duggan and Warrior as attacker/victim, left/right. CSVs record displacement and H-flip: opponent Hflip=1 when attacking to the right, 0 when attacking to the left.

## 2. Animations — YES, verified in the tested cases
**Second bug:** the b87 conversion lost the palette bank of each block and coloured the opponent's borrowed limbs with the attacker's colours. Fixed per block: source 2=Warrior, 7=Duggan; the arcade selects the effective palette per actor at 46A0. Without changing `spr_pal.bin`.
Tables 6CD8: banks 0/3. 1302E/12EF6: 1D0,1D1, catch 1D2/1D5,1DB,E,F; 1DA if no catch. Victim: 15,16, bounce 16, floor 17. Order and flip compared; their timings were not altered.
**38 exact pixel comparisons**, after the existing MD colour mapping, against the sprites actually emitted by MAME (RAM 100000). In addition, **20 loaded poses** compared word by word with the real VDP VRAM and CRAM palette: 0 differences. The two refreshes of delay between logical state and drawing were taken into account.

## Evidence and limits
`verify88/RESULTADO_b88.txt`, CSV, scripts and SAT dumps. Paired PNGs contact/flight/floor: `shots88/Duggan_R_comparacion.png`, `Duggan_L_comparacion.png`, `Warrior_R_comparacion.png`, `Warrior_L_comparacion.png`; also `par_*` and `pixels_*`.
Only the sign of the throw and the graphics conversion/loading of these poses change. Previous graphics prefixes, WWF logo, corner posts, punches and other resources intact. The collisions/ropes/energy pending from b87 are neither fixed nor extended. NTSC MAME tests; **b88 not yet tested on Everdrive**. The stated pixel equality is after conversion to the MD palette, not RGB equality of both platforms.
