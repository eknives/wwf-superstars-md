# Arquitectura de `src/main.c` (b95)

`main.c` (~1600 líneas) es un único módulo C para SGDK. Cada bloque lleva un comentario `bNN:` con la versión que lo introdujo y las direcciones arcade que reproduce. Las líneas son aproximadas a b95.

## Ficheros

| Fichero | Contenido |
|---|---|
| `src/main.c` | Motor completo: bucle principal, luchadores, cámara, fondo, cuerdas, público, árbitro, pin, sprites. |
| `src/select89.h` | Pantalla de título y selección de luchadores (arcade 704E/7240/749E…); `joy89()` normaliza C = A+B. |
| `src/duggan92.h`, `duggan92_poses.h` | Ataques de suelo de Duggan (Stomp, Elbow, Elbow desde poste; C79E/CB6C). |
| `src/knee90.h`, `native81.h`, `cl87.h` | Índices de pose del port para Knee Drop, banco nativo de Warrior y caída por clothesline. |
| `src/gen/*.h` | **Generados desde la ROM** (no publicados): mapas y paletas de cuerdas (`ropes.h`), pistas de suelo (`gs69.h`), marco del HUD (`hud.h`), navegación de la selección (`select89_data.h`). |
| `res/res.res` | Recursos binarios que `rescomp` enlaza (ver `tools/extractor/README.md`). |

## Reloj

- La lógica de actor del arcade avanza cada 2 refrescos de 57,44 Hz, es decir, un tick a 28,72 Hz.
- En la MD, el bucle principal acumula `arcClock += 3125·Δvtimer` y activa `arcTick` cuando supera `arcDen` (5440 en PAL, 6528 en NTSC). Como mucho hay 1 tick por vuelta.
- Desde b95 la carrera y algunos ataques de suelo avanzan por `arcTick`. El resto (andar, caídas `fs`, rebote, freno) sigue avanzando por vuelta o frame MD: está en PENDIENTES.

## Bucle principal (`main()`, ~l. 1434)

1. **Inicio:** VDP 256×224, planos 64×32, carga de paletas, HUD, cuerdas, poses iniciales; `selectScreen89()` (una sola vez); relleno inicial del fondo.
2. **Por vuelta:**
   1. reloj `arcTick`;
   2. mando (`joy89`, flancos, START = seguir; Y = cambiar de control);
   3. `grStep` (forcejeo) y `pinAdvance`;
   4. **por cada luchador** `f = 0, 1`, con `ctxLoad(f)`/`ctxSave(f)`, que copian el contexto del luchador a variables globales (`ox`, `oy`, `z0`, `rn`, `sx`…). Prioridad de estados, de mayor a menor:
      - `kvPhase90` (víctima del Knee);
      - `clHeld` (agarrado en clothesline);
      - `fs` (caída de acción 8: vuelo, choque contra cuerda 9F02, aterrizaje);
      - zafarse del pin (`pnS==2`);
      - el que cubre en el pin (`pinStepA`);
      - forcejeo o lanzamiento (`gr`, `tr` con `trStep`);
      - víctima de golpe (`vh` con `victimStep`);
      - si no, `engine()` (control normal).
   5. `grTry`, `countStep` (cuentas), `matchReset` si toca;
   6. `camera()`;
   7. público (`caLogic`/`caDraw`/`caApply`);
   8. vibración de cuerdas (`ropeDraw`, pasos 0x21324/0x213A4);
   9. **streaming del fondo** (`stCol`/`stRow`: cola DMA con presupuesto `ST_BUD`, desde b95);
   10. `sqTick` (secuencias de sonido);
   11. árbitro (`rfStep`, `refPinStep`, cuenta fuera).
3. **VBlank:** `SYS_doVBlankProcess()` vacía la cola DMA. Después vienen `fLoad` (tiles de pose de los luchadores), `rfLoad` (árbitro), dígitos de cuenta, `buildSat()` (tabla de sprites), scroll y DMA de la SAT.

## Módulos dentro de `main.c`

| Bloque | Funciones (línea aprox.) | Qué hace |
|---|---|---|
| Fondo y VRAM | `acq`, `rel`, `put` (~196), `acqQ`, `stCol`, `stRow` (~219–238) | Mundo de 88×68 celdas (`W`), pool de tiles con recuento de referencias, columnas y filas nuevas por DMA en cola (b95). |
| Cuerdas | `ropeA`, `ropeDraw` (~204–248), constantes de `gen/ropes.h` | Cuerdas dibujadas en los planos; vibración por fases arcade (0x213A4/0x213AC/0x2146E). |
| Público | `caLogic`, `caDraw`, `caApply` (~249–290) | Animación del público por zonas (23170). |
| Sonido | `smpPlay`, `sndCmd`, `sqTick` (~291–300) | Muestras PCM4 (2 WAV OKI) y secuencias. |
| HUD | `hudInit` (~302) | Marco del HUD (`gen/hud.h`). |
| Movimiento y cámara | `walkStep`, `camera` (~308–368) | Andar, límites del ring, cámara con márgenes. |
| Árbitro | `rfLoadEx`, `rfColumn`, `rfClamp`, `rfExtPose`, `refAvoid`, `rfStep` (~369–480) | Árbitro que camina, esquiva y cuenta (DD4E/DFE0/DECC). |
| Contexto | `ctxLoad`, `ctxSave` (~481–497) | Cambio de luchador activo. |
| Knee (víctima) | `kneeVictimStep90`, `kneeVictimStart90` (~498–534) | Reacción A2 de la víctima (A554/28EC). |
| Caídas, acción 8 | `fsStart`, `clFallStart`, `fsStep`, `fsAir`, `arcRope` (~530–600) | Vuelo, choque contra cuerda 9E78/9CD0/9F02 (b95), aterrizaje 9C3C/9C94. |
| Víctima | `victimStep`, `bounceRope`, `soilNudge` (~600–676) | Reacción a golpes, rebote en cuerda, empujón al tumbarse (ACA4). |
| Suelo Warrior | `groundOK`, `warriorGroundZone/Start/Step/End` (~677–805) | Knee Drop y remates en suelo (C706/10A5E/112F0). |
| Clothesline | `clStep87` (~806) | Clothesline en carrera (CD14/12E7A). |
| Control | `engine` (~845–1100) | Estados del luchador controlado: `rn` (1 correr, 2 rebote, 3 clothesline; freno según `mvOffR`), `sx` (salir/entrar del ring), `bx`, `climb` (poste), `gs` (5/11/12 pistas de suelo, 14/15 Duggan), combo de puños y patada, pin de Duggan. |
| Forcejeo y lanzamiento | `grTry`, `trStart`, `grStep`, `trCF`, `trStep` (~1101–1175) | Agarre y lanzamiento contra las cuerdas (pistas `sp_trk`). |
| Pin y cuentas | `pinAdvance`, `pinStart`, `pinStepA`, `refPinStep`, `countStep` (~1176–1258) | Pin (BD10/11A72/B012/B0A0), cuenta de 3 y de 20; al terminar reinicia el combate. |
| Combate | `fighterInit`, `matchReset` (~1259–1274) | Estado inicial. |
| Dibujo | `fLoad`, `drawF`, `buildSat` (~1275–1433) | Carga de tiles de pose (tabla `spr_tab`) y composición de sprites con prioridades. |

## Datos de recursos que usa el código

- `spr_tab` es una tabla de `Pose { u16 n, t0, nt; Piece p[12]; }` con `Piece { s16 dx, dy; u16 sz, line, toff; }`, 126 bytes por pose, y `spr_tiles` contiene sus tiles.
- `xl_w`/`xl_d` traducen la pose lógica a la pose del port para Warrior y Duggan.
- `move_seq`, `sx_seq`, `bx_seq`, `climb_pose`, `run_pos`, `sp_trk` son pistas de animación y posición.
- `camtab` es la tabla de la cámara; `crowd_b52` + `crowd_b49_tiles` son el público; `bgb_tiles` + `bgb_map52` + `ex52_tiles` son el fondo.
- La lista completa con tamaños está en `tools/extractor/README.md`.
