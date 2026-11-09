# Match clock (0x2626E, 1C1850)

- **Start:** frame (0x265F6) and match music.
- **Initial time:** 0x708 adjusted by DIP 180003 bits 4–5 (0: 0x708; 1: +0x96; 2: −0x96; 3: −0x12C).
- **Pace:** every 0x42 frames it subtracts 0xA. It is shown as mm:ss (/0x3C), so the default value reads 30:00.
- **At 5:00 (0x12C):** 1C1850 bit1, command 0x70 (NO-OP on the Z80) and music 8 (hurry). Below that time colour 140036 flashes.
- **At 0:** text 0x9B («TIME UP»), fg0 sign 0x2660E(0) (it is not the Z80) and the result according to table 0x2653C[1C0026&3]. The end of time sends 0x21 (repeated bell).
