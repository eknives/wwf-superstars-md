# b58 (desde b57)

ROM: `wwf_b58.bin`  md5 `cbe3a2b0976a142ceb25068edc660869`

b57 intacta (md5 `8651e4ef71af09be6260350b1489e20d`). Solo el árbitro cambia de estático a vivo.

## Reglas del árbitro (confirmadas Emilio)

1. **Como los demás:** prioridad HIGH + zonas de color (verde / morada / naranja / amarillo) + orden de dibujo por pies vs Duggan; **sigue rodeando** (`refAvoid`).
2. **HUD:** cualquier pieza del árbitro cuyo `y` de pantalla toque el HUD (`y < HUD_H`, 34) se fuerza a **LOW**; el resto no.
3. **Laterales:** se mantiene el tope — no pisa las cuerdas laterales (`RF_MARGIN 16` dentro de `RING_XL`/`RING_XR` con el `e` de perspectiva).
4. **Camina por el ring:** sigue a Duggan cuando se aleja más de `RF_KEEP` (56 px), 1 px/frame (lógica s41 / estado 0 arcade).

## Clamp (origen)

`rfClamp` en `src/main.c`:

- Y: `RING_Y0+8` … `RING_Y1-4`, y además `ylim` (techo HUD / cámara).
- X: `lo = RING_XL + e + RF_MARGIN`, `hi = RING_XR - e - RF_MARGIN` con `e = (rfy-RING_Y0)/6`.
- `RF_MARGIN = 16` (slack s51). Se llama antes y después de `refAvoid`.

`RING_XL=616`, `RING_XR=917` (tope derecho de b55).

## Walk (origen)

- **Follow:** `rfStep` — si `|ox-rfx|` o `|oy-rfy|` > `RF_KEEP`, avanza 1 px hacia Duggan (eje dominante; diagonal si ambos grandes). Fuente: serie s / s41 vuelta a casa / follow arcade estado 0.
- **Rodear:** `refAvoid` portado de **s51** (1 actor = Duggan): si solapa en X con pies más abajo en pantalla, busca hueco abajo / ±X sin violar el margen lateral.
- **Anim:** `spr_tab` poses **510–512** (`PT_RWK`) vienen **sin cabeza** (primera pieza en dy=16). En b58:
  - idle / movimiento lateral o hacia cámara → pose **8** + H-flip si va a la derecha;
  - solo alejándose (`hy>0`, sin `hx`) → alterna **508/509** (espalda, con cabeza).

## Paletas

Sin cambio respecto a b57:

| Línea | Uso |
|---|---|
| 0/1 | fondo + público + cuerdas + HUD + **árbitro** |
| 2 | Duggan |
| 3 | compañeros (Macho/Hogan) |

VRAM árbitro: `RF_T0=1088` (28 t), `RF_T1=1512` (resto). Cuerdas en 1120 sin tocar.

## Qué no se tocó

Compañeros, Duggan, cuerdas, esquineros, logo WWF (sigue pendiente manual), controles, sonido, `RING_XR`.

## Shots

- `shots/b58_idle.png` — idle con cabeza
- `shots/b58_walk1.png` … `b58_walk4.png` — follow por el ring (rfx 768→887 en la corrida MAME)
- MAME: `test/t58.lua` + `test/o_b58/`

Pendiente manual (sin cambio): esquineros superiores + logo WWF a parches.
