# b78 — base b77 conservada

ROM: `wwf_b78.bin` (1.572.864 bytes).
Base intacta: `/workspace/b77/wwf_b77.bin`, MD5 `947bdf6ccc66d33c7d9ecc526e3e8e97`.

**Único cambio:** la vibración de la cuerda al **chocar y caer** usa la secuencia corta del arcade (empieza en el paso 2 / frame 3). El rebote corriendo (secuencia larga) no se toca.

## Arcade

Fuentes: `analisis/arc_rec.dis`, `analisis/rutinas.md`, `analisis/tools/prog.bin`.

- **0x9700 `marcar_cuerda`**: pone bit15 y el nibble bajo = `d0` en `1C1898` / `1C189A` (lado).
- **0x21324 `cuerda_vibrar`**: si bit15, arranca sonido 0x2A y bit14=vibrando.
  - nibble `d0 == 0` → paso **0**, frame **1** (secuencia larga).
  - nibble `d0 != 0` → paso **2**, frame **3** (secuencia corta).
  - Avanza hasta el paso 8 con duraciones **0x213A4** = `10 08 06 04 03 02 02 01` (42 ticks) y frames **0x213AC** = `01 02 03 02 03 02 03 00` (&3).
- Quién pide qué:
  - **0x960A** rebote corriendo: `moveq #0,d0` → `0x9700` → larga.
  - **0x9F02** choque y caer: `moveq #1,d0` → `0x9700` → corta.
  - **0xF9B0** caída en llave pegada a la cuerda: `move.w #1,d0` → `0x9700` → corta.

Desde el paso 2: `6+4+3+2+2+1 = 18` ticks. Pasos 0+1: `16+8 = 24` ticks.

## Port

`bounceRope` antes ponía siempre `rk[sd]=0` (larga). Ahora:

- `fall==0` (correr / contacto de whip): `rk=0` (igual que b77).
- `fall==1` (0x9F02 y 0xF9B0): `rk=48`.

`sc0`/`sc1` tienen `NS=84 = 2×42`. Saltar pasos 0+1 = `2×(0x10+0x08) = 48`; quedan `2×18 = 36` frames de vibración corta. No se han cambiado tiles, mapas ni la animación larga.

Llamadas:
- `bounceRope(..., 1)`: caída `fs` contra cuerda (0x9F02) y caída en llave 0xF9B0.
- `bounceRope(..., 0)`: rebote al correr y contacto de la víctima en el whip.

## Compilación

- SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`.
- `make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk` en `/workspace/b78`.
- Solo se recompiló `src/main.c`; recursos idénticos a b77.
- b77 no se ha sobrescrito.

## Límites

No se ha tocado la física de la caída, el enganche, el árbitro ni el zafar del pin. Solo el arranque de la animación de cuerda en las rutas de choque-y-caer.
