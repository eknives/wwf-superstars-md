# b84 (base b83, md5 028b1ee1de56104bb26ab5fc56810c80; b83 intacta)

ROM: `wwf_b84.bin`, md5 `426988a7344009ffd63ad6e8f34e609b`. Compilación SGDK local.
Solo completar la secuencia de puñetazos de pie (A) de Duggan y Warrior. Sin IA, sin otros movimientos.

## Fallo (lo que Emilio vio)
- **Warrior:** desde b76 el impacto estiraba el brazo (`xl_w[41]=765` = arcade banco 0 pose `0x152`), pero la secuencia saltaba el wind-up `0x150` y no seguía el orden FD70.
- **Duggan:** `move_seq` hacía idle → pose 40 (`0x151`) → pose 41 (`0x150`) en 33 f; faltaba la tercera pose arcade `0x152` y el orden/tiempos no eran los de FD70.

## Arcade (citas)
| Addr | Qué |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 pasos de tabla |
| 0xFD70 | Punch sano: pose `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Alternativa de combo (`0x153`–`0x155`) al mantener/encadenar A — **no portada en b84** |
| Banco 0 | Warrior: `0x150`/`0x151`/`0x152` |
| Banco 3 | Duggan: mismos índices en su banco |

## Arreglo b84
1. **Pose nueva 792** = Duggan banco 3 pose `0x152` (`tools/gen84_punch.py`, mismo método/cmap que gen76).
2. **Motor 168** (u8 libre en `move_seq`): `xl_d[168]=792`, `xl_w[168]=765` (Warrior `0x152`).
3. **`xl_w[41]=658`** (Warrior `0x150`; antes 765). `xl_w[40]=657` (Warrior `0x151`, sin cambio).
4. **`move_seq[0..9]`** = `41×4, 40×3, 168×3` (FD70). Resto del bloque de 33 f = 0 (padding; kick sigue en offset 33).
5. **`main.c`:** `L` punch = 10; `MV_HIT_PUN` = 10 (primer frame de `0x152`).

## Verificación MAME Genesis (test/t84_pun.lua)
| Modo | Secuencia dPose | Hit |
|------|-----------------|-----|
| punD (Duggan) | 41 → 40 → 792 | vh Warrior=1 en mk=10 |
| pun (Warrior, C) | 658 → 657 → 765 | vh Duggan=1 al llegar a 765 |

## Capturas
- `shots/b84/warrior_{150,151,152}.png`
- `shots/b84/duggan_{150,151,152}.png`
- `shots/b84/ref_mame_warrior_punch.jpg` (ref Emilio)

## Caveat
- No se ha portado el encadenado FD7C (`0x153`–`0x155`) ni el camino CPU 0x15878 (40 f). Un A = un puñetazo FD70.
- Paleta de la pose 792: cmap via cmap gen76 (no inventada; puede diferir 1–2 índices del MD canónico).

## Reproducir
```sh
cd /workspace/b84
python3 tools/gen84_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b84.bin && md5sum wwf_b84.bin
T84=punD mame genesis -cart wwf_b84.bin -autoboot_script test/t84_pun.lua ...
```
