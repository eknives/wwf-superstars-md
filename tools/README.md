# Herramientas

Sólo las vigentes para b95. Las versiones anteriores y los conversores históricos están en el backup privado. Ninguna herramienta contiene datos del arcade: todas leen **tu propia ROM** o la ROM MD que compiles.

## `tools/mame/` — pruebas MAME 0.276 usadas para verificar b95

| Script | Qué mide |
|---|---|
| `mame95.sh rom.bin script.lua [genesis\|megadriv]` | Lanzador sin vídeo ni sonido. Variables: `MAME`, `ROMPATH`, `SHOTS`. |
| `run95.lua` + `runsum.py` | Velocidad de la carrera (px/s) y cambios de pose por segundo, W y D. |
| `post95.lua` + `postsum.py` | Frames perdidos andando hacia los 4 postes e integridad del fondo leyendo la VRAM por el puerto del VDP. |
| `zafar95.lua` + `zsum.py` | Zafarse del pin junto a la cuerda: X final en Xv 760/728/708/693/832. |
| `kick95.lua` | Zafarse en el centro y cuenta de 3. |
| `salir95.lua` | Salir y entrar del ring. |
| `pinvis95.lua` | Secuencia de estados del pin. |
| `fs2_95.lua` | Lanzamiento (sub 1) contra la cuerda. |
| `postes95.lua` | Capturas fijas de los postes. |
| `cl95_clothesline.lua` | Clothesline (variables `SYM`, `CLD`, `MODE88`). |
| `prof95.lua` | Perfilado de frames perdidos. |

- Los scripts leen las direcciones de las variables del port desde `out/symbol.txt` (variable `SYM`) y escriben CSV en la ruta de `OUT`.
- Algunos conservan rutas por defecto `/workspace/...` del equipo original: ajústalas con las variables o editando la cabecera.
- Botones en MAME: `P1 A`/`P1 B`… Índice de luchador en el port: 0 = Duggan, 1 = Warrior.

## `tools/analisis/` — análisis del programa arcade

`rdis.py` (desensamblador que genera `arc_rec.dis` desde tu ROM), `anot.py`/`anot2.py` (anotaciones de las 964 rutinas que producen `docs/analisis/rutinas.md`), `cg.py` (grafo de llamadas), `sig.py`, `rd.py`, `dump.py`, `reread.py`, `regen.py`, `audit_sample.py`, `oki.py` (decodificador ADPCM OKI), `z80rec.py`, `render_obj.py`, `sheets.py`. Varios llevan rutas `/workspace/...`: hay que ajustarlas.

## `tools/extractor/` — **PENDIENTE**

Especificación del extractor de recursos: `tools/extractor/README.md`.
