# b51 (desde b50)
ROM: wwf_b51.bin  md5 328134aa6dde7116b2ac863ecea7eb29
- Cuerdas laterales (izq y dcha) del arcade (frames de b45/b46) en plano A alta, en coordenadas del fondo (arcade x+32, y+16). Sin la cuerda horizontal de abajo.
- A = rebote cuerda izquierda, B = rebote cuerda derecha. Horarios del arcade de b45 (84 pasos, 1 por frame), como b46.
- Fondo en plano B baja (b50: cartel, margenes, HUD vacio).
- Camara: cruceta; C = rapido (A/B ya no aceleran). START+A/B/C = publico como b49.
- Cuerdas: 356 tiles en VRAM 1120+, PAL2 + PAL3 (3-9); pool del fondo baja a 1100.
- Pendiente: esquineros incompletos en algunos estados (limitacion de b45).
- Shots: shots/0001-0002 = dcha rebotando, 0003-0005 = izq rebotando, 0006 = reposo.
