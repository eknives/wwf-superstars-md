# b85 (base b84, md5 426988a7344009ffd63ad6e8f34e609b; b84 intacta)

ROM: `wwf_b85.bin`, md5 `0477ea3fbf29e81b98a79ca1d574abf0`. Compilação SGDK local.
Só a sequência/combo completa de socos do arcade (FD70+FD7C) para Duggan e Warrior. Sem IA, sem outros movimentos.

## O que o Emilio pedia
A b84 só fez FD70 (um soco: 0x150–0x152). Um combo **é** a sequência: é preciso portar também FD7C (0x153–0x155), idêntico ao arcade.

## Arcade (citações, prog.bin)
| Addr | O quê |
|------|-----|
| 0xFC84 | `sub_combo_golpes` — 3 passos; com o botão 1 no final faz `eori #$1,$c0` e repete |
| 0xFD70 | Soco são: `0x150`×4, `0x151`×3, `0x152`×3 (10 f) |
| 0xFD7C | Alternativa combo: `0x153`×4, `0x154`×3, `0x155`×3 (10 f) — usa-se com +0xC0 bit0 |
| 0xFD88/0xFD94 | Variante id 7 (André) — não se aplica a Duggan/Warrior |

Conteúdo (versão pública, sem dump de bytes): FD70 = poses 0x150, 0x151, 0x152 com esperas 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 com esperas 4, 3, 3.

## Correção b85
1. **Poses novas** (`tools/gen85_punch.py`, mesmo método/cmap que gen76/gen84):
   - Duggan banco 3: 793=`0x153`, 795=`0x154`, 797=`0x155` (792=`0x152` já na b84)
   - Warrior banco 0: 794=`0x153`, 796=`0x154`, 798=`0x155` (658/657/765 = 0x150/151/152 já na b84)
2. **Motores** 169/170/171 → xl_w/xl_d para essas poses.
3. **`move_seq`**: `[0..9]=FD70` (41×4,40×3,168×3); `[10..19]=FD7C` (169×4,170×3,171×3); o chute continua em 33.
4. **`main.c`**: `pAlt` (= +0xC0 bit0). Metade L=10; `so = pAlt?10:0`. Ao terminar a metade, se A continua pressionado (`joyHeld`) → `pAlt^=1; mk=0` (encadeia). Se não → idle e `pAlt=0`. Um toque curto = só FD70.

## Verificação MAME Genesis
| Modo | Resultado |
|------|-----------|
| tap A (2 f) | motores 41→40→168; sem 169–171; pAlt final 0 |
| holdD | 41×4,40×3,168×3 → 169×4,170×3,171×3 → alterna enquanto A |
| holdW (ctl=1) | poses Warrior 658→657→765→794→796→798 (0x150–0x155) |

## Capturas
- `shots/b85/{duggan,warrior}_{150..155}.png`
- `shots/b85/{duggan,warrior}_combo_*.png` (hold)
- `test/t85_pun.lua`, `test/t85_tap.lua`

## Ressalvas
- Não se porta o caminho CPU 0x15878 (40 f / durações ×6).
- André (FD88/FD94) fora do escopo.
- Paleta das poses novas via cmap (pode diferir 1–2 índices do MD canônico).
- Um frame de hold da última pose ao encadear (como o reset `$8=1` do arcade).

## Reproduzir
```sh
cd /workspace/b85
python3 tools/gen85_punch.py   # si hay que regenerar assets
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b85.bin && md5sum wwf_b85.bin
T85=holdD mame genesis -cart wwf_b85.bin -autoboot_script test/t85_pun.lua ...
```
(O comentário significa: se for preciso regenerar os assets.)
