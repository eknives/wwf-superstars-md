# b49: fondo de Emilio + cámara libre + público animado + sonido de público

ROM: `wwf_b49.bin` (también `out/rom.bin`), 524.288 bytes, md5 `6d1b50331b893d52879d7a11eff9f37f`
Base: b42 (`b42_camara`). No se ha sobrescrito ninguna ROM anterior.

## Qué hay
- Fondo de Emilio de b42, sin cambios (`bgb_tiles.bin`, `bgb_map.bin` y `pal.bin` son los mismos).
- La cámara libre funciona igual que en b42: cruceta para mover; A, B o C para ir rápido.
- **Público: CROWD_ARC de s67**, con las rutinas arcade 0x22462/0x224E8/0x225B0 (ciclo de fases {0,1,2,1,2,…,0} a 30 Hz), la valla 0x23406/0x230FC y el elemento pequeño 0x232DE/0x2336C.
  - Las listas de s67 estaban hechas sobre el fondo antiguo. `tools/remap_crowd.py` las pasa al fondo de Emilio comparando píxeles: añade 608 tiles nuevos y salen 10.244 celdas. No se ha tenido que omitir ninguna, porque las 331 celdas en las que el fondo de Emilio cambia no coinciden con celdas del público.
  - El mapa en RAM usa ids de 13 bits, porque 3.540 + 608 pasa de 4.095.
- **Sonido (driver PCM4 de SGDK, muestras OKI originales 3 y 4):**
  - 0x22 = muestra 3 una vez. 0x23 = muestra 4 una vez.
  - 0x50 / 0x51 = oleadas: las secuencias Z80 0x1152 / 0x117A copiadas tal cual. Cada entrada reinicia la muestra con su atenuación OKI. Los tiempos van en ticks de 100 Hz (timer B 0xDD), en total unos 9,4 s.

## Cómo probar
- Al arrancar suena 0x22, como en el arcade (0x1010).
- **Demo automática:** cada 8 s hay una reacción del público con oleada, alternando 0x50 y 0x51. Se desactiva compilando con `AUTO_DEMO=0`.
- **START + A** = reacción + 0x50. **START + B** = reacción + 0x51. **START + C** = valla + 0x22.
- El público está arriba y abajo: hay que subir o bajar la cámara para verlo (en el centro solo se ve el ring).

## Comprobado (mínimo)
- Arranca. Las capturas de `shots/` no muestran tiles rotos.
- El público cambia tras el disparo, unos 470 frames con cambios.
- Hay salida de audio en el arranque y en la oleada.
- Los datos están dentro de la ROM: `crowd_b49.bin` en 0x4FBC8 y las tiles en 0x5EC46. `res.h` y `res.rs` se borraron antes de compilar.

## Falta / límites
- **Flashes de cámara (0x6BA0):** no están. Son sprites (objeto 1C09A6) y van en otro paso.
- Sin luchadores no hay disparos reales. Las reacciones salen de la demo o de los botones.
- El volumen sale bajo con PCM4. Las muestras no se han normalizado, para no tocar el original.
- Esquineros: no aplica.
- **Sin cuerdas:** no hay bancos de rebote ni plano A. Las cuerdas son el siguiente paso.
