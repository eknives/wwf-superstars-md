# b52 (desde b51)
ROM: wwf_b52.bin  md5 7c3254185b41c1494120155d126850e7
- Camara a la par: mapa 80x68 -> 88x68 (+8 columnas = 64 px a la izquierda, sacadas del fondo del arcade, mismo metodo que el relleno de b50; 242 tiles nuevos en ex52_tiles). Limites cx 0..448. Margen desde el poste al borde: izq 162 px, dcha 165 px.
- Publico (crowd_b52.bin) y cuerdas desplazados +8 columnas; zonas del publico ajustadas (camx -64).
- Cuerdas horizontales delanteras (roja/blanca/azul + postes) de ring_edit/ring_cuerdas_planoA.png, en plano A alta, fijas. En las celdas de las laterales se mezclan con cada frame del rebote.
- Las horizontales de atras ya estaban en el fondo (plano B); no se tocan.
- A = rebote izq, B = rebote dcha (igual que b51). C = rapido.
- Cuerdas: 391 tiles en VRAM 1120+. Colores de las horizontales ajustados a la paleta de las cuerdas (5 tonos aproximados).
- Comprobado: assets en la ROM (byte a byte), MAME arranca, shots/b52_test.png (izq tope, rebote A, dcha tope, rebote B).
- Sonido entrecortado: sin tocar.
