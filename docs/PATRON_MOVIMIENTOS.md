# Patrón de movimientos — receta documental del arcade → port b92

**Sólo estudio; no implementación, compilación ni ensayo MAME nuevo.** b92 ya está entregada (PARCIAL en fidelidad visible). Esto no autoriza añadir personajes/movimientos ni tocar Hogan. La cadencia visible de Elbow Duggan suelo/poste y Knee Warrior poste queda **PRIORIDAD BAJA, «pulir al final»**.

Fuentes relativas a este backup: `02_arcade_decompilado/analisis/arc_rec.dis` (instrucciones alineadas), `arc.dis` sólo para las ocho BRA.W consecutivas FC64–FC80; estudios `02_arcade_decompilado/estudios/{kneedrop,duggan_suelo,energia}/`; `03_roms/notas/NOTAS_b87.md`, `NOTAS_b88.md`, `NOTAS_b90.md`, `NOTAS_b91.md`, `NOTAS_b92.md`. Port leído: `/workspace/b92/src/`, idéntico a `01_port_sgdk/actual/src/`. Las notas b89/b90 anteriores son antecedentes, no estado b92.

**Calidad:** C=instrucción/índice confirmado por código; D=valor ya extraído/documentado; M=ensayo histórico explícito de D/W; U=contenido o comportamiento no confirmado aquí. Un slot calculado por un stride C NO implica conocer su puntero/valores ni haber probado ese luchador. No se ha vuelto a abrir/procesar prog.bin ni ejecutado MAME.

## 1. El patrón común: selector → subrutina → tablas → reacción

1. **Identidad:** byte `actor+2B` es id nativo; `word+2A & FF` selecciona las tablas. CPU es bit3 del BYTE `+2A`, no «el rival que no controlo». Banco gráfico y casilla del selector son conceptos distintos (`6CD8`, conversión de selección `7FE2`). Identidades canónicas:0 Warrior,1 Hogan,2 Macho/Savage,3 Duggan,4 Bossman,5 Honky,6 DiBiase,7 André.
2. **Entrada/selector:** flancos `+114`; buffer `+116` mantenido por `4066–40B6`. Elegir acción/sub por estado, plano, rival y zona. No deducir técnica del nombre de un sprite.
3. **Despacho:** acción byte `+2D`, tabla `8CE2`/despacho `8C82`; acción0C ejecuta `F94C`, que en `F980–F994` llama al puntero `FB58 + 4*sub` (`word+30 & FF`). Acción0C no significa Knee ni combo por sí sola.
4. **Reloj:** actor cada2 refrescos (`1508–1510`), MAME57,444852941Hz. `+6` pose, `+8` timer y `+36` paso suelen compartirse, pero cada rutina decide si decrementa al entrar, usa > o ≥, conserva dibujo al salir o añade preparación. **No convertir un dato de tabla directamente a frames60Hz.**
5. **Física y contacto:** coordenadas mundo X/Y/Z `+0C/+10/+14` 16.16; velocidades `+24/+26/+28` 8.8. Integración `3DCE/3E20`. Broad-phase, caja activa y energía son tres cosas diferentes.
6. **Final:** cambiar acciones de atacante/víctima, enlaces y capas/objetos auxiliares; restar energía sólo en el evento correcto. No sustituir toda reacción por una caída genérica.

### Traducción actual (NO motor universal)

`main.c`: `FC fd[2]`, `ctxLoad/ctxSave`, `engine`, `pendBtn`, `curPose`, `p1face/dFace`, `sx/bx`, `climb/ck`, `mv/mk`, `rn`, `gs/gk`. **Slot port0=Duggan nativo3; slot1=Warrior nativo0.** `curF`, `f^1`, `ctl` y filas `[2]` NO son ids nativos. Existen ramas `if(curF)` y `if(!curF)` y relojes privados; no basta añadir una fila ni cambiar el retrato. `gs14/15` b92 son etiquetas internas, no subs arcade0E/0F; el antiguo `gs11` decimal tampoco demuestra identidad con sub0B.

`FC.ox/oy`+`oxf/oyf` y privados `w81X/Y/Z`, `dugX/Y/Z92`, `kvZ90`, `fsX/Z` usan escala256: no representan toda fracción16.16 arbitraria del arcade. La física documentada conserva las fracciones representables; no certificar precisión universal. `arcClock/arcLast/arcTick/arcDen` convierten VBlank a ticks (3125/6528 NTSC,3125/5440 PAL, NOTAS_b87). Lógica por tick NO garantiza publicación de pose puntual por CPU/DMA/SAT.

Gráficos: `Pose/Piece`, `poseTab`, `spr_tab`, `spr_tiles`, `xld/xlw`, `dLog/dPose/dLoaded`, `dFlip/dLyo`, `fLoad/drawF/buildSat`. Pose nativa, alias de secuencia y pose convertida son índices distintos. Ejemplos: `duggan92_poses.h` apéndice849..860; `native81.h` Warrior779..791; `knee90.h` A2/17/1A para D y W. No reutilizar números de tile como ids nativos ni tocar paletas de ring/compañeros/árbitro. Los bancos de paleta por bloque citados en cl87.h (2 Warrior,7 Duggan) NO son los ids de luchador (0 y3).

## 2. Catálogo por id: slots que YA existen en el arcade

Todas las direcciones de las tablas siguientes son hexadecimales. Son direcciones de ENTRADA, no sus punteros destino, salvo `→` explícito. Fuentes C: `4624–463A`(banco), `FC54–FC5E`(combo), `C778–C794`(suelo dentro/fuera), `F63C–F648`(poste), `1500E–15020`(presa). Destinos de combo: ocho BRA.W FC64–FC80 leídas en arc.dis; son instrucciones reales del despacho, no pseudo-op de datos.

|id|Luchador/banco|puntero banco 6CD8+4i|combo FC64+4i → rutina|puntero suelo CADE+4i|puntero exterior CAFE+4i|poste F6E6+3i|presa 15126+3i|
|---|---|---|---|---|---|---|---|
|0|Warrior|6CD8|FC64→FC84|CADE|CAFE|F6E6|15126|
|1|Hogan|6CDC|FC68→FC84|CAE2|CB02|F6E9|15129|
|2|Macho/Savage|6CE0|FC6C→FDA0|CAE6|CB06|F6EC|1512C|
|3|Duggan|6CE4|FC70→FDA0|CAEA|CB0A|F6EF|1512F|
|4|Bossman|6CE8|FC74→FC84|CAEE|CB0E|F6F2|15132|
|5|Honky|6CEC|FC78→FC84|CAF2|CB12|F6F5|15135|
|6|DiBiase|6CF0|FC7C→FDA0|CAF6|CB16|F6F8|15138|
|7|André|6CF4|FC80→FC84|CAFA|CB1A|F6FB|1513B|

Contenido D conocido: slot suelo CAEA→CB6C; exterior CB0A→CBEC. Filas cabeza CB72=`04,11,04`, cuerpo CB75=`05,06,06`, columnas P/K/P+K; cuerpo exterior CBF5=`05,05,05` (TABLAS_DUGGAN, baseCBEC+9). Warrior usa CB3C dentro y CBBC fuera (estudio Knee/main.c). **Los destinos/bytes de los demás slots de suelo NO se han confirmado aquí: no asumir CB3C+16*i.** Los grupos se eligen en C79E–C8A8; cabeza offset6,cuerpo9; no asignar nombres a las otras filas sin leer su rama.

Poste: W F6E6=`2C,20,2C`; D F6EF=`2F,20,20` (estudios). `F650–F664` elige columna0 si rival acciónB,1 si no: **NO son columnas P/K/P+K**; el tercer byte no se consume en ese selector concreto. Bytes del resto de luchadores U. Presa15126 sí usa botón−1 (1501C/15020); contenidos por otros ids U. Tener fila no demuestra que todas las técnicas se accedan igual.

### Tablas del salto/impacto: distinguir atacante y víctima

C: `10A72–10AB2`: física `11150+16*idAtacante`, cuatro punteros long: +0 suelo normal,+4 suelo especial,+8 aire/poste normal,+C aire especial. Especial si víctima id7, o atacanteid6/sub11 (`10A90–10AA8`). `10AB6–10AFA` añade variantes por zona para sub1A; no extrapolar el solver D/W sin esas ramas.

C: `10CC8–10CF6`/`10F54–10F84`: poses `112FA+40*idAtacante +20*poste +10*variante +2*paso` (bytes). Cada bloque tiene20words: cuatro listas de5poses. Timers112F0 compartidos, NO por luchador. Caja de víctima `11084+4*idVictima` (dos words;10FCC–11001A). Punto atacante `110A4+8*idAtacante +4*poste` (dos words;11001E–11004E).

|id|luchador|base4punteros física|base20words poses|caja víctima|punto atacante suelo / poste|
|---|---|---|---|---|---|
|0|Warrior|11150|112FA|11084|110A4 / 110A8|
|1|Hogan|11160|11322|11088|110AC / 110B0|
|2|Macho/Savage|11170|1134A|1108C|110B4 / 110B8|
|3|Duggan|11180|11372|11090|110BC / 110C0|
|4|Bossman|11190|1139A|11094|110C4 / 110C8|
|5|Honky|111A0|113C2|11098|110CC / 110D0|
|6|DiBiase|111B0|113EA|1109C|110D4 / 110D8|
|7|André|111C0|11412|110A0|110DC / 110E0|

D confirmados: física11180/11188→111F0; especial11184/1118C→11200;111F0 words `(0,−64,0,0,0500,0050,2000,2000)`, especialoffset−80. Poses11372=`61,62,1CB,1CC,1CC /61,62,1CD,1CE,1CE`, repetidas para poste. Punto110BC/110C0=(8,4). W poses112FA:61/62/7A/7B; variante76/77; punto110A4=(0,4). Otros bloques **existen por el índice C, contenidos U**: no se ha extraído una lista inventada de poses Hogan/Macho.

### Forcejeo, pin y energía: otras filas por personaje

C: forcejeo B370–B382 usa **id del rival** en B46C+4*i (dos poses; tiempos compartidos B468). 14E0A–14E1C usa rival en150F6+6*i (tres poses; tiempos150F0);150E0+2*i usa id propio en14DEE–14DF8 para contador de esa rutina, no energía. Pin BDCC–BE62 usa fila BEF2+16*idAtacante, dx byte `[idVictima]`, dz byte `[8+idVictima]`; NO son parejas word(dx,dz). Hay excepciones ids0/4 enBD84–BE84 y objeto auxiliar. Valores por otros personajes U.

Humano7FEC+2*i=48 para los ocho (TABLAS.txt energía). CPU8190+16*progresión+2*i, no valores universales48; `1CD48+id` es umbral de mareo (1CD84...), NO energía inicial. AF66/AF6A/AF72 son bandas de energía, NO ids. AA00 usa `+F0&7`, tampoco id.

|id|luchador|forcejeo B46C|poses150F6|contador150E0|pin BEF2|energía humano|columna CPU fila0|umbral mareo|
|---|---|---|---|---|---|---|---|---|
|0|Warrior|B46C|150F6|150E0|BEF2|7FEC=48|8190|1CD48|
|1|Hogan|B470|150FC|150E2|BF02|7FEE=48|8192|1CD49|
|2|Macho/Savage|B474|15102|150E4|BF12|7FF0=48|8194|1CD4A|
|3|Duggan|B478|15108|150E6|BF22|7FF2=48|8196|1CD4B|
|4|Bossman|B47C|1510E|150E8|BF32|7FF4=48|8198|1CD4C|
|5|Honky|B480|15114|150EA|BF42|7FF6=48|819A|1CD4D|
|6|DiBiase|B484|1511A|150EC|BF52|7FF8=48|819C|1CD4E|
|7|André|B488|15120|150EE|BF62|7FFA=48|819E|1CD4F|

## 3. Recetas por familia: qué reutilizar y qué NO clonar

### A. Puños de pie / combo
- Arcade: sub0→FC4E→despacho FC64 por atacante; FC84 para W/Hogan/Bossman/Honky/André, FDA0 para Macho/Duggan/DiBiase. **Mismo motor NO significa mismas poses**: FDA0 elige FE88, excepción id2 FEAC (FDA4–FDB2); sus secuencias/duraciones completas no se reextraen aquí.
- FC84: FD70/FD7C poses150..152/153..155,4/3/3 **ticks**=8/6/6 refrescos de esos pasos; preparación FCAC=3ticks, final/enlace FD2E/FD48 timer1. Para **atacante id7 (André)** se eligen FD88/FD94, comprobación de id propio en FCC0–FCE6; no sustituir esas tablas por FD70 automáticamente. FCFC sólo acumula NUEVAS pulsaciones en pasoC (la comparaciónB existe, pero incremento4 no la alcanza); se decide `&3==1`, no mantenerP.
- Daño1 humano por impacto: W cabecera18810/byte18811; D187F5. `1761E[pose]→[id]` y copia1697E. No repartir1/2/3 por ser combo.
- b92: `engine` rama `mv==1`, `mk/pAlt/pAcc/pEnd`, `move_seq`, `arcTick`; ambos slots usan patrón FC84. **El combo D nativo FDA0 NO está portado fielmente**. Para otro personaje escoger primero su BRA de FC64 y convertir su banco/secuencia; no copiar el combo W a todos. `hittable`/alcances actuales no son todo el motor de cajas arcade.

### B. Patada
- Arcade: sub1→FED0; FF3A normal, FF4A cuando idAtacante7 (FED6). Avance en FEFc–FF38, salida especial C9.2; durations reales dependen del decremento y salida, no se certifican aquí para otros ids. Pose158: W188AB=4,D188C7=4. El motor de cajas determina cuándo está activa.
- b92: rama `mv` restante, `move_seq` offset33, `MV_HIT_KIK/MV_REACH_KIK/MV_REACH_Y`; daño4 o6 contra carrera/whip representada. Reacción genérica `victimStep/vh`; no es un descriptor nativo completo. Dar patada a otro: tablaFF3A/FF4A + banco + cajas + reacción + daño, no sólo copiar `mv=2`.

### C. Carrera y clothesline
- Arcade: carrera93EE, rebote960A/96AA; A durante carrera CD14→acción0C/sub14→12E7A. Tabla compartida1302E:1D0/1D1/1DA/1DB, captura1D2+idVictima durante8ticks; detieneX en12F04 y lanza en12FAA, no al primer toque. Proximidad16634 (`|dx|<60hex,|dy|<8`, coordenadas mundo X/Y) NO es caja final;1672C/16796 y cajas1761E, caso1890C→18C2A (NOTAS_b87).
- b92: `engine` rn1/2/3, `clStep87`, `clInit/Step/Timer/Held/Pose`, `rnW`, `rnx`; usa broad-phase+intersección de pie, daños4/2. `clHeld` y liberación ligados al rival. Huecos conocidos: corredor, espalda/cuerdas y enlaces; `hittable` excluye carrera. No declararlo motor arcade íntegro.
- Para otro: convertir banco atacante incluyendo **las ocho capturas 1D2+victima**, probar qué caja toca, y convertir la caída del banco víctima. No confundir `rnd` con H-flip: liberación b92 llama `clFallStart(o,-rnd)` por12F16/12F1C y9BC6/27D2. El movimiento sin impacto/carrera ordinaria no resta energía por existir.

### D. Forcejeo / Irish Whip
- Arcade: B1D0/B48C/B670 y tablas B46C/B468; ruta14DD6 y150F6/150F0; entrada humana14FEE→15126. Varias tablas eligen **tamaño/id del rival**, no sólo personaje atacante. Selección de llaves por botón es diferente de decidir ganador del forcejeo.
- b92: `grTry/grStep`, `gr/grk/grCool`, `lkC*`, `trStart/trStep`, `spT`, `sp_trk`, `trO/N/Pose`, fases rebote`rw*`; pistas S/W1E representan sub1E→14CFC (contra-llave que suelta a acción15). No contienen Body Slam, Headlock, Gorilla Press ni finishers completos.
- Receta: modelar dos actores enlazados y sus tablas cruzadas, entrada/reverse/ganador, luego liberación y rebote con límites21E5A/21ED0. Daño propio forcejeo/whip/rebote interior=0; choque especial exterior2209C=5 sólo con filtros220BE/2208C y antirrepetición. No cobrar un daño de Body Slam por reutilizar la pista de whip.

### E. Suelo: Stomp y Knee/Elbow
- Selección común C706/C778–C8A8: mismo plano, |dy|<24; cabeza Xv±40 (André±56), zonas estrictas32/48 (André40/56), tabla de accionesCB1A. El buffer/las excepciones por acción son distintos de la prueba final de impacto. Pin/cabeza/cuerpo no se eligen sólo por distancia absoluta al centro.
- **Stomp sub5:**1173A/118BC `(159,8),(15A,4)`; consume al entrar11750→1175C:159×14/15A×10 refrescos incluyendo salida. Golpea al entrar15A (11782/11786→1179A); sólo plano/estado final, sin segundo filtroXY.117E0 daño1; excepción117E6 compara banco gráfico+3 con7 y escribe3. b92D=`dugZone92/dugStart92/dugStep92`, gs14; W=`warriorGround*`, gs13. **Reloj W stomp existente no es el D arcTick recién portado** (`if(!(gk&1))`): no afirmar igualdad universal.
- **Drop común10A5E:** W sub0C/2C, D11/2F; selecciona física/poses por las tablas §2, solver156FA→159AC, integración3DCE/3E20. D/W:8/18/10 refrescos iniciales, no112F0[0]=0 interpretado como1tick;10F54 espera4ticks, luego comparador10D42>8/>4. Tras eso contacto/recuperación variables.
- Impacto10BF8–10C3C→10FCC: descendente, víctimaB y mismo plano, Zword≤suelo+16; caja11084 por víctima y punto110A4 por atacante/poste. Escribe Yword=Yv−1 y Zword=suelo, conservando fracciones; W añade ajuste1152A y variante76/77, D NO ese+10 ni7D. Daños10DC0=5/10DCC=10, reacción8/subD→A2. Fuera offset solver se divide2 (15A52), no prohibir por «cerca de cuerda»; manejadores de D11/2F en24102/24106 terminan RTS24322/24324.
- b92W=`warriorGroundStart/Step/End`, `w81*`, `kneePost90`, gs12; b92D=`dugStart92/Step92/End92`, `dug*92`, gs15. Víctima compartida `kneeVictimStart90/Step90`. D conserva fracción, punto±8,+4, A2 y daño1/5/10; no usa antiguos alias genéricos gs5/gs11.
- **Otros personajes NO son copia D/W:** Hogan id1 duplicaVx/Vy en suelo10B70–10BAE, al descender los borra y cambia gravedad10C00–10C16; daño+1 en10DDA y final/rebote especial10E30–10EA8. Sub1A impone11,sub0F6; id7 impone12 al final de esa decisión10DFC–10E04. Orden de excepciones importa. Para DiBiase id6/sub11 hay selector especial10A98/10B42. No identificar aquí el nombre comercial de esas técnicas ni dar por probadas sus animaciones.

### F. Ataque desde poste
- Arcade: acciónF, estado+B8=2, F35A recibe P **o K**, F636 elige la filaF6E6 según rivalB. W sub2C/Dsub2F entran al MISMO10A5E, no un salto independiente. Flags+34, alturas y solver cambian la trayectoria; límites10B5E/110E4 (distancia horizontal≥96→Vx±200hex, vertical≥80 interior/112 exterior→Vy±100hex).
- b92: `climb/ck`, `cPOST/cD0`, `CK` tablasclimb*, ramas `engine` poste, `kneePost90` W / `dugPost92` D. Rival de pie/dropkick de poste sigue ausente. No cambiar input global ni elegir otra técnica sólo por compartir botón.
- Para otro: probar la sub que realmente devuelve su fila, resolver desde su esquina/altura, cargar lista de poses `+20` y punto `+4`, daño y final de SU rutina; puede no ir a10A5E. **Cadencia visible D suelo/poste y W poste pendiente BAJA «pulir al final»**, no se da por resuelta al copiar tablas.

### G. Pin / cuentas / reinicio
- Arcade: cubrir acción17→BD10, entradas1190C/11A72/12972, flag víctima+18.5; matriz BEF2 por pareja, poses65 o7F segúnid0/4 y188 porflag. ÁrbitroD7D8: DD4E cuenta3 (posesDED4, tiemposDEDC), DEE4 cuenta exterior20; E02C/E0A8 voces. Esas tablas del árbitro no son por luchador.
- Bandas AF66/AF6A/AF72 y pin humanoADEA/CPUAE7E dependen de energía/flags/tiempo, no «primer pin siempre se libra». Para escape humano prevalece estudio energía §Energía baja sobre simplificación antigua de pin_cuenta.md: AE24–AE40 compara acumulador con48−E; E0 bloquea esa salida, no KO automático.
- b92: `pinStart/pinStepA/pinAdvance`, `pn*`, `rs*`, `digPin`, `countStep` (RO_TICK/roC), `roC/roT/roDone`, `resetReq→matchReset→fighterInit`. El modelo de kickout aún no integra toda la energía nativa. Regla de diseño port autorizada:3/20 **reinicia combate sin SELECT**, no confundirlo con transición arcade que habría que copiar para equipos completos.

### H. Energía, daño y reacciones (comunes, con datos por pose/id)
- Energía+3C distinta de daño pendiente+3E; resta16488–1649A satura0. Sin regen pasiva identificada,0 no KO; existen recargas ENTRE combates2060–20EC y Power Up6F64/6FEE (no son regen durante lucha). b92=`energy90[2]`, `hurt90`, `fighterInit`48, sin HUD, ambos HUMANOS. `vdmg/vlast` no son energía. Todo luchador nuevo debe recibir energía independiente, no convertir al no controlado en CPU.
- Cajas:1672C→1761E[pose]→[id] (cabecera byte+1 daño),1697E copia;1698A CPU víctima contra sub0/1 fuerza0.1638E/1642A añade bonus sólo contra acciones1/15/16;16418 duplicaF9.0; enlaceFFFE162BC omite ambos. D/W: puño1,patada4,clothesline4/2,stomp1,drop5/10. No copiar valores a Hogan/André ignorando sus excepciones ni inventar contactos para llaves ausentes. Daño extra1642A/contador17590/sonido175CE son por SUB, no id.
- **A2**: reacción acción8/sub0D (despacho99BE/9A14, A554→28EC), Vz200hex,g40hex; alturas relativas4/7/9/10/10/9/7/4/0 en9ticks; poseA2 del banco de VÍCTIMA, aterriza17/estadoB; esperaB conservada segúnAB7A, levantada5/1A (AA00). Port `kneeVictim*90`, `kvPhase/Time/Z90`, `ground90`, `kneePose90`; no añadir espera fija universal.
- **Lanzado0x17**: acción8/sub17→9B9A, NO acción17 pin. A8BE/2964: desplaza±32, altura+24,Vx±80hex,Vz100hex,g30hex; pose15→16 al descender bajo24, rebote9C94→A4C8 sinVx, acaba17. Port `clFallStart/fsStep`, `koF==3`, `fs*`, `clFallPose` en `cl87.h`. b88 corrigió sentido/flip y paletas por bloque; pose native15/16/17 se carga del banco víctima, NO del atacante. Resto `victimStep/fsStart` no equivale automáticamente a estas dos reacciones.
- **Fallo drop**:10C4A–10CB2/10C6A, humano pierde2,CPU0;retroceso±24 por orientación,+acción8/sub5;9FCC voltea una vez y usa1CF→16→17→1A,AF66/AA00 para final. b92D fase6/7/8 en`dugStep92`; W rama de fallo`warriorGroundStep`. El salto125F0/1274E es OTRA rutina (fallo4), no universalizar−2.

## 4. Receta paso a paso para dar una técnica a otro luchador (trabajo futuro)

1. Identificar id/banco, rol humano/CPU y técnica desde su fila de selector; registrar slot y destino REAL. Si figura U arriba, leer ese dato antes de elegir comportamiento. No tocar Hogan por usarlo como ejemplo.
2. Anotar acción/sub, eventos/flags, rival admitido, zonas/orientaciones/planos; verificar si la tabla indexa atacante, víctima o pareja. Consultar excepciones id1/4/6/7; no repetir el error «mismo código=misma técnica».
3. Separar datos (poses, tiempos, offsets, cajas, física, daños) del controlador. Una futura estructura `descriptorPorId` sería DISEÑO PROPUESTO: **no existe como motor genérico en b92**. Sustituir ramascurF requerirá alcance autorizado específico, no cambiar sólo assets.
4. Convertir desde6CD8 el banco correcto con pose→piezas→tiles/paleta; respetar bloques prestados (b88), pivotes/H-flip/capas/auxiliares, añadir sin sobrescribir prefijos ni recursos de Emilio. Referencias: conversores `04_herramientas/scripts/b88/tools/gen88.py`, `b92/gen92.py`; compilar no necesita regenerarlos.
5. Reproducir init/step/hit/recover/miss/final con reloj nativo y fracciones, incluir víctima/reacción/energía. Enlaces de2actores no son una animación aislada. No aplicar contacto dos veces ni daño en cada refresh de caja activa.
6. Con autorización de implementación posterior: ensayos cortos MAME/MD por tick y por REFRESCO visible; registrar pose nativa/convertida/cargada, mundoXYZ/fracciones/velocidades/energía, espejo, suelo/poste/exterior y fallo. No comparar conteos57,44/60/50 sin tiempo real, ni dos capturas de fases distintas como sincronía.
7. Conservar controles C=A+B,Y cambia, sin IA nueva/START sólo persigue; energía para todo nuevo luchador; regresión de Hogan y recursos intocables, resto movimientos. Nueva carpeta/ROM+MD5 sólo cuando se autorice, nunca como consecuencia de esta guía.

## 5. Evidencia reutilizable y huecos

- Mecánica suelo D/W: estudios Knee/Duggan y `02_arcade_decompilado/notas_historicas/b92/shots92/{validation92.json,trajectory92_compare.csv,pose92_refreshes.csv}`. 88estados estables coinciden, no igualdad visible completa. Casos de b92 son fixtures RAM+botones, no todas las esquinas/partida natural/Everdrive.
- Combo/clothesline/caída: NOTAS_b87/b88 y capturas b88; huecos corredor/espalda/cuerdas siguen.
- Daño/excepciones: estudioenergía, `ENERGIA_ataques.csv`, `TABLAS.txt`, `cabeceras_poses.csv`; índice porpose/id confirmado, cabeceras de otros luchadores no recalculadas aquí.
- Hogan/Macho/Bossman/Honky/DiBiase/André: entradas/strides C listados, pocas excepciones leídas; **sin pruebas nuevas ni certificación de sus técnicas completas**. Punteros/bytes marcados U no se completan por semejanza visual.
- Prioridades oficiales: `PENDIENTES.md`; b92 entregada según `03_roms/CHANGELOG.md`. Documentar pendientes no vuelve a abrir la ROM.

## 6. Orientación del rival tumbado en Knee/Elbow (suelo y poste) — estudio 9-11-2026

Sólo lectura de `arc_rec.dis` + capturas b92 ya existentes; sin MAME nuevo, sin ROM ni cambios de port.

**Arcade (C):** el rival NUNCA cambia de orientación. `10A5E` sólo escribe `+A` del ATACANTE: copia la del rival (`10A6C`, otra vez `10BB2–10BB6`); id0 Warrior o sub1A la sustituyen por el signo de Vx (`10BC4–10BD8`). Desde poste (+34≠0, salvo id4) el flag gráfico `+4` del atacante sigue el signo de Vx en preparación/subida (`10F90–10FAC`, `10D02–10D26`). El impacto (`10D58–10E0A`: `+2C=8`, `+44=0D`, daño `+3E`, `161C8`, sonido `C6CA`) y la A2 (`A554`: `27D2(8)`, pose `A2`, `A56E move.b +A→+4`) dibujan la víctima con su MISMA `+A`. `C6CA` sólo elige sonido.
- Destino: solver `156FA` hacia `Xv ± offset` según bit7 del RIVAL (tabla física §2); poste: `10B5E/110E4` sustituye Vx/Vy por ±200/±100 hex si lejos de `Xv±64`. Caja `11084[idVíctima]` también por bit7 del rival (ori0 `Xv−64<X≤Xv`); punto `110A4[idAtacante]+4·poste`. Cabeza: ancla `Xv−40` si bit7=0, `Xv+40` si 1 (`C83E–C858`). El atacante se adapta al rival, nunca al revés.
- Acierto `10BF8–10C3C→10FCC`; fallo `10C4A–10CB2` (−2 humano, ±24, acción8/sub5, `9FCC` voltea SÓLO al atacante). Aterrizaje víctima `A5DA–A60A`: Z=suelo, acción B, `+AE=0`; orientación intacta.

**b92 (C, por código + PNG):** convención doble de `vface`.
- Todo dibujo de víctima tumbada usa flip `vface^1`: pose genérica 114–117/626 por `invFl` (`main.c:462`, `1485`, con `lyoOf` ±32) y caídas nativas 15/16/17 (`main.c:1468`, `dFlip=vface^1`). Al levantarse de A2, `main.c:473` pone `p1face=!vface`. Es decir, **la orientación nativa mostrada = `vface^1`**.
- El Knee/Elbow usa `vface` como si fuera bit7 nativo: zonas `main.c:649`, `duggan92.h:11–14`; destino `main.c:677/685`, `duggan92.h:34/39`; caja `main.c:736`, `duggan92.h:82`; atacante D copia `vface` (`duggan92.h:28`); y la A2/espera se dibujan con `dFlip=vface` y `dLyo=0` (`kneeVictimStart90 main.c:483`, bucle `main.c:1465`).
- Efecto: el atacante apunta al lado que en pantalla son los pies y, al contacto, la víctima se espeja (y pierde el desplazamiento ±32) para que la cabeza quede bajo la rodilla/codo. Evidencia: `05_referencias/capturas/b92/volteo_A2_b92_suelo.png` (refrescos 118→124 del caso elbow: botas a la izquierda → a la derecha) y `volteo_A2_b92_poste_suelo.png`. Ocurre también en suelo, no sólo poste.
- Los ensayos b92 no lo detectaron porque fijaban `vface=0` frente a arcade ori0, asumiendo `vface=bit7`; las coordenadas coinciden en ese marco, no en el visual.
- **Cadencia 8/18/10:** NO hay relación demostrada. El volteo no toca los temporizadores del atacante y las muestras irregulares de pose cargada son del atacante; sigue siendo pendiente BAJA de publicación visible. (U: no medido si la carga de tiles de la víctima en el refresco de contacto añade retraso.)
- U: posición exacta de 114 con `lyoOf` frente a pose nativa 17 en el mismo `ox` (posible salto de 32 px aun con flip correcto); flujo natural (derribo por golpes/clothesline → Knee/Elbow) sin fixtures, no ensayado.

**Propuesta b93 (base b92) — IMPLEMENTADA en b93, ver resultado abajo:**
1. Un único helper `oriVictima(o)=vface[o]^1` (orientación nativa mostrada) y usarlo en lugar de `vface[o]` en `warriorGroundZone`, `dugZone92`, destinos/solver/override de poste, caja de impacto, `kneeOutsideVictim91` y copia de orientación de Duggan (`duggan92.h:28`).
2. A2 y espera: `dFlip=oriVictima` en `main.c:483` y `1465`; conservar `p1face=!vface` al levantarse (ya coherente). Revisar si hace falta `dLyo` para que no salte 32 px.
3. No tocar `vface` ni cómo se asigna en caídas/golpes (evita romper clothesline b88 y pin). Stomp: la zona cuerpo se corrige con el mismo helper (hoy también invertida respecto a lo mostrado).
4. Verificar: fixtures con arcade ori0 ↔ port `vface=1` (y espejo), mismos contactos 88 estados; PNG por refresco sin espejo en contacto; caso natural derribo→Knee/Elbow suelo y poste, ambos lados; regresión Warrior/Duggan, clothesline y pin.

**Resultado b93 (MD5 a89af7ed95159c0899430bf0e81f6441):** implementados puntos 1–3 (`oriVictima` en main.c:464; A2/espera main.c:485 y 1467 con `dLyo=0`, que es la colocación arcade de la pose nativa en Xv). MAME: contactos = arcade en todos los casos Duggan y Warrior; flip del rival constante tumbado→A2→espera; capturas `05_referencias/capturas/b93/shots93/contacto93_*.png`. Clothesline: traza b88 idéntica b92/b93. Pin: mecanismo igual; el pin del Warrior (zona C798) ahora cae en el lado visible correcto. Confirmado lo que era U: sí hay salto ~32 px entre la pose genérica tumbada (con `lyoOf`) y la A2 nativa; queda pendiente (no es de la A2). Sin ensayar: derribo natural, poste lado opuesto, PAL.

## 7. Pin (cubrir) de Warrior sobre Duggan — verificación arcade vs b93 (9-11-2026, sólo verificación)

**Arcade, código (`arc_rec.dis`):** Warrior/Bossman (id 0/4) cubren por `11A72` (sin salto): `11A8A–11A90` orientación del que cubre `+A = +A(víctima) XOR 0x80`; pose 0x7E; `Y=Yv+1`; `X = Xv ± BEF2[0][3]` (=32; `btst #7,+A(víctima)`: bit7=1 → +32, 0 → −32 con `neg`), `Z=0xBB−16+2·18=207`. Tras 8 pasos (`11B2A–11B60`) acción 0x17 → `BD10`: misma X, `Y=Yv−1+2`, `Z=0xBB−16+16+16=203`, pose 0x7F con `+4=+A`, auxiliar `1C0AB2` pose 0x80 mismo X/Z, Y−2. Tabla `BEF2` fila0=[48,32,32,32,36,32,32,40 | dz 16,13,13,16,13,16,13,18]. Duggan (id3) usa `1190C` (salto 1C00B4): orientación = signo de Vx (`11992–119A2`), luego la MISMA `BD10`: `X=Xv±36` (BEF2[3][0]), `Y=Yv−1`, `Z=0xBB−13`, pose 0x65. Disparo Duggan: fila cuerpo `CB75=05,06,06` (K en zona cuerpo = pin, la misma zona que el Stomp, entre la cabeza y Xv).

**Resultado MAME arcade (6 casos: ori0 Xv 680/760/880, ori1 640/760/860; dentro del ring, sin empuje ACA4):** siempre `X−Xv=−32` (ori0) / `+32` (ori1), `Y=301`, `Z=203`, `+A/+4` del que cubre opuesto a la víctima. B→sub6 +2 f, pose 7E en la X final a +4 f (Z207, sin desplazamiento), 0x17 a +26 f, 7F a +28 f. En bordes el arcade empuja al tumbado hacia dentro (ori0 640→675, ori1 880→861).

**b93 (código, `main.c` `pinStart`/`pinStepA`, sin cambios desde b77):** lado por `pnM = oriVictima?−1:+1` y `pnX = Xv − lyoOf(114)`; X final = `pnX + pnM·32 = Xv` (no `Xv∓32`). `Y=Yv+1` y `Z=203` (pose 778 = 7F+80, dos capas) correctos. Orientación: `p1face=(pnM<0)=oriVictima`; como 778 se convirtió ya espejada (`gen77_pin.py arc(0,ap,1)`), el sprite sale ESPEJADO respecto al arcade.

**Resultado b93 (mismos 6 casos):** X=Xv en todos (32 px desplazado del arcade en absoluto, hacia los pies), pero respecto al cuerpo VISIBLE del tumbado (dibujado con `lyoOf` ±32) la posición coincide con el arcade a ≤4 px (medido en capturas: cabeza Warrior↔botas Duggan 2/−15 px vs arcade 6/−15). Y/Z exactos. Lado del cuerpo correcto en ambos lados del ring. **Volteo:** silueta de 778 contra arcade IoU 1,00 sólo espejada (0,97 sin espejar) en los 4 casos medidos; error de color 58 vs 117. Aproximación: b93 desliza 24 f con poses históricas 513/514 (Z187) desde Xv−35; arcade coloca 7E quieto en la X final. Asiento 778 a +29 f vs 7F a +28 f. b92 tiene el mismo código de colocación (sólo cambió la zona de disparo).

**Veredicto (b93):** NO del todo correcto (corregido en b94, ver §8). Bien: lado del cuerpo, Y, Z, relación con el cuerpo visible, tiempo del asiento. Mal: (1) Warrior cubriendo espejado en ambas orientaciones; (2) aproximación distinta (deslizamiento 513/514 vs 7E fijo); (3) X absoluta = Xv en vez de Xv∓32 (compensa el `lyoOf` de la pose tumbada genérica; mismo origen que el salto de 32 px). Propuesta (NO implementada): (1) en `pinStart`, para Warrior `p1face=dFace=!oriVictima(v)` (= `+A(víctima)^0x80` con la convención de 778), comprobar luego el flip de 513/514; (2) opcional: sustituir la aproximación por la pose 7E convertida (fija en X final, Z207, 24 f); (3) sólo junto con el arreglo de la pose tumbada (lyo): `pnX=Xv`, X=`Xv+(oriVictima?32:−32)`. Duggan: misma regla `BD10` (dx36/dz13), mismo `pinStart`; no medido en MAME aquí; su disparo (`bodyX±24`, lado pies) no es la zona arcade `CB75`.
Evidencia: `05_referencias/capturas/b93/pin_warrior/{pin93_comparativa,pin93_zoom_volteo,pin93_cmp_lados}.png`; datos `02_arcade_decompilado/notas_historicas/b93/pin_warrior/`.

## 8. b94 — tumbado en X arcade + pin ajustado (9-11-2026, MD5 b2a8ff5d4453067ad3d2bf8762239413)

**Implementado (sólo 2 puntos):** (1) `bodyX=ox`, `dLyo=0` en tumbado 114/626/752 (main.c:487, 1491): la pose sin lyo ocupa lo mismo que la 0x17 nativa en Xv (fl0 −56..16 vs −54..10). (2) `pinStart`: `pnX=pnVX=Xv`, `pnM=oriVictima?+1:−1` (BD10/11A72), `pnKD=pnM` (B012/B0A0); Warrior `dFlip=(pnM<0)` para 514/778 (convertidas espejadas, match69 flip1) e invertido para 513 (arc pose 2 flip0) ⇒ mira al revés que el tumbado (11A8A); Duggan flip sin cambio; árbitro `rfX=Xv±64`, `rfM=−pnM` (misma posición relativa al cuerpo que b77). Pin Duggan por `dugZone92==2`+B (C706/CB75 fila cuerpo, 06=cubrir); quitado `bodyX±PIN_ZONE` (b69).

**Resultado MAME (Xv=760):** barrido B d −88..+88 paso 8 IGUAL al arcade en W o0/o1 y D o0/o1 (W: K −64..−40, P −32..−16 / P +16..+40, K +48..+64; D: K −64..−40, P −32..0 / P 0..+40, K +48..+64). Quien cubre: W X−Xv ∓32, Y301, Z203; D ∓36, Y299, Z174 (arcade ∓36/+36.97, 299, 174.5); lado del ring 680/860 OK. Silueta: asiento y 514 directos en b94 (b93 espejados). Contactos Knee/Elbow/Stomp = arcade 16/16, flip/dX constantes sin lyo; levantarse 114→115 sin salto. Clothesline idéntico b93. Zafar: tumbado Xv∓8, cubre Xv∓48, Y−1, Z+4 (= fórmula B012/B0A0; no medido en arcade). Cuenta de 3 OK.
**Efecto colateral:** aterrizaje tras zafar cerca de la cuerda: ACA4 empuja ~33 px (pendiente medir arcade).
Evidencia: `05_referencias/capturas/b94/`; datos `02_arcade_decompilado/notas_historicas/b94/shots94/`.

## 9. Investigación 9-11-2026 (sólo estudio, sin cambios): carrera, ralentización junto a los postes, choques con las cuerdas

**(b) Carrera — arcade (código):**
- `93EE` acc_correr → `945C` init: velocidad byte `0x95BC[id]` → `+0x21` (= [28,28,30,27,24,30,27,20]; Warrior id0 = **28**, Duggan id3 = **27**), ángulo `+0x1E = (+A&0x80)|0x40`, modo de movimiento `+1 = 1`, sin aceleración.
- `3DCE`→`3DF0`: cada tick X += velocidad·2·0x20/256 px = **vel/4 px** (Warrior 7, Duggan 6,75).
- `94CE`: poses `0x95C4[id]` = 10..15, 2 ticks cada una.
- `953C`: `21E5A`; al tocar la cuerda del lado al que corre → acción 2 (`960A`).
- MAME arcade: 1 paso cada 2 refrescos en 65/65 casos (también por la cuerda superior junto a los postes). W 201,1 px/s, D 193,9 px/s (57,444 Hz). Poses cada 4 refrescos.

**(b) Port b94 (`main.c` 821–832):**
- Avanza `27<<6` (8.8 = 6,75 px) cuando `tick&1`. `tick` cuenta iteraciones del bucle (main.c:1460), no `arcTick` (main.c:1428, que sí descuenta 57,44→60/50).
- Mismo 27 para los dos; el arcade da 28 a Warrior.
- Medido en MAME:
  - NTSC: Warrior 194–202 px/s, con 3 de 75 frames perdidos (vs 201,1).
  - **PAL: 167,7 px/s (−16,6 % W, −13,5 % D)**, porque sigue siendo 1 paso cada 2 refrescos, ahora a 50 Hz.
  - Las poses van cada 4 frames del MD: también un 17 % más lentas en PAL.
- Causa: carrera (y andar/animaciones) por frame MD en vez de por tick arcade, más velocidad fija 27.

**(a) Ralentización — port b94:**
- Las pérdidas de frame coinciden siempre con el scroll de cámara que cruza un tile: el bucle de `main.c` 1507–1510 llama a `put()`/`rel()` (main.c 196–208).
  - `acq` carga cada tile nuevo con `VDP_loadTileData(...,CPU)`, y `put` hace 2× `VDP_setTileMapXY`.
  - Una columna son 29 filas (≈490–526 palabras de VDP por CPU) y una fila 33 tiles.
- Frame con streaming: ocupado 0,83 frame (mediana) frente a 0,25 sin él. Cualquier carga extra (pose nueva en `fLoad`, cuerdas, público `caApply`) pasa de 1 frame y se pierde.
- Como la lógica avanza por iteración (`tick`), cada frame perdido ralentiza el juego.
- Cerca de los postes la cámara (`camera()` 289–332, pasillo `camtab`) se mueve en X e Y a la vez. `main.c:330` impide columna y fila en el mismo frame, así que se encadenan.
- Medido (MAME genesis NTSC, ventanas de 59 frames):
  - aproximación diagonal al poste superior izquierdo: 8/59 frames perdidos (13,6 %);
  - poste inferior: hasta 12/59;
  - andar horizontal por el centro: 2,4 %;
  - quieto: 0.
- Sprites en la SAT (`nsat`): 3–20 junto a los postes superiores y 0–39 junto a los inferiores (límite 80). No coincide con los frames perdidos; los sprites por línea no se midieron por separado.
- Arcade: scroll por hardware, sin streaming; la lógica no pierde ticks junto a los postes. En hardware real (escrituras CPU al VDP en pantalla activa) puede ser peor; no medido.

**Cuerdas — tres casos arcade:**
1. **Rebote** (corre él o lo lanzan):
   - `953C`→acción 2 `960A`: gira, anim 0x10, velocidad 9 que baja 1 por tick, `9700` marca la cuerda.
   - Lanzado: acción 8 → `9CD0` → sub 2.
   - Port: rn==2 (pista 48 f, verificado en s66).
2. **Salir:**
   - `CD2C`→`CD5C/CDF8`: tocando la cuerda lateral (`+0x18` bit0/1 de `21E5A`), dirección 7/3 hacia ella, y+z en [0x1E0,0x230), sin 1C1898/189A bit6.
   - Humano de equipo: 12 ticks (`+0x102`).
   - Acción 3, o 6 si no es de equipo, está dentro y +2A bit4/bit1 están a 0.
   - Port main.c:1023–1026: 27 frames (`SX_HOLD`) en la X de la cuerda.
3. **Choque:**
   - `9E78` cada tick prueba X∓0x10 adelante con `21E5A` (lo deshace si toca, salvo poses 9A/A1).
   - `9CD0` compara el byte alto de +0x44, así que **siempre pasa a sub 2** (MAME: sub 0x1C→2 al primer contacto, no a sub 1).
   - `9F02`: `9700` marca la cuerda (1C1898/189A = 0x4001: vibra), z≥0xCB, pose 0x16, `27D2` índice 0x11 (parámetros de vuelo 0x2934: Vx 0x100, Vz 0, g 0x10; no es sonido — corregido en b95), **Vx negada**: rebota hacia dentro 2 px/tick hasta z=0xBB → acción 0xB.
   - Sin cuerda, sub 0x1C cae con −0x20 extra (`9C5A`).
   - `ACA4` al tumbarse prueba ±0x30 y ∓8 **según bit7 de +A**.

**Choque al zafarse (B012/B0A0) — MAME arcade vs b94** (S = X del que cubre al zafarse):

| Xv | S | Arcade | b94 |
|---|---|---|---|
| 760 | 712 | 642, sin cuerda, se queda | 642 → `soilNudge` → **675** (salto 33) |
| 728 | 680 | 643, se queda | 627 → 675 (salto 48) |
| 708 | 660 | choca: cuerda vibra, pose 22, rebota hasta **677** | cruza hasta 627 sin rebote → 675 |
| 693 | 645 | choca → 677 | 627 → 675 |
| 832 (der.) | 880 | choca → **859** | 906 → 858 |

Causas port (`main.c` 498–552, 625–632):
- `fsRope` mira la X propia ya recortada, no X∓16 adelante.
- Sub 0x1C pasa a fs2 en vez de fs3.
- fs3 no mueve X (falta la Vx negada).
- `soilNudge` usa `vface` como bit7, cuando la convención b93 es `oriVictima = vface^1`; por eso empuja hacia el lado equivocado.

Evidencia: `02_arcade_decompilado/notas_historicas/inv95/` (arc_run*.csv, arc_zafar*.csv, port_zafar.csv, b94_*.csv y scripts .lua).

## 10. b95 — carrera por tick arcade, fondo por DMA, choque contra cuerda (9-11-2026, MD5 7be789d70d892c1efb86af8630b296a6)

**Implementado (sólo los 3 puntos de §9):** (1) carrera: `rnSpd` = byte 0x95BC[id] (945C → +0x21; W 28, D 27), paso vel/4 px por `arcTick` (3DF0), pose cada 2 `arcTick` (94CE); resto de la lógica sigue por frame (pendiente). (2) streaming: tiles y celdas BG_B/BG_A de columnas/filas por cola DMA (`acqQ`, `stCol`, `stRow`, presupuesto 40 tiles/frame, `DMA_flushQueue` si se excede), público y cuerdas calculados antes; aparecen en el mismo vblank que en b94. (3) cuerda: 9E78 prueba X±0x10 cada tick con 21E5A/22140 (616+e / 920−e, sin recorte con z≥0xDB) → X=límite∓0x10; 9CD0 siempre sub 2 (fallo `cmpi.b` copiado); contacto en el tick del aterrizaje → 9C94 sin ∓0x20; 9F02 al tick siguiente: cuerda vibra, z≥0xCB, pose 0x16, Vx 0x100 hacia dentro, g 0x10, aterriza con z<0xBB → tumbado. `soilNudge` con `oriVictima` (vface^1) como bit7 de ACA4; llamadas 875/893 revisadas (vface=atacante a la derecha, convención b93).
**Resultado MAME:** carrera W 200,5/D 194,0 px/s NTSC, 199,7–200,1/192,6–193,0 PAL (arcade 201,1/193,9), poses 14,0–14,8/s (arcade 14,36); frames perdidos hacia postes sup izq/sup der/inf izq/inf der 20/14/18/19 → 3/2/1/0 de 580 (máx en 59: 10/6/12/10 → 2/1/1/0), fondo verificado leyendo VRAM: 0 errores; capturas estáticas idénticas a b94. Zafar Xv 760/728/708/693/832 → 642/643/677/677/859 = arcade (b94 675/675/675/675/858). Rebote de carrera, salir del ring, clothesline (víctima igual, atacante 6–8 px más lejos por la carrera por tick) y pin siguen bien.
**Sin verificar:** sub 1 contra cuerda en lanzamientos y derribos por golpes junto a la cuerda vs arcade; PAL en postes; hardware real; sonido 0x29 inexistente en el port.
Evidencia: `05_referencias/capturas/b95/`; datos `02_arcade_decompilado/notas_historicas/b95/shots95/`.
