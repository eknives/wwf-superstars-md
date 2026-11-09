# b77 — base b76 conservada

ROM: `wwf_b77.bin` (1.572.864 bytes). MD5: `947bdf6ccc66d33c7d9ecc526e3e8e97`.
Base intacta: `/workspace/b76/wwf_b76.bin`, MD5 `49075e62b6b23d071da6035564adcea8`.

Solo tres cambios: árbitro en la cuenta, asiento/capas del pin de Warrior, salida del pin de ambos. Sin cambios de IA, HOME, esquineros, logo, público, sonido ni otros movimientos. Los recursos antiguos de sprites son prefijos idénticos; solo se añade la pose 778.

## 1. Árbitro: corrupción de piezas, no supuesto límite por línea

En Mega Drive el árbitro ocupa dos bloques **no contiguos**: tiles 1088–1115 y 1512–1524. El dibujo antiguo traducía solo el primer tile de cada pieza y después sumaba offsets como si el bloque fuese continuo. Algunas piezas de las poses 503, 506 y 507 cruzan el tile lógico 28; entonces se leían tiles ajenos (incluso de cuerdas), independientemente de dónde estuvieran los luchadores.

`rfColumn` corta las columnas exactamente en ese salto de VRAM. También traduce los offsets antes —no después— del troceado de prioridad de las cuerdas. Se mantienen las paletas, el bit de prioridad, las cifras por delante y las posiciones del árbitro de b76.

La comprobación exhaustiva de todos los tiles de las poses 500–509 encuentra **36 direcciones erróneas en el cálculo antiguo y 0 en el nuevo**. No se han tapado los síntomas ocultando al árbitro o cambiándolo de sitio.

Fuente de orden de dibujo arcade: `analisis/arc_rec.dis`, 0x43D4–0x4508 (entrada con X, Y y Z separados), 0x45AE–0x45FA (orden por Y de suelo; comparación en entrada+8), 0x45FC–0x4614 (Z se añade solo para proyectar). Cifras: 0xE02C y 0x2549E; el fondo transparente de `pin_glyph.bin` no cambia.

## 2. Warrior cubriendo: Z y dos capas arcade

La tabla real **0xBEF2**, fila Warrior 0 / columna Duggan 3, da **dx=32 y dz=16**, no dz=13. En 0xBDCC–0xBE84:

- Warrior (id 0): Y = Y del cubierto +1.
- Z inicial = 0xBB−16 y después se suma 16 dos veces: **Z=203**.
- Pose principal 0x7F: 0xBD96.
- Objeto auxiliar 0x1C0AB2, pose 0x80: 0xBE84–0xBEC0, mismo X/Z y Y del cuerpo−2.

La pista histórica WPIN ya tenía el Z plegado dentro de sus píxeles. b75/b76 le aplicaban además el fallback 174: lo bajaban otros 13 píxeles. No se ha cambiado ese fallback para Duggan ni para las llaves.

En el asiento de Warrior se usa ahora la pose **778**, convertida directamente de las poses arcade 0x7F y 0x80. Sus 48 tiles se cargan juntos, pero se dibujan en dos pasadas: cuerpo detrás del cubierto y manos delante, por sus respectivas Y de suelo. Durante la aproximación histórica WPIN no se duplica el Z plegado. Se conserva el centrado X del pin existente.

El conversor es `tools/gen77_pin.py`; comprueba que el programa usado por el decodificador coincide exactamente con `analisis/tools/prog.bin`. La unión de las máscaras 0x7F/0x80, con el desplazamiento y Z originales, coincide con la máscara histórica de la pose 515. No hay píxeles dibujados ni generados por IA.

Capturas: `shots/b77_01_warrior_pin.png`, `b77_02_warrior_cuenta2.png`, `b77_06_antes_despues_pin.png` (misma fixture en b76 y b77). La captura de Emilio en MAME es la referencia visual; cámara, escala y paleta del port no se han cambiado.

## 3. Zafarse y salir lanzado: ticks, colocación y velocidad

Fuente primaria: `analisis/arc_rec.dis` y `analisis/tools/prog.bin`:

- **0xB012–0xB04C**: el cubierto se desplaza ±8 una vez.
- **0xB0EA**: pose 0x9F durante 8 ticks y 0xA0 durante 4 ticks. Son **16+8 fotogramas**, no los 8+4 fotogramas de b76.
- Durante la primera pose, quien cubre todavía conserva el pin. **0xB0A0–0xB0E4** solo lo coloca en la segunda pose: 0x9B, X del cubierto±0x28, Y−1, Z+4. b76 lo cambiaba desde el principio.
- **0xB068–0xB084**: cubierto → acción 5; quien cubre → acción 8 sub 0x1C, girado.
- **0x9B66 / 0x9BBE / 0x9C14**: desplazamiento inicial ±0x10 y Z+0x18.
- Tabla **0xA74A[0x1C] → 0xA8E6**, parámetro físico 0x21; **0x2814[0x21] → 0x29B4**: vx=0x100, vy=0, vz=0x100, g=0x40. Son valores fijados por el arcade, no la gravedad/vz supuestas de las notas b76.
- **0x27D2–0x280E** carga esos valores; **0x3E20–0x3E8C** aplica X/Z y gravedad una vez por tick (dos fotogramas). b76 no desplazaba X en vuelo y arrancaba con vz=0.
- **0x9E4C**: 0x9B/0x9C según altura al caer. **0x9C5A–0x9C92**: desplazamiento ±0x20 al tocar suelo, sub 0xC. **0xA4C8–0xA53E**: rebote pequeño con vz=0x100/g=0x30.
- **0xA90E–0xA954**, tabla 0xAA00, índice 0: levantarse 8 ticks =16 fotogramas, solo para estas salidas. No se añaden atontados.

La salida usa el origen visible del cubierto, sin trasladarlo súbitamente al origen corregido del pin (la corrección `lyo` solo era de dibujo). Los signos se convierten al eje X del port por separado del giro de dibujo. La actualización del pin se hace una vez antes de ambos actores: no depende de que cubra Duggan o Warrior ni del orden del bucle.

Capturas/hojas: `shots/b77_04_warrior_lanzado.png`, `b77_05_duggan_lanzado.png`, `b77_07_kickout_warrior.png`, `b77_07_kickout_duggan.png`.

## Compilación y comprobaciones

- SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`.
- Es necesario reconstruir `out/res/res.o`: la copia de b76 traía un `.d` con rutas absolutas de b76. Ya está reconstruido con dependencias exclusivas de b77. No se entrega una ROM con recursos antiguos.
- Compilación final sin instrumentación de diagnóstico: `BUILD_b77.log`, sin errores. Avisos heredados de indentación/variables sin uso.
- `python3 tools/verify77.py`: verifica la base, los prefijos de sprites, recursos ajenos al alcance y el direccionamiento del árbitro. Resultado: `VALIDACION_b77.txt`.
- Fixtures de MAME para Genesis: `test/fixture77.lua`, `test/fixture77.sh`. Ejemplos: `test/fixture77.sh Wvalidated 1 1 1` (cuenta de tres), `test/fixture77.sh Dvalidated 0 0 1`, `test/fixture77.sh WKvalidated 1 1 0` y `test/fixture77.sh DKvalidated 0 0 0` (salidas). Llegan a sus finales sin timeout. Capturas son del emulador, no recreaciones.
- Las fixtures colocan la pareja y preparan su estado para repetir el caso; la ROM de entrega no contiene esos atajos. Los CSV leen RAM durante el frame y pueden mostrar una lista SAT todavía en construcción: no se usan como prueba de ausencia de sprites. El intento de leer el espacio `videoram` del VDP devolvió ceros y **no constituye una validación hardware**. La comprobación exhaustiva de direcciones sí es independiente de ese intento, y se han revisado las capturas.
- La ejecución arcade auxiliar de diagnóstico avisó de checksum de `24j6-0.112`; no se usa para importar arte ni fijar constantes. Las constantes anteriores salen del binario/desensamblado de `analisis`, y el arte de su mismo decodificador.

## Límites de esta entrega

No es una validación de todos los casos del juego ni una promesa de equivalencia global con el arcade. Se verificaron los casos repetibles de cuenta y salida descritos. Se conservan las decisiones anteriores de cuándo zafarse (primera cuenta automática), la duración del tumbado y los límites/caídas de cuerda del port; no se ha ampliado su máquina de colisiones. GameFAQs no ha sido necesario para estos tres arreglos.
