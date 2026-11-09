# Relógio do combate (0x2626E, 1C1850)

- **Início:** moldura (0x265F6) e música do combate.
- **Tempo inicial:** 0x708 ajustado pelo DIP 180003 bits 4–5 (0: 0x708; 1: +0x96; 2: −0x96; 3: −0x12C).
- **Ritmo:** a cada 0x42 frames subtrai 0xA. É mostrado como mm:ss (/0x3C), então o valor padrão é lido 30:00.
- **Em 5:00 (0x12C):** 1C1850 bit1, comando 0x70 (NO-OP no Z80) e música 8 (pressa). Abaixo desse tempo pisca a cor 140036.
- **Em 0:** texto 0x9B («TIME UP»), letreiro fg0 0x2660E(0) (não é o Z80) e o resultado segundo a tabela 0x2653C[1C0026&3]. O fim do tempo envia o 0x21 (sino repetido).
