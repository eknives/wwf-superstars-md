# b50 (desde b49)
ROM: wwf_b50.bin  md5 68f778ed3bbc111e38fa0ebeb78e93df
- Cartel: la cara de arriba-dcha tenia el trozo de abajo (filas 10-11, col 38-41) de otra cara (id 3). Puesto el trozo correcto de Macho Man (tabla arcade 0x2197A id 2). En el arcade las 4 caras se ponen segun los luchadores del combate (rutina 0x1F50C); aqui quedan fijas.
- Margenes azules: rellenados con el escenario del arcade (RLE 0x1F474 + columnas 0x1F5C8, mundo de 768 px). Fondo x = arcade x-96, y = arcade y+16. 444 celdas, 254 tiles nuevos (res/ex50_tiles.bin, ids detras del publico).
- Filas 0-3 (publico duplicado por el wrap de 512 px del arcade) en negro; el publico animado ya no escribe ahi.
- HUD vacio en el plano window (filas 0-3, fijo): 2 cajas, marco doble (exterior/interior), interior negro, PAL3. Color del marco aproximado (azul), a confirmar.
- Igual que b49: camara libre, publico y sonido. Sin cuerdas.
- Mapa nuevo: res/bgb_map50.bin (ya en formato RAM).
