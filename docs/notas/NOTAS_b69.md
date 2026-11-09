# WWF b69 (base b68, md5 b68 3a41cd79ddf5d3b669c0475ca56ca20c, sin tocar)

ROM: `wwf_b69.bin`, md5 `b3d460cb3f2bd3bc97338e499f1c2046`

## Cambios
1. **Caída de espaldas**: si mira a la derecha, la cabeza queda a la IZQUIERDA; si mira a la izquierda, a la DERECHA (shots 01 y 07).
2. **Golpes en el suelo + reacción, para los dos**: con el rival tumbado, A = codazo (poses 521-523) y el que está en el suelo se sacude. B, a 16-100 px del cuerpo, = salto y pisotón (poses 537-554), que cae sobre el cuerpo. Mientras le golpean, el rival sigue tumbado (shots 02-05 y 08-10).
3. **Warrior con el mismo motor que Duggan**: corre (A+B), sale y entra del ring y sube y baja los esquineros del fondo y delanteros (shots 13-17).
4. **C = cambiar control Duggan ↔ Warrior**. Solo cambia a quién mandan los mandos; los sprites y las posiciones siguen igual (shot 06).
5. **START**: el oponente (el que no controlas) te persigue; con otro START se para (shots 11-12).

## Arreglos técnicos
- Los tiles de Warrior se han movido a VRAM 1672, porque en 1525 se corrompían (salía basura en el público).
- El salto del pisotón ya no suma una altura extra: la altura ya viene en las poses.
- El perseguidor no se mete encima de ti: si está a menos de 20 px, se aparta.

## Aproximaciones y pendientes
- Si el jugador camina encima del rival, los sprites pueden solaparse.
- El HUD sigue igual que en b68 (por ejemplo, el rótulo "DUGGAN" sale aunque controles a Warrior).
- Los offsets del codazo y del pisotón se han revisado a ojo con las capturas de MAME, no comparándolos fotograma a fotograma con el arcade.
