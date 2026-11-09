# b82 (base b81, md5 ffa3e48e22aee99750cd82af10d6ab31; b81 intacta)

ROM: `wwf_b82.bin`, md5 `b6c57f8cb194c7c7805b5a75b3775dc8`. Compilación SGDK local.
Solo se toca el remate de Warrior en el suelo (salto sobre el rival tumbado). Las cuerdas no se han tocado.

## 1. Desde dónde se lanza (arcade 0xC706 / 0xC798–0xC8A8 / 0xC928–0xC95A)
- En CB1A[acción 0xB] = 0xFF el rival está tumbado, así que se usa la rama del ancla. Ancla = rival.x ± 0x28 (+ con bit7).
- Fila de Warrior en 0xCB3C: delante del ancla (<0x20) → A = sub 4, **B = sub 0x0C (salto)**. Hacia el cuerpo (<0x30) → A = sub 5 (pisotón), B = sub 6 (pin). En 0xC928 el pin solo vale si la distancia es <0x20 y propio.y ≥ rival.y; si no, B da un golpe normal (sub 1).
- **Comprobado en MAME arcade** (`test/probe.lua`, `test/warrior_probe.txt`) con Warrior id 0 y rival tumbado en x=760:
  - sin bit7 (cabeza a la izquierda): salto en dx −64..−40; pisotón en −32..0; pin en −32..−16.
  - con bit7: salto en +48..+64; pisotón en 0..+40; pin en +16..+40.
  - **Por el lado de los pies nunca salta.**
- La pose 0x17 del arcade ocupa x−48..x+16, con la cabeza en x−48. Es decir, **el salto solo sale desde más allá de la cabeza**.
- **Fallo de b81:** confundía la orientación del port con el bit7 del arcade y tomaba ox como si fuera la x arcade. Por eso saltaba desde los pies, como en tu captura.
- **Arreglo:** bit7 = !vface y X = ox ± 48. Con eso la selección es exactamente la de 0xC798, incluida la restricción del pin de 0xC928.

## 2. Trayectoria
- 0x10A6C: Warrior toma la orientación del rival. Destino según 0x111D0: rival.x − 0x20, en espejo con bit7.
- En el arcade (MAME) va de x 712 a 727 con el rival en 760. Antes iba hacia el centro del cuerpo y miraba al revés.

## 3. Pierna y puño duplicados
- 0x1152A: el objeto 7D (1C0AB2) es **otro sprite** que se coloca en y−10, z+10, con la orientación opuesta y x±4.
- Warrior se queda en y = rival+9, **detrás** del rival, y el 7D (rodilla y puño) en y−10, **delante**.
- b81 lo metía todo en un solo sprite encima de todo, y por eso se veían dos rodillas y dos puños.
- Ahora las poses 787/788 llevan el cuerpo y el 7D en piezas separadas (`tools/native82.py`) y se ordenan cada uno con su profundidad. Es el mismo mecanismo de dos capas que el pin 778.
- Resultado: las piernas del rival tapan el cuerpo de Warrior, como en `shots/arcade_MAME_impacto_7D.png`.

## Pruebas (MAME Genesis, `test/b82.lua`)
- headL/headR (desde la cabeza, B): salta (gs=12). feetL/feetR (desde los pies, B): **no salta**.
- stompL/stompR: pisotón. pinL/pinR: pin.

## Capturas (`shots/`)
- Arcade: `arcade_MAME_salto_desde_cabeza.png`, `arcade_MAME_impacto_7D.png`.
- b82: `b82_salto_cabeza_R.png`, `b82_salto_cabeza_L.png`, `b82_impacto_capas.png`, `b82_pies_B_no_salta.png`.

## Fuera de alcance / pendiente
- A delante del ancla = sub 4 en el arcade (agarre al tumbado). No está implementado; el port da un puñetazo.
