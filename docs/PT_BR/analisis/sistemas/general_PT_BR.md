# Laço principal, IRQ e RNG
- Reset 0xE00; laço 0x1010; modo via 0x1F434/0x1F450 (C).
- IRQ vblank 0xEBA: sprites 0x259A, fila 0x269A, paletas 0x29F6, 0x2626E e os desenhos 0x20928, 0x55C6, 0x1F5C8, 0x213B4, 0x224E8 (público), 0x2336C, 0x206BE, 0x219AA, 0x1F3CE (scroll) (C).
- IRQ 0xF5C: moedas 0x4A10 e temporizador de attract 0xF92 (C).
- Frame de combate 0x1C86: 0x221CA → 0x25064 → 0x22462 (público) → 0x6BA0 → 0x435C (enfileirar sprites) → 0x455C (C).
- RNG 0x450A: semente em 1C003A, à qual se somam d0, a1, a2, a4, a5, a6 e d2-d7; devolve (semente+1)>>8 (C). É determinístico segundo o estado dos registradores, não depende do relógio. Usa-se na seleção de rival 0x2228/0x22D2, na seleção 0x73DE, no attract 0x7B6C, na IA 0x15B90 e no público.
