# Movimientos Duggan y Ultimate Warrior — estado b92

Actualización del inventario b89 (que contenía notas b83), contrastada con b90/91 y NOTAS_b92.md. **Sí=usable, no verificación completa arcade**; no=ausente; parcial=incompleto. Sólo se ensayaron nuevamente los tres ataques Duggan autorizados y regresión de Knee Warrior; los demás estados son heredados, no pruebas nuevas. P=A,K=B,C=A+B,Y=cambia control.

## Controles FAQ (leyenda)

| Símbolo | Significado |
|--------|-------------|
| P / K | Punch / Kick (A / B en Mega Drive) |
| P+K | Correr |
| U+P | Arriba + Punch |
| *R / *U | Reversible / irrevesible (FAQ) |

---

## Duggan (`"HACKSAW" JIM DUGGAN`)

| Movimiento | Input FAQ | Estado | Nota corta |
|------------|-----------|--------|------------|
| Punch | P (1 tras 3) | sí | Combo FD70+FD7C por pulsaciones (heredado b87); despacho nativo Duggan distinto, ver estudio energía |
| Kick | K (1 tras 2) | sí | B de pie (`mv=2`) |
| Run | P+K | sí | A+B o C (b89) → `rn=1`; rebote en cuerda |
| Clothesline | P en carrera | sí | Colisión al contacto + caída rival 0x17 boca arriba (b86–b88, MAME); faltan variantes espalda/cuerdas |
| High Knee | K en carrera | no | B en carrera no lanza ataque |
| Body Slam | U+P en grappling | no | No hay U+A en agarre |
| Headlock | P en grappling | no | Solo forcejeo genérico (b70), no presa Headlock |
| Bulldog | P desde Headlock (*U) | no | Finisher de presa ausente |
| Back Suplex | K desde Headlock (*R) | no | Finisher de presa ausente |
| Irish Whip | K en grappling | sí | Tras forcejeo: `trStart` → lanzamiento a cuerdas (ambos) |
| Back Body Drop | P vs corredor | no | Sin rama “Against Running” |
| Drop Kick | K vs corredor | no | Idem |
| Pick Up | P junto a cabeza | no | Agarre al tumbado no portado (`NOTAS_b82`) |
| Stomp | P junto al cuerpo | sí (b92 probado) | Motor nativo Duggan, zona CB75,159/15A, daño1, arcTick; límites23/24 y sin refiltrado comprobados |
| Elbow Drop | K junto a cabeza | parcial (b92) | Solver/poses/reacción/daño5 y fallo−2 nativos; contactos suelo/espejo/variante cotejados. Cadencia visible pendiente |
| Pin | K junto al cuerpo | sí | B cerca → `pinStart`; cuenta árbitro (b71+) |
| Dropkick (poste, de pie) | P/K desde turnbuckle | no | Se puede **subir** esquinero; no hay ataque desde arriba |
| Elbow Drop (poste, tumbado) | P/K desde turnbuckle | parcial (b92) | Sub2F, trayectoria P/K/daño10/A2 cotejados; cadencia visible pendiente |

**Duggan:** 7 sí / 2 parcial / 9 no (18 del FAQ; sí = usable, no certificación general idéntico arcade).

---

## Ultimate Warrior

| Movimiento | Input FAQ | Estado | Nota corta |
|------------|-----------|--------|------------|
| Punch | P (1 tras 3) | sí | Combo FD70+FD7C por pulsaciones, heredado b87; no retocado en b92 |
| Kick | K (1 tras 2) | sí | B de pie |
| Run | P+K | sí | Igual que Duggan (A+B o C) |
| Clothesline | P en carrera | sí | Igual que Duggan (b86–b88) |
| Shoulder Tackle | K en carrera | no | B en carrera no ataca |
| Body Slam | U+P en grappling | no | — |
| Headlock | P en grappling | no | — |
| GORILLA PRESS | P desde Headlock | no | Finisher ausente |
| Atomic Drop | K desde Headlock (*R) | no | Finisher ausente |
| Irish Whip | K en grappling | sí | `trStart` simétrico (pistas W1E) |
| Back Body Drop | P vs corredor | no | — |
| Dropkick | K vs corredor | no | — |
| Pick Up | P junto a cabeza | no | En zona suelo A → pisotón, no levantar (`NOTAS_b82`) |
| Stomp | P junto al cuerpo | sí | Zona 2 + A → `gs=13` / sub 5 arcade (`warriorGroundStart`) |
| Knee Drop | K junto a cabeza | sí (b90/91 heredado) | Motor/solver nativos, variante76/77 sin7D, A2 y energía; regresión b92 de contacto/energía sí. Sin cambios en b92 |
| Pin | K junto al cuerpo | sí | Zona 2 + B si `w82PinOK` → pin Warrior |
| Dropkick (poste, de pie) | P/K turnbuckle | no | Sube poste; sin ataque aéreo |
| Knee Drop (poste, tumbado) | P/K turnbuckle | parcial (b90/91) | Contacto/daño10 implementados; cadencia visible pendiente BAJA «pulir al final». No corregida en b92 |

**Warrior:** 8 sí / 1 parcial / 9 no (18 del FAQ; estado heredado b91, no nuevas técnicas b92).

---

## Compartidos / sistema (cuentan para ambos)

| Sistema | Estado | Nota |
|---------|--------|------|
| Forcejeo / lock-up (2 luchas + reverse) | sí | b70: `grTry` / `grStep`; mash → whip |
| Irish Whip a cuerdas + rebote | sí | Incl. vib corta al chocar/caer (b78–b81) |
| Caída / tumbado / levantarse | sí | Reacciones + get-up (más lento b70) |
| Golpes de suelo | parcial | Duggan motor independiente b92; Warrior sin cambios b91. Elbow/poste aún con cadencia visible pendiente |
| Pin + cuenta de 3 + kickout 1.er pin | sí | Ambos cubren; árbitro (b71+) |
| Cuenta fuera 20 / cuenta 3 → reinicia combate | sí | b89: no vuelve a selección |
| Pantalla título + SELECT PLAYERS arcade | sí | b89; elección aún no cambia luchadores |
| Subir/bajar esquineros | sí | Remates contra tendido implementados parcialmente; contra rival de pie siguen ausentes |
| Salir/entrar al ring (lateral / atrás) | sí | `sx` / `bx` |
| Vibración cuerda corta (collide+fall / kickout cerca) | sí | b78–b81 |
| IA / rival ataca solo | no | Rival solo con START (seguir); Y cambia control (b89) |
| Ataques “Against Running” | no | — |
| Ataques desde turnbuckle | parcial | Sólo remate contra tendido; ver límites de cada luchador |
| Pick Up / agarre al tumbado | no | Confirmado pendiente |

---

## Evidencia actual

- Duggan: `src/duggan92.h`, `duggan92_poses.h` y ramas de entrada en main.c. Sustituyen sólo sus antiguas activaciones gs5/gs11; pin y otros movimientos siguen.
- Warrior: `src/knee90.h`, `native81.h`, funciones warriorGround* sin modificar; regresión de cinco casos.
- Direcciones nativas, daños, contactos, cadencias medidas y límites: `NOTAS_b92.md`, `shots92/validation92.json`, `pose92_refreshes.csv`.
- Inventario histórico original: `MOVIMIENTOS_DUGGAN_WARRIOR_b89.md`. No usar sus resúmenes b83 como estado actual. Energía vs pin/levantarse sigue pendiente; sin IA nueva, sólo START sigue.

ROM `d9af08525a0f49f4bdc025ed00499135`.
