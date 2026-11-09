# Discrepancies port (s66 wip19, 67efe37a…) vs arcade — not fixed
1. The crowd barrier effect (1C1854) is missing. (C)
2. There is no sound driver; requests to 0x25E6 have no equivalent. (C)
3. The CPU daze table for Duggan is missing. (C)
4. lieTab is measured by eye; it is not table 0xAF66. (C)
5. The 0x15→0x01 transition and the return attack are approximate (WHIP_RET). (C)
6. The crowd randomness does not use the RNG 0x450A formula (registers + seed 1C003A). Pending verification in the port's code. (P)
7. Opponent selection by level (0x21C4, with rng): it remains to be checked whether the port follows the same order. (P)

## Review (full read 0x17C6–0x8AB0)
- Pending: compare with the s66 code. This pass did not get to it, so the 7 discrepancies remain UNCONFIRMED against the port.
- New arcade data (already confirmed) to compare:
  - The energy bar shows ceil(energy/4), with a maximum of 12 segments.
  - Energy is kept between matches; it is only reset in match 0, from table 0x7FEC.
  - RNG 0x450A does not add d1 or a3.
  - With a human at energy 0, music 8 plays.
  - In versus (mode 2) there is no game over: the winner continues in 1-player mode.
