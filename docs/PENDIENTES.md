# Pendientes de implementación — por prioridad

No autoriza cambios. Estado a b95; síntomas comunicados por Emilio sin ensayo nuevo se marcan como tales. Investigación sin resolver está separada en ESTUDIAR.md.

## ALTA — fidelidad funcional / foco Duggan

- **Movimientos todavía ausentes (excluidas las cadencias de prioridad BAJA)** del inventario `01_port_sgdk/actual/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`: Duggan High Knee, Body Slam, Headlock, Bulldog, Back Suplex, Back Body Drop, Dropkick contra corredor, Pick Up y Dropkick de poste; Warrior Shoulder Tackle, Body Slam, Headlock, Gorilla Press, Atomic Drop, ataques contra corredor, Pick Up y Dropkick de poste. El inventario b89 es histórico; consultar b92: Knee Warrior y energía avanzaron en b90/91; Stomp Duggan b92 supera los ensayos; Elbow suelo/poste funcionales, con cadencia pendiente exclusivamente BAJA.
- **Energía vs pin/kickout y levantarse:** integrar las reglas nativas que aún no cubre b90/91 fuera de Knee. Cero no KO; no extender indiscriminadamente AF66 ni el bloqueo de escape por cero. Fuente: estudio energía §§ Energía baja / Diferencias; `NOTAS_b90.md`.

## MEDIA — errores visuales/sonoros y cobertura de variantes

- **Público: sonido entrecortado**, comunicado por Emilio; revisar reproducción/mezcla y compararla con arcade antes de corregir. No diagnosticado de nuevo en este backup. Ver análisis sonido/público y notas históricas.
- **Macho verde**, comunicado por Emilio; corregir sólo tras comprobar fuente/paleta/banco. No se presenta como problema ya medido ni como cambio autorizado en otra versión.
- **Huecos del clothesline:** faltan variantes espalda/cuerdas y cobertura completa de enlaces/reacciones; b88 corrigió sentido de caída y paleta, no todas las variantes. Ver inventario b89, NOTAS_b87/b88 y estudio energía. No reabrir el contacto ya corregido sin evidencia.
- Completar cobertura natural de Knee/selección: otras esquinas, límites, rivales, juego sin fixtures y hardware. La normalización exterior específica y flicker de selección sí quedaron corregidos/verificados en b91, no se listan como fallos abiertos.

## Tras b93 (orientación rival tumbado corregida)
- **Sin verificar en b93:** derribo natural en partida→Knee/Elbow (sólo fixtures equivalentes), poste por el lado opuesto (sin datos arcade), PAL, Everdrive.

## Tras b94 (tumbado en X arcade + pin)
- **Zafar/cuenta vs MAME arcade:** sólo contrastado con código B012/B0A0; el fixture arcade sin árbitro no cuenta.
- **Aproximación del pin:** deslizamiento 513/514 histórico (arcade: 7E fijo en la X final, Z207). Volteo de 513 por convención de conversión (flip0), no medido por silueta. Salto de Duggan no medido.

## Tras b95 (carrera por tick arcade, fondo por DMA, choque contra cuerda)
- **Extender arcTick al resto de la lógica (apuntado, NO autorizado):** andar, arranque de carrera (3 frames), rebote rn 2 (pista 48 f), freno, clothesline y caídas (fs avanza cada 2 vueltas con `fsTick`) siguen por frame MD; en PAL/NTSC o con frames perdidos su ritmo difiere del arcade.
- **Frames perdidos corriendo entre cuerdas:** 40/580 en b95 (b94 55); no es el streaming (postes ya 0–3/580). Causa sin investigar (sospecha sin medir: `ropeDraw` CPU / carga de sprites).
- **Sin verificar en b95:** choque contra cuerda en lanzamientos/clothesline (sub 1, fixture del port: rebota W 627→659, D 906→874) y derribo por golpes junto a la cuerda (soilNudge 875/893 revisado sólo en código) frente a MAME arcade; frames perdidos en PAL; hardware real/Everdrive. Sonido 0x29 del aterrizaje de 9F02 no existe en el port (no añadido).
- **Límite derecho del ring:** `RING_XR` 917 del port vs 920 arcade (21E5A); sólo el choque nuevo usa 920−e. No tocado.

## BAJA — pulir al final

- **Cadencia del Knee Drop desde poste — PRIORIDAD BAJA, “pulir al final”.** Arcade **8/18/10 refrescos** frente a registros de b91 port **K11/19/7, P5/19/14**. Son muestras de pose cargada, no una certificación visual atómica. b91 NO resolvió este punto; descartó los experimentos de reloj/render. En NTSC/PAL hay que conservar tiempo real57,44485Hz, no imponer conteos idénticos a60/50Hz. Fuente `01_port_sgdk/actual/NOTAS_b91.md:6–12`, CSV por refresco y experimentos etiquetados. No es bloqueo para seguir con las prioridades de arriba.

- **Cadencia visible Elbow Drop Duggan, suelo y poste — PRIORIDAD BAJA, «pulir al final».** b92 ya entregada. Física/contacto/daños/A2 verificados; visible aún desigual: NTSC suelo10/17/12, posteP9/21/5,K6/19/12 frente a8/18/10 nativos antes de conversión. No reabrir ROM ni tocar Warrior por esta anotación. Fuentes NOTAS_b92.md y pose92_refreshes.csv. Se sitúa junto al pendiente de Knee Warrior desde poste.

## COMPLETADO EN ENSAYOS b92
Stomp: zonas23/24, daño1, impacto15A sin refiltro, conversión NTSC/PAL. Elbow: física/contacto/A2/daño/fallo y posteP/K, NO cadencia visible. Cobertura natural/exterior/otras esquinas pendiente.

## COMPLETADO EN ENSAYOS b93
Orientación del rival tumbado: sin espejo de tumbado→A2→espera en 16 casos; contactos = arcade (Duggan stomp/elbow/espejo/arriba/poste P/K; Warrior cabeza izq./der., arriba, poste K/P, exterior). Clothesline traza idéntica b92.

## COMPLETADO EN ENSAYOS b94
Tumbado sin lyoOf: zona pin sobre torso visible, Knee/Elbow sobre la cabeza; barrido B = arcade (W/D, ambas orientaciones); sin salto tumbado→A2 ni 114→115; pin Duggan por zona cuerpo CB75; quien cubre en X/Y/Z y orientación arcade.

## COMPLETADO EN ENSAYOS b95
Carrera = arcade en NTSC y PAL (W 200,5/199,7–200,1, D 194,0/192,6–193,0 px/s; arcade 201,1/193,9). Ralentización junto a los postes resuelta (20/14/18/19 → 3/2/1/0 frames perdidos de 580; 0 errores de fondo). Zafar junto a cuerda = arcade en Xv 760/728/708/693/832 (choque 9E78→9CD0→9F02, sin salto soilNudge).
