# b79 — base b78 conservada

ROM: `wwf_b79.bin` (1.572.864 bytes).
Base intacta: `/workspace/b78/wwf_b78.bin`, MD5 `baa09bf2c1316b25c6881ca0ec0a4019`.

**Único cambio:** vibración **corta** de la cuerda al chocar y caer con redibujo real de tiles (arcade). El rebote corriendo (secuencia larga `sc0`/`sc1`) no se toca.

## Problema en b78

`bounceRope(..., 1)` ponía `rk=48` dentro de `sc[]`. Eso cae en la fase tardía 6↔7 del timeline largo, **no** en el arranque arcade del paso 2. Emilio: la cuerda no se animaba (como vibración de choque).

## Arcade (analisis)

- **0x9700 `marcar_cuerda`**: bit15 + nibble `d0` en `1C1898`/`1C189A`. Siempre reinicia.
- **0x21324 `cuerda_vibrar`**: si bit15 y nibble≠0 → **paso 2**, dur `0x213A4[2]=6`, frame reg=3.
- **0x213A4**: `10 08 06 04 03 02 02 01`.
- **0x2146e** (índice de mapa por paso): `00 01 02 01 02 01 02 03`.
- **0x213B4 → 0x21412/0x21420**: si vibra y cambió el índice, copia el bloque de tiles del lado golpeado.

Corta (pasos 2..7): mapas **2,1,2,1,2,3** y luego reposo. Ticks 6+4+3+2+2+1=18 (×2 en el port = 36 frames).

Quién pide corta: **0x9F02** y **0xF9B0** con `d0=1`. Larga: **0x960A** con `d0=0`.

## Port b79

- `rFall`/`rStep`/`rTimer` + tablas `ropeDurA` / `ropeMapA`.
- Caída: reinicia siempre (como bit15), mapa inicial 2, `ropeDraw` inmediato.
- Tick corto: avanza pasos 2..7; al acabar restaura mapa 0 y redibuja.
- Caída `bounceRope(..., 0)` / `sc[]` sin cambios.

## Validación

Test MAME `rope` (x=627): `rcur` recorre 2→1→2→1→2→0 en el lado izquierdo. Caps: `shots/b79_rope_frames_arcade_short.png`, diffs `b79_diff_rest_vs_map2.png`, `b79_diff_map2_vs_map1.png`.

## Compilación

SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` en `/workspace/b79`. b78 no sobrescrito.
