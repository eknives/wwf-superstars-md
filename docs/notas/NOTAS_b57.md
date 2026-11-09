# b57 (desde b56)

ROM: wwf_b57.bin  md5 8651e4ef71af09be6260350b1489e20d

Solo reparto de paletas + árbitro visible (b56 intacta):

| Línea | b56 | b57 |
|---|---|---|
| 0 | fondo + público | fondo + público + **cuerdas** (380 tiles) + árbitro (piezas 0-1) |
| 1 | fondo + público | fondo + público + **cuerdas** (11 tiles) + **HUD** + árbitro (pieza 2) |
| 2 | Duggan + Macho/Hogan remapeados | **solo Duggan** |
| 3 | cuerdas + HUD (palR3) | **compañeros** (spr_pal 16..31, como s35) |

- Compañeros: tiles originales de las poses 449/450 (sin remap a la de Duggan; part_tiles ya no se usa), línea 3.
- Cuerdas: cada tile remapeado al color más cercano de la línea 0 ó 1 (la que menos error da); bits de paleta del mapa A cambiados. Casi todos los tonos existen exactos en la 0; faltan 0x00A, 0xAAA, 0x222, 0x444 → aproximados.
- HUD: línea 1. Azul claro E44 → A00, azul oscuro 822 → 442, negro → índice 7 (000). No queda perfecto.
- Árbitro: pose 8 del arcade, (768,352), estático, prioridad ALTA, sin interacción. Sus piezas ya venían en líneas 0/1 (paleta original). VRAM 1088 (28 t) y 1512 (9 t), huecos libres. En el centro-fondo la cabeza queda bajo la ventana del HUD.
- Sin tocar: posiciones, prioridad, clamps, esquineros, logo, controles, sonido.

Shots: shots/b57_companeros.png, shots/b57_arbitro.png. MAME arranca OK; no probado en hardware.
