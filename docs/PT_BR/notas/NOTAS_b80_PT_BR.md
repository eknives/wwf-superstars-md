# b80 — base b79 conservada

ROM: `wwf_b80.bin` (1.572.864 bytes).
MD5: `d843bac410485579980872341264fda9`
Base intacta: `/workspace/b79/wwf_b79.bin`, MD5 `80c22913744ca241ac6a4673d64b7a09`.

**Única mudança:** ao escapar do pin (kickout) perto das cordas, a corda vibra com a sequência **curta** do arcade. O rebote correndo (longa) e a máquina curta da b79 não são mexidos.

## Problema na b79 (teste do Emilio)

Contagem perto das cordas → kickout → o arremessado bate na corda, mas a corda **não se anima**.

Causa: o arremesso do kickout usa ação 8 sub **0x1C** (`fs==1`, arcade `0xB012` → `0x9B66`). Na b79 só se verificava a corda com `fs==2` (sub 1). O sub 0x1C voava, fazia clamp na borda e ao tocar o chão passava para sub 0xC (`fs==4`) **sem** chamar `marcar_cuerda`.

## Arcade (analisis)

- **0xB012 `acc_alzar_lanzar`**: após 2 passos quem cobria → ação 8 sub **0x1C**; o coberto → ação 5.
- **0x9B66**: init do sub 0x1C (texto 0x9B, impulso ±0x10, física tabela).
- **0x9CD0** (cada frame no ar, após `0x9E78`): se `+0x9E&3` (contato com a corda):
  - se `+0x44 == 0x1C` → `+0x44 = 1` (passa para sub 1) e reinicia a ação 8;
  - se não → `+0x44 = 2` (sub 2 = **0x9F02**).
- **0x9F02**: `moveq #1,d0` → **0x9700 `marcar_cuerda`** (nibble≠0).
- **0x21324 `cuerda_vibrar`**: nibble≠0 → começa no **passo 2** (sequência curta; b79).

Quem já pedia curta no port: **0x9F02** (queda `fs==2→3`) e **0xF9B0** (chave). Faltava o elo **0x9CD0** para o kickout 0x1C.

## Port b80

Em `fsStep`, depois de mover o X do sub 0x1C:

```
if (fs==1 && fsRope) fs=2;          /* 0x9CD0: 0x1C → 1 */
if (fs==2 && fsRope) { fs=3; bounceRope(..., 1); }  /* 0x9CD0 → 0x9F02 */
```

Mesma máquina curta da b79 (`rFall` / `ropeMapA` / `ropeDurA`). `bounceRope(..., 0)` (rebote correndo) intacto.

## Validação

Teste MAME natural `t80_korope_nat.lua` (pin junto à corda esq., primeiro kickout, sem forçar ox):

| ROM | Ao arremessar | Resultado |
|-----|-----------|-----------|
| b79 | `fs=1 rFall=0 rcur=0` | `FAIL_no_rope_vib` |
| b80 | `fs=3 rFall=1 rcur=2` | `ok_rope_vib` caminho curto 2→1→2→1→2→…→0 |

Capturas: `shots/b80_01_kickout_start.png`, `b80_02_kickout_hit_rope_rc2.png`, `b80_03_vib_start_rc2.png`, `b80_ko_df015_rc1.png` (corda arqueada), `b80_rope_kickout_strip.png`.

## Compilação

SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` em `/workspace/b80`. Só muda `src/main.c`. b79 não sobrescrita.
