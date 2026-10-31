# Inventario de movimientos: Duggan y Warrior (arcade wwfsstar → port SGDK s40)

Fecha: 30-10-2026. Es solo investigación: la ROM del port no se ha tocado.

**Fuentes**
- Desensamblado de la ROM arcade (/tmp/arc.s).
- Sondas MAME: p68–p72 (/tmp/p56, planes plan18–plan20).
- Medidas anteriores de s34–s40.

**Leyenda de la columna «Port»**
- ✅ hecho en s40
- 🟡 parcial
- ❌ falta

**Identificadores de luchador** (byte bajo de +0x2A): Warrior = 0, Duggan = 3. Hay 8 luchadores y todas las tablas se indexan con este id.

## 1. Arquitectura de la lógica arcade

**Objeto luchador.** Hay cuatro, en 0x1C0100, 0x1C021A, 0x1C0334 y 0x1C044E. Campos principales:

| Campo | Significado |
|---|---|
| +0x2C/+0x2D | acción (estado) |
| +0x30/+0x31 | movimiento |
| +0x3C | energía (palabra, 0..48) |
| +0x3E | daño pendiente |
| +0x68 | rival |
| +0xA4 | compañero |
| +0x116 / +0x114 | botones latcheados (1 = B1, 2 = B2, 3 = B1+B2) |
| +0x19 | fuera del ring / apron |
| +0x2A bit 3 | lo maneja la CPU |
| +0x107 bit 0 | «ya se le intentó pinear» |

**Tablas de despacho**
- **ACT, 0x8CE2:** 33 acciones, de 0x00 a 0x20.
- **MOV, 0xFB58:** 61 ids, de 0x00 a 0x3C.
  - 0x0C, 0x11, 0x2B, 0x2C y 0x2F comparten el manejador 0x10A5E, que va por datos.
  - 0x1A, 0x23 y 0x24 comparten 0x1143A.
  - 0x37 a 0x3A comparten 0x1603E.

**Acciones conocidas**

| Acción | Uso |
|---|---|
| 00 | de pie / andar |
| 01, 15, 16 | carrera y rebote en cuerdas |
| 02 | caído tras proyección |
| 05 | levantarse (16 f) |
| 08 | cae (34 f) |
| 09 | aturdido por puñetazo (10 f) |
| 0A | aturdido por golpe (22 f) |
| 0B | en el suelo |
| 0C | ejecutando un movimiento |
| 0E | aturdido, ventana de derribo (16 f) |
| 0F | en el poste |
| 10 | lo levantan del suelo (48 f) |
| 11 | lock-up |
| 14 | frenada |
| 17 | encima del rival (cover/pin) |
| 1E | lanzado / irish whip |
| 1F | salir del ring (0xC554) |

### 1.1 Tablas de selección por luchador (dirección arcade → valor)

Todas indican el id de movimiento resultante.

| Situación (rutina) | Tabla | Warrior | Duggan |
|---|---|---|---|
| Golpe de pie (0xC776): B1 / B2 / B1+B2 | 0xCADE → 0xCB3C/0xCB6C, contexto 0 | 00 puñetazo / 01 patada / — (el lock-up sale por el contacto) | igual |
| Rival en acción 1/2 (caído tras proyección), contexto 3 | idem | 03 / 02 / — | 03 / 02 / — |
| Rival tumbado (0B/08), junto a cabeza o pies (≤ 0x20–0x28 px del extremo), contexto 6 | idem | 04 levantar / **0C** / 04 | 04 levantar / **11** / 04 |
| Rival tumbado, junto al cuerpo, contexto 9 | idem | 05 / 06 cover / 06 | 05 / 06 cover / 06 |
| Fuera del ring (+0x19, tabla 0xCAFE) | | 05 / 05 / 05 en el contexto 9 | igual |
| Apron/cuerdas (+0x5E bit 6) | 0xCB16 | 30 / 30 / 30 | igual |
| Carrera + botón (0xCC26) | 0xCD14 (luchador × 3) | 14 / **31** / 2A | 14 / **17** / 2A |
| Carrera con choque automático (0xC18C) | 0xC326 | 31 | 2A |
| Lock-up, humano (0xB468) | 0xB5B2 | B1 26 presa, B2 1E whip, B1+B2 26; caso especial (+0x10D = 1/2/8) 1F | igual |
| Lock-up, CPU | 0xB5BA | 1F / 1E / 1F / 1F | igual |
| Presa 0x26 + 2.ª pulsación (0x14FD8) | 0x15126 | B1 **33** press slam / B2 **22** / B1+B2 33 | B1 **29** carry / B2 **21** / B1+B2 29 |
| CPU gana la presa (0x14F00) | 0x14FE8 | 22 | 21 |
| Choque en carrera / rebote (0x16FAA) | 0x170B2 | 22 | 21 |
| Desde el poste (acción 0F, 0xF636) | 0xF6E6 | rival tumbado 0B → **2C**; si no, 20 | **2F** / 20 |
| Poste, CPU (0x1E8B0) | 0x1E8EC | 2C / 20 | 2F / 20 |
| CPU con el rival lanzado (0x1D2B0) | 0x1E14E | 1E o 1F (al azar) | 1E o 1F |
| «Mejora» de la CPU (0x1E88A) | lista en 0x1E170 | 21→21, 1B→1B, 07→07, 22→**33** | 21→**26**, 1B→1B, 07→07, 22→22 |

## 2. Inventario por movimiento

**Notas sobre las columnas**
- Los frames y los daños vienen de MAME: s34–s40 y las sondas p68–p71 de hoy.
- «?» = sin medir.
- Los nombres marcados con (*) se deducen del contexto y hay que confirmarlos viendo capturas.

| Id | Movimiento | Quién | Entrada / condición | Frames atac. / víct. | Daño | Port |
|---|---|---|---|---|---|---|
| 00 | Puñetazo | ambos | B1 de pie | ~24 / 0x09 10 f (0x0A/0x0E a partir del 3.er golpe) | +1 contador | ✅ D, 🟡 W (solo como CPU/humano básico) |
| 01 | Patada | ambos | B2 de pie | ~28 / 0x0A 22 + 0x0E 16 | +1 | ✅ |
| — | Derribo por acumulación | ambos | golpe durante 0x0E, o a un rival que corre | víct.: 08 34 + 0B 44 + 05 16 | — | ✅ s40 |
| 26 | Presa (lock-up hold) | ambos | lock-up + B1 / B1+B2 | 261 (se rompe sola a los 256 f) | — | ✅ |
| 1E | Irish whip | ambos | lock-up + B2 | 25 / 237 | 0 | ✅ D, ✅ W (CPU) |
| 1F | Lanzamiento del lock-up, variante (*) | ambos | caso especial del lock-up (+0x10D 1/2/8) y CPU | ? | ? | ❌ |
| 29 | Carry / proyección de Duggan | D | presa + B1 (≥ f34) | pulsación f40 → mov. f42 | 12 | ✅ |
| 21 | Proyección con B2 | D (W como CPU tras «mejora») | presa + B2 | 109 / 177 | 12 (k92) | ✅ D |
| 33 | Press slam de Warrior | W | presa + B1 / B1+B2; CPU vía 22→33 | 263 / 319 (R2w) | 13 (k252) | ✅ W (s64; humW presa+A; over-top apron) |
| 22 | Proyección con B2 de Warrior | W | presa + B2; la CPU gana la presa | 97 / 158 (L2_N2) | 12 (k80) | ✅ W (s64; humW presa+B; CPU→22) |
| 03 | Golpe a rival caído (acción 1/2) | ambos | B1 junto al rival | 43 / 117 | 6 | ✅ D |
| 02 | Golpe con B2 a rival caído (+ fallo 0x02M) | ambos | B2 | 79 / 115 (fallo 87) | 3 | ✅ D |
| 04 | Levantar al rival (*) | ambos | B1 o B1+B2 junto a cabeza/pies del rival tumbado | 48 / víct. 0x10 48 → lock-up 0x11 | 0 | ✅ D (s61) |
| 05 | Elbow drop / caída sobre el rival (*) | ambos | B1 junto al cuerpo (fuera del ring: cualquier botón) | 24 + 50 de recuperación / víct. 0x08 16, sigue en el suelo | 1 (f18) | ✅ D (s61) |
| 06 | Cover (pin) | ambos | B2 o B1+B2 junto al cuerpo | D: salto 28 + acción 17 128; W (rama 0x11A72): se tumba andando | — | ✅ D (s41) / ✅ W→D (s62) |
| 0C | Movimiento de suelo B2 de Warrior (*) | W | B2 junto a cabeza/pies | ? | ? | ✅ W (s62) |
| 11 | Movimiento de suelo B2 de Duggan (*) (stomp/knee) | D | B2 junto a cabeza/pies | 42; si falla, cae (08 26 + 0B 44 + 05 16) | 5 (f42); fallo −2 al atacante | ✅ D (s61, hit+miss) |
| 14 | Ataque en carrera B1 (RAT) | ambos | carrera + B1 | existente | ? | ✅ D |
| 17 | Ataque en carrera B2 de Duggan | D | carrera + B2 | 47 / 95 | 3 | ✅ |
| 31 | Ataque en carrera de Warrior (*) (flying tackle) | W | carrera + B2, o choque automático | 45 / 58 (c4) | 3 (k8) | ✅ W (s64; humW B cerca; sin rn Warrior aún) |
| 2A | Ataque en carrera B1+B2 | ambos (choque automático de D) | carrera + B1+B2 | 75 / 89 | 3 | ✅ D |
| 20 | Salto desde el poste (rival de pie) | ambos | en el poste + B1 | 79 / 111 | 3 | ✅ delanteros+traseros (s63; track frontal)|
| 2C | Salto desde el poste sobre rival tumbado (W) (*) (splash) | W | poste + B, rival en 0B | 87 (P2) | 10 | ✅ W (s63; apex-snap, sin subida P2)|
| 2F | Salto desde el poste sobre rival tumbado (D) (*) (elbow) | D | idem | 87 / 78 (bounce S05) | 10 | ✅ D (s63)|
| 30 | Movimiento desde el apron/cuerdas (*) | ambos | +0x5E bit 6, cualquier botón | ? | ? | ❌ |
| 0x02M / 08 | Fallos: el atacante cae | ambos | fallo de 02, 11, 20… | 87 / 34+44+16 | — | 🟡 |
| 1B, 07 | Ids genéricos de la CPU | CPU | lista 0x1E170 | ? | ? | ❌ (bajo) |
| 0D, 12, 13, 15, 16, 18, 19, 1A, 1C, 1D, 23–25, 27, 28, 2B, 2D, 2E, 32, 34–3C | Repertorio de los otros 6 luchadores, comunes y sumisiones (0x2D/0x2E, 0x13 = llaves de 6 pasos de 4 de daño con victoria si la energía llega a 0) | — | ninguna tabla de W/D los selecciona | — | — | fuera de alcance |

**Acciones de estado / reacciones de la víctima**

| Estado | Detalle | Port |
|---|---|---|
| Levantarse (0x05) | 16 f | ✅ |
| Tiempo tumbado (0x0B) | depende de la energía (tramos de 0xAF26: ≥54/48/36/25/14/0). Medido tras el derribo: energía 48 → 170 f; 12 → 290 f; ≤ 4 → 350 f | 🟡 el port usa 247 fijo, ajuste pedido |
| Víctima 0x10 | la levantan | ❌ |
| Víctima 0x02 | caída tras whip/proyección | ✅ |
| Salir / entrar del ring (0x1F, 0xC554), regla de over-the-top | | 🟡 s64: 33 over-top → sx apron (parcial; no regla genérica) |
| Fuera del ring (+0x19) | tablas propias (0xCAFE): solo 05 | ❌ |
| Rebote en cuerdas (15/16) y carrera (01) | | ✅ |
| Relevo (tag) | se deja la animación sin función | — |

## 3. Pin, cuenta y final del combate (del código)

**Cover (mov. 0x06)**
- Requisitos: el rival está en 0x0B y en el ring, y el atacante no está fuera.
- El atacante pasa a la acción 0x17 y se coloca encima del rival. El offset en x y la altura salen de la tabla 0xBEF2 (16 bytes por luchador).
- El árbitro (objeto 0x1C0568) pasa a la acción 2 (cuenta) mientras dure.

**Decisión** (rutinas 0x11BC6 y 0x129A4)
- **Primer pin a un rival:** solo marca +0x107 bit 0 y siempre hay kickout.
  - Medido: pin de 128 f; después el atacante sale despedido (08 34 + 0B 44 + 05 16), incluso con energía 0.
- **Pines siguientes:** cuentan la energía y el azar.
  - Se usa un aleatorio de 0 a 15 contra la tabla 0x11C30. El índice es nivel/ronda (0x1C0028) × 3 + tramo de energía (0x1CEF4: energía ÷ (energía máx. del luchador ÷ 3), con tope 2).
  - Si la energía es 0, gana con aleatorio < 3/16 extra (0x129F2); si no, va a 0xAF9A.
  - Victoria: banderas 0x1C0BC2 / 0x1C0BDA = 0x80 / 0x40.

**Otras formas de ganar**
- **Sumisiones (0x13, 0x2D/0x2E):** gana quien deja la energía rival a 0.
- **Tiempo agotado (0x26510):** empate o decisión según el modo.

**Energía**
- Arranca y tiene tope en 48 (0x30).
- El daño se aplica en 0x16488 (energía −= +0x3E).
- El compañero fuera del ring recupera +4 por tick (0x20C2). Sin relevos, no aplica.

> ⚠️ La probabilidad exacta del pin a energía 0 está deducida del código y **no está verificada en MAME**. Es la siguiente sonda: dos pines seguidos a energía 0.

## 4. IA de la CPU (resumen)

- **Lock-up:** si gana, usa la tabla 0xB5BA (1F/1E). Si gana la presa, 0x14FE8: W 22, D 21.
- **Rival lanzado contra las cuerdas:** 1E o 1F al azar (0x1E14E).
- **Poste:** 0x1E8EC (2C/2F/20).
- **Tablas de decisión:** se indexan por nivel (0x1C0028) y luchador (0x8190 en CPU, 0x7FEC en humano; los dos dan la energía de referencia).
- **«Mejora» de movimiento:** 0x1E88A convierte el movimiento genérico en el especial del luchador (Warrior 22→33 press slam; Duggan 21→26).
- **Reacción a la distancia:** acciones 0x12/0x16/0x1C (0x1C68C, 0x1C60E, 0x1CC30). Sin documentar en detalle: pendiente de la fase de IA.

## 5. Gráficos: coste estimado

**Base actual**
- NPOSE_ALL 494; spr_tiles 8735, de los que 5635 son únicos (s33).
- Duggan tiene 1597 tiles únicos y Warrior 2895.
- Las poses de s34 no se deduplicaron contra s33. Ahí hay una oportunidad: deduplicar por firma de tile con flip H/V. Estimación de ahorro: 25–35 % según s33.

**Estimación por movimiento nuevo**

| Movimiento | Atacante | Víctima |
|---|---|---|
| Suelo (04, 05, 06, 0C/11) | 6–12 poses | 2–4 poses (tumbado, rebote) |
| Postes (2C/2F) | reutilizan la subida y el salto de 0x20, + 3–5 poses de caída | + 2 |
| Press slam 33 y 22 de Warrior, 31 | 10–20 poses cada uno (víctima en el aire: poses grandes, 60–80 tiles) | ✅ s64 (28 poses nuevas tras dedupa; max ~61 tiles) |

**Total pendiente**
- Unas 120–180 poses, unos 6.000–9.000 tiles sin deduplicar (190–290 KB) y quizá 3.500–5.000 tras deduplicar (110–160 KB de ROM).
- En VRAM no cambia nada: se sigue con streaming por slot (P1 72, P2 80). El press slam puede pasar de 80 tiles por pose, como la pose 237 (78). Hay que vigilar SLOTP2 o partir la pose.
- La víctima lleva la pose del atacante (luchador cogido) en muchos movimientos. Hay que grabar las dos combinaciones: Duggan → Warrior y Warrior → Duggan.

## 6. Limitaciones del port

- **Warrior como humano:** solo tiene andar, puñetazo y patada.
  - Están grabadas las pistas de W1E.
  - Falta todo su repertorio con las combinaciones invertidas (Warrior atacante, Duggan víctima).
- **Postes:**
  - Solo están los dos delanteros, y el derecho es el izquierdo espejado.
  - Traseros (s63): misma lógica de dive; tracks/perspectiva = frontales (no verificados vs arcade frame a frame).
- **Fuera del ring:** no hay salida genérica, apron ni conteo fuera. Over-the-top parcial (s64): 33 → sx apron; regla genérica (+0x18 bit 7, z ≥ 219) aún sin implementar.
- **Pin (s41):** hecho Duggan→Warrior con cuenta del árbitro, BEGIN NEXT MATCH y reinicio arcade; NO_RESTART eliminado. Faltan: pin Warrior→Duggan (P1 aún no puede perder) y kickouts por run-in del compañero (aproximados: P1 sale con el cover invertido).
- **Tiempo tumbado:** según energía (s62; bands 224/164/108/44).
- **KK8 (buffer de la 2.ª patada):** discrepancia sin resolver.
- **Soak NTSC:** 1 frame de error (desde s39).
- **Recursos:** DMA por frame al límite al subir al poste (9904). Más poses grandes = vigilar el presupuesto de DMA.

## 7. Recuento y orden propuesto

**Recuento** (alcance Duggan + Warrior, unos 27 movimientos/estados)
- Hechos: 25 (… + **05/04/11 [s61]**, **0C + pin W→D + lie×energía [s62]**, **2F/2C + postes traseros [s63]**, **22/33/31 W [s64]**).
- Parciales: 3 (20, fallos 08/02M, over-top parcial s64).
- Faltan: unos 9, a saber:
  - ~~suelo: 0C de Warrior (y pin W→D)~~ (s62);
  - ~~postes: 2C, 2F, postes traseros~~ (s63; 2C apex-snap; traseros=track frontal);
  - ~~Warrior: 31, 33, 22~~ (s64; humW presa A/B + B cerca; CPU→22; sin rn Warrior; over-top solo vía 33);
  - lock-up: 1F;
  - fuera del ring: 30, salida/entrada genérica;
  - resto Warrior como humano (carrera rn, etc.).

**Orden propuesto**
1. ~~Pin 06 + cuenta + victoria + quitar NO_RESTART~~ (hecho en s41). Pendiente: pin W→D y run-ins del compañero.
2. ~~Tiempo tumbado según la energía~~ (hecho en s62).
3. ~~Suelo: 05 (elbow), 04 (levantar → lock-up) y 11 de Duggan~~ (hecho en s61).
4. ~~Postes: 2F/2C sobre rival tumbado, y después los 2 postes traseros~~ (s63).
5. ~~Warrior humano: 22, 33 press slam, 31~~ (s64) + ~~0C~~ (s62) + ~~2C~~ (s63) y reacciones de Duggan víctima.
6. 1F, el movimiento 30 desde el apron, y salida y entrada del ring.
7. IA de la CPU: usar el repertorio completo con las tablas por nivel.
8. Deduplicar gráficos de s34+. (s64: dedupa exacta del base s63 −6936 tiles antes de extraer 22/33/31.)

> Nota s41: la energía en la estructura del luchador es la palabra en +0x3c (an68.py leía +0x3e por error; corregido).
