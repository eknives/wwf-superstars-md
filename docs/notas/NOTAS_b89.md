# b89 — selección y controles

ROM: `/workspace/b89/wwf_b89.bin`  
MD5: `7c1c5202f5fb27f115278eecd9b9ffb9`  
Base b88 intacta: `96371335c6b9cb43b08d158ba73ec488`. Compilación local SGDK con el PATH/make solicitados, `BUILD_b89.log`.

## 1. SELECT PLAYERS — verificado, con límites indicados abajo

- Pantalla aislada antes del combate, después de título/START. Retratos, nombres, trama, logo central y cursores decodificados de los datos arcade, no redibujados. Escena: `0x704E`, `0x1F434 → 0x2034A`; mapa `0x210A8`; seis bloques 4×4 de `0x20404` (tiles `383–392`, `393–3A2`, `3A3–3B2`, `3D3–3E2`, `3C3–3D2`, `3B3–3C2`). Paleta 4: `0x706C/0x29F6`, tabla BG `0x2FAE`.
- Misma distribución 2×3 y posiciones. Conversión de 4 a 3 bits por canal propia de MD; no se reducen los colores de los retratos. Se reutilizan bancos CRAM en los huecos verticales: cambios al terminar líneas MD 95/119/143. La selección conserva las primeras 224 líneas arcade: solo se omiten las 16 inferiores de margen, sin escalar.
- Cursores verde 1P / amarillo 2P: tablas nativas `0x7686/0x782A`, dibujo `0x75B6`. Movimiento por flancos y sin envolver: tabla `0x74F2`. **Confirma A**, que ya era puñetazo/Button 1; B no confirma, igual que el despacho `0x749E/0x7552`. No permite elegir repetidos.
- Temporizador invisible `0x180` = **384 refrescos arcade**, `0x7098/0x72A4`. Reloj convertido a tiempo real: 6250/6528 por VBlank NTSC, 6250/5440 PAL; prueba: llega a cero tras **401** VBlanks NTSC y **334** PAL, aproximadamente 6,68 s nominales. Sorteo: módulo 6 y filtro de elegidos `0x740E–0x742A`; movimiento `0x747A`; nuevos candidatos cada 16 y confirmación en fase 63/64 (`0x73E8`). La semilla MD no reproduce los registros CPU aleatorios de `0x450A`.
- Destello: colores/pens de `0x2048/0x2054/0x205A`, pasos de 2 refrescos y duración `0x40`, motor `0x1F5C/0x1F86`. **81 ticks de registros de destello comparados con MAME: cero diferencias** (`flash89_result.txt`). Cierre de 64 refrescos, o 112 en versus: `0x7134–0x717A`, comprobados.
- Adaptación de inicios MD: START del mando 1 = solo, eliges dos; START del mando 2 = cooperativo, uno cada jugador; ambos START = versus, dos cada jugador. Los modos corresponden al cierre `0x72DA–0x73DC`. **El resultado se guarda pero no modifica el combate: sigue Duggan contra Warrior de b88.**
- Evidencia gráfica: 12 capturas comparadas con MAME, **0/57.344 píxeles distintos** tras conversión de color. Otras tres solo difieren en la fase visible del destello, no en los dibujos; se identifican así en las parejas. Inicial también comprobada en PAL y mando de tres botones. Resultados: `verify89/RESULTADO_b89.txt`.

## 2. Cuenta terminada → reiniciar combate — verificado

La selección solo se llama una vez antes del bucle de lucha. Se conserva `countStep/pinAdvance → matchReset` de b88; ningún reinicio vuelve al menú. Pruebas cortas con fixtures RAM justo antes del tercer golpe de cuenta y del 20 fuera: aparece 3/20, termina la espera existente de 120 frames y ambos luchadores vuelven a X=736/660, cuentas a cero, fase de combate=4 durante todo el recorrido. No se simuló una pelea completa para llegar naturalmente a esas posiciones.

## 3. C=A+B; intercambio a Y — verificado

Se normaliza C a A+B **antes de calcular flancos**, no se añade otra lógica de carrera. En dos ejecuciones independientes C y A+B generan **32 instantáneas idénticas de los 100 bytes del luchador**; C corre sin cambiar `ctl`. Mismo resultado con mando de 3 y 6 botones. Y del mando de 6 botones cambia `ctl` 0→1→0, una vez por pulsación. El atajo antiguo START+C pasa igualmente a START+Y para que C sea realmente equivalente a A+B.

## Capturas y límites

En `shots89/`: `pareja_C_initial.png`, `pareja_C_partner.png`, `pareja_C_confirmed2.png`, `pareja_COOP_initial.png`; `md_C_C_run.png`, `md_C_Y_swap.png`, `md_C_pin3.png`, `md_C_pin_restarted.png`, `md_C_ringout20.png`, `md_C_ringout_restarted.png`.

b88 no tenía título/inicio: se añade una puerta START con el título arcade **estático y reducido a 16 colores**; no se porta el attract, la presentación posterior ni la música 0x0A. Tras seleccionar hay restauración/carga del combate; no se afirma que esa transición sea idéntica al arcade. Tampoco se afirma sincronía de captura frame a frame en las tres imágenes con diferente fase de destello. MAME avisa de checksum distinto en `24j6-0.112` del set local existente; las comparaciones son contra ese set. Sin prueba Everdrive/placa física.

Todos los recursos preexistentes de `res/` siguen idénticos a b88 (excepto la lista/declaraciones de recursos nuevos). **Esquineros superiores y logo WWF del ring intactos; ningún otro movimiento, IA o timing de combate retocado.**
