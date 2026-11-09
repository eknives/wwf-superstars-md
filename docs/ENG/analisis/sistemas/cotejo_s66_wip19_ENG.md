# Arcade ↔ s66 wip19 comparison (read-only; fix in wip21)
| Case | Arcade | s66 wip19 | Does it matter today (Duggan vs Warrior + referee)? |
|---|---|---|---|
| 0x22040 barrier damage | Damage 5 except action 8 with +0x45≠0xA | Inverted in action 8 (line 155) | No: only called with action 0. Fixed in wip21 (identical ROM) |
| 0x23406 crowd-barrier start | bit6, or bit7 with 1C1890≠1 | bit7 with zone==1 (inverted) | No: CA_FENCE only from w22040, never fires. Fixing it requires zone lists 0/2 (decision) |
| 0x230FC crowd-barrier drawing | Only with 1C1890≠1 and 1C182C=0 | Only with zone 1 (inverted) | No (same reason) |
| Pin #1 kick-out | Own (mashing / CPU by energy and count) + roll 0x11BC6 + partner | 1st pin always kicks out; then roll | Yes. Design decision |
| Pin #2 energy 0 | CPU with 0 never gets out; human 0x30 presses | 13/16 count of 3 | Yes. Decision |
| Pin #5 lieBand CPU | max 0x8190/4 | e/12 | Yes if the maximum ≠48 (V) |
| Pin #8 CPU downed /2 | 0xAB1E /2 and +0x20 | No | Yes. Decision |
| #6 initial CPU energy 55 | Not read | 55 | V |
| #7 / 0x1D1A8 / 0x1D0E2 / 0x1AE44 / 0x1B120 / 0x1BEE4 AI | Table-driven planner (with the 0x1D0E2 bug) | Own provisional AI | Yes (AI rule). Porting the planner = decision |
| #9 clock / 0x26548 | 30:00, hurry 5:00, TIME UP | Missing | Yes. Decision |
| #10 count-out / double DQ | Up to 20 | Missing | Yes. Decision |
| #11 sound | Z80/OKI driver | Missing | Yes. Out of scope |
| #12 RNG 0x450A | Sum of registers | shared random() | Accepted by Emilio (wip19) |
| 0x244EE/0x24554 pose adjustment | x/z restoration | Not ported (no references) | No |
| 0x2549E texts / 0x21A4E | RLE text engine | Own texts | No (no DiBiase) |
| 0x73E8 random choice | mod 6 with retry | No selection | No |
| 0x19D96 / 0x1B7FA / 0x1B88C relay/tag | Partner | No partner | No (note) |
| André/DiBiase/Honky/Bossman (0x134D2, 0x14222, 0x13CD0, 0x169C2, 0x1578E, 0x1907C, 0x1AB34, 0x1B942, 0x1C180/0x1C306, 0x16488 sound 0x23, 0x1A6B6, 0x1CDA4, 0x1CB16, 0x1C726, 0x13114) | Own logic | Not ported | No: note them when porting |
