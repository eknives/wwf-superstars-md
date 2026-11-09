# b87 — candidate; DO NOT claim full arcade equality
ROM: `wwf_b87.bin` — MD5 `f956cfbcbf5012f63d66c8b0ac457a0d`. Base b86 intact (MD5 `0cbe0756ba9ff3dff97b4acfaa8a76b8`).

## 1. Punches — verified in emulator
- FC84/FD04: the timer is consumed in ticks of two refreshes. FD70/FD7C = 4/3/3 **ticks**, not MD frames. FCAC: start 3 ticks. FD2E/FD48: decision/recovery and link with timer 1. FCFC: only new edges with +36=0xC (0xB is not reached with increments of 4).
- MAME measures 17.408 ms/arcade refresh (57.44485 Hz): tick=34.816 ms. Clock by real VBlank: 3125/6528 ticks/frame NTSC; 3125/5440 PAL. Other moves are not slowed down.
- NTSC, both: 150/151/152 = 9/6/8 visible frames in the tested phase; the last 8 include 6 of animation + 2 of recovery. The other half-combo: 9/6/8. PAL: 7/5/7. Holding A does NOT chain; a new press DOES. Quantisation may vary by one frame depending on the clock phase.

## 2. Clothesline — contact verified; arcade coverage incomplete
- 12E7A/1302E: 1D0/1D1/1DA/1DB, and contact 1D2+opponent id for 8 ticks; exit E/F. 12F04 stops X during the catch; 12FAA throws the opponent afterwards, not on touching him.
- 16634 uses coordinates +C/+10 in pixels: |dx|<96, |dy|<8; it is NOT a hitbox. 1672C/16C60/16CA8: boxes 18C2A (-20,12,48,16) and 18B82 (-16,28,0,72); standing defence 18B02 (-8,16,0,80). Active 1D1 and 1DA. Inherited speed: 6.75 px/tick; then 4 px/tick (12F76).
- b86 DID fire the hit in MAME, but at 64 px and before the visual contact: it pushed the opponent away with the pin kick-out. It was not a dead conditional. That premature impact was removed.
- PASS: Duggan/Warrior, left/right; contact 1D1; late contact 1DA; Y separation=20 does NOT hit.
- **Pending for full equality:** victim boxes in other poses/running (hittable still excludes running), variants from behind and against the ropes. The current defence box is the standing one: do not present it as the complete 16796 engine.

## 3. Reaction 0x17 — flight/bounce/final pose verified
- 9B9A/9BBE/A8BE/2964: initial displacement +/-32 px, height +24, vx=+/-0x80, vz=0x100, gravity=0x30. 3E20: position +=2*v, then vz-=2*g. 9E4C: pose 15 until height 24 while descending; then 16. 9C94 -> A4C8: bounce without X velocity; ABBC: final pose 17.
- The vertical fraction is preserved when 9C44/A530 write only the integer word. Heights per tick measured: 213,214,214,214,213,211,209,206,202,197,191,187 / 189,190,191,191,190,188,187: equal to arcade MAME.
- New arcade graphics only by addition: poses 799..820, motors 627..637. The previous graphics data and maps remain as identical prefixes; the WWF logo and corner posts were not touched.
- **Limit:** the subsequent lying uses 22 ticks (AF66, healthy band); it does not reproduce all of the arcade's energy bands. The transition against the rope keeps the port's previous fall.

## Pace/slowdown and evidence
- b86: 40 Clothesline advances took 42 MD refreshes (2 without advance). b87 without impact: 43 refreshes, of which 42 are poses (11/8/8/15): ~700 ms versus 40 arcade refreshes=696.32 ms. No loop loss was observed in that case.
- On impact in b87: right Duggan 0 losses; Warrior 1; left 4. There is residual render/loop lag; CPU vs DMA was not isolated. The clock for these moves uses elapsed VBlank so as not to accumulate slowdown from those losses. **Do not claim that all lost frames were eliminated.**
- Eight short MAME Genesis/PAL trials, input A+B -> run -> new A; RAM only places wrestlers/control to repeat the case. CSV, scripts and assertions: `verify/`; summary `verify/RESULTADO_b87.txt`. Real emulated arcade: `verify/arcnatural.log`, contact without forcing flags; `arc87.log` for punch/timer. Captures: `shots87/DR_contact.png`, `DR_catch.png`, `DR_flight.png`, `DR_bounce.png`, `DR_land.png`, equivalents WR/DL/WL.
- The MAME driver says HTOTAL/VTOTAL are estimated: there is no measurement of a physical arcade board nor a test of this candidate on Everdrive.

**Result: candidate tested in the cases described, NOT a final "identical to the arcade" delivery due to the limits above.**
