# b78 — base b77 conservada

ROM: `wwf_b78.bin` (1.572.864 bytes).
Base intacta: `/workspace/b77/wwf_b77.bin`, MD5 `947bdf6ccc66d33c7d9ecc526e3e8e97`.

**Única mudança:** a vibração da corda ao **bater e cair** usa a sequência curta do arcade (começa no passo 2 / frame 3). O rebote correndo (sequência longa) não é mexido.

## Arcade

Fontes: `analisis/arc_rec.dis`, `analisis/rutinas.md`, `analisis/tools/prog.bin`.

- **0x9700 `marcar_cuerda`**: põe o bit15 e o nibble baixo = `d0` em `1C1898` / `1C189A` (lado).
- **0x21324 `cuerda_vibrar`**: se bit15, inicia o som 0x2A e bit14=vibrando.
  - nibble `d0 == 0` → passo **0**, frame **1** (sequência longa).
  - nibble `d0 != 0` → passo **2**, frame **3** (sequência curta).
  - Avança até o passo 8 com durações **0x213A4** = `10 08 06 04 03 02 02 01` (42 ticks) e frames **0x213AC** = `01 02 03 02 03 02 03 00` (&3).
- Quem pede o quê:
  - **0x960A** rebote correndo: `moveq #0,d0` → `0x9700` → longa.
  - **0x9F02** bater e cair: `moveq #1,d0` → `0x9700` → curta.
  - **0xF9B0** queda numa chave colada à corda: `move.w #1,d0` → `0x9700` → curta.

A partir do passo 2: `6+4+3+2+2+1 = 18` ticks. Passos 0+1: `16+8 = 24` ticks.

## Port

`bounceRope` antes punha sempre `rk[sd]=0` (longa). Agora:

- `fall==0` (correr / contato do whip): `rk=0` (igual à b77).
- `fall==1` (0x9F02 e 0xF9B0): `rk=48`.

`sc0`/`sc1` têm `NS=84 = 2×42`. Pular os passos 0+1 = `2×(0x10+0x08) = 48`; restam `2×18 = 36` frames de vibração curta. Não foram mudados tiles, mapas nem a animação longa.

Chamadas:
- `bounceRope(..., 1)`: queda `fs` contra a corda (0x9F02) e queda numa chave 0xF9B0.
- `bounceRope(..., 0)`: rebote ao correr e contato da vítima no whip.

## Compilação

- SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`.
- `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` em `/workspace/b78`.
- Só se recompilou `src/main.c`; recursos idênticos aos da b77.
- A b77 não foi sobrescrita.

## Limites

Não foram mexidos a física da queda, a pegada, o árbitro nem o escape do pin. Só o início da animação da corda nas rotas de bater-e-cair.
