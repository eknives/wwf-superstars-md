# Extractor de recursos — **PENDIENTE**

Esta utilidad **todavía no existe**. Su trabajo será leer **tu propia ROM** (set MAME `wwfsstar`, obtenido legalmente) y generar los recursos que el port necesita para compilar, sin que el repositorio tenga que contener ningún dato del arcade. Hasta que exista, el código no se puede compilar con contenido real (ver `docs/COMPILAR.md`).

## Requisitos

1. Comprobar el set (CRC32/SHA1 de cada fichero según `mame -listxml wwfsstar`) antes de extraer nada.
2. Generar, **byte a byte iguales** a los usados en b95, los 32 ficheros de `res/` y las 4 cabeceras de `src/gen/` listados abajo.
3. Las salidas no se suben nunca: `.gitignore` excluye `res/**/*.bin`, `res/**/*.wav` y `src/gen/*.h`.
4. Los conversores originales se hicieron versión a versión (b42–b92) y están en el backup privado del proyecto. Hay que reunirlos en un solo proceso reproducible; las notas de cada versión (`docs/notas/`) describen cómo se obtuvo cada recurso.
5. **Excepción:** los esquineros superiores y el logo WWF del fondo (`bgb_tiles.bin`/`bgb_map52.bin`/`pal.bin`, «fondo de Emilio» desde b42) llevan ediciones manuales de Emilio que **no se publican**. El extractor generará la versión del arcade, así que el MD5 de la ROM no coincidirá con b95 salvo que se apliquen esas ediciones por otra vía.

## Recursos de `res/` (32, referenciados por `res/res.res`)

| Fichero | Bytes | Contenido | Origen en las notas |
|---|---:|---|---|
| `graficos/paletas/pal.bin` | 64 | Paletas del fondo (2×16 colores MD) | b42/b49 (fondo de Emilio) |
| `graficos/fondos_cuerdas_publico/bgb_tiles.bin` | 113280 | Tiles del fondo (ring, suelo, gradas) | b42/b49 |
| `graficos/mapas/bgb_map52.bin` | 11968 | Mapa del mundo de fondo (88×68) | b52 |
| `datos/crowd_b52.bin` | 61566 | Animación del público por zonas | b49/b52 |
| `graficos/fondos_cuerdas_publico/crowd_b49_tiles.bin` | 19456 | Tiles del público | b49 |
| `graficos/fondos_cuerdas_publico/ex52_tiles.bin` | 16160 | Tiles de relleno del exterior | b50/b52 |
| `sonidos/oki_s03.wav` | 65580 | Muestra OKI 0x03 decodificada: WAV mono, 16 bits, 8000 Hz, 32768 muestras (PCM4 en SGDK) | análisis de sonido |
| `sonidos/oki_s04.wav` | 65580 | Muestra OKI 0x04 decodificada, mismo formato | análisis de sonido |
| `graficos/fondos_cuerdas_publico/ropes_tiles.bin` | 12512 | Tiles de las cuerdas (391 tiles, en VRAM 1120) | b53/b61 |
| `graficos/luchadores/spr_tiles.bin` | 933600 | Tiles de todas las poses (Duggan, Warrior, árbitro…) | b55/b56 y añadidos b81–b92 |
| `datos/spr_tab.bin` | 108486 | 861 `Pose` × 126 bytes (ver `docs/ARQUITECTURA.md`) | b55/b56 y añadidos |
| `graficos/paletas/spr_pal.bin` | 64 | Paletas de sprites | b53 |
| `datos/move_seq.bin` | 1716 | Secuencias de movimiento (pose, duración) | b65/b85 |
| `datos/sx_seq.bin` | 1856 | Salir/entrar del ring | — |
| `datos/bx_seq.bin` | 1056 | Secuencia exterior | — |
| `datos/climb_pose.bin` | 1360 | Subida al poste | — |
| `datos/run_pos.bin` | 436 | Posiciones de la carrera/rebote | — |
| `datos/camtab.bin` | 772 | Tabla de cámara | — |
| `graficos/luchadores/part_tiles.bin` | 2752 | Tiles parciales remapeados a PAL2 | b56 |
| `datos/xl_w.bin` | 1276 | Pose lógica → pose del port (Warrior) | b76/b84 |
| `datos/xl_d.bin` | 1276 | Pose lógica → pose del port (Duggan) | b84 |
| `datos/sp_trk.bin` | 48720 | Pistas arcade de lanzamientos/vuelos | b69/b70 |
| `datos/pin_glyph.bin` | 1472 | Cifras de la cuenta de pin | b76 |
| `datos/credit_dig.bin` | 320 | Cifras de créditos | — |
| `datos/big_dig.bin` | 3200 | Cifras grandes de la cuenta fuera | b72 |
| `graficos/seleccion/select89_tiles.bin` | 16512 | Pantalla de selección | b89 |
| `graficos/seleccion/select89_map.bin` | 1792 | Mapa de la selección | b89 |
| `graficos/seleccion/select89_cursors.bin` | 21504 | Cursores y retratos | b89 |
| `graficos/paletas/select89_pal.bin` | 256 | Paletas de la selección | b89 |
| `graficos/titulo/title89_tiles.bin` | 21888 | Pantalla de título | b89 |
| `graficos/titulo/title89_map.bin` | 1792 | Mapa del título | b89 |
| `graficos/paletas/title89_pal.bin` | 32 | Paleta del título | b89 |

«—» = el origen exacto hay que localizarlo en las notas y scripts históricos del backup. En el backup hay 3 ficheros más que `res.res` no usa (`bgb_map50.bin`, `ex50_tiles.bin`, `crowd_b49.bin`) y que no hacen falta. `res/crowd_b49.h` (3 constantes de tamaño) sí está publicado.

## Cabeceras de `src/gen/` (4)

Declaraciones que el código espera. Los valores salen de la ROM y **no se publican**:

```c
/* src/gen/ropes.h — mapas de tiles de las cuerdas (vibración) y 2 paletas */
#define X0 22
#define Y0 19
#define W0 6
#define H0 27
#define NS0 84
static const u16 mp0[8][162];  static const u8 sc0[84];
#define X1 60
#define Y1 18
#define W1 6
#define H1 28
#define NS1 84
static const u16 mp1[5][168];  static const u8 sc1[84];
#define XH 20
#define YH 39
#define WH 48
#define HH 9
static const u16 mph[432];  static const u16 palR2[16];  static const u16 palR3[16];
#define VT 1120
#define NR 391

/* src/gen/gs69.h — pistas sp_trk 0x05 (codazo en suelo) y 0x11 (salto sobre el tumbado) */
#define GS5_N 29
#define GS5_K 16
#define GS11_N 83
#define GS11_K 40
static const u16 gs5P[29];  static const u16 gs11P[83];  static const s8 gs11X[83];  static const s8 gs11Z[83];

/* src/gen/hud.h — marco del HUD: 12 tiles 4bpp y su mapa */
static const u32 hudT[12*8];  static const u8 hudMap[4][32];
#define HUD_NT 12

/* src/gen/select89_data.h — navegación y colores de la selección (747A, 2048, 2054) */
#define SEL89_NT 516
#define TITLE89_NT 684
static const u8 selNav89[96];  static const u8 autoNav89[36];  static const u16 flashColor89[6];  static const u8 flashPen89[6];
```

Las constantes `#define` son geometría y tamaños que el código necesita. Con estas declaraciones inicializadas a `{0}` y los ficheros de `res/` a cero, el proyecto compila (probado el 9-11-2026) y sale una ROM negra.
