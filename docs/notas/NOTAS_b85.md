# b85 (base b84, md5 426988a7344009ffd63ad6e8f34e609b; b84 intacta)

ROM: `wwf_b85.bin`, md5 `0477ea3fbf29e81b98a79ca1d574abf0`. Compilación SGDK local.
Solo la secuencia/combo completa de puñetazos arcade (FD70+FD7C) para Duggan y Warrior. Sin IA, sin otros movimientos.

## Qué pedía Emilio
b84 solo hizo FD70 (un puñetazo: 0x150–0x152). Un combo **es** la secuencia: hay que portar también FD7C (0x153–0x155) e idéntico al arcade.

## Arcade (citas, prog.bin)
| Addr | Qué |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 pasos; con botón 1 al final hace `eori #$1,$c0` y repite |
| 0xFD70 | Punch sano: `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Alternativa combo: `0x153`×4, `0x154`×3, `0x155`×3 (10 f) — se usa con +0xC0 bit0 |
| 0xFD88/0xFD94 | Variante id 7 (André) — no aplica a Duggan/Warrior |

Contenido (versión pública, sin volcado de bytes): FD70 = poses 0x150, 0x151, 0x152 con esperas 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 con esperas 4, 3, 3.

## Arreglo b85
1. **Poses nuevas** (`tools/gen85_punch.py`, mismo método/cmap que gen76/gen84):
   - Duggan banco 3: 793=`0x153`, 795=`0x154`, 797=`0x155` (792=`0x152` ya en b84)
   - Warrior banco 0: 794=`0x153`, 796=`0x154`, 798=`0x155` (658/657/765 = 0x150/151/152 ya en b84)
2. **Motores** 169/170/171 → xl_w/xl_d a esas poses.
3. **`move_seq`**: `[0..9]=FD70` (41×4,40×3,168×3); `[10..19]=FD7C` (169×4,170×3,171×3); kick sigue en 33.
4. **`main.c`**: `pAlt` (= +0xC0 bit0). Mitad L=10; `so = pAlt?10:0`. Al terminar la mitad, si A sigue pulsado (`joyHeld`) → `pAlt^=1; mk=0` (encadena). Si no → idle y `pAlt=0`. Un toque corto = solo FD70.

## Verificación MAME Genesis
| Modo | Resultado |
|------|-----------|
| tap A (2 f) | motores 41→40→168; sin 169–171; pAlt final 0 |
| holdD | 41×4,40×3,168×3 → 169×4,170×3,171×3 → alterna mientras A |
| holdW (ctl=1) | poses Warrior 658→657→765→794→796→798 (0x150–0x155) |

## Capturas
- `shots/b85/{duggan,warrior}_{150..155}.png`
- `shots/b85/{duggan,warrior}_combo_*.png` (hold)
- `test/t85_pun.lua`, `test/t85_tap.lua`

## Caveats
- No se porta el camino CPU 0x15878 (40 f / duraciones ×6).
- André (FD88/FD94) fuera de alcance.
- Paleta de poses nuevas vía cmap (puede diferir 1–2 índices del MD canónico).
- Un frame de hold de la última pose al encadenar (como el reset `$8=1` del arcade).

## Reproducir
```sh
cd /workspace/b85
python3 tools/gen85_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b85.bin && md5sum wwf_b85.bin
T85=holdD mame genesis -cart wwf_b85.bin -autoboot_script test/t85_pun.lua ...
```
