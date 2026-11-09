# WWF Superstars (arcade) → Sega Mega Drive — port aficionado

Port del arcade *WWF Superstars* (Technōs, 1989) a Mega Drive / Genesis, escrito desde cero en C con SGDK. El objetivo es que el port sea notablemente igual al arcade: mismos tiempos, física, colisiones, reacciones y poses, comprobados con MAME y con el código del arcade.

Idiomas: **español (original)** · [Português (Brasil)](README_PT_BR.md) · [English](README_ENG.md). En las notas manda el original en español; las traducciones llevan el sufijo `_PT_BR` o `_ENG`.

## Aviso legal

- Proyecto aficionado, **gratuito y sin ánimo de lucro**. Port hecho con ayuda de IA. No se puede vender ni distribuir con fines comerciales.
- **Sin afiliación**: no está afiliado ni respaldado por los titulares de *WWF Superstars*.
- **Las marcas, personajes, nombres, gráficos, música y sonido pertenecen a sus dueños.**
- El repositorio **no contiene ninguna ROM ni material con copyright**: ni gráficos, ni sonido, ni paletas, ni mapas, ni tablas de datos extraídas, ni el desensamblado. Sólo nuestro código, nuestras notas y nuestras herramientas.
- **Para compilar hace falta una ROM propia, obtenida legalmente** (set MAME `wwfsstar`), de la que se extraerán los recursos.
- Nuestro código y notas: licencia MIT ([LICENSE](LICENSE)). Los ficheros de arranque `src/boot/` proceden de SGDK (MIT, © Stephane Dallongeville).

## Estado actual: b95 (9-11-2026)

- Se juega con 2 luchadores humanos: **Duggan** y **Warrior** (mando de 6 botones: A = puño, B = patada, C = A+B, Y = cambia el luchador controlado; START = el rival te sigue o se para). Hay pantalla de título y selección (SELECT PLAYERS); la selección todavía termina siempre en Duggan contra Warrior.
- Hecho y cotejado con MAME, con los límites de cada versión anotados en sus notas:
  - andar, carrera con rebote en cuerdas (b95: velocidad y ritmo del arcade, igual en PAL y NTSC);
  - salir y entrar del ring, subir al poste;
  - combo de puños, patada, clothesline;
  - Knee Drop de Warrior (suelo, poste y exterior), Stomp y Elbow Drop de Duggan (suelo y poste);
  - lanzamiento contra las cuerdas, energía interna con los daños del arcade;
  - pin con cuenta de 3, cuenta fuera de 20, árbitro, público, HUD;
  - choque contra la cuerda al zafarse del pin (b95 = arcade).
- Desde b95 el fondo se carga por DMA en cola y ya no se pierden frames junto a los postes.
- Lo que falta está en [docs/PENDIENTES.md](docs/PENDIENTES.md) (resumen más abajo).
- La última ROM (b95) tiene el MD5 `7be789d70d892c1efb86af8630b296a6`. Las ROMs no se publican.

## Importante: hoy el código no compila sin los recursos

El código está completo, pero **necesita recursos que salen de la ROM arcade**. No se publican y se generarán con un **extractor que todavía está PENDIENTE** ([tools/extractor/README.md](tools/extractor/README.md)). Hacen falta dos cosas:

- 32 ficheros en `res/` (30 `.bin` y 2 `.wav`): sprites, tiles, mapas, paletas, pistas de animación, público, selección, título y sonido;
- 4 cabeceras en `src/gen/`: `ropes.h`, `gs69.h`, `hud.h`, `select89_data.h`.

Mientras no exista el extractor:

- **Con los recursos reales** (backup privado del proyecto) la ROM da exactamente el MD5 de b95. Comprobado al preparar este repositorio, con `src/gen/` y los `#include` ya cambiados.
- **Con recursos a cero** (mismo tamaño) y las 4 cabeceras declaradas a cero, **compila sin errores** y sale una ROM del mismo tamaño, negra y sin contenido jugable. Sirve sólo para comprobar que el código compila.

**Las ediciones de Emilio no se publican**: los esquineros superiores y el logo WWF del fondo del ring. El extractor generará el fondo original del arcade, así que con él el MD5 no coincidirá con b95 en esa parte.

## Compilar (resumen; paso a paso en [docs/COMPILAR.md](docs/COMPILAR.md))

1. Instalar **SGDK 2.11**, **m68k-elf-gcc 13.1.0** (con binutils), **Java 17** (para `rescomp`) y `make`.
2. Generar `res/**` y `src/gen/*.h` desde tu set `wwfsstar` (extractor PENDIENTE).
3. `make GDK=/ruta/a/SGDK` → `out/rom.bin`. **No uses `make -B`**: la plantilla de SGDK puede sobrescribir `main.c`.
4. Probar en MAME 0.276 (`genesis` = NTSC, `megadriv` = PAL) o en hardware real.

## Método de trabajo

Resumen; las reglas completas están en [docs/REGLAS.md](docs/REGLAS.md).

1. **Primero el decompilado.** Localizar la rutina y las tablas del arcade, con su dirección (`docs/analisis/rutinas.md`, `tablas.md`, `ram.md`). No inventar números: cada valor se traza a una dirección o a una medida.
2. **Después MAME.** Medir el arcade (`wwfsstar`) y el port (`genesis`/`megadriv`) con scripts Lua: posiciones, ticks, poses, RAM. El arcade mueve la lógica de actor cada 2 refrescos (57,44 Hz → tick de 28,72 Hz); en la MD se usa `arcTick`. No hay que confundir ticks con frames de 60/50 Hz.
3. **Igualdad notable.** Al cerrar una técnica debe coincidir con el arcade en entrada, ritmo real, colisión, física, reacción, poses y paleta. No se da por verificado lo que no se ha medido.
4. **Los fallos del arcade se reproducen** (p. ej. la comparación de byte alto de `9CD0`); **no se inventan fallos nuevos**.
5. **Sólo lo pedido.** Cada versión va en carpeta nueva, la base queda intacta y se apuntan la ROM nueva y su MD5. Los estudios no autorizan cambios.
6. **Respetar lo existente:** el motor SGDK (ring, cuerdas en planos, prioridades), Hogan como referencia, paletas, esquineros y logo. No añadir IA nueva.

## Dónde están los hallazgos

- [docs/INDICE.md](docs/INDICE.md): índice maestro por tema y dirección. Es el punto de entrada.
- [docs/PATRON_MOVIMIENTOS.md](docs/PATRON_MOVIMIENTOS.md): receta común de los movimientos (selector → rutina → tablas → física/contacto → reacción). Incluye los estudios b93–b95: orientación del tumbado, pin, carrera, postes y cuerdas.
- [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md): cómo está organizado `src/main.c`.
- [docs/analisis/](docs/analisis/): mapa del programa arcade (rutinas, RAM, tablas, sistemas).
- [docs/estudios/](docs/estudios/): estudios a fondo de energía, Knee Drop, suelo de Duggan y selección.
- [docs/notas/](docs/notas/): nota de cada versión b49–b95. [docs/CHANGELOG.md](docs/CHANGELOG.md) es el resumen.
- [docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md](docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md): qué técnicas están hechas, a medias o faltan.
- [docs/ESTUDIAR.md](docs/ESTUDIAR.md): dudas abiertas.

Las notas por versión se conservan literales. Las rutas que citan (`/workspace/...`, `01_port_sgdk/...`, `02_arcade_decompilado/...`, `05_referencias/...`) son del backup privado y no están aquí si contienen datos del arcade.

## Pendientes principales (detalle en [docs/PENDIENTES.md](docs/PENDIENTES.md))

1. **Extractor de recursos** desde la ROM propia: [tools/extractor/README.md](tools/extractor/README.md).
2. **Movimientos que faltan**:
   - Duggan: High Knee, Body Slam, Headlock, Bulldog, Back Suplex, Back Body Drop, Dropkick contra el que corre, Pick Up, Dropkick desde el poste.
   - Warrior: Shoulder Tackle, Body Slam, Headlock, Gorilla Press, Atomic Drop, ataques contra el que corre, Pick Up, Dropkick desde el poste.
3. **Energía frente a pin, kickout y levantarse**: faltan las reglas nativas fuera del Knee.
4. **Pasar al reloj arcade (`arcTick`)** el andar, el arranque y el freno de la carrera, la clothesline y las caídas. Hoy van por frame MD.
5. Frames perdidos corriendo entre cuerdas (40 de 580; causa sin investigar).
6. Errores comunicados: sonido entrecortado del público, «Macho verde», variantes de clothesline que faltan.
7. Sin verificar todavía: hardware real/Everdrive, PAL junto a los postes, choque contra la cuerda en lanzamientos.
8. BAJA, «pulir al final»: cadencia visible del Knee desde el poste y del Elbow de Duggan.

## Estructura

```
README.md, README_PT_BR.md, README_ENG.md   este documento y sus traducciones
LICENSE                                    MIT (código y notas propios)
Makefile                                   make GDK=/ruta/a/SGDK
src/        main.c y cabeceras propias; boot/ (SGDK)
src/gen/    (ignorado por git) cabeceras generadas desde la ROM: ropes.h, gs69.h, hud.h, select89_data.h
res/        res.res (lista de recursos), crowd_b49.h; los .bin/.wav se generan (ignorados por git)
docs/       notas en español: REGLAS, PENDIENTES, ESTUDIAR, INDICE, PATRON_MOVIMIENTOS, COMPILAR,
            ARQUITECTURA, MOVIMIENTOS, CHANGELOG, notas/, analisis/, estudios/
docs/PT_BR/, docs/ENG/   traducciones (*_PT_BR.md, *_ENG.md), misma estructura
tools/mame/        pruebas MAME vigentes (b95)
tools/analisis/    herramientas de análisis del programa arcade (leen tu propia ROM)
tools/extractor/   PENDIENTE: especificación del extractor de recursos
```
