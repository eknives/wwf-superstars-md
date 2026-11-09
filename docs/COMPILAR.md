# Compilar el port (b95)

## Entorno usado y verificado

| Componente | Versión | Notas |
|---|---|---|
| SGDK | **2.11** (abril 2025) | `GDK` apunta a su raíz (`makefile.gen`, `bin/`, `inc/`, `lib/`). |
| Toolchain | **m68k-elf-gcc 13.1.0** + binutils m68k-elf | En el `PATH` (`m68k-elf-gcc`, `m68k-elf-objcopy`…). |
| Java | **17** | Para `rescomp.jar` y `sizebnd.jar` de SGDK. |
| make | GNU make | Linux x86_64 (también debería funcionar en Windows con SGDK, sin probar). |
| MAME | **0.276** | Sólo para pruebas: `genesis` = NTSC, `megadriv` = PAL, `wwfsstar` = arcade. |

Si la instalación de SGDK no trae `lib/libmd.a`, compílala antes con `make -f $GDK/makelib.gen`.

## Paso a paso

1. **ROM propia.** Consigue legalmente el set MAME `wwfsstar`. No se distribuye aquí.
2. **Recursos.** Genera los 32 ficheros de `res/` y las 4 cabeceras de `src/gen/` con el extractor. **PENDIENTE**: la especificación está en `tools/extractor/README.md`. Las rutas que espera `res/res.res` son `res/graficos/...`, `res/datos/...` y `res/sonidos/...`.
3. **Compilar** en la raíz del repositorio:
   ```sh
   export PATH=/ruta/toolchain/bin:/ruta/jdk17/bin:$PATH
   make clean
   make GDK=/ruta/a/SGDK-2.11
   md5sum out/rom.bin
   ```
   **No uses `make -B`**: la plantilla de SGDK puede sobrescribir `src/main.c`.
4. **Comprobar.**
   - Con los recursos exactos de b95 (incluidas las ediciones de Emilio en esquineros y logo, que no se publican), el MD5 es `7be789d70d892c1efb86af8630b296a6`. Verificado el 9-11-2026 con esta misma estructura (`src/gen/`).
   - Con recursos extraídos sólo del arcade, el fondo será el original y el MD5 será distinto.
5. **Probar** en MAME: `mame genesis -cart out/rom.bin` (o `megadriv` para PAL). En hardware real, con un flashcart (Everdrive): aún sin verificar en b95. Las pruebas automáticas están en `tools/mame/`.

## Comprobar sólo que compila (sin ROM arcade)

- Crea cada fichero de `res/` del tamaño de la tabla de `tools/extractor/README.md`, lleno de ceros. Los `.wav` deben ser WAV PCM válidos con silencio.
- Crea las 4 cabeceras con las declaraciones de esa misma tabla, inicializadas a `{0}`.
- `make` termina sin errores y genera una ROM de 1.703.936 bytes que no tiene gráficos ni sonido útiles. Probado el 9-11-2026: en MAME (`genesis`) la pantalla sale completamente negra en los frames 300 y 900.
- Los dos `.wav` deben ser mono, de 16 bits, a 8000 Hz y con 32768 muestras. Con otro formato también compila, pero la ROM cambia de tamaño.

## Memoria de vídeo y tamaño

ROM de 1.703.936 bytes (alineada a 128 KB por `sizebnd`). Mapa VRAM, en `main()`: BG_B 0xE000, BG_A 0xC000, Window 0xD000, sprites 0xF000, HScroll 0xF800.
