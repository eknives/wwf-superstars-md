# b53 (desde b52)

ROM: wwf_b53.bin  md5 61a87b67e3fbb6df3b64dd7362789db2

- Base b52 intacta en visuales: mapa 88×68, fondo B baja, cuerdas (laterales + horizontales delanteras) en A alta, público, rebote A/B. Sonido entrecortado: sin tocar.
- Duggan controlable (walk / run A+B / rebote en cuerda / exit-enter laterales y abajo / subir postes). Pad mueve a Duggan; la cámara le sigue (arcade→scroll b52: cx≈camx+96, cy≈camy+32). Sin pelea ni IA (stub dormido).
- HUD cajas vacías: bake −4 px a la izquierda (tile-bake; CRT RGB come el borde izq). Misma ventana.
- Prioridad sprites (esquema color s49 de Emilio; HIGH casi siempre):
  - VERDE: HIGH por defecto dentro del ring / delantal delantero.
  - MORADO: LOW dentro, a la altura de las cuerdas horizontales de abajo (trocea la pieza si cruza rl=ROPE_FRONT_R0).
  - NARANJA: HIGH si dentro; LOW si fuera junto a laterales (cuerda delante).
  - Postes: muro; subir = HIGH. Cruzando sx: inside según x vs cuerda.
  - Fondo B baja; plano A baja vacío. Orden SAT futuro: jugador, oponente, relevo J, relevo O, árbitro.
- Paletas: PAL2 = spr_pal (Duggan); PAL3 = palR3 (cuerdas remapeadas + HUD). VRAM: pool tiles 16..1015, sprites en 1016 (72 slots), cuerdas 1120+.
- Controles: D-pad andar; A+B correr; mantener contra lateral = salir/entrar; ABAJO en poste abajo = subir; ARRIBA en poste atras = subir; A/B+START crowd trig (b52).
- Shots: shots/b53_walk.png, b53_side.png, b53_run.png, b53_mat.png (+ serie 0000–0009). MAME smoke OK; no probado en hardware.
