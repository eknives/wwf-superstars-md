# Collision system (0x1657E)

Read in full at the 75 % milestone. Everything on this page is confirmed (C) unless stated otherwise.

1. **Loop** (0x1657E): called every frame. Sets +0x40 to 0 on the 4 wrestlers and goes through the 6 pairs of list 0xEA4C (0x165B2).
2. **Victim reset** (0x165FE): when the pose changes, +0xCE goes back to 0. That way the same active frame does not hit the same victim twice.
3. **Proximity filter** (0x16634): |dx| < 0x60 and |dy| < 8, the same +0x19 (< 2), neither one grabbed (action 0x10), etc.
4. **Hitboxes** (0x1672C): table 0x1761E[pose] gives a list per frame. Each box: priority (+0), damage (+1), attack box (+2), defence box (+6), alternative box (+0xE) and reaction table (+0xA).
5. **Impact** (0x16796): requires attacker priority ≥ defence, overlap in x (0x16C60) and in z (0x16CA8), and that the victim's pose be hittable (0x172FA). Then:
   - writes the reaction to +0x40 (with +2 if the hit is from behind) and the sub to +0x44;
   - damage goes to +0x3E (0 against the CPU with subs 0/1);
   - there are special adjustments for id 7 (0x169C2, 0x16AD4, 0x16B2A, 0x16C14);
   - strike against strike (0x16B6A): they cancel out;
   - grab (+0x40 = −2): both become linked.
6. **Body crash** without a strike (0x16DF8): both go to action 0x11.
7. **Sound and combo** (0x16CF4): tables 0x175CE and 0x17590 fill the accumulator +0x48. Its timer +0x46 is 0x30 frames.
8. **Application** (0x162A0, in the wrestler loop): action = +0x40; extra damage if downed (0x1638E), ×2 with +0xF9 bit0; 0x16488 subtracts the energy and plays 0x22/0x23.
