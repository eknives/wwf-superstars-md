# b84 (base b83, md5 028b1ee1de56104bb26ab5fc56810c80; b83 intacta)

ROM: `wwf_b84.bin`, md5 `426988a7344009ffd63ad6e8f34e609b`. Compilação SGDK local.
Só completar a sequência de socos em pé (A) do Duggan e do Warrior. Sem IA, sem outros movimentos.

## Erro (o que o Emilio viu)
- **Warrior:** desde a b76 o impacto esticava o braço (`xl_w[41]=765` = arcade banco 0 pose `0x152`), mas a sequência pulava o wind-up `0x150` e não seguia a ordem FD70.
- **Duggan:** `move_seq` fazia idle → pose 40 (`0x151`) → pose 41 (`0x150`) em 33 f; faltava a terceira pose do arcade `0x152` e a ordem/tempos não eram os de FD70.

## Arcade (citações)
| Addr | O quê |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 passos de tabela |
| 0xFD70 | Soco são: pose `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Alternativa de combo (`0x153`–`0x155`) ao manter/encadear A — **não portada na b84** |
| Banco 0 | Warrior: `0x150`/`0x151`/`0x152` |
| Banco 3 | Duggan: mesmos índices no seu banco |

## Correção b84
1. **Pose nova 792** = Duggan banco 3 pose `0x152` (`tools/gen84_punch.py`, mesmo método/cmap que gen76).
2. **Motor 168** (u8 livre em `move_seq`): `xl_d[168]=792`, `xl_w[168]=765` (Warrior `0x152`).
3. **`xl_w[41]=658`** (Warrior `0x150`; antes 765). `xl_w[40]=657` (Warrior `0x151`, sem mudança).
4. **`move_seq[0..9]`** = `41×4, 40×3, 168×3` (FD70). Resto do bloco de 33 f = 0 (padding; o chute continua no offset 33).
5. **`main.c`:** `L` soco = 10; `MV_HIT_PUN` = 10 (primeiro frame de `0x152`).

## Verificação MAME Genesis (test/t84_pun.lua)
| Modo | Sequência dPose | Hit |
|------|-----------------|-----|
| punD (Duggan) | 41 → 40 → 792 | vh Warrior=1 em mk=10 |
| pun (Warrior, C) | 658 → 657 → 765 | vh Duggan=1 ao chegar a 765 |

## Capturas
- `shots/b84/warrior_{150,151,152}.png`
- `shots/b84/duggan_{150,151,152}.png`
- `shots/b84/ref_mame_warrior_punch.jpg` (ref do Emilio)

## Ressalva
- Não se portou o encadeamento FD7C (`0x153`–`0x155`) nem o caminho CPU 0x15878 (40 f). Um A = um soco FD70.
- Paleta da pose 792: cmap via cmap gen76 (não inventada; pode diferir 1–2 índices do MD canônico).

## Reproduzir
```sh
cd /workspace/b84
python3 tools/gen84_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b84.bin && md5sum wwf_b84.bin
T84=punD mame genesis -cart wwf_b84.bin -autoboot_script test/t84_pun.lua ...
```
(O comentário significa: se for preciso regenerar os assets.)
