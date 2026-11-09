# b80 — base b79 conservada

ROM: `wwf_b80.bin` (1.572.864 bytes).
MD5: `d843bac410485579980872341264fda9`
Base intacta: `/workspace/b79/wwf_b79.bin`, MD5 `80c22913744ca241ac6a4673d64b7a09`.

**Único cambio:** al zafarse del pin (kickout) cerca de las cuerdas, la cuerda vibra con la secuencia **corta** arcade. El rebote corriendo (larga) y la máquina corta de b79 no se tocan.

## Problema en b79 (test de Emilio)

Cuenta cerca de las cuerdas → kickout → el lanzado choca con la cuerda, pero la cuerda **no se anima**.

Causa: el lanzado del kickout usa acción 8 sub **0x1C** (`fs==1`, arcade `0xB012` → `0x9B66`). En b79 solo se comprobaba cuerda con `fs==2` (sub 1). El sub 0x1C volaba, hacía clamp en el borde y al tocar suelo pasaba a sub 0xC (`fs==4`) **sin** llamar a `marcar_cuerda`.

## Arcade (analisis)

- **0xB012 `acc_alzar_lanzar`**: tras 2 pasos el que cubría → acción 8 sub **0x1C**; el cubierto → acción 5.
- **0x9B66**: init del sub 0x1C (texto 0x9B, impulso ±0x10, física tabla).
- **0x9CD0** (cada frame en el aire, tras `0x9E78`): si `+0x9E&3` (contacto cuerda):
  - si `+0x44 == 0x1C` → `+0x44 = 1` (pasa a sub 1) y reinicia acción 8;
  - si no → `+0x44 = 2` (sub 2 = **0x9F02**).
- **0x9F02**: `moveq #1,d0` → **0x9700 `marcar_cuerda`** (nibble≠0).
- **0x21324 `cuerda_vibrar`**: nibble≠0 → empieza en **paso 2** (secuencia corta; b79).

Quién ya pedía corta en el port: **0x9F02** (caída `fs==2→3`) y **0xF9B0** (llave). Faltaba el eslabón **0x9CD0** para el kickout 0x1C.

## Port b80

En `fsStep`, tras mover X del sub 0x1C:

```
if (fs==1 && fsRope) fs=2;          /* 0x9CD0: 0x1C → 1 */
if (fs==2 && fsRope) { fs=3; bounceRope(..., 1); }  /* 0x9CD0 → 0x9F02 */
```

Misma máquina corta de b79 (`rFall` / `ropeMapA` / `ropeDurA`). `bounceRope(..., 0)` (rebote corriendo) intacto.

## Validación

Test MAME natural `t80_korope_nat.lua` (pin junto a cuerda izq, primer kickout, sin forzar ox):

| ROM | Al lanzar | Resultado |
|-----|-----------|-----------|
| b79 | `fs=1 rFall=0 rcur=0` | `FAIL_no_rope_vib` |
| b80 | `fs=3 rFall=1 rcur=2` | `ok_rope_vib` path corta 2→1→2→1→2→…→0 |

Capturas: `shots/b80_01_kickout_start.png`, `b80_02_kickout_hit_rope_rc2.png`, `b80_03_vib_start_rc2.png`, `b80_ko_df015_rc1.png` (cuerda arqueada), `b80_rope_kickout_strip.png`.

## Compilación

SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`, `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` en `/workspace/b80`. Solo cambia `src/main.c`. b79 no sobrescrito.
