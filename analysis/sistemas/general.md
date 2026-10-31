# Bucle principal, IRQ y RNG
- Reset 0xE00; bucle 0x1010; modo vía 0x1F434/0x1F450 (C).
- IRQ vblank 0xEBA: sprites 0x259A, cola 0x269A, paletas 0x29F6, 0x2626E y los dibujos 0x20928, 0x55C6, 0x1F5C8, 0x213B4, 0x224E8 (público), 0x2336C, 0x206BE, 0x219AA, 0x1F3CE (scroll) (C).
- IRQ 0xF5C: monedas 0x4A10 y temporizador de attract 0xF92 (C).
- Frame de combate 0x1C86: 0x221CA → 0x25064 → 0x22462 (público) → 0x6BA0 → 0x435C (encolar sprites) → 0x455C (C).
- RNG 0x450A: semilla en 1C003A, a la que se suman d0, a1, a2, a4, a5, a6 y d2-d7; devuelve (semilla+1)>>8 (C). Es determinista según el estado de los registros, no depende del reloj. Se usa en la selección de rival 0x2228/0x22D2, en la selección 0x73DE, en el attract 0x7B6C, en la IA 0x15B90 y en el público.
