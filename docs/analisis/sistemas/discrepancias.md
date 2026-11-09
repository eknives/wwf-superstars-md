# Discrepancias port (s66 wip19, 67efe37a…) vs arcade — sin corregir
1. No está el efecto de valla del público (1C1854). (C)
2. No hay driver de sonido; las peticiones a 0x25E6 no tienen equivalente. (C)
3. Falta la tabla de mareo de la CPU para Duggan. (C)
4. lieTab está medido a ojo; no es la tabla 0xAF66. (C)
5. La transición 0x15→0x01 y el ataque de vuelta son aproximados (WHIP_RET). (C)
6. El azar del público no usa la fórmula del RNG 0x450A (registros + semilla 1C003A). Pendiente de verificar en el código del port. (P)
7. Selección de rival por nivel (0x21C4, con rng): queda por comprobar si el port sigue el mismo orden. (P)

## Revisión (lectura completa 0x17C6–0x8AB0)
- Pendiente: contrastar con el código de s66. Esta pasada no llegó a hacerlo, así que las 7 discrepancias siguen SIN CONFIRMAR contra el port.
- Datos nuevos del arcade (ya confirmados) para comparar:
  - La barra de energía muestra ceil(energía/4), con un máximo de 12 segmentos.
  - La energía se conserva entre combates; solo se reinicia en el combate 0, desde la tabla 0x7FEC.
  - El RNG 0x450A no suma d1 ni a3.
  - Con un humano a energía 0 suena la música 8.
  - En versus (modo 2) no hay game over: el ganador sigue en el modo de 1 jugador.
