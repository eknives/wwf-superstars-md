# b79 — base b78 conservada

ROM: `wwf_b79.bin` (1.572.864 bytes).
Base intacta: `/workspace/b78/wwf_b78.bin`, MD5 `baa09bf2c1316b25c6881ca0ec0a4019`.

**Única mudança:** vibração **curta** da corda ao bater e cair com redesenho real de tiles (arcade). O rebote correndo (sequência longa `sc0`/`sc1`) não é mexido.

## Problema na b78

`bounceRope(..., 1)` punha `rk=48` dentro de `sc[]`. Isso cai na fase tardia 6↔7 da timeline longa, **não** no início do arcade no passo 2. Emilio: a corda não se animava (como vibração de choque).

## Arcade (analisis)

- **0x9700 `marcar_cuerda`**: bit15 + nibble `d0` em `1C1898`/`1C189A`. Sempre reinicia.
- **0x21324 `cuerda_vibrar`**: se bit15 e nibble≠0 → **passo 2**, dur `0x213A4[2]=6`, frame reg=3.
- **0x213A4**: `10 08 06 04 03 02 02 01`.
- **0x2146e** (índice de mapa por passo): `00 01 02 01 02 01 02 03`.
- **0x213B4 → 0x21412/0x21420**: se vibra e o índice mudou, copia o bloco de tiles do lado atingido.

Curta (passos 2..7): mapas **2,1,2,1,2,3** e depois repouso. Ticks 6+4+3+2+2+1=18 (×2 no port = 36 frames).

Quem pede curta: **0x9F02** e **0xF9B0** com `d0=1`. Longa: **0x960A** com `d0=0`.

## Port b79

- `rFall`/`rStep`/`rTimer` + tabelas `ropeDurA` / `ropeMapA`.
- Queda: reinicia sempre (como bit15), mapa inicial 2, `ropeDraw` imediato.
- Tick curto: avança passos 2..7; ao terminar restaura o mapa 0 e redesenha.
- Queda `bounceRope(..., 0)` / `sc[]` sem mudanças.

## Validação

Teste MAME `rope` (x=627): `rcur` percorre 2→1→2→1→2→0 no lado esquerdo. Caps: `shots/b79_rope_frames_arcade_short.png`, diffs `b79_diff_rest_vs_map2.png`, `b79_diff_map2_vs_map1.png`.

## Compilação

SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` em `/workspace/b79`. b78 não sobrescrita.
