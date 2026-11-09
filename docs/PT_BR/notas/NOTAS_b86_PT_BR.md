# b86 (base b85, md5 0477ea3fbf29e81b98a79ca1d574abf0; b85 intacta)

ROM: `wwf_b86.bin`. Compilação SGDK local (`PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`).
Só: (1) timing arcade dos socos, (2) combo por **pressionamentos** (não hold), (3) Clothesline com hit + reação do rival. Sem IA, sem outros movimentos.

## O que o Emilio pedia
A b85 encadeava FD70↔FD7C com **hold** (`joyHeld`) e ficava rápido demais. No arcade não se mantém A: são vários pressionamentos. Além disso, os Clotheslines de ambos não tinham colisão nem reação.

## Arcade (citações)

### Socos — `sub_combo_golpes` 0xFC84
| Addr | O quê |
|------|-----|
| 0xFC84 | Três passos; nos passos `+0x36==0xB/0xC` faz `OR +0x114 → +0x22` (**recém-pressionados**, não hold) |
| 0xFD2E | Ao terminar: se `+0x22 & 3 == 1` (só o botão 1) → `eori #$1,+0xC0` e repete; se não → ação 0 |
| 0xFD70 | Soco são: `0x150`×4, `0x151`×3, `0x152`×3 |
| 0xFD7C | Alternativa: `0x153`×4, `0x154`×3, `0x155`×3 |
| 0xFD48 | Ao encadear: `$8=1` (carrega a 1ª pose da outra metade no frame seguinte) |

Conteúdo (versão pública, sem dump de bytes): FD70 = poses 0x150, 0x151, 0x152 com esperas 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 com esperas 4, 3, 3.

GameFAQs: `Punch = P (1 after 3 Punches)` → após as 3 poses de uma metade, outro pressionamento de P continua.

### Clothesline — corrida A → sub 0x14
| Addr | O quê |
|------|-----|
| 0x93EE | `acc_correr`: 0xCC26 pode lançar golpe correndo |
| 0xCD14 | A na corrida: Warrior/Duggan → sub **0x14** |
| 0xFB58+0x14*4 | → `0x12E7A` `sub_carrera_hombro` |
| 0x1302E | Poses da investida: `0x1D0`×6, `0x1D1`×4, `0x1DA`×4, `0x1DB`×6, … |
| 0x12E7A | Conecta antes do passo 0x10 (+0xC9 bit3); no passo 0xC o rival → ação **8** sub **0x17** |
| 0x9B9A | `rec_lanzado_20` (impulso 0x20) |
| 0x16634 | Filtro de proximidade da colisão: \|dx\|<0x60, \|dy\|<8 |

GameFAQs: `Clothesline = P (2)` na corrida.

## Correção b86
1. **Combo por pressionamentos:** `pAcc` (= +0x22). Durante a última pose (mk 10..12 = 0x152/0x155) acumula-se a borda de A (`pendBtn`, já é +0x114). Ao terminar a metade: só se `(pAcc & (A|B)) == A` → `pAlt^=1; mk=2` (equiv. `$8=1`). O hold **já não** encadeia.
2. **Timing:** mantêm-se as durações FD70/FD7C (4+3+3) em `move_seq`; não se inventam multiplicadores. O ritmo percebido diminui porque é preciso pressionar de novo entre as metades.
3. **Hit do Clothesline:** em `rn==3`, se `rnk∈[1,20]` e o rival estiver a ≤0x60/≤8: `vdmg+=2`, `fsStart(o,1,…)` = queda arremessada (ação 8 / `rec_lanzado_20`). `rnW` evita multi-hit. Ambos os lutadores (mesmo motor).

## Ressalvas
- Não se porta o caminho CPU 0x15878 nem o André (FD88/FD94).
- A animação do Clothesline atacante continua sendo a trilha MD `atkR/atkL` (já na b83+); não se regeneram as poses 0x1D0–0x1DB do arcade.
- `fsStart(...,1,...)` usa o impulso do port (arremessado); o arcade sub 0x17 é 0x20 exato nos parâmetros A74A — aproximação do sistema de quedas já portado.
- Um frame de sobreposição ao encadear (como o `$8=1` do arcade).

## Reproduzir
```sh
cd /workspace/b86
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b86.bin && md5sum wwf_b86.bin
```

Teste manual: um toque de A = só FD70 (0x150–152). Segundo toque de A durante a última pose → FD7C. Hold sem soltar não deve encadear. A+B na corrida → corrida; só A na corrida → Clothesline; ao conectar o rival sai voando/cai.
