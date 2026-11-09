# RAM / hardware map
Hardware (C, MAME wwfsstar.cpp): ROM 0-3FFFF; fg0 080000; bg0 0C0000; sprites 100000; palette 140000; DSW 180000/2; P1 180004; P2 180006; SYSTEM 180008 (bit0 vblank); sound latch writing to 180008 (byte 180009); scroll 180004/6 (write); flip 18000A. RAM 1C0000-1C3FFF. Old notes that say "FFxxxx" refer to 1Cxxxx.
| Addr | Use | C/P |
|---|---|---|
| 1C0000/1C0002 | sprite offset x/y | P |
| 1C001A | demo/attract mode | P |
| 1C0016 | credits | P |
| 1C0026 | game mode (bits 0-1: players/teams) | P |
| 1C0027 | pad assignment (bit0) | P |
| 1C0028 | difficulty level / index into table 0x8190 | C |
| 1C0029 | match no. (4 and 9 are special; 9 = final) | P |
| 1C002A/1C002E | camera x/y | P |
| 1C003A | RNG 0x450A seed | C |
| 1C0042 | palette reload mask | C |
| 1C006A-1C0095 | selection screen state | P |
| 1C00A2 | table of 6 opponents (bit15 = used) | P |
| 1C0100, 1C021A, 1C0334, 1C044E | 4 wrestlers (stride 0x11A; the pointers are in ROM 0xEA4C) | C |
| 1C0568, 1C0682, 1C078E, 1C089A | extra objects | P |
| 1C0AB2 | referee | P |
| 1C0BC2/1C0BDA | energy flags | P |
| 1C1814 | input translation table | P |
| 1C1854 | crowd barrier effect | C (according to the notes) |
| 1C18C4 | deferred write queue (32) | C |
| 1C1A7A | 6 scoreboard flags | P |
| 1C1AB0 | sprite buffer (10 B each, counter 1C208C, max 0x4B) | C |
| 1C2094 | draw list | C |
The object fields (+0 … +0xFA) are in sistemas/luchadores.md.

## Added at the 25 % milestone (read in full)
- Wrestler +0x19: 1 = outside the ring (floor z 0x80; inside, 0xBB). +0x38: time on the floor. +0x34: presses when getting up. +0x114/+0x116: human presses/direction. +0xFF: struggle counter. +0xD6 bit7: the opponent is down and can be covered. +0x18 bit5: is covered (pin).
- Object 1C0568 (pin count): +0x2D=1C0595 (mode; 2 = final count), +0x2F=1C0597 (count number), 1C059E, 1C059F, 1C05A5 bit2 (count running), 1C0570 (sub-counter). That it is the referee is UNCONFIRMED, because its routine has not been read yet.
- 1C0AB2: an object that is deactivated (bit7) in actions 0x99BE and 0xB012. It is NOT confirmed to be the referee.
- 1C1858 / 1C185A: set to 0x81 (0x80 with id 7) in falls and throws. Effect UNCONFIRMED.

## Added at the 50 % milestone
- 1C185A: fg0 flashing message (texts 0x1E/0x1F with 0x23A28; cleared at 0x80B04). Activated by 0xB012 with 0x81. CONFIRMED.
- 1C00B4: target chosen by the CPU (0xF4DA).
- 1C1852: match counter; the AI difficulty (0x1CEF4) is 0 until ≥0x258 (0x1D1A8).
- 1C1890/1C1891/1C1892: current background column and state of the fixed cells (0x1F5C8). 1C1860/62/66: tilemap copy split over two frames.
- 1C182C: last background command (0x1F434). 1C182D≠0: freezes column scrolling.
- 1C1854 bit4 / 1C1856 / 1C1857: crowd animation (0x230FC).
- 1C1894/1C1896: selector of the shadow/rope poses per side (0x222D6). 1C1895/1C1897 bit0: player marks (0x251F0).
- 1C183E bit7: set by holds (0x105DC, 0x13A46, 0x149B0…). Meaning UNCONFIRMED (who consumes it has not been read).
- Wrestler: +0xCC/+0xCD/+0xDC/+0xDD grab streaks; +0xFC=1 forces a miss; +0x5C/+0x5D AI state; +0x2E/+0x2F intention; +0x30/+0x31 hold sub; +0xF3 AI delay; +0xC6/+0xC7 tag roll; +0xCA seen pose; +0x104 floor hold mark; +0x106 first time in tag; +0xF6 counter +3 per hold.

## Added at the 75 % milestone
- 1C0568: referee; states in 0xD7D8 (0 follow, 1 watch, 2 pin count up to 3, 3 count-out in BCD up to 20).
- 1C05D0: referee auxiliary block.
- 1C0BBE / 1C0BD6: result structures per side. At +4 (1C0BC2 / 1C0BDA): 0x40 / 0x80 (bits 6/7 = who wins or loses). Written on submission (0x1481C) and on the pin.
- 1C0682 / 1C078E / 1C089A: objects (stride 0x10C).
- 1C1820 / 1C1821 / 1C1823: object state.
- 1C00B4: jump trajectory block (computed by 0x159AC). +0/+2 dx, +4 dy, +8 vz, +0xA gravity, +0xC/+0xE vx/vy maxima, +0x10 target (−1 = fixed point +0x16/+0x18), +0x14 target z.
- 1C0AB2 / 1C144E: effects.
- 1C183E: hold impact flag (set in the strength steps).
- 1C185A: submission hold state (0xC0 active, 0xC1 escaped).
- 1C1858 / 1C1859: screen shake. Bit7 = request; 0x81 = short (3 frames), otherwise 9. Bit6 = in progress; 1C1859 counts the frames. Adds table 0x16286 to 1C002E (scroll).
- Confirmed wrestler fields:
  - +0x3C energy; +0x3E damage (0x16488 subtracts).
  - +0x40 pending strike reaction (−1 none, −2 grab, −4 special).
  - +0x46/+0x48 combo timer/accumulator.
  - +0xC9 bit0 hit, bit3 connected, bit4 grabbed, bit5 strikes cancelled.
  - +0xCE mask of victims already hit with the current pose; +0x42 previous pose.
  - +0xF0 bit7 heavy strike; +0xF6 CPU accumulator.
  - +0x28/+0xDE struggle times.
