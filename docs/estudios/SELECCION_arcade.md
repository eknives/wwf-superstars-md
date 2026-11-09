# Selección arcade — estudio, sin cambios en el port

**Método:** MAME `wwfsstar`, ROM local; moneda + inicio + joystick/botón mediante `observe.lua`. Solo entradas, lecturas de RAM y capturas: sin escribir RAM, sin editar el port y sin compilar ROM. Cuatro recorridos cortos: 1P, versus, cooperativo y espera sin elegir. Evidencia: `1P.log`, `VS.log`, `COOP.log`, `TIMEOUT.log`; vistas originales de 256×240, sin interfaz MAME. `RESUMEN_seleccion.png` reúne seis estados.

## Aspecto y controles observados

- Fondo azul con trama WWF; arriba **SELECT PLAYERS** y logo WWF en el centro. Seis retratos en dos filas de tres, con los centrales desplazados verticalmente. Nombres bajo los retratos:

| ID de selección | Arriba | ID | Abajo |
|---|---|---|---|
| 0 | RANDY SAVAGE, izquierda | 3 | HONKY TONK MAN, izquierda |
| 1 | HULK HOGAN, centro | 4 | HACKSAW JIM DUGGAN, centro |
| 2 | ULTIMATE WARRIOR, derecha | 5 | BIG BOSS MAN, derecha |

- 1P comienza en Savage: marco verde y rótulo **1P**. 2P comienza en Warrior: marco amarillo y **2P**. Derecha desde Savage pasa a Hogan; abajo desde Hogan pasa a Duggan. El movimiento es por nuevas pulsaciones, no desplazamiento continuo por mantener la dirección. La tabla `0x74F2` conecta vecinos de la cuadrícula: los bordes **no envuelven**.
- Confirma **Button 1** del jugador. No confundirlo con los tres botones de inicio del mueble. Código: lectura/flancos `0x7240–0x729A`; despacho `0x749E` (0 = mover, 1 = confirmar, 2/3 = retorno sin selección). Confirmación `0x7552`: bloquea duplicados mediante bits en `0x1C0069` y hace destellar el fondo del retrato; se ven cambios verde/magenta. Prueba: P2 intentó confirmar Duggan ya elegido por P1 y su contador siguió en cero.

## Equipos y transición, verificados

- **Inicio A — 1P VS CPU:** en la misma pantalla eliges luchador y después compañero; no hay otra pantalla de compañero. Prueba: Duggan y Honky; ambos figuran en el HUD del combate (`08_1P_combate.png`). Los dos rivales CPU se sortean entre los restantes (`0x71E8`).
- **Inicio B — 1P VS 2P:** cada jugador elige dos, sin repetir entre equipos. Confirmación manual verificada: Duggan/Honky contra Big Boss Man/Warrior (`10` y `11`).
- **Inicio C — 1P/2P VS CPU:** cada jugador elige uno y forman el mismo equipo. Verificado Duggan + Big Boss Man, juntos en el HUD izquierdo (`13`). Código de unión: `0x7392–0x73A6`; condiciones de cierre `0x72DA–0x731E`.
- Al confirmar se retiran los cursores y destellan los elegidos. Después hay transición: en 1P se capturó el mensaje **THREE MORE VICTORIES TO GET TO THE TITLE MATCH!!**, presentación **WWF Live from NEW YORK**, entrada y combate. El bucle `0x704E–0x71B2` espera al cerrar `0x40` refrescos, o `0x70` en versus.

## Tiempo y sonido

- **No se ve un contador numérico** en las capturas de selección, tampoco justo antes del límite. Sí existe tiempo interno: `0x7098` carga `0x180` = 384 en `0x1C006A`; `0x72A4` descuenta uno por refresco. En el registro: 383 en fotograma 602 y 363 en 622. Aproximadamente 6,68 s con el refresco configurado en este MAME (~57,44 Hz; no medición de placa).
- Sin elegir, al agotarse empieza un sorteo animado que completa las plazas libres: `0x7328`, `0x73E8`. En `TIMEOUT.log`, primera elección automática en fotograma 1049 y segunda en 1113. No significa que toda la pantalla dure solo 384 fotogramas: el sorteo y cierre añaden tiempo.
- `0x705E–0x7066` prepara comando musical **0x0A**, enviado mediante `0x25E6`. **Nombre de la melodía y SFX no identificados**: las pruebas se ejecutaron sin salida de audio.

## Localización gráfica rápida, desde código/driver

- Escena 4: `0x7078 → 0x1F434 → 0x2034A`. Mapa base en ROM CPU `0x210A8`, escrito a BG RAM `0x0C0000`; descompresor `0x203C2`. Retratos: `0x2035A–0x203B0`, bloques 4×4 tiles de 16×16 mediante `0x20404`:

| Retrato | Tiles BG inclusivos | Banco de color BG |
|---|---|---|
| Savage | 0x383–0x392 | 0 |
| Hogan | 0x393–0x3A2 | 1 |
| Warrior | 0x3A3–0x3B2 | 2 |
| Honky | 0x3D3–0x3E2 | 3 |
| Duggan | 0x3C3–0x3D2 | 4 |
| Big Boss Man | 0x3B3–0x3C2 | 5 |

- Región `bgtiles` del driver: `24j7-0.113` en 0x00000 y `24j6-0.112` en 0x40000; formato de planos `tiles16x16_layout`. No son offsets lineales de imágenes completas. Texto/cursor: FG RAM `0x080000`, región `fgtiles`, ROM `24aa-0.58`; actualización del cursor `0x75B6`, tablas `0x7686` y `0x782A`.
- Paleta de selección: selector **4** en `0x706C`; carga `0x29F6`. BG: tabla `0x2F0A`, entrada 4 → `0x2FAE`, ocho punteros a colores: `0x3416/3434/3452/3470/348E/34AC/34CA/34CA`, destino `0x140200`. Parpadeo: `0x1F5C/0x1F86`. Referencias contrastadas con `analisis/tools/prog.bin` y `wwfsstar.cpp`; no se extrajeron ni modificaron gráficos.

## Capturas principales (en esta carpeta)

`01_1P_inicial.png`, `02_1P_cursor_hogan.png`, `03_1P_cursor_duggan.png`, `04_1P_primero_confirmado.png`, `05_1P_elegir_companero.png`, `06_1P_equipo_confirmado.png`, `07_1P_transicion.png`, `08_1P_combate.png`, `09_2P_versus_inicial.png`, `10_2P_versus_equipos.png`, `11_2P_versus_combate.png`, `12_2P_coop_inicial.png`, `13_2P_coop_combate.png`, `14_limite_sin_contador_visible.png`, `15_timeout_sorteo.png`.

**Límites:** observación del set local en MAME, no placa física ni otras revisiones/regiones. Sonido sin identificar; no se hizo extracción completa de todos los textos/tiles.
