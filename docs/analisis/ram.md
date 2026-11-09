# Mapa de RAM / hardware
Hardware (C, MAME wwfsstar.cpp): ROM 0-3FFFF; fg0 080000; bg0 0C0000; sprites 100000; paleta 140000; DSW 180000/2; P1 180004; P2 180006; SYSTEM 180008 (bit0 vblank); latch de sonido escribiendo en 180008 (byte 180009); scroll 180004/6 (escritura); flip 18000A. RAM 1C0000-1C3FFF. Las notas antiguas que dicen "FFxxxx" se refieren a 1Cxxxx.
| Dir | Uso | C/P |
|---|---|---|
| 1C0000/1C0002 | desplazamiento de sprites x/y | P |
| 1C001A | modo demo/attract | P |
| 1C0016 | créditos | P |
| 1C0026 | modo de juego (bits 0-1: jugadores/equipos) | P |
| 1C0027 | asignación de mandos (bit0) | P |
| 1C0028 | nivel de dificultad / índice de la tabla 0x8190 | C |
| 1C0029 | nº de combate (4 y 9 son especiales; 9 = final) | P |
| 1C002A/1C002E | cámara x/y | P |
| 1C003A | semilla del RNG 0x450A | C |
| 1C0042 | máscara de recarga de paletas | C |
| 1C006A-1C0095 | estado de la pantalla de selección | P |
| 1C00A2 | tabla de 6 rivales (bit15 = usado) | P |
| 1C0100, 1C021A, 1C0334, 1C044E | 4 luchadores (paso 0x11A; los punteros están en ROM 0xEA4C) | C |
| 1C0568, 1C0682, 1C078E, 1C089A | objetos extra | P |
| 1C0AB2 | árbitro | P |
| 1C0BC2/1C0BDA | flags de energía | P |
| 1C1814 | tabla de traducción de entrada | P |
| 1C1854 | efecto de valla del público | C (según las notas) |
| 1C18C4 | cola de escrituras diferidas (32) | C |
| 1C1A7A | 6 flags de marcador | P |
| 1C1AB0 | buffer de sprites (10 B c/u, contador 1C208C, máx 0x4B) | C |
| 1C2094 | lista de dibujo | C |
Los campos de objeto (+0 … +0xFA) están en sistemas/luchadores.md.

## Añadidos en el hito 25 % (leído entero)
- Luchador +0x19: 1 = fuera del ring (suelo z 0x80; dentro, 0xBB). +0x38: tiempo en el suelo. +0x34: pulsaciones al levantarse. +0x114/+0x116: pulsaciones/dirección del humano. +0xFF: contador de forcejeos. +0xD6 bit7: el rival está tumbado y se le puede cubrir. +0x18 bit5: está cubierto (pin).
- Objeto 1C0568 (cuenta del pin): +0x2D=1C0595 (modo; 2 = cuenta final), +0x2F=1C0597 (número de la cuenta), 1C059E, 1C059F, 1C05A5 bit2 (cuenta en marcha), 1C0570 (subcontador). Que sea el árbitro está SIN CONFIRMAR, porque aún no se ha leído su rutina.
- 1C0AB2: un objeto que se desactiva (bit7) en las acciones 0x99BE y 0xB012. NO se confirma que sea el árbitro.
- 1C1858 / 1C185A: se ponen a 0x81 (0x80 con el id 7) en las caídas y lanzamientos. Efecto SIN CONFIRMAR.

## Añadidos en el hito 50 %
- 1C185A: mensaje parpadeante fg0 (textos 0x1E/0x1F con 0x23A28; se borra en 0x80B04). Lo activa 0xB012 con 0x81. CONFIRMADO.
- 1C00B4: objetivo elegido por la CPU (0xF4DA).
- 1C1852: contador de combate; la dificultad de la IA (0x1CEF4) vale 0 hasta ≥0x258 (0x1D1A8).
- 1C1890/1C1891/1C1892: columna de fondo actual y estado de las celdas fijas (0x1F5C8). 1C1860/62/66: copia de tilemap partida en dos frames.
- 1C182C: último comando de fondo (0x1F434). 1C182D≠0: congela el scroll de columnas.
- 1C1854 bit4 / 1C1856 / 1C1857: animación del público (0x230FC).
- 1C1894/1C1896: selector de las poses de sombra/cuerda por lado (0x222D6). 1C1895/1C1897 bit0: marcas de jugador (0x251F0).
- 1C183E bit7: lo activan las llaves (0x105DC, 0x13A46, 0x149B0…). Significado SIN CONFIRMAR (no se ha leído quién lo consume).
- Luchador: +0xCC/+0xCD/+0xDC/+0xDD rachas de agarre; +0xFC=1 fuerza un fallo; +0x5C/+0x5D estado de la IA; +0x2E/+0x2F intención; +0x30/+0x31 sub de la llave; +0xF3 retardo de la IA; +0xC6/+0xC7 tirada tag; +0xCA pose vista; +0x104 marca de llave en el suelo; +0x106 primera vez en tag; +0xF6 contador +3 por llave.

## Añadidos en el hito 75 %
- 1C0568: árbitro; estados en 0xD7D8 (0 seguir, 1 vigilar, 2 cuenta de pin hasta 3, 3 cuenta fuera en BCD hasta 20).
- 1C05D0: bloque auxiliar del árbitro.
- 1C0BBE / 1C0BD6: estructuras de resultado por bando. En +4 (1C0BC2 / 1C0BDA): 0x40 / 0x80 (bits 6/7 = quién gana o pierde). Se escriben en la rendición (0x1481C) y en el pin.
- 1C0682 / 1C078E / 1C089A: objetos (stride 0x10C).
- 1C1820 / 1C1821 / 1C1823: estado de los objetos.
- 1C00B4: bloque de trayectoria del salto (calculado por 0x159AC). +0/+2 dx, +4 dy, +8 vz, +0xA gravedad, +0xC/+0xE máximos de vx/vy, +0x10 objetivo (−1 = punto fijo +0x16/+0x18), +0x14 z de destino.
- 1C0AB2 / 1C144E: efectos.
- 1C183E: flag de impacto de llave (se pone en los pasos de fuerza).
- 1C185A: estado de la llave de sumisión (0xC0 activa, 0xC1 escapada).
- 1C1858 / 1C1859: temblor de pantalla. Bit7 = pedir; 0x81 = corto (3 frames), si no 9. Bit6 = en curso; 1C1859 cuenta los frames. Suma la tabla 0x16286 a 1C002E (scroll).
- Campos del luchador confirmados:
  - +0x3C energía; +0x3E daño (0x16488 resta).
  - +0x40 reacción pendiente del golpe (−1 ninguna, −2 agarre, −4 especial).
  - +0x46/+0x48 temporizador/acumulador del combo.
  - +0xC9 bit0 golpeado, bit3 conectó, bit4 agarrado, bit5 golpes anulados.
  - +0xCE máscara de víctimas ya golpeadas con la pose actual; +0x42 pose anterior.
  - +0xF0 bit7 golpe fuerte; +0xF6 acumulador de la CPU.
  - +0x28/+0xDE tiempos del forcejeo.
