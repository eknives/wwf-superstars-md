# Cotejo arcade ↔ s66 wip19 (solo lectura; corrección en wip21)
| Caso | Arcade | s66 wip19 | ¿Afecta hoy (Duggan vs Warrior + árbitro)? |
|---|---|---|---|
| 0x22040 daño valla | Daño 5 salvo acción 8 con +0x45≠0xA | Invertido en la acción 8 (línea 155) | No: solo se llama con acción 0. Corregido en wip21 (ROM idéntica) |
| 0x23406 arranque público-valla | bit6, o bit7 con 1C1890≠1 | bit7 con zona==1 (invertido) | No: CA_FENCE solo desde w22040, nunca dispara. Arreglarlo exige listas de zonas 0/2 (decisión) |
| 0x230FC dibujo público-valla | Solo con 1C1890≠1 y 1C182C=0 | Solo con zona 1 (invertido) | No (mismo motivo) |
| Pin #1 kick-out | Propio (machacar / CPU por energía y cuenta) + tirada 0x11BC6 + compañero | 1.er pin siempre sale; luego tirada | Sí. Decisión de diseño |
| Pin #2 energía 0 | CPU con 0 nunca sale; humano 0x30 pulsaciones | 13/16 cuenta de 3 | Sí. Decisión |
| Pin #5 lieBand CPU | máx 0x8190/4 | e/12 | Sí si la máxima ≠48 (V) |
| Pin #8 CPU tumbada /2 | 0xAB1E /2 y +0x20 | No | Sí. Decisión |
| #6 energía inicial CPU 55 | No leído | 55 | V |
| #7 / 0x1D1A8 / 0x1D0E2 / 0x1AE44 / 0x1B120 / 0x1BEE4 IA | Planificador por tablas (con el fallo de 0x1D0E2) | IA provisional propia | Sí (regla IA). Portar el planificador = decisión |
| #9 reloj / 0x26548 | 30:00, prisa 5:00, TIME UP | Falta | Sí. Decisión |
| #10 cuenta fuera / doble DQ | Hasta 20 | Falta | Sí. Decisión |
| #11 sonido | Driver Z80/OKI | Falta | Sí. Fuera de alcance |
| #12 RNG 0x450A | Suma de registros | random() compartido | Aceptado por Emilio (wip19) |
| 0x244EE/0x24554 ajuste de pose | Restauración x/z | No portado (sin referencias) | No |
| 0x2549E textos / 0x21A4E | Motor de texto RLE | Textos propios | No (sin DiBiase) |
| 0x73E8 elección al azar | mod 6 con reintento | Sin selección | No |
| 0x19D96 / 0x1B7FA / 0x1B88C relevo/tag | Compañero | Sin compañero | No (nota) |
| André/DiBiase/Honky/Bossman (0x134D2, 0x14222, 0x13CD0, 0x169C2, 0x1578E, 0x1907C, 0x1AB34, 0x1B942, 0x1C180/0x1C306, 0x16488 sonido 0x23, 0x1A6B6, 0x1CDA4, 0x1CB16, 0x1C726, 0x13114) | Lógica propia | No portados | No: anotar al portarlos |
