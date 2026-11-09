# b64 (desde b63) — md5 9b3cffff1bd585fc241f684f09ab77a4
Solo rfStep:
- El paso de seguir (hx/hy) ya no avanza rfPh ni pone pose antes del clamp: la anim se decide al final con el movimiento NETO tras rfClamp+refAvoid+rfClamp.
- En el limite lateral (RF_MARGIN 16, no toca cuerdas), empujones de ±1 px sin seguir en Y no cuentan como andar: congela ultimo frame.
- Neto 0 = congela (como arcade).
Prueba MAME: arbitro forzado al borde dcho (x 887) con Duggan pegado a la cuerda: pose fija 618 todo el rato.
Ojo: con b63 en esa misma prueba tampoco ciclaba; no logré reproducir el ciclo en el sitio. Al bajar por la diagonal del borde sí anda (movimiento real).
Shots: shots/b64_borde_*.png, b64_borde_contact.png.
