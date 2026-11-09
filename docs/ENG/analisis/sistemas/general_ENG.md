# Main loop, IRQ and RNG
- Reset 0xE00; loop 0x1010; mode via 0x1F434/0x1F450 (C).
- vblank IRQ 0xEBA: sprites 0x259A, queue 0x269A, palettes 0x29F6, 0x2626E and the drawings 0x20928, 0x55C6, 0x1F5C8, 0x213B4, 0x224E8 (crowd), 0x2336C, 0x206BE, 0x219AA, 0x1F3CE (scroll) (C).
- IRQ 0xF5C: coins 0x4A10 and attract timer 0xF92 (C).
- Match frame 0x1C86: 0x221CA → 0x25064 → 0x22462 (crowd) → 0x6BA0 → 0x435C (queue sprites) → 0x455C (C).
- RNG 0x450A: seed in 1C003A, to which d0, a1, a2, a4, a5, a6 and d2-d7 are added; returns (seed+1)>>8 (C). It is deterministic according to the register state, it does not depend on the clock. It is used in opponent selection 0x2228/0x22D2, in selection 0x73DE, in attract 0x7B6C, in AI 0x15B90 and in the crowd.
