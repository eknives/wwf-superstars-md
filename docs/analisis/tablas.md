# Tablas de ROM
| Dir | Contenido | C/P |
|---|---|---|
| 0x1F450 | 9 modos de juego (0x1F434) | C |
| 0x21C4 | selección de rival por nivel | C |
| 0x3DEA | modo de movimiento (+1) | C |
| 0x3EC4… | 8 octantes de polar→xy | C |
| 0x6CD8 | poses de sprite | P |
| 0x7340, 0x805A, 0x828E | despachos por modo | C |
| 0x7686/0x78CA | retratos | P |
| 0x7D6A | barras de energía | P |
| 0x7FE2 | id de selección → id de luchador | P |
| 0x7FEC/0x8190 | índices de energía humano/CPU por nivel | C |
| 0x8AB0 | textos por nivel | P |
| 0x8CE2 | 33 acciones (+0x2D) | C |
| 0xAF66 | tumbado (lieTab) | C |
| 0xBCB8 | objetos extra a dibujar | C |
| 0xEA4C | punteros a los 4 luchadores | C |

## Añadidos en el hito 25 %
- 0xA74A: parámetros por subacción de "recibir" (+0x44); 0x9A14: tabla de saltos de las subacciones; 0x9E38/0x9E42: sonido y pose de rodar.
- 0xAF66: tiempo en el suelo según la energía; 0xAF6A: pulsaciones para levantarse; 0xAF72: umbral de la cuenta para librarse del pin; 0xAF76: subacciones aéreas del rival (lista que termina en 0xFF); 0xAF82/0xAF96: probabilidad de esquivar por nivel/energía.
- 0xAA00: tiempo para levantarse; 0xAA10/0xAA20: subida al poste de la CPU (acción y probabilidad por id).
- 0xAFF4: tirada de la CPU por nivel; 0xB0EA: poses para alzar; 0xB162: provocar; 0xB46C/0xB468: forcejeo.

## Añadidos en el hito 50 %
- 0x14346 / 0x143AA: probabilidad de agarre para el humano / la CPU por nivel (+5 si DIP 0x180002 bit3=0). 0xB74A: ganador del forcejeo.
- 0xD54C/0xD646: entrada al ring. 0x1C26E/0x1C2AA y 0x1C3F6/0x1C432: pasos de salida/entrada por las cuerdas (normal / id 7).
- Llaves: 0x14A82, 0x14C5C, 0x154BC/0x154AE, 0x15E7A/0x15EB2/0x15EE2/0x15F12, 0x1464E (contra mutua), 0x15944/0x15960/0x1597C (golpe rápido).
- IA: 0x18F16 (despacho por +0x5C), 0x18F92, 0x1A554, 0x1AFA8, 0x1B938/0x1B8F4, 0x1C028 (descriptores de 6 bytes), 0x1D18E (retardos), 0x1D33A/0x1DD7E (intenciones), 0x1D2FA/0x1D31A (máscaras), 0x1D2B8 (remapeo), 0x1D2B0, 0x1E1A6/0x1E392/0x1E14E/0x1E19A, 0x1E55E/0x1E74A/0x1E55A, 0x1E8EC.
- Gráficos: 0x1F706/0x1F726 (columnas de fondo), 0x23AC4 (gráficos fg0), 0x22760/0x22640 (geometría RLE), 0x23170 (público), 0x2237A/0x22392/0x223FA (sombra/cuerda), 0x216A6/0x2146E (retratos), 0x23536/0x2354E (versus), 0x26166/0x26176/0x261B6, 0x265D2/0x265E6, 0x26692/0x26696, 0x2535A.

## Añadidos en el hito 75 %

**Cajas de golpe y daño**
- 0x1761E: tabla de cajas por pose (lista por frame); 0x18076 para la pose −1.
- 0x172FA: índice de reacción por pose de la víctima (0xFF = no golpeable).
- 0x1636C: filtro de impacto por acción.
- 0x1642A: daño extra al tumbado por sub.
- 0x164FA: golpes fuertes por sub (0xFF).
- 0x175CE: sonido por sub.
- 0x17590: combo por sub.

**Listas**
- 0x16B20 / 0x16BCC: listas de acciones (terminadas en 0xFF).
- 0xEA4C: lista de los 4 luchadores.

**Agarre, sumisión y forcejeo**
- 0x124D6: umbral de escape de la sumisión por dificultad.
- 0x149A2 / 0x149AA: duraciones y poses de la sumisión.
- 0x150E0: tiempo de la CPU en el forcejeo.
- 0x150F6 / 0x150F0: poses y duraciones del forcejeo.
- 0x15126: sub por id y botón.
- 0x14FD8 / 0x14FE0 / 0x14FE8: contra del humano.

**Llaves (indexadas por el id del rival)**
- 0x1310C, 0x132B8, 0x134CC, 0x13938 / 0x13956 / 0x13918, 0x13E44, 0x14108 / 0x14124, 0x14378 / 0x143DC, 0x1465E / 0x14676, 0x14DD0, 0xB46C / 0xB468, 0x155EA, 0x156C8, 0x15692 (bra), 0x15FFC.

**Otras**
- 0x15B70: z de destino por zona propia/rival.
- 0x15BE4: probabilidad de burla de la CPU por id.
- 0x1576E / 0x15860 / 0x15878: combos de la CPU.
- 0x160CC: avance al entrar al ring.
- 0x16286: desplazamientos del temblor.
