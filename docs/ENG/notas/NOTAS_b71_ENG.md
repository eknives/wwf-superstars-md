# b71 (base b70, md5 24854415d3674c5e784b99ea9f7cc8da; b70 intact)

ROM: `wwf_b71.bin`, md5 `dbfe401359b8f726186dd01e82cd5b2c`

## Changes (only the 4 requested)
1. **3 count (pin) for both.** With the opponent lying, **B right next to the body (closer than 24 px)** = cover, like the arcade's B2 (action 0x06/0x17). Duggan covers with his poses (494-499) and Warrior with his (513-515). The referee drops to the floor and slaps with the arcade tracks (500-506). The big figure 1/2/3 appears at +94/+194/+294, as in the arcade. If it reaches 3, the match restarts 2 s later.
2. **Kick-out only on the 1st count.** On each wrestler's first pin, after the "1" (arcade +128 Duggan / +136 Warrior), the covering wrestler gets off and moves away 40 px, and the lying one gets up (pose 115). The referee gets up (507-509) and goes back to following. From the 2nd pin on, the count reaches 3.
3. **Count of 20 outside the ring.** While someone is outside (side or back), the referee counts 1…20, adding 1 every 64 frames (arcade 0xDEE4/0xDA38: 4 steps × 8 ticks of 2 f). If both come back inside, the count is cleared. If it reaches 20, the match restarts 2 s later.
4. **Warrior's jump on the opponent complete.** Before, it used Duggan's translated poses, and from 547 to 554 a standing Warrior appeared. Now it uses his real arcade move, 0x0C (track S0C from s62, his own poses 569-573 and then 277/483/72): he rises, drops onto the body on his knees (impact at f40) and gets up. It is triggered with B at 24-100 px from the body, as before. Duggan's jump (0x11) has not been touched.

**Match reset:** both go back to the starting position and with no damage, and the referee to his place. The console is not reset. C (whom you control) and START (chase) are kept. The camera comes back at its normal pace.

## Not touched
There is no attack AI: the one you don't control only chases with START. The controls are the same: B next to the body covers, B further away jumps and A gives the elbow. The graphics of the top corner posts, the WWF logo and the palettes have not been touched either. The figures use the background's PAL0.

## VRAM
- Big figure: tiles 1525-1534.
- Figures of the outside count: tiles 1779-1788. Both zones were free.

## Limits
- During the outside count the referee does not make the arcade's counting gesture: he keeps walking as before. Only the small figure (8×8) is visible, and there are no 1-2-3 voices.
- The arcade decides the kick-out by energy/button mashing. Here, at Emilio's request, the 1st pin is always kicked out of and the following ones always reach 3.
- The kick-out is the cover in reverse plus a 40 px displacement (approximation from s41). In the arcade, the partner comes in.
- The lying opponent has to be in the face-up phase (pose 114) to cover him or jump on him.

## Tests (MAME, test/t71.lua, modes pin / jump / ro with T71=…)
Captures in shots/: 01-04 pin 1 (covers, "1", gets off, gets up), 05-08 pin 2 (1, 2, 3 and reset), 10-16 Warrior's jump, 20-24 outside count (1, 2, 10, 20 and reset). The sheets are hoja_*.png.
