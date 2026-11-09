# ROM tables
| Addr | Content | C/P |
|---|---|---|
| 0x1F450 | 9 game modes (0x1F434) | C |
| 0x21C4 | opponent selection by level | C |
| 0x3DEA | movement mode (+1) | C |
| 0x3EC4… | 8 octants of polar→xy | C |
| 0x6CD8 | sprite poses | P |
| 0x7340, 0x805A, 0x828E | per-mode dispatches | C |
| 0x7686/0x78CA | portraits | P |
| 0x7D6A | energy bars | P |
| 0x7FE2 | selection id → wrestler id | P |
| 0x7FEC/0x8190 | human/CPU energy indices by level | C |
| 0x8AB0 | texts by level | P |
| 0x8CE2 | 33 actions (+0x2D) | C |
| 0xAF66 | downed (lieTab) | C |
| 0xBCB8 | extra objects to draw | C |
| 0xEA4C | pointers to the 4 wrestlers | C |

## Added at the 25 % milestone
- 0xA74A: per-sub-action parameters for "receiving" (+0x44); 0x9A14: jump table of the sub-actions; 0x9E38/0x9E42: rolling sound and pose.
- 0xAF66: time on the floor according to energy; 0xAF6A: presses to get up; 0xAF72: count threshold to escape the pin; 0xAF76: opponent's aerial sub-actions (list ending in 0xFF); 0xAF82/0xAF96: dodge probability by level/energy.
- 0xAA00: time to get up; 0xAA10/0xAA20: CPU climbing the post (action and probability by id).
- 0xAFF4: CPU roll by level; 0xB0EA: lifting poses; 0xB162: taunt; 0xB46C/0xB468: struggle.

## Added at the 50 % milestone
- 0x14346 / 0x143AA: grab probability for the human / the CPU by level (+5 if DIP 0x180002 bit3=0). 0xB74A: struggle winner.
- 0xD54C/0xD646: ring entry. 0x1C26E/0x1C2AA and 0x1C3F6/0x1C432: exit/entry steps through the ropes (normal / id 7).
- Holds: 0x14A82, 0x14C5C, 0x154BC/0x154AE, 0x15E7A/0x15EB2/0x15EE2/0x15F12, 0x1464E (mutual counter), 0x15944/0x15960/0x1597C (quick strike).
- AI: 0x18F16 (dispatch by +0x5C), 0x18F92, 0x1A554, 0x1AFA8, 0x1B938/0x1B8F4, 0x1C028 (6-byte descriptors), 0x1D18E (delays), 0x1D33A/0x1DD7E (intentions), 0x1D2FA/0x1D31A (masks), 0x1D2B8 (remapping), 0x1D2B0, 0x1E1A6/0x1E392/0x1E14E/0x1E19A, 0x1E55E/0x1E74A/0x1E55A, 0x1E8EC.
- Graphics: 0x1F706/0x1F726 (background columns), 0x23AC4 (fg0 graphics), 0x22760/0x22640 (RLE geometry), 0x23170 (crowd), 0x2237A/0x22392/0x223FA (shadow/rope), 0x216A6/0x2146E (portraits), 0x23536/0x2354E (versus), 0x26166/0x26176/0x261B6, 0x265D2/0x265E6, 0x26692/0x26696, 0x2535A.

## Added at the 75 % milestone

**Hitboxes and damage**
- 0x1761E: table of boxes per pose (list per frame); 0x18076 for pose −1.
- 0x172FA: reaction index by victim pose (0xFF = not hittable).
- 0x1636C: impact filter by action.
- 0x1642A: extra damage to the downed wrestler by sub.
- 0x164FA: heavy strikes by sub (0xFF).
- 0x175CE: sound by sub.
- 0x17590: combo by sub.

**Lists**
- 0x16B20 / 0x16BCC: action lists (terminated by 0xFF).
- 0xEA4C: list of the 4 wrestlers.

**Grab, submission and struggle**
- 0x124D6: submission escape threshold by difficulty.
- 0x149A2 / 0x149AA: submission durations and poses.
- 0x150E0: CPU time in the struggle.
- 0x150F6 / 0x150F0: struggle poses and durations.
- 0x15126: sub by id and button.
- 0x14FD8 / 0x14FE0 / 0x14FE8: human counter.

**Holds (indexed by the opponent's id)**
- 0x1310C, 0x132B8, 0x134CC, 0x13938 / 0x13956 / 0x13918, 0x13E44, 0x14108 / 0x14124, 0x14378 / 0x143DC, 0x1465E / 0x14676, 0x14DD0, 0xB46C / 0xB468, 0x155EA, 0x156C8, 0x15692 (bra), 0x15FFC.

**Others**
- 0x15B70: target z by own/opponent zone.
- 0x15BE4: CPU taunt probability by id.
- 0x1576E / 0x15860 / 0x15878: CPU combos.
- 0x160CC: advance on entering the ring.
- 0x16286: shake offsets.
