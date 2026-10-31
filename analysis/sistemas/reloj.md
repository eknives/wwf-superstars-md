# Reloj del combate (0x2626E, 1C1850)

- **Arranque:** marco (0x265F6) y música del combate.
- **Tiempo inicial:** 0x708 ajustado por el DIP 180003 bits 4–5 (0: 0x708; 1: +0x96; 2: −0x96; 3: −0x12C).
- **Ritmo:** cada 0x42 frames resta 0xA. Se muestra como mm:ss (/0x3C), así que el valor por defecto se lee 30:00.
- **A 5:00 (0x12C):** 1C1850 bit1, comando 0x70 (NO-OP en el Z80) y música 8 (prisa). Por debajo de ese tiempo parpadea el color 140036.
- **A 0:** texto 0x9B («TIME UP»), cartel fg0 0x2660E(0) (no es el Z80) y el resultado según la tabla 0x2653C[1C0026&3]. El fin de tiempo envía el 0x21 (campana repetida).
