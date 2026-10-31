# Árbitro (objeto 1C0568)

## Elección de estado: 0xD7D8
Toma el luchador activo de cada equipo y elige el estado. Si el estado cambia, lo escribe en +0x2D y borra +0x2C.

| Estado | Cuándo |
|---|---|
| 2 | Alguno está cubierto (+0x18 bit5) |
| 3 | Alguno está fuera del ring (+0x19=1) o en la acción 4 |
| 1 | Sub 0x13/0x2E de la acción 0xC, o acción 0x1B |
| 0 | En los demás casos: seguir el combate |

## Estado 2: cuenta del pin (0xDD4E)
- Se acerca al punto medio entre los dos luchadores.
- Palmadas: poses de la tabla 0xDED4 y duraciones de 0xDEDC.
- En cada palmada: +0x2E++ y 0xE02C.
- Al llegar a 3: el resultado va a 1C0BBE+4 / 1C0BD6+4.

## Estado 3: cuenta fuera del ring (0xDEE4)
- Cuenta en BCD hasta 20.
- Al llegar a 20: bit7 o bit6 según si cada luchador sigue fuera. Puede haber doble descalificación.

## Sonido de la cuenta: 0xE02C
- Tabla 0xE0A8 = ff,3d,3e,3f: voces «1, 2, 3».
- En el estado 3 con +0x2E<4 no suena nada: la cuenta fuera es muda.
- También muestra el texto 0x9B y el texto de 0xE086[+0x2E].
