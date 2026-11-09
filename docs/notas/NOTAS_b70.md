# b70 (base b69, md5 b3d460cb3f2bd3bc97338e499f1c2046; b69 intacta)

ROM: `wwf_b70.bin` — md5 `24854415d3674c5e784b99ea9f7cc8da`

## 1. Levantarse más lento
- `wrDown`: tumbado boca arriba (pose 114) dura 140 frames (antes 68) y la animación de levantarse (115) dura 30 (antes 18).
- Medido en MAME: está tumbado del frame +14 al +154 (unos 2,3 s, antes 1,1 s), así que hay más tiempo para probar los golpes en el suelo (codo A / salto B).

## 2. Agarre arcade (los dos luchadores)
- **Cómo empieza:** cuando los dos están libres, a menos de 32 px en X y 16 en Y, y uno de ellos camina, se agarran (lock-up). Los dos se juntan en el punto medio y usan las poses arcade del forcejeo (move_seq 118 para Duggan y 343 para Warrior, en bucle). Cada luchador usa siempre **sus propias** poses, así que no se mezclan sprites.
- **Forcejeo 1 (básico):** el luchador que controlas (C) pulsa A o B antes de que el contador llegue a 17 → gana y lanza al rival contra las cuerdas.
- **Forcejeo 2 (revertir la llave):** si no pulsas nada antes de 16, la llave se invierte y gana el otro luchador (lo lleve la IA o esté parado sin START) cuando el contador llega a 32. En ese caso te lanza a ti.
- **Lanzamiento contra las cuerdas:** se usan las pistas arcade `sp_trk` (S_1E cuando lanza Duggan, W1E cuando lanza Warrior). La víctima corre hasta la cuerda **real**: si la cuerda está más cerca salta al frame de contacto, y si está más lejos repite los pasos de carrera. Rebota (con la cuerda flexionando), vuelve corriendo hasta la cuerda contraria, rebota otra vez y queda de pie. El que lanza se libera a los 25 frames y ya puede moverse.
- Después de cada agarre hay 40 frames de espera antes de poder agarrarse otra vez.
- Mientras dura el agarre o el lanzamiento no se pueden dar golpes.
- C sigue cambiando solo el mando y START solo la persecución (igual que en b69).

## Pendiente / limitaciones
- A y B hacen lo mismo (el lanzamiento a las cuerdas). La llave arcade 0x26 de A queda pendiente.
- Todavía no hay nada al volver de las cuerdas (clothesline, etc.): la víctima rebota y se queda de pie.
- Como la distancia de agarre (32) es menor que el alcance del puñetazo (40), si vas andando hasta pegarte al rival se agarra, igual que en el arcade.

## Pruebas (MAME, test/t70.lua y test/t70g.lua) — capturas en shots/b70
- 01-04: Duggan agarra, pulsa B y gana; Warrior corre, rebota en la cuerda derecha (x=912) y en la izquierda (x=621).
- 05-08: no se pulsa nada, la llave se invierte (blk=1, c2 llega a 32), Warrior lanza a Duggan y Duggan rebota en la cuerda derecha.
- 09-11: tras C (controlas a Warrior) pulsas A y Warrior lanza a Duggan.
- 12-13: Warrior en el suelo (los datos del test confirman que sigue tumbado hasta el frame +154).
