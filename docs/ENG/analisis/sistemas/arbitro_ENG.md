# Referee (object 1C0568)

## State choice: 0xD7D8
Takes the active wrestler of each team and chooses the state. If the state changes, it writes it to +0x2D and clears +0x2C.

| State | When |
|---|---|
| 2 | Someone is covered (+0x18 bit5) |
| 3 | Someone is outside the ring (+0x19=1) or in action 4 |
| 1 | Sub 0x13/0x2E of action 0xC, or action 0x1B |
| 0 | In all other cases: follow the match |

## State 2: pin count (0xDD4E)
- Approaches the midpoint between the two wrestlers.
- Slaps: poses from table 0xDED4 and durations from 0xDEDC.
- On each slap: +0x2E++ and 0xE02C.
- On reaching 3: the result goes to 1C0BBE+4 / 1C0BD6+4.

## State 3: count-out outside the ring (0xDEE4)
- Counts in BCD up to 20.
- On reaching 20: bit7 or bit6 depending on whether each wrestler is still outside. There can be a double disqualification.

## Count sound: 0xE02C
- Table 0xE0A8 = ff,3d,3e,3f: voices «1, 2, 3».
- In state 3 with +0x2E<4 nothing sounds: the count-out is silent.
- It also shows text 0x9B and the text of 0xE086[+0x2E].
