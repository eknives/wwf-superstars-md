# b88 — sólo sentido de caída y revisión gráfica Clothesline
ROM: `wwf_b88.bin` — MD5 `96371335c6b9cb43b08d158ba73ec488`. Base b87 intacta.

## 1. Caída — SÍ, verificada en MAME
**Fallo:** b87 llamaba `clFallStart(o,rnd)`: lanzaba al rival en el mismo sentido y elegía el espejo contrario. Ahora usa `-rnd`.
Arcade: 12F16/12F1C copia la orientación del atacante al rival y cambia bit7; 9B9A/9BC6 aplica ±32 px; 27D2/2964 aplica vx=±0x80. Resultado: atacante →, rival ← (y viceversa), 32 px iniciales + 1 px/tick. 9E4C/A8BE y ABBC: 15→16→17, caída **boca arriba**, cabeza hacia el atacante. No se cambia a una pose boca abajo.
Probados Duggan y Warrior como atacante/víctima, izquierda/derecha. CSV registran desplazamiento y H-flip: rival Hflip=1 al atacar a derecha, 0 al atacar a izquierda.

## 2. Animaciones — SÍ, verificadas en los casos probados
**Segundo fallo:** la conversión de b87 perdía el banco de paleta de cada bloque y coloreaba las extremidades prestadas del rival con los colores del atacante. Corregido por bloque: fuente 2=Warrior, 7=Duggan; el arcade selecciona la paleta efectiva por actor en 46A0. Sin cambiar `spr_pal.bin`.
Tablas 6CD8: bancos 0/3. 1302E/12EF6: 1D0,1D1, captura 1D2/1D5,1DB,E,F; 1DA si no captura. Víctima: 15,16, rebote 16, suelo 17. Orden y flip contrastados; no se alteraron sus tiempos.
**38 cotejos exactos de píxeles**, tras la correspondencia de colores MD existente, contra los sprites realmente emitidos por MAME (RAM 100000). Además, **20 poses cargadas** cotejadas palabra por palabra con VRAM real del VDP y paleta CRAM: 0 diferencias. Se tuvieron en cuenta los dos refrescos de retraso entre estado lógico y dibujo.

## Evidencia y límites
`verify88/RESULTADO_b88.txt`, CSV, scripts y volcados SAT. PNG emparejadas contacto/vuelo/suelo: `shots88/Duggan_R_comparacion.png`, `Duggan_L_comparacion.png`, `Warrior_R_comparacion.png`, `Warrior_L_comparacion.png`; también `par_*` y `pixels_*`.
Sólo cambia el signo del lanzamiento y la conversión/carga gráfica de estas poses. Prefijos de gráficos anteriores, logo WWF, esquineros, punches y demás recursos intactos. No se arreglan ni se amplían las colisiones/cuerdas/energía pendientes de b87. Pruebas NTSC MAME; **b88 aún no probada en Everdrive**. La igualdad de píxeles indicada es tras conversión a la paleta MD, no igualdad RGB de ambas plataformas.
