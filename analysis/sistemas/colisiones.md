# Sistema de colisiones (0x1657E)

Leído entero en el hito 75 %. Todo lo de esta página está confirmado (C) salvo que se indique.

1. **Bucle** (0x1657E): se llama cada frame. Pone +0x40 a 0 en los 4 luchadores y recorre las 6 parejas de la lista 0xEA4C (0x165B2).
2. **Reinicio de víctimas** (0x165FE): cuando cambia la pose, +0xCE vuelve a 0. Así un mismo frame activo no golpea dos veces a la misma víctima.
3. **Filtro de proximidad** (0x16634): |dx| < 0x60 y |dy| < 8, el mismo +0x19 (< 2), ninguno agarrado (acción 0x10), etc.
4. **Cajas de golpe** (0x1672C): la tabla 0x1761E[pose] da una lista por frame. Cada caja: prioridad (+0), daño (+1), caja de ataque (+2), caja de defensa (+6), caja alternativa (+0xE) y tabla de reacciones (+0xA).
5. **Impacto** (0x16796): necesita prioridad del atacante ≥ defensa, solape en x (0x16C60) y en z (0x16CA8), y que la pose de la víctima sea golpeable (0x172FA). Entonces:
   - escribe la reacción en +0x40 (con +2 si el golpe es por la espalda) y la sub en +0x44;
   - el daño va a +0x3E (0 contra la CPU con las subs 0/1);
   - hay ajustes especiales para el id 7 (0x169C2, 0x16AD4, 0x16B2A, 0x16C14);
   - golpe contra golpe (0x16B6A): se anulan;
   - agarre (+0x40 = −2): los dos quedan enlazados.
6. **Choque de cuerpos** sin golpe (0x16DF8): los dos van a la acción 0x11.
7. **Sonido y combo** (0x16CF4): las tablas 0x175CE y 0x17590 llenan el acumulador +0x48. Su temporizador +0x46 vale 0x30 frames.
8. **Aplicación** (0x162A0, en el bucle del luchador): acción = +0x40; daño extra si está tumbado (0x1638E), ×2 con +0xF9 bit0; 0x16488 resta la energía y suena 0x22/0x23.
