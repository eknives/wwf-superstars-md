# b91 — entrega PARCIAL

**ROM:** `/workspace/b91/wwf_b91.bin` — **MD5 1f7f183b0ef6fe6367d62360697935c6**.
Base b90 copiada íntegramente. **Puntos 2 y 3 corregidos/verificados; punto 1 NO resuelto. No presentar esta ROM como cumplimiento completo.**

## 1. Knee desde poste — pendiente, no se da por arreglado

MAME nuevo confirma `arc_corner_frames.csv`: **61×8 / 62×18 / 7A×10 refrescos**, P y K. Son **4/9/5 ticks** (`10F54/10FB2`, `112F0/112FA`; reloj `1508–1510`, 57,44485 Hz). MD necesita conversión temporal, no forzar esos números literalmente a 60 Hz.

Se ensayaron reloj separado con fase compartida, transporte DMA acotado y SAT preparado antes de VBlank. **Las repeticiones no mantuvieron la equivalencia por refresco**, aunque la trayectoria por tick coincidía. Se retiraron TODOS esos cambios: el ROM final conserva el render, reloj, público y cadencia de poste de b90. Ensayo final: registros de pose cargada K **11/19/7**, P **5/19/14**; no se afirma que sean contadores visuales atómicos ni que coincidan con arcade. Hay PNG consecutivos `post_corner*_f*.png` y CSV por refresco.

Experimento descartado: `tools/experimental_post91.c.txt`, evidencia en `shots91/experimental_post/`; **no está compilado en el ROM entregado**. El perfil mostró trabajo de scroll y construcción SAT atravesando refrescos; no hay atribución CPU/DMA definitiva para todas las pausas. Documentación SGDK consultada: [SYS/VBlank](https://stephane-d.github.io/SGDK/sys_8h.html), que advierte que perder el inicio puede aplazar el proceso un refresco. No se amplió el alcance ni se quitó el polling de mandos para ocultarlo.

## 2. Exterior — corregido y verificado

Causa: b89 recorta el origen W510 a512 antes de entrar y no aplica a la víctima tendida el ajuste **`AB1E→ACA4`**, dos pruebas con desplazamientos ±48 y ±8. Su límite exterior está en **`21ED0/22140`**, tabla **`221B2`**: suelo128, Y192..456, X488..1040, pendiente /6, margen interior48 (`21F2A/21F54`).

**Solo al iniciar Knee exterior** se recupera el origen previo al recorte, si aún corresponde a la misma posición, se limita como el arcade y se normaliza la víctima. Caminar y los demás movimientos conservan sus límites originales; no se cambió el solver.

Caso W510/R558/Y300: origen W510, víctima R546, **Vx150**; contacto MD y MAME **(528,75;309;128)**, energía48→43 y A2. Se ha eliminado la diferencia anterior MD540,125/Vx225.

Regresión rápida contra MAME: suelo **(727;309;187)**; variante **(727;299,375;187)**; poste P/K **(725,59375;309,8125;187,5)**, daño10. **88 estados estables de trayectoria coinciden**; A2 conserva alturas4/7/9/10/10/9/7/4/0. Las lecturas capturadas entre instrucciones se descartan al contrastar estados; no se confunden con un contacto ya completado.

## 3. Selección — corregido y verificado visualmente

Causa: `selDraw89` escribía los **896 tiles** de overlay por CPU con interrupciones bloqueadas, retrasando los cambios de paleta HINT. Ahora prepara solo las celdas distintas y las publica durante VBlank; no hay escritura masiva durante pantalla activa. Navegación/confirmación y destello nativo de confirmación permanecen sin cambios (`749E/74F2/7552`, `1F5C/1F86`).

**74 PNG consecutivos por versión**, cuatro cambios de cursor: b90 altera hasta **2799 píxeles ajenos al cursor en 4 cuadros**; b91 **0 píxeles, 0 cuadros**. Además se comprueba que el cursor NO queda congelado: Savage→Hogan→Duggan→Honky→Savage, cuatro posiciones visuales distintas (258 píxeles verdes). Referencia MAME también recapturada. Evidencia: `select_b90/`, `select_b91/`, `select_arcade/`, `validation91.json`.

## Archivos y límites

- Comparativas: `comparativa91_seleccion_secuencia.png`; `comparativa91_exterior_{vuelo,impacto,reaccion}.png`; `comparativa91_poste_K_{vuelo,impacto,reaccion}.png`; suelo/variante equivalentes. Son fases comparables, no el mismo refresco/cámara: MAME mantiene cámara fija en los fixtures.
- `trajectory91_compare.csv`, `pose91_refreshes.csv`, Lua y `tools/validate91.py`; NTSC y PAL ejecutados. Fixtures RAM + entradas, no partida completa, cuatro esquinas/geometrías exteriores exhaustivas ni Everdrive. MAME mantiene el aviso CRC del chip de fondo24j6-0.112; CPU MD5 4bd7c20fe4dbaf1b7ee8225e0e5d7359.
- Auditoría completa: b90 intacto (`b90_manifest91.json`). **Solo cambian `src/main.c` (normalización Knee exterior) y `src/select89.h` (cursor)**. Todos los recursos gráficos, esquineros, logo, Hogan, energía y otros movimientos son idénticos. Diffs `source91_main.diff`/`source91_select.diff`.
- **Fuera de alcance en el ROM: nada. Pendiente principal: resolver realmente el punto 1.**
