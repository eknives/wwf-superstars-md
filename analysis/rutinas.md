# Rutinas (R = leída entera; A = firma antigua sin releer)

Cobertura leída entera: 964 rutinas, 100.0% de bytes (bytes por entrada = min(distancia a la siguiente, 0x400)).

Estado: C = confirmado leyendo el código entero; "SC: motivo" = SIN CONFIRMAR; P(A) = anotación antigua por firma, pendiente de releer.

| Dir | Nombre | Estado | Fuente | Función |
|---|---|---|---|---|
| 000E00 | reset_arranque | C | R | Vector de reset: IPL 7, USP=1C3B00, borra 1C180C, IRQ ack (180002/180000) y 1C2B9C; inicializa el vídeo (0x24AE/24C8/24E2/254E/25B8/29DC); baja el IPL; 180008=0; vuelve a inicializar dos veces (con 0x24FC); sonido 0xD (0x2549E), espera 0xFF frames (0x453A); 140200=0 → bucle 0x1010. |
| 000EBA | irq_vblank | C | R | IRQ (vector 30): si 1C180C bit7 y no reentrante (1C0019 bit7): 1C180D++; con 1C0019 bit0 (frame listo): DMA/paletas/sprites (0x259A, 0x269A, 0x29F6, 0x2626E), 1C0019 bit1 y los ticks de frame: 0x20928, 0x55C6, 0x1F5C8, 0x213B4 (cuerdas a vídeo), 0x224E8, 0x2336C, 0x206BE, 0x219AA, 0x1F3CE. Espera a que baje 180009 bit0. ACK 180000. |
| 000F5C | irq_timer | C | R | IRQ (vector 29), no reentrante (1C0019 bit5): 0x4A10 y 0xF92 (temporizador de la demo/atracción). ACK 180002. |
| 000F90 | irq_nula | C | R | rte. |
| 000F92 | tick_atraccion | C | R | Con 1C00E4 bit7: cuenta hasta 0x100 → 1C182A=2, 1C00E6=0x800083FE, sonido 2. Con 1C00E6 bit7: contador 1C00E8 en ciclo de 0x9ECF; en 0x860F y 0x8E7D lanza el sonido 0x22 (0x25E6). |
| 001010 | bucle_juego | C | R | Inicializa variables y el vídeo; sonido 0x22 (1C00E4=0x8000); paleta/escena (0x1F434 modo 3, 0x497C). Sin crédito: sonidos 0xE/0x37. 0x78FA (atracción/créditos). Con partida (1C001A): 0x704E (selección); 1C004B de la tabla 0x139E según los DIP (180002 &3). Entre combates: intro con música de la tabla 0x135C[1C0028], escena 0x1F434 modo 5, 0x1326 (objeto 1C0AB2), 0x43D4. Prepara el combate (tabla 0x1364/0x136E: música, paleta, escena, textos 0x24B38/0x24C5C/0x235CE, 0x1E62, salto a la rutina). Bucle por frame (0x1502): luchadores (tabla 0x1DF0, 8 objetos, 0xEA74 para los ≥4), 0xC6C8 árbitro, 0x212A6 cuerdas, 0x25064, 0x22462, 0xF844, 0x232DE, 0x1676 (música), 0x6BA0, 0x7CAE, 0x17D2, 0x435C, 0x1657E colisiones; marca el frame (1C0019 bit0) y espera la IRQ. Fin de combate (1C0BC2/1C0BDA bits 7/6) → 0x178C. 1C0046 = frames. |
| 001326 | init_obj_ab2 | C | R | Objeto 1C0AB2: activo, pose 0x10, estado 8, pos (0xC6, 0x155, 0xBB). |
| 001676 | musica_combate | C | R | En la partida, o en la demo con 1C0026&0xF=2: música 0x27 (bit7 = sin bucle si 1C0047 bit5=0). Si no: sonidos 0xA7, 0x261BC(0), 0x28. |
| 0017C6 | modo_attract_creditos | C | R | Caso de la tabla 0x17B6: tst 0x1C0016 (créditos) y salta a 0x1DC8 (fin de partida → attract/0x1010). |
| 0017D2 | cargar_graf_luchadores | C | R | Para cada luchador no CPU (+0x2A bit3=0) llama 0x26120 con d0=+0x2B (id), d1=+0x2A bit1, d2=índice. |
| 001810 | gana_equipo_A | C | R | Caso de 0x17B6. d2=1 si en el equipo B el legal (+0x2A bit1) tiene +0x19==1 (o 0x1C1852<0 → d2=0). Si 0x1C0026 bit6 (humano en B) → 0x1A30 (derrota del humano). Si no: 0x1AC8 (secuencia de victoria); si devuelve CC → 0x1DC8. Modo 2 jugadores → 0x1926. Resto: d0 = ids de tabla 0x1C7E de los luchadores ganadores, 0x1C0026 bit7, libera rivales (0x1CFA), avanza combate (0x1D22) y guarda rivales nuevos en 0x1C0085/87; vuelve a 0x113C. |
| 0018D2 | gana_equipo_B | C | R | Simétrica de 0x1810 para el equipo B (bit7 → 0x1A30, ids 0x1C0479/0x1C035F, 0x1C0026 bit6, rivales en 0x1C006F/71). En modo 2 (versus) 0x1926: limpia pantallas, paleta 6 y modo 6 (0x1F434). |
| 0019C6 | empate_o_derrota | C | R | Si el líder del equipo A es CPU → 0x1810; si el de B es CPU → 0x18D2. Si no (ambos humanos): sonidos 0x15 y 0x23, 0x80 frames, 0x651C, borra cajas y fin (0x1DC8). En 0x1A30 (derrota humano): sonidos 0x15/0x23, en el frame 0x3F si d2 texto 0x9B y 0x2660E; luego pantalla de continuar 0x853E: si continúa restaura equipos (0x1EE8/0x1F22) y vuelve a 0x13A2. |
| 001AC8 | secuencia_victoria | C | R | 0x20 frames de combate (0x1C86). Combate 9 (final): sonidos 0x38, 0x09, 0x22; +0x40=0xC en los 4; 0xE8 iteraciones con recarga de energía 0x2060 y barras 0x7CAE; luego paletas 0, sonido 0x12, FINAL 0x2387C, limpieza, 0x245BE y CC (fin de juego). Resto: sonido 0x38 si combate 4, si no 0x39; texto 0x0C; misma recarga; combate 4: paleta 8, sonido 0x0D, escena 0x2347E, 0x100 frames saltables, 0x2387C. Devuelve CS (sigue). |
| 001C86 | frames_combate | C | R | d6+1 frames: 0x221CA, 0x25064, 0x22462, 0x6BA0, 0x435C, copia contador sprites, 0x455C, 0x2516; pide vblank (0x1C0019 bit0) y espera bit1; 0x1676; 0x1C0046++. |
| 001CFA | liberar_rivales | C | R | bclr bit7 de 0x1C00A2[d5&F] y [d6&F] (palabras). |
| 001D22 | avanzar_combate | C | R | 0x1C0029++ saltando 3→4 y 8→9; si llega a 0xA → fin (0x1DA4: limpia, 0x245BE, 0x1DC8). Combates 4 y 9: pareja fija d2=0x706 o 0x607 (rng bit2). Resto: 0x21AE por nivel. 0x1DC8: limpia 0x1C0024/28, sonido 0, a 0x1010 si hay créditos, si no a 0xE60. |
| 001E38 | esperar_saltable | C | R | Espera d1 frames (0x453A); tras los primeros 0x10 permite salir con botones (0x1E90 CS). |
| 001E62 | texto_y_esperar | C | R | Si d3==FFFF solo espera; si no, fundido de paleta 0x24B54 (d3=1, a3=0, d2=1) y espera d1-0x10. (Corregido: 0x24B54 es el fundido de paleta, no texto.) |
| 001E90 | boton_pulsado | C | R | CS si P1 o P2 tienen pulsado bit4 o bit5 (activo bajo). |
| 001EC4 | borrar_caja_fg0 | C | R | Borra 20 filas × 25 longs de fg0 desde 0x80390 (fila 0x80 B). |
| 001EE8 | guardar_equipos | C | R | Guarda +0x2A y +0x3C de los 4 y 0x1C0026 en d0-d7. |
| 001F22 | restaurar_equipos | C | R | Inversa de 0x1EE8. |
| 001F5C | indicador_activar | C | R | 0x1C1A7A[d0*4]: bit7, bit6 si obj+0 bit0, fase 2, duración 0x40. |
| 001F86 | destello_paleta_seleccion | SC: qué elemento de la pantalla usa ese color (¿marco del retrato?); formato xBGR444 asumido | R | Pantalla de selección: 6 indicadores (uno por luchador, activados por 0x1F5C desde 0x7552 al confirmar, 0x40 frames; bit6 según bit0 del cursor, probablemente jugador). Cada 2 frames fase 0..2: NO son sprites ni tiles, escribe un color con 0x2636 en la RAM de paleta 0x140200 (tabla 0x268E[1]) en (paleta,color) de 0x2048: (0,15),(1,15),(2,1),(3,15),(4,15),(5,12). Colores 0x2054: 0x0F66/0x0F0F/0x00F0 (lila-azul, magenta, verde); 0x205A en otro orden. Al acabar, restaura. Render: obj1f86/. |
| 002060 | recarga_energia | C | R | Si 0x1C0BC2≥0 recarga los luchadores A (contadores +0x40); si 0x1C0BDA≥0 los B. 0x1C0BC2/0x1C0BDA son flags de equipo: su origen está pendiente. |
| 0020C2 | recarga_uno | C | R | Si d7≥0: d7-=4; si DSW2 bit7==0, +0x3C += 4; tope 0x30. |
| 0020EC | energia_llena_si_eliminado | C | R | Si 0x1C0BC2<0 pone +0x3C=0x30 en A; si 0x1C0BDA<0 en B. |
| 00211E | sonido_publico_fuera | C | R | Legal A (bit1 de +0x2A, o el compañero) y legal B: si ambos +0x19==1, o alguno ==2 → la primera vez sonido 0x22 + 0x1C183E bit7; repite 0x22 cada 0x50 frames (0x1C1A9D). Si no, limpia 0x1C1A9C. |
| 0021AE | elegir_rivales_nivel | C | R | jmp tabla 0x21C4[0x1C0028&F]. Devuelve d2 = (id1<<8)/id2. |
| 0021EC | rivales_nada | C | R | rts |
| 0021EE | rivales_primeros_libres | C | R | Los 2 primeros de 0x1C00A2 sin bit0 (derrotado); les pone bit1. |
| 002228 | rivales_azar_a | C | R | Dos rng&1: el n-ésimo derrotado y el n-ésimo no derrotado sin bit7. |
| 002284 | rivales_por_seleccion | C | R | Marca bit0 de los que tienen bit15 y usa 0x71E8 (elección como la pantalla de selección) con 0x1C0084/86 salvados. |
| 0022D2 | rivales_azar_uno | C | R | rng&7 (<6, si no 0) y avanza hasta uno no derrotado; d7=6 fijo. |
| 002308 | rivales_primero_y_azar | C | R | d6 = primer libre (bits 0-1 a 0); d7 = rng&7 (<6) sin bit7 y distinto de d6. El final común 0x2352 intercambia d6/d7 con rng&1. |
| 002368 | limitar_6 | C | R | d0=0 si ≥6. |
| 002372 | fundido_paletas | C | R | 16 pasos: en cada vblank (0x180009 bit0) resta 1 a R, G y B de paletas 0x140200/0x140000/0x140100 (64 colores cada una). |
| 002422 | oscurecer_64 | C | R | Resta 1 a cada nibble de color no nulo en 64 entradas. |
| 00246C | enlazar_rivales | C | R | +0x68 de 1C0334 y 1C044E = 1C0100; +0x68 de 1C0100 y 1C021A = 1C0334. |
| 0024AE | borrar_ram | C | R | 0x1C0014–0x1C1AAF. |
| 0024C8 | borrar_bg0 | C | R | 0xC0000–0xC0FFF. |
| 0024E2 | borrar_fg0 | C | R | 0x80000–0x80FFF. |
| 0024FC | borrar_objetos | C | R | 0x1C0100–0x1C1AAF. |
| 002516 | borrar_sprites_sobrantes | C | R | Borra las piezas entre el contador nuevo 0x1C208C y el anterior 0x1C208E. |
| 00254E | borrar_sprites | C | R | Contadores y buffer 0x1C1AB0 (75×10 B) y sprite RAM 0x100000 (0x400 B). |
| 00259A | copiar_sprites | C | R | 75×10 B de 0x1C1AB0 a 0x100000. |
| 0025B8 | flip_pantalla | C | R | DSW1 bit7 (activo bajo) → bit0 de 0x1C2B9C → 0x18000A. |
| 0025E6 | pedir_sonido | C | R | Salvo 2 y 0x22 limpia 0x1C00E6. Envía solo si 0x1C001A≠0 o DSW2 bit2=1 (sonido en demo). 0x34→0x48 si a0+0x19==1. Escribe la palabra en 0x180008 y espera 0x81 vueltas. El Z80 solo ve el byte bajo (latch 0x180009 → NMI → cola 0x8400). Mapa de comandos en sistemas/sonido.md. |
| 002636 | encolar_escritura | C | R | Entrada 0x1C18BC: tabla, fila, col, valor. Dir = 0x268E[tabla] + fila*0x20 + col*2 (la tabla de bases está en 0x268E). Cola 0x1C18C4 (máx 0x20). |
| 00269A | aplicar_cola | C | R | Escribe las palabras encoladas y vacía la cola. |
| 0026BC | delta_objetos | C | R | a0=*(0x1C004E), a1=*(0x1C0052): /dy/→0x1C0052, /dx/→0x1C0050, signos en 0x1C004E bits 1/0. |
| 00270C | angulo_objetos | C | R | Ángulo aproximado (atan por cociente×0x40 / suma, tabla de octante 0x2782) de a0 a a1 → byte 0x1C004E. |
| 002786 | fuera_de_pantalla | C | R | CS si x ∉ (camx−0x30, camx+0x130) o y+z ∉ (camy−0x40, camy+0x150). |
| 0027D2 | trayectoria | C | R | Velocidades +0x24/+0x26/+0x28 y gravedad +0x22 de la tabla 0x2814[d0]; modo 2 (cartesiano); vx negada si mira a la izquierda (salvo d0=0x11). |
| 0029DC | forzar_paletas | C | R | 0x1C003E=0, 0x1C0042=FFFFFFFF, carga. |
| 0029F6 | cargar_paletas | C | R | Espera vblank; para 3 bancos, si 0x1C003E[i]≠0x1C0042[i] copia 8 paletas×15 colores de la tabla 0x2A60[i][id] a 0x2A6C[i] (color 0 a 0). |
| 003B42 | paletas_luchadores | C | R | Paleta de 15 colores de la tabla 0x3BC8[+0x2A&FF] (alternativa 0x3BEE si el id está en la lista 0x3BE8 y +0x32 bit7: colores del mismo luchador repetido) → 0x140100+0x20*i; +0x1A=0x8000+0x10*i. |
| 003BFE | decorado_por_nivel | C | R | Nivel 0x1C0028 (1..; 0 y 5 nada): bloques de tiles de la tabla 0x3C5A encolados y aplicados. |
| 003DCE | mover | C | R | jsr tabla 0x3DEA[+1]. |
| 003DF0 | mover_polar | C | R | d0=+0x1E (velocidad.l: alto=dirección, bajo=módulo; ×2 en la palabra baja), 0x3E8E → dx,dy (8.8) sumados a x/y. |
| 003E20 | mover_cartesiano | C | R | x+=vx*2, y+=vy*2, z+=vz*2 (8.8); vz−=g*2 (+0x22); vz mínima 0xF800. |
| 003E8E | polar_a_xy | C | R | Octante = dirección>>5 (8 de 32 pasos). Casos 0x3EC4–0x3F6E: un eje = 32·v y el otro = f·v (f = 0..31 o 32−f), con los signos de cada octante. Es una aproximación lineal (rombo/cuadrado): no usa seno ni coseno. |
| 003EC4 | oct0 | C | R | (+32v, +fv) |
| 003ED8 | oct1 | C | R | (+(32-f)v, +32v) |
| 003EF2 | oct2 | C | R | (−fv, +32v) |
| 003F06 | oct3 | C | R | (−32v, +(32−f)v) |
| 003F24 | oct4 | C | R | (−32v, −fv) |
| 003F3C | oct5 | C | R | (−(32−f)v, −32v) |
| 003F5A | oct6 | C | R | (+fv, −32v) |
| 003F6E | oct7 | C | R | (+32v, −(32−f)v) |
| 003F8C | leer_mandos | C | R | d0 = ~(P2<<8 / P1) & 0x3F3F (bits 0-3 dirección, 4-5 botones). El tst 0x1C001A + nop es un resto parcheado. |
| 003FAE | repartir_mandos | C | R | Lee los mandos y salta por la tabla 0x3FC6[0x1C0026&3]. |
| 003FCC | mandos_tag | C | R | Modo tag: P1 → pareja A (1C0100, que copia a 1C021A) si 0x1C0027 bit0; P2 → pareja B (1C0334→1C044E) si bit1. |
| 004000 | mandos_individual | C | R | Si 1C0027 bit0: 0x40C0 para 1C0100 y 1C021A; si 1C0027 bit1: 0x40C0 para 1C0334 y 1C044E. 0x40C0 lee P1, o P2 si +0x2A bit5. |
| 00403E | mando_compartido | C | R | 0x4066 en a1 y copia +0x10D, +0x110, +0x114 y +0x116 a a2. |
| 004066 | procesar_mando | C | R | +0x10E=+0x10C anterior; +0x10D = dirección traducida por la tabla 0x40DA; +0x110 = botones (bits 4-6); +0x114 = recién pulsados ((ant^act)&act); +0x112 = actual; +0x116 = OR de pulsaciones, se borra cada 4 frames (0x1C0046&3). |
| 0040C0 | mando_por_bit5 | C | R | Usa el byte de P2 si +0x2A bit5. |
| 0040EA | relaciones_4 | C | R | 0x4100 para los 4 luchadores. |
| 004100 | relaciones_luchador | C | R | Si a0 es uno de los 4, copia de la tabla 0x42C2 los 3 "otros" a 1C1814 y llama 0x4166 para cada uno. |
| 004166 | relacion_con_otro | C | R | Con el otro objeto a1 calcula en a0, en los desplazamientos de las tablas 0x42F2–0x4316: /dx/ (±0x20 si la acción es 0xB, según orientación), /dy/ y /dz/, y una palabra de flags (lado izq/der, delante/detrás, posición respecto a las constantes 0x4332/0x4334−0xBB, bits de +0x18 y +0x2A). Copia también +0x2C, +0x3C (energía) y +0x2A&FF del otro. Es la "tabla de percepción" que usan la IA y las colisiones. |
| 00435C | encolar_todos | C | R | Encola si son visibles: los 4 luchadores (0xEA4C), 4 objetos de 0xBCB8, 10 de 0x7E22, 1C0568 y 23 objetos desde 1C155A (paso 0x1E). Los objetos 1C0682/78E/89A no se dibujan con la acción 1. |
| 00439A | encolar_lista | C | R | Para d0+1 punteros de a1: si son visibles (0x2786 CC) y no son la excepción anterior → 0x43D4. |
| 0043CA | encolar_si_visible | C | R | 0x2786 y 0x43D4. |
| 0043D4 | encolar_dibujo | C | R | Si está activo, la acción ≠0x10, +0x2C bit6=0 y la pose ≠FFFF: entrada de 16 B en 1C2094 (máx 0x40). Capa = +0x18&3; la capa 1 se refina: bit4→4; bit7 y z≥0xBB→3; z≥0xD3→0. Hay 5 cubos (tabla 0x449A, máx 0x30) y el tipo de entrada va por +0x1C&7 (0x44AE). |
| 0044BE | entrada_propia | C | R | banco(+2), pose(+4), anim(+6), x, y, z, attr(+0x1A). |
| 0044C6 | entrada_banco_rival | C | R | Banco del rival (+0x68)+2, resto propio. |
| 0044DA | entrada_banco_rival_anim_rival | C | R | Banco +2 del rival y anim +6 del rival. |
| 0044E6 | entrada_anim_rival | C | R | Banco propio y anim +6 del rival (llaves compartidas). |
| 00450A | rng | C | R | semilla(1C003A) = d0+semilla+a1+a2+a4+a5+a6+d2..d7 (d1 y a3 no se suman); devuelve (semilla+1)>>8. |
| 00453A | esperar_vblanks | C | R | Espera d0+1 flancos de vblank (0x180009 bit0). |
| 00455C | dibujar_cubos | C | R | Si hay entradas: 4 cubos (tabla 0x457E) → 0x458E; contador a 0. |
| 00458E | dibujar_cubo | C | R | Ordena (0x45AE) y convierte cada entrada (0x45FC). |
| 0045AE | ordenar_y | C | R | Burbuja por la palabra +8 (y) de la entrada, de mayor a menor. |
| 0045FC | entrada_a_sprites | C | R | sx = x−camx, sy = y+z−camy. Pose de la tabla 0x6CD8[banco][pose]; desplazamientos en 1C0000/2. Para los bancos ≤7 de varias piezas asigna paleta (0x46A0). Piezas con 0x46F4 (máx 0x4B). |
| 0046A0 | paleta_por_banco | C | R | Busca el banco del gráfico en 0x6CD8 y el luchador que lo usa → paleta 0..3 (4 si no hay; 7 si el gráfico < *(0x3B87E)) en +0xC. |
| 0046F4 | emitir_pieza | C | R | Pieza en 1C1AB0 + n*10; tipo por bit0 del primer byte (0x4724: 0x472C o 0x47D2). |
| 00472C | piezas_lista | C | R | Bloque con códigos de tile explícitos. |
| 0047D2 | piezas_consecutivas | C | R | Bloque de tiles consecutivos (+1, o +2 si es de doble alto). |
| 004878 | pieza_x | C | R | x con flip (+2 bit7 niega el desplazamiento), +9, 9 bits; recorta fuera de 0x108–0x1F8 (CS). |
| 0048D4 | pieza_y | C | R | y −8 (−16 si es doble alto); recorta a 0x110 (0xD8 en demo con 1C182C=0). |
| 004934 | pieza_cerrar | C | R | Marca la pieza como visible; contador++; Z si ≥0x4B. |
| 004952 | pieza_color | C | R | d3 = paleta (+0xC, o +0xD si bit7); d4 = flips (bits del gráfico XOR +2 bits 6-7). |
| 00497C | texto_0x20 | C | R | Texto 0x23A28 (d1=0x20) y una palabra fija en fg0 0x806DC. |
| 004A10 | monedas | C | R | En el IRQ: monedas en SYSTEM bits 1-3 (activo bajo) con antirrebote de 0x23 frames y 4 lecturas; sonido 0x2F; tarifa según DSW1 bits 0-2/3-5 (tablas 0x4B6A monedas, 0x4B7A créditos); créditos BCD en 1C0016 (máx 99). Si no estaba en juego (1C001A bit7=0) reinicia pila y salta a 0x1010. |
| 004B4E | moneda_repetir | C | R | Espera y relee las monedas (AND con la primera lectura). |
| 004C2E | escena_attract | C | R | Escena de guion con 1C182C=5: inicializa (0x4D4C) y repite el paso de 1C09D2 (tabla 0x4D24) hasta el paso 4 (o 9 si 1C180C bit1), con la animación del objeto 1C0AB2 (0x4E8E) y la música 0x25408 la primera vez. |
| 004D4C | escena_init | C | R | 1C0100 en (0x98, 0x154, 0xBB) y 1C0AB2 en (0xC6, 0x155, 0xBB), ambos banco 0x10. |
| 004DCE | escena_paso0 | C | R | Anima 1C0100 (tablas 0x4E76/0x4E82), sonido 0x35 en el paso 3; tras 9 vueltas pasa al paso 1. |
| 004E8E | escena_obj_ab2 | C | R | Guion de 1C0AB2 por +0x2C (tabla 0x4EC6) y lo dibuja. Que en el combate sea el árbitro está SIN CONFIRMAR: esta escena no lo demuestra. |
| 004ECE | escena_ab2_quieto | C | R | anim 8 |
| 004ED6 | escena_ab2_anim | C | R | anim 9..11 cada 8 frames |
| 004F08 | escena_paso1 | C | R | 1C021A: bloque de tiles 0 (0x5578) y 0x20 frames → paso 2. |
| 004F48 | escena_paso2 | C | R | 1C0334: bloque 1 y 0x20 frames → paso 3. |
| 004F88 | escena_paso3 | C | R | 1C0334: sonido 0x46 y 2 bloques por fase (tabla 0x5086); al acabar, paso 4. |
| 0050B6 | escena_sub_021a | C | R | Bloques 0xA/0xB alternos de 1C021A. |
| 00512C | escena_paso4 | C | R | 0x10 frames → paso 5. |
| 00516C | escena_paso5 | C | R | 3 bloques por fase (0x5246) → paso 6. |
| 00526A | escena_paso6 | C | R | 4 bloques (0x52EE/0x52FE) → paso 7. |
| 00530E | escena_paso7 | C | R | Sonido 0x36, bloques 0x20+n y luego la secuencia 0x545E/0x5436 → paso 8. |
| 00546E | escena_paso8 | C | R | 3 bloques por fase (0x551E) y escritura en bg0 0xC0358 → paso 9. |
| 00554E | escena_paso9 | C | R | 0x20 frames → paso 0xA. |
| 005578 | encolar_bloque | C | R | Mete (d0, +0x30, +0x5C) en el primer hueco libre (FFFF) de 1C186E/78/82 (5 huecos); los dibuja 0x55C6 en el IRQ. |
| 0055C6 | dibujar_bloques_escena | C | R | IRQ: si 1C182C==5 dibuja los 5 bloques encolados por 0x5578. |
| 005D80 | presentacion_combate | C | R | Música: en los combates 4/9, 0xB si el rival es 7, si no 0x10; en el resto 3 (no la repite si ya suena). Paleta 7. Combate 0 (o 4/9 con 1C0026 bit6/bit7): modos 7/8 (0x1F434), nombres 0x62B0, colocación 0x5F54/0x5FDE y 0x50 frames 0x5EC4. |
| 005EC4 | presentacion_bucle | C | R | 0x51 frames: sonido 0x22 (público), anima a los 4 (0x6192), 0x20824, nombres 0x6256 y dibujo. |
| 005F54 | colocar_humano_A | C | R | Ids de la tabla 0x7FE2[1C0070/1C006E] → +0x2B de 1C0100/1C021A; B = id 6; posiciones de 0x60EE; banco 0x10; +0x1A = paleta id&7; los ids 0, 1 y 7 se voltean; paletas 3; 0x611E. |
| 005FDE | colocar_humano_B | C | R | Igual con 1C0086/84 y posiciones 0x6106 (lado contrario). |
| 00611E | paleta_libre_cpu | C | R | Busca el primer id 0..7 no usado por A y le da a B su paleta (tabla 0x6172) en 0x140100+id*0x20. |
| 006192 | anim_presentacion | C | R | Para d0≥2: animación cíclica de la tabla 0x61F6[+0x2A&7]; luego +4=+0xA, mover (0x3DCE) y dibujar. |
| 006256 | nombres_actualizar | C | R | En los modos 7/8 redibuja el nombre si cambió 1C1833/1C1835. |
| 0062B0 | dibujar_nombre | C | R | 3 filas de 31 tiles de la tabla 0x62EE (id*0x5D + lado*0x117) en fg0. |
| 00651C | escena_fin_partida | C | R | Tras perder o empatar: limpia y carga paletas 6/4, coloca 6 objetos (0x65EC), 0x6796, modo 6, música 0x13, 0x101 frames animando (0x680A) y texto 0x84B8. |
| 0065EC | fin_partida_colocar | C | R | En los combates 4/9 con rival 7 intercambia +0x2A/+0x2B de B; 1C0122 bit7 = modo 2 y bit6 = combate 4/9 (sonido 0x37; si no, 0x3C); desactiva el equipo que corresponda; 6 objetos de la tabla 0x6766. |
| 006796 | paleta_libre_extra | C | R | Como 0x611E para los objetos 1C0568/1C0682. |
| 00680A | obj_fin_partida | C | R | Guion por +0x2C&7 (tabla 0x6834). |
| 006848 | fin_p0 | C | R | Paso 0 del guion de fin de partida. |
| 0068FE | fin_p1 | C | R | Paso 1 del guion de fin de partida. |
| 0069A4 | fin_p2 | C | R | Paso 2 del guion de fin de partida. |
| 006AA6 | fin_p3 | C | R | Paso 3 del guion de fin de partida. |
| 006B98 | fin_p4 | C | R | Oculta (+0x2C bit6). |
| 006BA0 | efecto_publico_azar | C | R | Objeto 1C09A6: si está libre, cada 8 frames con rng&7 contra la máscara 0x6C76 aparece en una posición de la tabla 0x6C78 (según la cámara y rng&0x38), con la variante 0x3A o 0x40 elegida por rng frente a 0x6C77, y dura 6 pasos de animación. Son los flashes de cámara del público (confirmado visualmente por Emilio en el arcade, 31-10-2026). |
| 006D2C | musica_combate | C | R | En juego: si algún humano tiene índice de energía 0 (0x1CE9C) → música 8; si no, la de la tabla 0x6DC0[nivel] (salvo 1C1850 bit1). Solo cambia si es distinta de 1C182A. |
| 006DD4 | musica_nivel | C | R | d0 = 0x6DC0[nivel]. |
| 006DEE | unirse_partida | C | R | En juego con créditos y 1C0026&0x300=0: tabla 0x6E2E[1C0027&3]. |
| 006E3E | unirse_nada | C | R | rts |
| 006E40 | unirse_P1 | C | R | Si se pulsa start (1C1A95 bit2), el compañero libre del equipo A pasa a humano (/0x21) y el modo a 0x103; gasta un crédito. |
| 006EC6 | unirse_P2 | C | R | Igual para el equipo B. |
| 006F4C | gastar_credito | C | R | 1C0016 −= 1 (BCD). |
| 006F64 | comprar_energia | C | R | En juego con créditos y sin modo 2: start (0x7B1E) rellena la energía del equipo humano (tabla 0x7FEC[+0x2A&7]), 1C1850=0x80, 0x7CA6 y gasta un crédito. |
| 006FEE | energia_A | C | R | +0x3C de A = 0x7FEC[+0x2A&7]. |
| 00701E | energia_B | C | R | +0x3C de B = 0x7FEC[+0x2A&7]. |
| 00704E | pantalla_seleccion | C | R | Limpia 1C00A2, música 0xA, paleta 4, modo 4; tiempo 0x180; cursores. Bucle: leer (0x7240), tick o confirmación, retratos y 1F86. Al terminar espera 0x40/0x70 frames, marca los elegidos (0x71B4) y elige rivales CPU (0x71E8), o los de P2 en modo 2. |
| 0071B4 | marcar_elegidos | C | R | En 1C00A2[d0], [d1]: bit7 = en combate y bit0 = ya usado. |
| 0071E8 | cpu_elige_pareja | C | R | 2 veces: rng&7 (<6), el siguiente sin bit7 ni bit0 → bit0 y se guarda en el puntero de la tabla 0x7FD4. |
| 007240 | seleccion_leer | C | R | P1 (0x180004) y P2 (0x180006) → 0x727E; resultados en 1C0072.. y 1C0088.. (6 palabras). |
| 00727E | flancos_mando | C | R | d1 = dirección (bits 0-3, activa alta), d3 = recién pulsadas; d4 = botones (bits 4-5), d6 = recién pulsados. |
| 00729C | seleccion_tick | C | R | Mientras quede tiempo (1C006A) mueve los cursores (0x749E); si se acaba, 0x7328 (eligió la CPU). Cuando todos confirman, el tiempo pasa a 1. |
| 007328 | seleccion_tiempo_fuera | C | R | Tabla 0x7340[modo&3]. |
| 007350 | tfuera_m0 | C | R | Modo 0: si no está confirmado, elección al azar (0x73E8); si lo está, fin. |
| 00736E | tfuera_m1 | C | R | Modo 1: elección de cada mando y paso a la pareja. |
| 0073B0 | tfuera_m2 | C | R | Modo 2: igual que el modo 0 con dos jugadores. |
| 0073DE | seleccion_fin | C | R | 1C0067 bit0 = fin. |
| 0073E8 | tfuera_azar | C | R | Elección al azar del luchador (modos 0 y 2). Sin confirmar (1C0066 bit7=0): cada 16 frames (1C0046&0xF==0) elige; si no, salta a mostrar. Con 1C0066 bit7 elige solo si 1C0047 bit0=0. Elección: d0=(RNG 0x450A + 1C0046) mod 6, repite mientras el bit d0 de 1C0069 esté puesto (ocupado); guarda d0 en +0x14 con bit15 de 'elegido'. Mostrar: si +0x14 tiene bit15 y su byte bajo difiere de +1, pone +0xB=tabla 0x747A[(+0 & 7)*6 + d0] y llama 0x74C4; cada 64 frames (1C0046&0x3F==0x3F) llama 0x7552. Si los 6 bits de 1C0069 están puestos el bucle no termina: si eso puede ocurrir, SIN CONFIRMAR. Qué hacen 0x74C4/0x7552 (refresco de retrato/sonido): SIN CONFIRMAR. |
| 00749E | cursor_estado | C | R | Tabla 0x74B4[+0x10&3]; sus estados 0x75B2/0x75B4 son rts. |
| 0074C4 | cursor_mover | C | R | Si hay dirección: nuevo índice de la tabla 0x74F2[pos*16+dir] (FF = no se mueve); retratos 0x762A. |
| 007552 | cursor_confirmar | C | R | Si el luchador no está tomado (bit en 1C0069): lo marca, guarda el historial y sube +0x12; en modo de 2 jugadores lo anuncia (0x1F5C). |
| 0075B2 | rts_75b2 | C | R | rts. |
| 0075B4 | rts_75b4 | C | R | rts. |
| 0075B6 | retrato_dibujar | C | R | Marco y nombre del luchador bajo el cursor, con parpadeo cada 16 frames si está repetido. |
| 00762A | retrato_borrar | C | R | Borra los dos bloques (tabla 0x78CA). |
| 007658 | cola_7658 | C | R | Continuación: d2=0x11 (sigue en la rutina siguiente). |
| 00765C | bloque_fg0 | C | R | Escribe una lista (desplazamiento, tile) en fg0 con el color d2 (0x7658 usa d2=0x11). |
| 0078FA | attract_espera | C | R | Bucle de título/créditos (0x2FF frames si no hay créditos): 0x879A lee los start. bit1 y 1 crédito → modo 0x8001 (1 jugador); bit0 y ≥2 créditos → 0x8101; bit2 y ≥2 → 0x203 (2 jugadores); se gastan 1 o 2 créditos. Textos parpadeantes con 0x2549E (INSERT COIN / PRESS START según los créditos, con un ciclo de 3) y 2 objetos animados (0x7B6C). |
| 007B1E | start_pulsado | C | R | Z = !(1C1A95 bit1). |
| 007B32 | attract_init_objs | C | R | Borra 1C0100 y 1C021A. |
| 007B6C | attract_obj | C | R | Con rng (máscara 0x7C34) aparece en la posición de la tabla 0x7C66/0x7C86 y hace 6 pasos de animación (0x7C36/0x7C4E). |
| 007CA6 | musica_forzar | C | R | Entra en 0x6D2C sin la comprobación de daño. |
| 007CAE | barras_energia | C | R | Para cada luchador sin +0x2A bit3: borra (0x7CD2) y dibuja (0x7CF2) su barra. |
| 007CD2 | barra_borrar | C | R | 6 entradas (0x1F, 0) en el búfer de la tabla 0x7D6A[i]. |
| 007CF2 | barra_dibujar | C | R | segmentos = ceil(energía/4), máximo 12, en medios tiles; los enteros salen de 0x7D92 y el medio de la tabla 0x7D7A/82/8A según el modo y +0x2A bit5. La barra muestra energía/4, es decir 48 puntos = barra llena. |
| 007D92 | barra_enteros | C | R | d2 tiles de la tabla 0x7DD8/0x7DE0/0x7DF0. |
| 007E00 | borrar_objs_extra | C | R | Borra los 10 objetos de 0x7E22 (0x10C B) y 1C1822. |
| 007E4A | crear_obj_78e | C | R | Crea la MESA plegable que se parte en dos (objeto 1C078E, id 1, fuera del ring en 0x300,0xC8, paleta 7; gráficos banco 8, poses 0x3B402). No se crea en los combates 4/9 (los de André), que además desactivan la lógica de objetos. Identidad CONFIRMADA por Emilio (vista en el arcade) y por el render del sprite (obj78e/). |
| 007EB6 | preparar_combate | C | R | 0x7EE6 y luego 0x7FFC con 1 (modo 2), 0 (combate 0 o equipo B humano) o 2. |
| 007EE6 | init_luchadores | C | R | 5 objetos (tabla 0x7F9A): los borra conservando +0x3C y +0x2A bit13; id = 0x7FE2[selección]; +0x2A de la tabla 0x7FAE; +0xDA=3; en el combate 0, energía = 0x7FEC[+0x2A&7]. |
| 007FFC | colocar_combate | C | R | Asigna control según el modo (tabla 0x805A) y la energía de la CPU de la tabla 0x8190[nivel*16 + id*2] + (1C004A&3)*8; posiciones iniciales (x, y, z, +0x18, anim) de la tabla 0x8230. |
| 008066 | ctrl_modo0 | C | R | A humano (+0x20 compañero en el combate 0 con modo bit0); a la CPU de B se le da energía por nivel y +0x2A bit3. |
| 0080F6 | ctrl_modo1 | C | R | A1 humano; B1 /0x21 y B2 /0x20 (humano P2). |
| 008110 | ctrl_modo2 | C | R | Energía por nivel para el equipo A de la CPU; B humano. |
| 008276 | elegir_legales | C | R | Tabla 0x828E[modo]: el luchador "legal" de cada equipo (el de +0x2A bit0, o el otro) → 1C18AC/1C18B0; +0x2A en 1C18AA. |
| 00829E | rts_829e | C | R | rts. |
| 0082A0 | asignar_controlados_a | C | R | Tabla 0x7F9A: 1C18AC = el luchador con control (+0x2A bit0) del par 0/1 (1C18AA = su +0x2A); 1C18B0 = el del bando (bit1) del par 2/3. |
| 0082DA | asignar_controlados_b | C | R | Ídem con los pares cambiados. |
| 008314 | asignar_controlados_c | C | R | Ídem: los dos con +0x2A bit0. |
| 00834E | nada | C | R | rts |
| 008350 | inicio_combate | C | R | Tiempo 1C002E=0x180; 2 frames de dibujo; según la tabla 0x84AE[combate] y el modo tag, decide qué compañero empieza fuera (+0x5C=7, +0x33 bit7). Luego barras, marcador, música 1, sonido 0x3B, espera 0xC0, sonido 0x20 y espera 8. La campana de inicio es el 0x20 (muestra OKI 1: pico espectral 2.360 Hz, decaimiento exponencial de 1,5 s), no el 0x3B (muestra 0x1C). El 0x21 (muestra 2, misma frecuencia, sostenida) es la campana repetida de musica_combate y del fin de tiempo. Se ha deducido del espectro y del contexto de llamada, sin oírlo. |
| 0084B8 | texto_fin_partida | C | R | Textos 0xF, 0x10 y 0x11 de 0x23A28, cada uno con 4×(1 frame + 0x206BE). |
| 00850A | fg0_rellenar_area | C | R | 14×16 celdas de fg0 desde 0x80120 = 0x1100F3. |
| 00852A | espera_fundido | C | R | 4×(1 frame + 0x206BE). |
| 00853E | continuar | C | R | Cuenta atrás de CONTINUE: 1C001C=0x10 (BCD), cada 0x30 frames baja 1 (0x870C); un parpadeo (0x85D0) anima bg0. Si pulsa start con créditos suficientes (0x8758) → CS (continúa); si llega a 0 → 0x886E y CC. |
| 0085D0 | continuar_anim | C | R | Alterna los gráficos 0x2123E/0x21272 cada 8 frames y anima tiles en bg0 0xC00C0 con la tabla 0x207F6/0x20800. |
| 0086A2 | continuar_textos | C | R | Textos de precio/número (0x2549E con la tabla 0x89A4) y 0x34. |
| 00870C | continuar_tick | C | R | Descuenta el número 1C001C cada 0x30 frames; CC al llegar a 0. |
| 008758 | continuar_start | C | R | Lee los start (0x879A); según el modo (tabla 0x878E) exige el botón correspondiente y cobra 0x88E6 créditos. |
| 00879A | leer_starts | C | R | d0 = bit1 P1 start (0x180004 bit7), bit0/bit2 de P2 (0x180006 bits 6/7); flanco en 1C1A94; 1C1A96 = estado. |
| 0087FC | cont_m0 | C | R | Start bit1 y créditos suficientes. |
| 008820 | cont_m1 | C | R | Start bit2 y créditos suficientes. |
| 008842 | cont_m2 | C | R | Start bit0 y créditos suficientes. |
| 00886E | game_over | C | R | En los modos 0/1: texto 0xB y 0x100 frames de animación. En el modo 2 (versus) no hay fin: el modo pasa a 1 jugador (0x4000 o 0x8000 según 1C0BC2 bit7, es decir, quién ganó) y 1C001F bit4. |
| 0088E6 | precio_continuar | C | R | d1 = créditos por partida (tabla 0x4B7A según DSW1 y 1C0015), el doble en el modo 1; compara con 1C0016 (CS si no llega). |
| 00895C | bg0_limpiar_zona | C | R | 7×8 longs de 0xC0050 a 0. |
| 008980 | fg0_limpiar_zona | C | R | 14×16 longs de 0x80120 a 0. |
| 0089A8 | demo_preparar | C | R | Demo: ids de la tabla 0x8AB0[nivel] (4 columnas de 10), modo 0, 0x7EB6; controles CPU (+0x2A: 0xA/0x1A/8/0x18), energías 0xFFF/0xF00/0/0, rivales fijos, compañeros fuera (pos 0x260/0x3B0) y duración 1C1984=0x400. |
| 008AD8 | intro_escena | C | R | Cortinilla 0x25408 (d0=1) y 0x25474, borra bg0 y sprites, modo 1C0040=5 (0x29F6), espera 8, escena 0x1F434 con d0=5, 1C180C bit1 = NOT(1C0025 bit1), escena 0x4C2E, limpia 1C180C; si 1C0025 < 4: otra cortinilla, espera 8 y borra bg0/sprites. (Corregido: 0x25408 es la cortinilla, no la música 1.) |
| 008C82 | luchador_update | C(A) | A | Actualización por frame de un luchador: flags CPU/humano (+0x2A bits0/1/3), 0x162A0, y despacho de la acción +0x2D por la tabla 0x8CE2 (33 acciones). |
| 008D66 | acc0_cpu_comun | C | R | Acción 0 (de pie) en la rama CPU/compañero: si +0xF2 bit6, +0x5C=0; inicializa 0x911E; tabla 0x8D8A por +0x18&3 (plano: ring, fuera, poste…). |
| 008D9A | acc0_plano0 | C | R | Si +0x5C&7≠7: orientar (0x919C), zona (0x9202), pose quieta (0x92BE), 0x21E5A y 0x8E7A; si es 7, 0x8DC0. |
| 008DC0 | acc0_espera_tag | C | R | +0x5C=7: orienta por zona (0x91DC/0x9202) y llama 0x19E3A. |
| 008DD8 | acc0_plano1 | C | R | jmp 0x1A532 |
| 008DDE | acc0_plano_b | C | R | Si +0x5E bit6 → acción 0x1C; si no, 0x1A830. |
| 008DFE | acc0_plano3 | C | R | Subtabla 0x8E1E[+0x5D&7] → 0x1B54A/0x1B656/0x1BBB4/0x21ED0/0x1BCB6/0x1BD5C. |
| 008E2E | apron_cpu_0 | C | R | Zona 3 / +0x5D: 0x1B54A (pasear por el delantal). |
| 008E40 | apron_cpu_1 | C | R | 0x1B656 (seguir al rival por el delantal). |
| 008E52 | apron_cpu_2 | C | R | 0x1BBB4 (bajar del delantal). |
| 008E5A | apron_cpu_3 | C | R | 0x919C, 0x9202, 0x92BE, 0x21ED0. |
| 008E6E | apron_cpu_4 | C | R | 0x1BCB6. |
| 008E74 | apron_cpu_5 | C | R | 0x1BD5C. |
| 008E7A | tag_contador | C | R | = 0x8E7E |
| 008E7E | tag_espera | C | R | Salvo si el rival legal está en acción 0xB (modo tag) o el luchador es +0x2A bit1: en modo tag +0x10A++ y al llegar a 0x60 (sin tag, inmediato) +0x5C=7 y se pone a 0. +0x5C=7 → tabla CPU 0x1B40C[7] = 0x19E3A: ir a su esquina y subir al delantal (salir por relevo). |
| 008EC8 | acc_correr_cpu | C | R | Borra +0xA8 bit7 y sigue en 0x8ECE. |
| 008ECE | correr_cuerpo | C | R | Init (0x945C), animación (0x94CE); si +0xF2 bit7, 0x9598; mover (0x953C). |
| 008EEA | pasos_liberar | C | R | Si 1C1828 == id, 1C1828=FF (deja libre el sonido de pasos). |
| 008F08 | acc0_humano | C | R | Acción 0 del humano: CPU (+0x2A bit3) o +0xF2 bit7 → 0x18E70 (IA/automático); +0x2A bit0=0 → 0x8D66; +0x33 bit4 limpia bits 2-3; tabla 0x8F58 por plano. |
| 008F68 | acc0_h_ring | C | R | Subtabla 0x8F7E[+0x5C&7]. |
| 008F9E | acc0_h_andar | C | R | Andar con el mando: dirección → velocidad (0x919C, 0x924A anim, 0x9310 velocidad, 0x3DCE) o quieto (0x92BE); 0x21E5A (límites); subir al poste (0x9738); botones 0xF78E → 0xCD2C / 0xC706 (golpes con d3=0). Si algún rival está en acción 0x17 no corre el contador de tag. |
| 009014 | acc0_h_fuera | C | R | Subtabla 0x902A[+0x5C&7]. |
| 00904A | acc0_h_fuera_andar | C | R | Igual que andar, pero con los límites de fuera del ring (0x21ED0), 0xD2D6 y botones 0xC706 (d3=1). |
| 009094 | acc0_h_apron | C | R | Solo en modo tag (si no, acción 7): andar con 0x220C4 y 0x1B942; 0x90DE. |
| 0090DE | tag_relevo_fin | C | R | Si el rival legal y su compañero están en el plano 1: borra +0x2A bit0 (deja de ser legal), acción 0 y +0x5C=2. |
| 00911E | acc_init_de_pie | C | R | Primera vez (+0x2C bit7): borra contadores (+0x36, +0xA8, +0xBE, +0x104, +0x102, +0x9E, +0x1C, +0xC8), anim 1, zona y pose quieta. |
| 009184 | anim_reset | C | R | Borra +0x36 y +8, marca init, borra +0xA8 y +0xBE. |
| 00919C | orientar_y_dir | C | R | +0xA = signo(x_rival − x) (mira al rival +0x68). Con dirección (+0x10C): ángulo de la tabla 0x9334 → +0x1F, CC; sin dirección: velocidad 0, CS. |
| 0091DC | orientar_zona | C | R | +0xA = bit15 de la entrada +0x6E[+0x6C*16]; CS si es negativa. |
| 009202 | zona_flags | C | R | +0x18 bit6 ← bit14 de la entrada de zona; si es 0 y el plano coincide y entrada+4 < 8 → bit6=1. |
| 00924A | anim_andar | C | R | Ciclo de 4 frames de la tabla 0x93AE (+8 si +0x18 bit6, +0x10+n*0x10 si lleva a alguien, +0x5E bit6). |
| 0092BE | pose_quieto | C | R | Pose de la tabla 0x9308 según lleve a alguien (+0x5E) y +0x18 bit6. |
| 009310 | velocidad_andar | C | R | +0x20 = tabla 0x933E[id][dirección] (cada luchador tiene la suya). |
| 0093EE | acc_correr | C | R | CPU → 0x1BE30. No legal → 0x8EC8. Init, y si no hay automático 0xCC26 (golpe corriendo, CC → sigue); animación, movimiento; si la dirección es la opuesta (tabla 0x9600 frente a +0x1F) → acción 0x14 (frenar). |
| 00945C | correr_init | C | R | Solo la primera vez (+0x2C bit7): limpia +0x22/24/26/36/104/A8, +8=1, +1=1, +0x18 bit7=0; velocidad 0x95BC[id] → byte +0x21; ángulo +0x1E = 0x40 o 0xC0 según la orientación +0xA bit7 (corregido: antes decía 0/0x80); si 1C1828 == 0xFF, 1C1828 = id (+0x2B). |
| 0094CE | correr_anim | C | R | Animación de la tabla 0x95C4[id]; sonido 0x24 (pasos) en los frames 0 y 3 solo para el luchador de 1C1828. |
| 00953C | correr_mover | C | R | Mueve. Fuera del ring: si choca (+0x9E&3) → acción 8 sub 7. En el ring: si toca la cuerda del lado hacia el que corre → +0xA8++ y +0x2C=2 (rebote). |
| 009598 | correr_auto | C | R | 0x1B120 (control automático); si acaba, acción 0x14 y CC. |
| 00960A | acc_rebote_cuerdas | C | R | Gira (+0xA ^ 0x80), anim 0x10, velocidad 9 que baja 1 por frame; 0x9700 marca la cuerda tocada en 1C1898 (plano bit0) o 1C189A. A los 2 pasos sigue según +0xA8 (tabla 0x96A4). |
| 0096AA | rebote_seguir | C | R | Acción 1 (correr), o 0x15 si +0xA8 bit7, con la velocidad de correr. |
| 0096F0 | rebote_parar | C | R | Acción 0, +0x5C=0, libera los pasos. |
| 0096FE | nada | C | R | rts |
| 009700 | marcar_cuerda | C | R | 1C1898/1C189A bit15 y nibble = d0. |
| 009738 | subir_poste_chk | C | R | Solo si +0x2A bit1: según la esquina tocada (+0x9E&0xF <0xB, tabla 0x975C) comprueba la distancia <8 a las esquinas (constantes 0x6D24–0x6D2A, 0x281, 0x37F) y que la dirección (+0x10C) sea la diagonal correcta; si el poste está libre (bit en 1C1820), acción 0xF (subir) y lo reserva. |
| 009788 | poste_chk_a | C | R | Distancia a la esquina en y. |
| 0097D4 | poste_chk_b | C | R | Distancia a la esquina en y. |
| 009820 | poste_chk_c | C | R | Distancia a la esquina en x. |
| 00986C | poste_chk_d | C | R | Distancia a la esquina en x (0x281/0x37F). |
| 0098B4 | poste_esq0 | C | R | Esquina 2 (dirección 6/5). |
| 0098D4 | poste_esq1 | C | R | Esquina 8 (dirección 4/5). |
| 0098F2 | poste_esq2 | C | R | Esquina 1 (dirección 1/8). |
| 009910 | poste_esq3 | C | R | Esquina 4 (dirección 1/2). |
| 009958 | nada | C | R | rts |
| 00995A | chk_tabla_umbral | C | R | Si +0x18 bit7 y /+0x24/ ≥ 0x400 → CC. Si no, compara +0x48 con la tabla 0x999E[d0][+2]. |
| 0099BE | acc_recibir | C | R | Acción "recibir/caer". Si la subacción anterior +0x45 es 0x1C o 0x13 desactiva el objeto 1C0AB2 (bit7 de +0). Primer frame: si +0x5E bit6, el portado (+0x60) pasa a +0x2C=4. Salta a la subacción +0x44 (tabla 0x9A14) con los parámetros de la tabla 0xA74A[+0x44] en a2. |
| 009AAC | rec_s0 | C | R | Gira, sonido 0x14 (0x27D2) y cae hasta el suelo (z 0xBB, o 0x80 fuera) → acción 0xB (en el suelo) y sonido 0x29; animación de la tabla 0x9B3E/0x9B41. |
| 009B44 | rec_lanzado | C | R | Rama de la subacción lanzado: impulso (0x9BBE). |
| 009B52 | rec_lanzado_girado | C | R | Igual, pero girado. |
| 009B66 | rec_lanzado_txt | C | R | Igual, con el texto 0x9B (0x2549E). |
| 009B7E | rec_lanzado_d7 | C | R | Igual, con d7=1. |
| 009B88 | rec_lanzado_10 | C | R | Impulso 0x10. |
| 009B9A | rec_lanzado_20 | C | R | Impulso 0x20. |
| 009BBE | impulso_lanzado | C | R | x += ±d0; +0x18 bit7 (en el aire); +8 de a2+0x10; sonido de a2+0x12 (0x23 si es el id 7 en la subacción 1, o 0x12 si el rival es el 7); z += a2+0xE; anim a2+0. |
| 009CD0 | caida_cuerda_ring | C | R | Si choca con cuerda (+0x9E&3) → acción 8 con la subacción 1 o 2. |
| 009CFC | caida_cuerda_fuera | C | R | Fuera: subacción 3. |
| 009D18 | rec_rodar | C | R | Sonido 0x34 y el de la tabla 0x9E38; avanza 0x30 por paso con choque de cuerdas (0x9700); al tocar el suelo, acción 0xB y sonido 0x29. |
| 009E4C | anim_por_altura | C | R | Elige la anim de a2+8.. según la altura sobre el suelo (umbrales a2+2..). |
| 009E78 | empuje_ring | C | R | x ±0x10 con límites 0x21E5A; deshace si choca (salvo poses 0x9A/0xA1). |
| 009EC2 | empuje_fuera | C | R | x ±0x20 con límites 0x21ED0. |
| 009F02 | rec_contra_cuerda | C | R | Marca la cuerda, z ≥ 0xCB, sonido 0x11, rebota (+0x24 negado); al caer a 0xBB → 0xB y sonido 0x29. |
| 009F74 | rec_rebote_suelo_fuera | C | R | Velocidad z/4 negada; al llegar a 0x80 → acción 0xB. |
| 009FCC | rec_empujado | C | R | Sonido 0x25/0x1D/0x1B/0x19 según la subacción e id; avanza 0x30 con choque; al suelo → 0xB y sonido 0x29. |
| 00A16E | rec_caer_fuera | C | R | Cae hasta 0x80 → acción 0xB. |
| 00A196 | rec_sobre_rival | C | R | Se coloca sobre el rival (+0x68): x±0x10, y−2, z+0x28 (salvo +0x31 del rival =0x34) y cae (0xA230). |
| 00A230 | caida_general | C | R | Mueve. En el ring con cuerda → subacción 2. Si cruza las cuerdas por arriba (0xA39A) → pasa fuera (+0x19=1, +0x33 bit0). Al tocar 0xBB: 1C1858=0x81 (0x80 si id 7), acción 8 sub 0x20, sonido 0x29 si +2=7 y 0x3E (sub 0xA) o 0x34. Fuera: suelo 0x80. 1C1858 = temblor de pantalla, confirmado en 0x1621A (0x81 = corto, 3 frames; 0x80 = 9 frames, id 7). |
| 00A358 | caida_pose | C | R | Pose 0x17, x += tabla 0xA392[id]. |
| 00A39A | cruza_cuerda_chk | C | R | Z si el lado (+0x18 bit8) coincide con la orientación. |
| 00A3BC | nada | C | R | rts |
| 00A3BE | rec_suplex | C | R | Impulso 0/−0x10 y caída; en la sub 0xA anima las poses 0x9B+n con los tiempos de la tabla 0xA43C. |
| 00A440 | rec_vertical | C | R | Pose 0x9C, vz=0x10; al suelo: 1C1858, acción 0xB, gira y sonido 0x29. |
| 00A4C8 | rec_elevado | C | R | Sonido 0x29, vz=0x30 y +0x28=0x100; al suelo → 0xB y sonido 0x29. |
| 00A540 | rec_soltado | C | R | 0xA554; si acaba en 0xB borra +0x2C bit1. |
| 00A554 | rec_soltado_cuerpo | C | R | Sonido 8, anim 0xA2/4. Si el rival estaba en 0x17 (llave) con él, lo suelta (acción 8 sub 0x13) y limpia las celdas fg0 0x808BC/0x808C0. Al suelo → 0xB. |
| 00A612 | rec_tumbado_por | C | R | Mira como el rival, sonido 0xE; cae con choque de cuerdas. |
| 00A6BC | rec_aturdido | C | R | Sonido 0x15, pose 0x14F; al suelo, sonido 0x29; cuando +8 termina → acción 5. |
| 00A748 | nada | C | R | rts |
| 00A90E | acc_levantarse | C | R | z al suelo, pose 0x1A, tiempo de la tabla 0xAA00[+0xF0&7]. Al acabar, si es CPU y está junto al poste (zona tipo 0xC, dist <0x30/<8): con rng&0xF < tabla 0xAA20[id] sube al poste (acción 0xC, +0x30 de la tabla 0xAA10, mira al lado opuesto del rival); si no, acción 0 (o 0xD si +0xF0 bit7). +0xF0 bit0 frena la velocidad 8 por frame. |
| 00AA28 | acc_bloqueo | C | R | Suelta a quien lleve; si no está fuera (o el rival no está en 0x31=1) y 0x995A da CC → acción 0xA. Si no, pose 0x11 (0x12 si el rival tiene +0xC1 bit0) durante 6 frames y vuelve a 0. |
| 00AA9C | acc_aturdido_corto | C | R | 0xC6CA, suelta, pose 0x14 durante 0xC frames → acción 0xE. |
| 00AAF2 | acc_aturdido_fin | C | R | Pose 0x14/8 hasta acabar → acción 0 y 0xB16A. |
| 00AB1E | acc_en_suelo | C | R | Acción 0xB (tumbado). Init: z al suelo, pose 0x17, ajuste contra las cuerdas (0xACA4). Tiempo en el suelo +0x38 = tabla 0xAF66[índice de energía 0x1CE9C]; a la CPU se le divide entre 2 si 0x1CD80 da CS, y +0x20 si venía de fuera. Marca +0xD6 bit7 en el rival y su compañero (pueden cubrir). Humano: machacar botones (+0x116) adelanta el levantarse (0xAD12, umbral 0xAF6A[energía] → acción 0x19). Con +0x18 bit5 (le están cubriendo) va a la salida del pin: 0xADEA el humano, 0xAE7E la CPU. Al acabar el tiempo → acción 5 (levantarse) salvo que el rival esté en 0x12/0x17/0xC-6. |
| 00ABA0 | tumbado_cpu_div2 | C(A) | A | Divide +0x38 entre 2 si CPU mareada/≥umbral. |
| 00AC88 | suelo_ajuste_x | C | R | x ±0x38 |
| 00ACA4 | suelo_chk_cuerdas | C | R | Prueba los límites 0x30/8 por delante y deja el resultado en d7. |
| 00AD12 | suelo_machacar | C | R | Humano: cada pulsación sube +0x34; al llegar a la tabla 0xAF6A[energía] → acción 0x19 (levantarse rápido). CPU: si el rival cae sobre él desde el poste (acción 0xC con una subacción de la lista 0xAF76, bajando, a una altura relativa de 0x10–0x30), con rng < tabla 0xAF82[nivel][energía] (0xAF96 para el id 7) esquiva (acción 0x19), y el rival en la sub 4 pasa a la acción 5. |
| 00ADEA | pin_salida_humano | C | R | Humano cubierto: umbral = 0xAF72[energía]/2. Si la cuenta del objeto 1C0568 (+0x2F = 1C0597) aún no lo alcanza, cada pulsación (+0x114) suma; con 0x30−energía pulsaciones → se libra (acción 0x1E). Si la cuenta llega al umbral (y en 1C0595=2 con 1C059E≠0) también sale. Al salir, cancela los agarres (0xC554). |
| 00AE7E | pin_salida_cpu | C | R | CPU cubierta, mientras 1C05A5 bit2 (cuenta en marcha): nivel de energía d1 (0xAF26). d1=6 (energía 0) nunca sale. d1=0 sale si 1C0595=2, 1C059F≥1 y 1C0570≠0. En los demás, sale cuando cuenta*2+(1C059E bit0 negado) ≥ d1 y 1C059F≥2 y 1C0570≥4 → acción 0x1E y suelta al rival. |
| 00AF26 | nivel_energia_pin | C | R | d1 según la energía: ≥0x36→0, ≥0x30→1, ≥0x24→2, ≥0x19→3, ≥0xE→4, >0→5, 0→6. |
| 00AF9A | cpu_tirada_nivel | C | R | En modo tag fuera del combate 0, la primera vez (+0x107 bit0) da CC. Si no, rng&0xF frente a la tabla 0xAFF4[nivel*3 + 0x1CEF4] (CS si la tirada se cumple). |
| 00B012 | acc_alzar_lanzar | C | R | Desactiva 1C0AB2 (bit7). Anima con las poses de la tabla 0xB0EA y lleva al rival encima (pose 0x9B, x±0x28, y−1, z+4). Tras 2 pasos el rival pasa a la acción 8 sub 0x1C y se gira, 1C185A=0x81 (activa el mensaje parpadeante fg0, ver 0xF844), y el texto 0x9B (0x2549E); él va a la acción 5. |
| 00B0F2 | acc_provocar | C | R | Fuera del ring → acción 0 y 0x8F08. Si no, alterna las poses de 0xB162 tres veces y vuelve a 0 (más 0xB16A). |
| 00B16A | cpu_tras_accion | C | R | CPU: si 0x1D0E2 con la tabla 0xB188 da CS → +0x5C=0xC (tabla 0x1B40C[0xC] = 0x1A05E: alejarse del rival dando vueltas y pedir relevo). |
| 00B1A0 | acc_espera | C | R | Marca +0x2C bit6. |
| 00B1A8 | acc_espera_rival_1b | C | R | Espera mientras el rival está en 0x1B; luego acción 0 y borra +0x1C en ambos. |
| 00B1D0 | acc_forcejeo | C | R | Forcejeo (lock-up) con el rival, que debe estar en la acción 0x11; si no, vuelve a 0. Init: velocidades a 0; +0xFF cuenta los forcejeos (sin +0xFE bits5/6); +0xAE=2; 0x16F58 y 0xB670. El dirección del humano (+0x116&3) va a +0x28. +0x26 cuenta frames. Si +0xAF bit1 → 0xB5C2. Ventana: CPU 0x20 frames; humano 0x10 (o 8/0x11 según el bit1 de +0x2A; 0x30 si 1C001A≠0). En el frame 0x10, en tag (1C0026 bit1) o con el rival CPU que gana la tirada 0x1CD80, entra en el modo tirar/empujar (+0xAF=3/2). Al cerrar la ventana con dirección → 0xB48C (gana la llave). Si no, alterna las poses de la tabla 0xB46C[id del rival] con los tiempos 0xB468. Cuando 0x2786 da CS, ambos se separan 0x18 y vuelven a la acción 0 (+0xFF a 0 si +0xFE bit7). |
| 00B2DC | presa_tick16 | C(A) | A | Presa: en el tick 16 gana el humano si CPU mareada/≥umbral. |
| 00B422 | forcejeo_limite | C | R | Si +0xFF > 3 → +0xFE bit7 y CS. |
| 00B442 | forcejeo_anim | C | R | Alterna 2 poses/tiempos de las tablas a3/a1. |
| 00B48C | forcejeo_resolver | C | R | El rival pasa a la acción 0x10 y él a la 0xC. La CPU elige la llave con 0x1E05C. El humano la elige por la entrada +0x28 con la tabla 0xB5B2 (bando 1) o 0xB5BA (+4 fuera); si dir bit0 y +0x10D∈{1,2,8}, usa el índice 3. Sin entrada, los dos van a 0x8011 (+0xAF 3/2). Con la sub 0x26 → contra mutua 0x145F2. Borra +0xAA, +0xFE bits5–6 y +0xFF. |
| 00B5C2 | forcejeo_anim | C | R | 2 pasos de 4 frames con las poses de la tabla 0xB650[id del rival]; al acabar borra +0xAE/+0xAF bits. |
| 00B670 | forcejeo_ganador | C | R | Decide quién gana el forcejeo (+0xAF bit0). +0xFE bit6 da la victoria directa. Sin 1C001A, gana 1C0100. En tag, decide 1C0046 bit1. Si no, contra la CPU (rng>>1&7) con la tabla 0xB74A[nivel*8] (+0x50 si +0xFF≠2); con +0xF8 bit7 o +0xF9 bit0 del rival, o +0xFF>3, gana el otro. Al final 0xB7EA. |
| 00B7EA | ajuste_x_limites | C | R | Prueba x±0x24 con 0xB822 y copia x al rival. |
| 00B822 | limites_x | C | R | 0x21E5A dentro del ring; 0x21ED0 fuera. |
| 00B838 | acc_presa_mantenida | C | R | Presa sobre un rival en la acción 0x13. Al empezar: sonido 0x2D, pose 0x105, +0x34=0xFF (−4/frame con +0x117), rival enfrentado a x±0x10 y 0xBBB2. Al acabar el tiempo, sub 3. Despacha +0x44 por la tabla 0xB91E. La sub 0 alterna las poses 0xBCCC/0xBCC8; con 1C1898/1C189A (por lado) bit14 = cuerda vibrando (0x21324) → 0x2786 → suelta (los dos a la acción 0, +0x5C=0). Si el rival deja la 0x13 → suelta y él a la 0xD. |
| 00B92E | presa_sub0 | C | R | La sub 0 de 0xB838: alterna 2 poses (tablas a5/a3) y comprueba 0xB988 (cuerda vibrando) → 0x2786 → suelta (los dos a la acción 0, +0x5C=0). |
| 00B988 | presa_chk_salida | C | R | Lee 1C1898 (lado 1) o 1C189A; con bit14, suelta: el rival a la acción 0 y él a la 0xD (CC). Si no, CS. Bit14 = la cuerda de ese lado está vibrando (animación de 0x21324; no es una entrada). |
| 00B9D0 | borra_objs_efecto | C | R | Con +0x5C=0, libera los objetos +0x22/+0x26 y pone +0x5C=1. |
| 00BA18 | presa_sub_golpe | C | R | Prueba 0x995A(d0=2): si falla, él a la acción 8, 0xC6CA, el rival a la 0. Si no: pose 0xBE+id*2−(+0xC0&1), 16 frames y luego 0xBA8C. |
| 00BA8C | presa_vuelta_sub0 | C | R | Temporizador; al acabar, sub 0 y pose 0xBCCC[id]. |
| 00BAC2 | presa_sub_golpe2 | C | R | Como 0xBA18 con d0=3 y la pose 0x125+(id&0xF), 8 frames. |
| 00BB2A | presa_sub_final | C | R | Poses 0xBCEC/0xBD0C, 2 pasos; luego suelta y él a la 0xD. |
| 00BBB2 | crear_objs_llave | C | R | Toma 2 objetos libres de la lista 0xBCB8 (4 punteros) y los enlaza (+0x26 y +0x22) con los dos luchadores: uno con pose 0 a x±0x10, y el otro con pose 0xBC a y−2/z+2. Copian id, control y estado. |
| 00BD10 | acc_cubrir_pin | C | R | Acción 0x17 (tabla de acciones 0x8CE2: entrada 0x8D3E) = CUBRIR (pin). La pone 0x12972 a la vez que marca al rival con +0x18 bit5 (cubierto), que es lo que hace pasar al árbitro al estado 2 (0xD7D8 → cuenta del pin 0xDD4E). Acción de colocarse encima del rival (a2=+0x68, enlace mutuo). Si es la CPU: +0xC6=0x80 de un luchador fijo por slot (1C02E0/1C01C6/1C0514/1C03FA). Si el rival es humano: 1C185A bit7 (mensaje fg0). Pose 0x65 (0x7F para los ids 0/4), o 0x188 con +0x2C bit5. Posición desde la tabla 0xBEF2[id*0x10][id del rival] (dx, dz) e y del rival−1. Activa el objeto 1C0AB2 (pose 0x80) con la misma posición. Al acabar (dentro o sin bando 1): z=0x80, acción 5, apaga 1C0AB2. |
| 00BF72 | acc_ir_a_punto | C | R | Calcula la zona con 0xC018; si es 0xFF, acción 6. Si no, +0x1E=dirección y anima con las tablas 0xC072/0xC082 (4 pasos de 5 frames). |
| 00BFC4 | anim_ciclo4 | C | R | Ciclo de 4 poses (tabla 0xC072, 5 frames) y orientación (0xC082) según 0xC058; 0xC00A: acción 6 y borra +0xC0 bit6. |
| 00C018 | zona_destino | C | R | Compara x e y+z con el punto de la tabla 0xC094[0xC058] y devuelve la dirección de la tabla 0xC084. |
| 00C058 | es_bit4_ctrl | C | R | d0 = +0x2A bit4. |
| 00C09C | acc_15_correr | C | R | 0x8ECE. En la acción 0x15: +0xA8 bit7 y +0x24++. Fuera (+0x19=1), tras 0x15 frames la CPU hace 0x8EEA y pasa a la acción 0x14. Dentro, con +0xA8&0x8001 → 0xC116; fuera de los límites x 0x2F1/0x30F → acción 1. |
| 00C116 | cpu_reaccion_carrera | C | R | Solo la CPU. Si el rival hace una llave de la lista 0xC2AA y está cerca (hitbox dz<8, dx<0x50) → tirada 0xC34C → acción 5 (+0xF1=3). A media distancia (0x20–0x40, o 0x40–0x68 según el id) → tirada 0xC308 → acción 0xC sub 0xC326[id]. A 0x30–0x4A (0x3B para ids 4/7) → tirada 0xC32E → +0x26 bit4. |
| 00C2B4 | tirada_nivel3 | C | R | rng&7 frente a a2[nivel*3 + 0x1CEF4]. |
| 00C36A | acc_rodar_fuera_ring | C | R | Acción 0x19 (entrada 0x8D46). La ponen las salidas del pin (0xAD3A, 0xADD2), 0x11610/0x118A6 (al rival) y 0x12B00 (al cubierto al acabar la cuenta). Poses 0xC54C, sonido 0x32. Sub 0: anima dentro hasta que +0x9F bit2 (contacto con la cuerda) → sub 1: trepa hasta y<0xD8 y cae fuera del ring tumbado. Si ya estaba fuera, termina en la acción 5. El nombre es descriptivo: el código no contiene nombres de movimientos. |
| 00C3DE | c36a_sub0 | C | R | Dentro: anima 2 pasos y luego acción 5. |
| 00C444 | c36a_sub1 | C | R | Despacha +0x34 por la tabla 0xC458. |
| 00C45C | c36a_trepar | C | R | Anima en bucle con la física 0x3DCE; cuando y<0xD8 → +0x34=1. |
| 00C4A6 | c36a_caer_fuera | C | R | y−8, z+8, sonido 7 (0x27D2), +0x18 bit7, pose 0x16, +0x19=1 (fuera). Cae con 0x3DCE; al llegar a z<0x80 → acción 0xB (tumbado) con bit1 y +0xAE=0. En la rama de fuera, anima con los límites 0x21ED0 y luego acción 5. |
| 00C554 | tag_cambio_control | C | R | Con el bando bit1: alterna +0x33 bit1. Si los dos son humanos y 1C0026&3≠1: intercambia el bit0 de control entre él y su compañero (a1) y borra +0x10C/+0x110/+0x114/+0x116. Calcula si el compañero está en pantalla (cámara 1C002A/1C002E) → +0xF2 bit7 (fuera de pantalla) y bit6. |
| 00C628 | acc_deslizar | C | R | +0x22=2; frena +0x20 en 4 por frame con 0x3DCE y la pose 0xB. Contra la cuerda (+0x9E&3): dentro → acción 2 (+0xA8=2); fuera → acción 8 sub 7. Parado: cuenta +0x23 y pasa a la acción 0; +0x5C=1 si +0xF2 bit7 y no 1C0026 bit0. |
| 00C6C8 | nop | C | R | rts. |
| 00C6CA | sonido_44_2b | C | R | Sonido 0x44, o 0x2B con +0x2A bit4 (modo 1C0026 bit1) o bit3 (CPU). |
| 00C706 | humano_golpe_boton | C | R | Con el botón +0x116&3 en la acción 0, o en la 0xC con sub<9 y la tabla 0xCC1C. Con +0x5E bit6 (lleva a alguien): sub de la tabla 0xCB16. Si no, la tabla 0xCADE (0xCAFE fuera)[id][desplazamiento+botón]. Desplazamiento según el rival (tabla 0xCB1A[acción del rival]): +0xC si está tumbado cerca (0xFE), +6 delante (<0x20/0x28) o +9 detrás (<0x30/0x38), con dz<0x18. 0xFF → acción 1 y reinicia la entrada. Ajustes de las subs 6/9 y 0xC9E2/0xCA4E. Acción 0xC; la sub 4 enlaza al rival en la acción 0x10 (salvo que el compañero lo esté sujetando, acción 0x17); 0xE462. |
| 00C9E2 | chk_sub3_alcance | C | R | La sub 3 solo vale con el rival a dx<0x70 y dz<0x10, enfrentados, y el rival en la acción 1/2/0x15/0x16; si no, restaura la acción (d4=0x80). |
| 00CA4E | cpu_chk_alcance | C | R | CPU (o humano en la sub 0x10): si está a menos de 0x70 (0x30 en la sub 0x10) en x y 0x10 en y, mirándose, y el rival no está en las acciones 1/2/0x15/0x16 → +0x2C=d6, d4=0x80. Sub 0x10 con el rival a energía ≥0x16 → +0x30=3. |
| 00CC26 | cpu_boton_a_sub | C | R | Con un botón en +0x116: sub = tabla 0xCD14[id*3+botón−1] y acción 0xC; 0xCC8A; CS. |
| 00CC8A | chk_golpe_por_cuerdas | C | R | Si él está dentro y el rival fuera (sin bit4), dz<0x20 y del lado correcto: prueba x±0x80 con 0x21E5A; si toca la cuerda y dx<0x100 → +0x30=0x35. |
| 00CD2C | chk_cuerdas_salir | C | R | Despacha +0x9E&0xF (<5) por la tabla 0xCD48. |
| 00CD5C | cuerda_lateral_izq | C | R | Sin 1C1898 bit6, con la dirección 7 en el lado 1 e y+z en 0x1E0–0x230 → acción 3 (+0xAC=0). El humano de equipo necesita 12 frames (+0x102). Sin bit4/bando y dentro → acción 6. CS. |
| 00CDF8 | cuerda_lateral_der | C | R | Simétrica: 1C189A, dirección 3, +0xAC=1. |
| 00CE8E | cuerda_frontal | C | R | Dirección 5 con x 0x280–0x380 → acción 3, +0xAC=2. CS. |
| 00CEC2 | cuerda_no | C | R | Borra +0x102 y CC. |
| 00CECC | acc_cruzar_cuerdas | C | R | Acción 3: trayectoria de la tabla 0xD0AE (0xD1AA para el id 7)[+0xAC] (+3 si +0x19=3), con pasos (pose, dx, dy). Al empezar copia los parámetros a +0x22..+0x28 y 0xD00A. Entre los pasos d0 y d1 salta (vuelo con 0x3DCE, +0x18 bit7) hasta z<0x80. Al acabar: acción 0, +0x5C=0, z=0x80; 0xD04A. |
| 00D00A | cuerda_interp_x | C | R | Salvo con +0xAD 2/5: x = x0 ± (y−y0)/6 (cuerda en diagonal). Si no, y=y0. |
| 00D04A | marca_pose_especial_id7 | C | R | Id 7: si la pose está en la lista 0xD092 (2 entradas), 1C1A92 bit7 = 1 y 1C1A93 = +0x18 bit0; si no, borra el bit. |
| 00D2D6 | humano_salir_ring | C | R | Con contacto +0x9F y la dirección (+0x10C=7/3, sin 1C189A/1C1898 bit6) e y+z en 0x1A0–0x210 → +0xAC=0/1 (+3 con bit4/no bando) y acción 4 (7 si +0x19=3; 0x20 si lleva a alguien). Cuerda frontal: bit3, dirección 1, x 0x280–0x380 → +0xAC=2. CS. |
| 00D400 | acc_entrar_ring | C | R | Secuencia guiada por la tabla 0xD54C[+0xAC&0xF] (0xD646 para el id 7): (pose, dx, dy) por paso; +0x19=3 salvo en la entrada 2. Al acabar: +0x19 /= tabla 0xD52E, vuelve a la acción 0 y, en tag con el compañero dentro, texto 0x9B. |
| 00D7D8 | arbitro_elige_estado | C | R | Árbitro (1C0568), salvo en el estado 4 con id 1. Toma el luchador activo (bando bit1) de cada equipo: 1C0100/1C021A y 1C0334/1C044E. Estado nuevo: 2 si alguno está cubierto (+0x18 bit5); 3 si alguno está fuera (+0x19=1) o en la acción 4; 1 si alguno hace la sub 0x13/0x2E (acción 0xC) o la acción 0x1B (guarda el luchador en 1C05D0); 0 en otro caso. Si cambia, lo escribe en +0x2D y borra +0x2C. |
| 00D8F4 | arbitro_e0_seguir | C | R | Va al punto medio entre los dos luchadores (0xDFE0), con y forzada a 0x175 o 0x118 según el lado de 0x148. Dirección con 0x270C (1C004E→1C0052), velocidad 8. Si el destino cambia de lado: +0x3D bit4 y el cuadrante en +0x3C → rodea por las cuerdas con la tabla 0xDB44. Mira hacia el centro; si está a más de ±4, se mueve (0x3DCE) y anda (0xDA38). Límites 0x21E5A. |
| 00DA38 | anim_8dir | C | R | Animación de 4 frames cada 8 ticks; elige la pose por dirección (+0xA en 8 sectores) en la tabla 0xDAC4 (0xDB04 en el estado 3, o el 4 con control 2). |
| 00DB54 | arbitro_rodear_q0 | C | R | Rodeo: y mínima 6D26+0x38−0xBB (sale del bit4); con contacto +0x9F bit0 → dirección 0x80, si no 0xC0. |
| 00DB8E | arbitro_rodear_q1 | C | R | Igual con +0x9F bit1 → 0x80/0x40. |
| 00DBCE | arbitro_rodear_q2 | C | R | Con +0x9F bit3 termina; bit0 → dirección 0, si no 0xC0. |
| 00DBF8 | arbitro_rodear_q3 | C | R | Con +0x9F bit3 termina; bit1 → dirección 0, si no 0x40. |
| 00DC22 | arbitro_e1_vigilar | C | R | Va junto al luchador +0x68, a x±0x30 (lado según x≥0x300), y cuando llega (±4) alterna las poses 0x12/0x13 cada 4 frames, mirándolo. |
| 00DD4E | arbitro_e2_cuenta_pin | C | R | Cuenta del pin: se acerca al punto medio (±0x20 x, ±0x30 y) y luego da palmadas con las poses de la tabla 0xDED4 y las duraciones 0xDEDC (bucle de los pasos 2–3). En el paso 3, frame 1: +0x2E++ y 0xE02C (muestra/suena la cuenta). Al llegar a 3: escribe el resultado en 1C0BBE+4 y 1C0BD6+4 (bit6/bit7 según qué bando está cubierto, a1+0x18 bit5). |
| 00DEE4 | arbitro_e3_cuenta_fuera | C | R | Cuenta fuera del ring en BCD (abcd) hasta 0x20 (20). Mira al luchador que está fuera (+0x18&3=1). Cada ciclo de la animación: +1 y 0xE02C. Al llegar a 20: 1C0BBE+4 / 1C0BD6+4 bit7 si ese luchador está fuera (+0x18&3 ∈ {1,3}), si no bit6. Permite la doble descalificación por cuenta fuera. |
| 00DFDE | arbitro_nop | C | R | rts (estado vacío de la tabla 0xD7AE). |
| 00DFE0 | punto_medio | C | R | a2 = punto medio entre a2 y a1 (x e y). |
| 00E016 | arbitro_reset | C | R | Borra +8, +0x36, +0x2E, +0x2A y +0x18. |
| 00E02C | sonido_texto_estado | C | R | Sonido de la tabla 0xE0A8[+0x2E] (salvo 0xFF, o en el estado 3 con +0x2E<4), texto 0x9B y el texto de 0xE086[+0x2E]. |
| 00E132 | obj_nop | C | R | rts. |
| 00E134 | obj_seguir_portador | C | R | Copia la posición del portador (+0x60) con x±0x10 y su orientación. |
| 00E172 | obj_reposo | C | R | Pose 0xE1B6[id]; 0xE1BC; la primera vez, 0xE7E8. |
| 00E1BC | obj_ofrecerse | C | R | Para cada luchador (tabla 0xE224) que esté fuera (+0x19=1) y sin llevar nada: si es el objeto más cercano en x, lo marca como disponible (+0x5E bit7, +0x60=objeto, +0x64/+0x66 distancia). |
| 00E234 | obj_romper | C | R | Sonido 0x28; x±0x20, z+0x20; 5 pasos de pose (0xE2B8) y desaparece (borra bit7 de +0 y 1C1823 bit1 o bit2). |
| 00E2CC | obj_lanzado | C | R | Vuelo con 0x3DCE (velocidades 0xE374), pose 0xE37C[id] (+2 según el lanzador +0x18 bit6). Al caer (z<0x80): sonido 0x27, acción 2 y vuelve a estar disponible (+0x5E bits 7/6). |
| 00E388 | obj_caida_desp | C | R | Despacha +0x44&1 por la tabla 0xE39E. |
| 00E3A6 | obj_rebote | C | R | Trayectoria 0xE45A; pose 6/0xA (1 para el id 0). Al caer: sonido 0x27, acción 2 sub 3. |
| 00E462 | recoger_objeto | C | R | Busca entre los 3 objetos (1C0682, stride 0x10C) uno en la acción 2, a la misma z, dentro de la caja 0xE542 y disponible. La CPU solo coge su objetivo (+0x60). Si lo encuentra: acción 0x1D, enlace mutuo por +0x60, +0x5F=id del objeto, +0x5E bit6 y el objeto a la acción 1. Si no: la CPU pone +0x5C=0. |
| 00E572 | acc_coger_obj | C | R | La CPU va a 0x1CC36. El humano: 0x9184 y 2 pasos de 8 frames, pose base de la tabla 0xE5F0[+0x5E&3]; luego acción 0. |
| 00E5F6 | acc_soltar_obj | C | R | La CPU va a 0x1B326. Si no: 2 pasos de 8 frames y luego la acción 4 (0 sin bando). El objeto pasa a la acción 2, a x±0x20, disponible; borra +0x5E bit6. |
| 00E6E0 | crear_obj_2 | C | R | Crea el objeto 1C089A (id 2, 0x8002, acción 5, disponible) en la posición de 1C078E con z+0x20 y x±0x20; 1C1823 bit2. |
| 00E76E | soltar_obj_682 | C | R | El objeto 1C0682 aparece donde está él (z+0x20, x±0x20), acción 5; 1C1823 bit2; borra +0x5E bit6. |
| 00E7E8 | obj_evitar_pared | C | R | Desplaza x según la tabla 0xE874 (0xE880 en la acción 2) con los límites de fuera 0x21ED0; si choca (+0x9E&3), deshace. |
| 00E88C | zonas_todos | C | R | Para los 10 objetos de la tabla 0xEA4C (salvo el árbitro) llama a 0xE8A6. |
| 00E8A6 | calc_zona_18 | C | R | Salvo en las acciones 3/4/6/7 recalcula los bits 0–4 de +0x18. bit0: x ≤ [0x4332]. bit1: y+0xBB < [0x4334]. bit2/bit3: esquinas/delantal según las cajas 0xEA34 (lado 1) o 0xEA40 (sin bit2, borra +0xE3 bit0). bit4: +0x18&3=1 con y+0x80 ≤ 0x158. |
| 00EA74 | elegir_rival | C | R | Con 1C001A≠0 y fuera de los estados de la tabla 0xEBCC/+0xC8: toma los dos rivales posibles de la tabla 0xEBBC[slot] y despacha por la zona +0x18 (tabla 0xEAF0). Preferencia: el que sujeta (0x17) o hace la sub 6, el no cubierto, el que está en la misma zona, el del bando activo. Escribe +0x68 (rival), +0xA0 (el otro) y +0x6C (0/1). |
| 00EB00 | elegir_rival_z0 | C | R | Preferencias de 0xEA74 para la zona 0 (ver ahí). |
| 00EB60 | elegir_rival_z1 | C | R | Elige por coincidencia del bando bit1. |
| 00EB72 | elegir_rival_z2 | C | R | Elige el de bando bit1. |
| 00EBA0 | cmp_bando | C | R | Compara el bit1 de +0x2A (bando) de a0 y a2; ramas de la tabla 0xEAE6. |
| 00EBEE | acc_subtabla_b8 | C | R | Salta por +0xB8 a la tabla 0xEBFE. |
| 00EC12 | acc_subir_esquina | C | R | Sube a la esquina (+0x19=2) por pasos de la tabla 0xED20 (0xED40 para la CPU id 2, que además alarga +8 del rival tumbado en 0x40). Lado/posición por +0xB4 (copia de +0x18) con 0xECB8 y 0xECE2. Al acabar, +0xB8=2 (3 para la CPU en el lado bit1). |
| 00ECB8 | esquina_tablas | C | R | Selecciona las tablas de pose (a2) y posición (a3[id]) según +0xB4>>8&3; y desde la tabla. |
| 00ECE2 | cpu_id2_sonido22 | C | R | CPU id 2: con d0=5 (o 3 si +0xB4 bit1) → +0xE2 bit0 y sonido 0x22. |
| 00F018 | acc_bajar_esquina | C | R | Recorre los pasos al revés. Al acabar: z=0xBB, acción 0, +0x5C=0, libera su bit de 1C1820 (+0x34), +0x19=+0xB5. Si es humano sin control bit0, +0x5C=7. |
| 00F098 | esquina_paso | C | R | Pose, x y z del paso d0. La CPU id 2 en el lado no-bit1 se gira a partir del paso 5. |
| 00F0DE | esquina_esperar | C | R | La CPU va a 0x1C47E. El humano despacha por la esquina (+0x18&3) con la tabla 0xF100. |
| 00F110 | esquina_q0 | C | R | Mira a 0x80, pose 0x1F, posición 0xF280. Con control: remapea la dirección (tabla 0xF6BA → +0x10D) y 0xF35A; si no, 0xF2B0. |
| 00F15E | esquina_q1 | C | R | Igual mirando a 0 con la tabla 0xF6C4. |
| 00F1AC | esquina_q2 | C | R | Mira a 0, pose 0xF0DA[+0xBE&1]; sin dirección pone 4 (u 8 con +0xBF bit0); 0xF35A → 0xF2FA, 0xF2B0. |
| 00F218 | esquina_q3 | C | R | Igual mirando a 0x80, dirección 6 (o 2). |
| 00F280 | esquina_posicion | C | R | x, y, z de la tabla 0xF6CE[esquina]; +0x5C=0x7F (tiempo máximo en la esquina). |
| 00F2B0 | esquina_chk_bajar | C | R | Humano: la dirección 5 (o 1 en el lado bit1) → +0xB8=1 (bajar). Si no, decrementa +0x5C; a 0 (o sin control) → bajar. |
| 00F2FA | esquina_elige_salto | C | R | Si no está en las acciones 3/4/6/7: según el rival (o +0xA0 si no es el del bando) a y≥0xDD → +0xB8=3, si no 4 (salvo poses 0x69/0x1F). |
| 00F35A | esquina_boton | C | R | Despacha por la esquina con la tabla 0xF37A. |
| 00F38A | esquina_boton_q0 | C | R | Con un botón en +0x114: 0xF636, 0xF684 y la tabla 0xF3A6. |
| 00F3B6 | esquina_boton_q1 | C | R | Igual con la tabla 0xF3D2. |
| 00F3E2 | esquina_boton_q2 | C | R | Igual (o con +0xBA bit7) con la tabla 0xF406. |
| 00F416 | esquina_boton_q3 | C | R | Igual con la tabla 0xF43A. |
| 00F44A | dir_rotar_mas | C | R | +0x10C++ circular 1..8. |
| 00F466 | dir_rotar_menos | C | R | +0x10C-- circular 8..1. |
| 00F47A | salto_destino_q0 | C | R | Tabla 0xF6FE → 0xF498. |
| 00F482 | salto_destino_q1 | C | R | Tabla 0xF721. |
| 00F48A | salto_destino_q2 | C | R | Tabla 0xF746. |
| 00F492 | salto_destino_q3 | C | R | Tabla 0xF76A. Común: destino del salto en 1C00B4 (+0x16 x+dx, +0x18 y+dy, +0x14) según la dirección +0x10C; +0xB6=1; +0x10=−1; continúa en 0xF564. |
| 00F4DA | cpu_objetivo | C | R | Escribe el objetivo en 1C00B4: rival (+0x10), x/y; si está a ≥0x30, el destino es ±0x30 desde él (+0x10 = −1). z del rival a +0xBE. Despacha por +0x30 con la lista 0xF594 y la tabla 0xF59C. |
| 00F636 | esquina_salto_sub | C | R | Sub de la tabla 0xF6E6[id*3 + (rival no tumbado)]; acción 0xC; libera su bit de 1C1820. |
| 00F684 | const1 | C | R | d0=1. |
| 00F68A | b8_sub_pose68 | C | R | Pose 0x68 durante 8; al acabar, +0xBE^=1 y +0xB8=2. |
| 00F78E | tag_chk_relevo | C | R | Dentro, del bando, con un botón (+0x115), en la esquina (+0x18 bit2, sin +0xE3 bit0), con el compañero en la esquina bit2, y a 0x150 (0x108 con bit4) ±0x10. Si el compañero está fuera (+0x19=3) y en la acción 0: los dos +0x2A bit2 y acción 0x1A (relevo). CC. |
| 00F81A | esquina_ocupada | C | R | CC si el bit de la tabla 0xF840[esquina] está puesto en 1C1821. |
| 00F844 | flash_fg0 | C | R | Con 1C001A≠0, gestiona 1C185A. bit7 → pasa a bit1 con un temporizador de 3 (1C185B). bit1: cada 2 frames alterna bit2 y dibuja el texto 0x1E/0x1F (0x23A28); con bit6 borra las celdas fg0 0x80B04–0x80B18. bit0: borra 9 filas de fg0 desde 0x80B04 y pone 1C185A a 0. Así que 1C185A=0x81 es un mensaje parpadeante en fg0 (el texto 0x1E/0x1F), no un temblor. |
| 00F94C | acc_0c_llave | C | R | Acción 0xC: 0x240B6 (llaves por sub); dentro, si choca con la cuerda, 0xF9B0. Despacha +0x30 por la tabla 0xFB58. Al salir de la 0xC borra +0x33 bit3 de los dos. |
| 00F9B0 | llave_fuera_ring | C | R | Si el rival no está en la acción 0x10 → acción 8 sub 1. Según la subacción +0x31: 0x1B/0x21/0x22/7 colocan a los dos en x=0x280/0x390 (según +0x9F bit0) y les dan la acción 8; 0x29 y 0x28 son variantes de esa colocación. |
| 00FC4C | nop | C | R | rts. |
| 00FC4E | despacho_id | C | R | Llama a la tabla 0xFC64[id]. |
| 00FC84 | sub_combo_golpes | C | R | La CPU va a 0x15758. Tres pasos de la tabla 0xFD70 (0xFD88 para el id 7; 0xFD7C/0xFD94 con +0xC0 bit0). En los pasos 0xB/0xC acumula los botones en +0x22. Con el botón 1 alterna +0xC0 bit0 y repite (combo); si no, acción 0. |
| 00FDA0 | sub_combo_golpes2 | C | R | Como 0xFC84, con la tabla 0xFE88 (0xFEAC para el id 2) y 10 pasos. En los pasos 0x10/0x1C alterna +0xC1 bit0 y comprueba el botón 1 para encadenar; acumula +0x114 en +0x22 salvo en los pasos 0/0xC/0x18. Sin botón: acción 0. |
| 00FED0 | sub_golpe_simple | C | R | Tres pasos de la tabla 0xFF3A (0xFF4A con +0x2A=7); en el paso 0xC termina si +0xC9 bit2. Luego acción 0. |
| 00FF5A | sub_proyeccion_salto | C | R | Si el rival es el id 7: rival a la acción 0xC sub 0x1E, él a la acción 0x10, y se ejecuta 0x14CFC como el rival (contraataque). Si no: se gira, 0x14222, +0x5C=1 si +0xFC; rival a la acción 0x10. Animación de la tabla 0x10136[id del rival]+paso, duraciones 0x1013E/0x10146. Paso 2: sonido 0x50, 1C183E bit7, salto (+0x22=0x40, z+0x10). Paso 4: él a la acción 5, el rival a la acción 8 sub 0x1F pose 0x1CF a x±0x40, +0x3E=0xC, 0x161C8, +0xF6+=3, 0x15B90. En caída (z≤0xBB): 1C1858=0x80 (temblor) y sonido 0x48. Con +0x5C: 3 repeticiones y 0x145F2. |
| 01014A | sub_embestida | C | R | Pose 0x1D0 y voz 3 (0x27D2); +0x18 bit7. Si conecta (+0xC9 bit3 y el rival +0xC9 bit4 o +0x40=−2): sonido 0x2F y +0x34=1 (con el rival). Se mueve (0x3DCE, 0x1600C); si choca con la cuerda: acción 8 (y el rival también si +0x34). Al acabar los pasos (duraciones 0x10340): acción 5 a x±0x30; si +0x34, el rival a la acción 0xB pose 0x17. Al caer (z≤0xBB, o 0x80 fuera): sonido 0x34 y temblor; sin conectar, acción 8 sub 0x22 pose 0x1CF; si conectó, rebote (paso 6, velocidad /4, +0x28=0x200). |
| 01031C | anim_tablas_a2a4 | C | R | Pose/tiempo desde a2/a4[+0x36] (a2 = 0x10348 si +0x34 = 0). |
| 01037E | sub_salto_voz_b | C | R | Como 0x103A8 con la voz 0xB. |
| 0103A8 | sub_salto_aereo | C | R | Salto con la tabla 0x104FE y la voz 1; +0x18 bit7. Avanza ±8 con los límites dentro (0x21E5A) o fuera (0x21ED0). Al chocar con la cuerda: acción 8 sub 2 (o 3 fuera, si va hacia esa cuerda). Al caer (z ≤ 0xBB, o 0x80 fuera): pose 0x15F, sonido 0x29 (0x48 fuera), paso 0x10. Al acabar: acción 5 y se gira. |
| 01050E | sub_salto_hacia_rival | C | R | Igual que 0x103A8, pero se orienta como el rival, coloca la trayectoria con 0x156FA (tabla 0x1599C, ±0x20) y 0x110E4 (velocidad 0x180/0x180) hacia el rival. |
| 01055A | sub_golpe_rival_8_9 | C | R | Tres pasos de la tabla 0x105D0. En el paso 4 borra +0xC9 bit5 y, si el rival está en la acción 8, le iguala la x. Luego acción 0. |
| 0105DC | llave_lanzamiento_A | C | R | Si 0x14222 da fallo (+0xFC≠0), el rival contraataca (acción 0xC sub 0x1E). Si no, 4 pasos de pose (tabla 0x106F8[id del rival]) con sonido 0x2F; al final el rival pasa a la acción 8 sub 1, daño +0x3E=8 (0x161DA) y +0xF6 += 3. |
| 0107CA | chk_caer_sobre_rival | C | R | Si está en el mismo plano que el rival y el rival está tumbado (0xB) o sujeto (0x17), y z ≤ suelo+0x10: pose 0x1D2, se coloca sobre él con la tabla 0x10920[id] (orientación). Si está tumbado: rival a la acción 8 sub 0xD, +0x3E=1 y 0x161EC; si no, 0x108E2 con el compañero. Si no: al llegar al suelo d0, acción 5. |
| 0108B0 | copiar_8w | C | R | Copia 8 words de a6 a a1. |
| 0108E2 | soltar_llave | C | R | El rival pasa a la acción 8 sub 0x13; cancela los agarres (0xC554). |
| 010950 | sub_levantarse_rapido | C | R | Empieza en el paso 0x10 de la tabla 0x10A4A (continúa en 0x10976). |
| 010976 | sub_rodar | C | R | Rueda con la tabla 0x10A4A: +0x20=0x11 velocidad, +0x1E dirección (±0x40). A partir del paso 0x10 frena 2/frame. Con la cuerda: fuera → acción 8 sub 3; dentro, si va hacia la cuerda → acción 2 con +0xA8=2. A 0x14 acaba: acción 0. |
| 010A5E | sub_salto_esquina_ataque | C | R | Ataque desde la esquina/aire. Trayectoria de la tabla 0x11150[id*16 + aire*8 + variante] (con la sub 0x1A, según la zona x≥0x300/y<0x120) colocada con 0x156FA. +0x34 = 1 desde la esquina (2 en el lado bit1); +0x5C=1 si el rival está más arriba o (id 6 con la sub 0x11). Con +0x34, 0x110E4 (0x200/0x100). El id 1 en el suelo dobla la velocidad. En vuelo: si el rival está tumbado en el mismo plano y la z llega a +0xF4+0x10 → 0x10FCC. Si llega al suelo sin rival: acción 8 sub 5, temblor 0x81, pose 0x1CF (0x14F id 7), sonido 0x34, +0x3E=2 y 0x16488 (humano). Si impacta (paso 4): rival a la acción 8 sub 0xD, +0x3E = 5/0xA/+1 id1/0xB sub 0x1A/6 sub 0xF/0xC id 7; 0x161C8, temblor, sonido 0x49, 0xC6CA del rival; el id 1 añade la voz 8 y rebota (0x10EA8). Al acabar: acción 5, borra 1C0AB2/1C144E. |
| 010EA8 | sprite_efecto_144e | C | R | Objeto efecto 1C144E (0x8000) junto al luchador: y−2, z+6, pose 0x1CC, +3=1. |
| 010F04 | ajuste_y_impacto | C | R | id 0 sin +0x5D bit0: y+0xA y 0x1152A. Para el id 1 con +0x5C, la sub 0x1A sin +0x5C o el id 6 con la sub 0xF: y+2. |
| 010FCC | chk_impacto_aereo | C | R | Caja del rival: tabla 0x11084[id] (x±, con márgenes 0x10/0x30 según la orientación; y±8). Punto de impacto del atacante: tabla 0x110A4[id*2+esquina]. Si está dentro: paso 4 (impacto) y sonido 0x22 (0x23 para los id ≥ 6). |
| 0110E4 | cpu_ajuste_vel | C | R | Limita la velocidad hacia el rival: dx<0x60 (±0x40 si está tumbado) y dy<0x50/0x70. |
| 01143A | llave_10a5e | C | R | bsr 0x10A5E |
| 01152A | sprite_efecto_0ab2 | C | R | Objeto efecto 1C0AB2: y−0xA, x∓4, z+0xA, pose 0x7D, orientación invertida. |
| 011598 | sub_presa_intento | C | R | Si el rival está cubierto: acción 0. La CPU rival tira 0x450A contra la tabla 0x11726[dificultad 1C0028 + 0x1CE9C]; si resiste, él a la acción 5 y el rival a la 0x19. Si no: rival a la acción 0x10, pose 0x31+id*3, 3 pasos (duración 0x11724). Luego los dos a la acción 0x11 (forcejeo: +0xFE bit6 / bit5), +0xAA = +0x3C+0x30 (0x50 CPU), poses −1, enfrentados. En modo 1C0026 bit1, con 1/4 de probabilidad, +0x2C bit4 en los dos. |
| 01173A | sub_pisoton | C | R | Dos pasos de la tabla 0x118BC; en el paso 4: 0x1185A y 0x1179A. |
| 01179A | pisoton_impacto | C | R | Mismo plano. Si el rival está tumbado: acción 8 sub 0xD, sonido 0x49, 0xC6CA, +0x3E=1 (3 si +3=7), 0x161DA, +0xBF++ (máx. 4). Si el rival sujeta (0x17): 1C185A=0x81, acción 8 sub 0x13, borra el cubierto del compañero; los que tengan +0x33 bit1 → 0xC554. |
| 01185A | pisoton_rival_levanta | C | R | En el modo 1C0026 bit1 (o CPU), rival tumbado sin cubrir: tirada 0x450A contra la tabla 0x118B6[+0xBE] → el rival pasa a la acción 0x19 (se levanta) y borra +0xBE. |
| 0118D8 | despacho_id2 | C | R | Salta a la tabla 0x118EC[id]. |
| 01190C | sub_salto_cubrir | C | R | Salto hacia el rival: 1C00B4 con la altura de la tabla 0xBEF2[id][id del rival], velocidad 0x380/0x50, gravedad 0x4000/0x80, destino +0x68, 0x15B40 → +0x14, 0x159AC. Cuando baja: pose 0x64; si el rival está tumbado dentro, sin cubrir y él no está fuera, con z<0xC3: acción 0x17 (cubrir), rival +0x18 bit5 y +0x68=él; 0x11BC6 y, si no CC, 0x129A4. Si no: al suelo, acción 8 sub 0. |
| 011A72 | sub_cubrir | C | R | Se coloca sobre el rival (x de la tabla 0xBEF2[id][id del rival], −4 para el id 4; z de +8), pose 0x7E (id 0/4) o la tabla 0x11BBE. En el paso 8, si el rival está tumbado dentro, sin cubrir y él no está fuera: acción 0x17 y cubrir como en 0x1190C. Si no, reintenta. En el paso 0xC: acción 0. |
| 011BC6 | cubrir_chk_kickout_inmediato | C | R | Solo el modo normal (no 1C0026 bit1; con bit0, 1C0029≠0) con +0x107 bit0: tirada 0x450A&0xF contra la tabla 0x11C30[dificultad*3 + 0x1CEF4]. CC/CS invertido (CS = cubre). |
| 011C4E | sub_lanzar_por_encima | C | R | Agarra (0x14222), el rival delante a ±8. Si el rival es el id 7: acción 0xC sub 0x34 (contra). Poses 0x11E1E[id del rival]+paso (paso 5 pose 0x20E), 4 frames (8 con +0x5C). Paso 2: sonido 0x50, 1C183E bit7, +0xF6+=3. Paso 5: rival a la acción 8 sub 0x1E a ±0x80, pose 0x1CF. Paso 6: él a la acción 5 (x∓0x20), +0x3E=0xC, 0x161C8, temblor, 0x15B90, sonido 0x34. Con +0x5C: 3 repeticiones y 0x145F2. |
| 011E2E | sub_golpe_cabeza | C | R | Con +0xFC: contra (rival a la acción 0xC sub 0x1E, 0x14CFC). Poses 0x11F52[id del rival]+paso, duraciones 0x11F62. Paso 1: sonido 0x49. Paso 2: él a la acción 0; rival a la acción 8 sub 1 pose 0x15 a x−0x10; sonido 0x50, 1C183E bit7, +0xF6+=3, 0x15B90, +0x3E=8, 0x161C8. |
| 011F66 | sub_suplex | C | R | Con +0x30 bit7: 0x1229C (el rival, en la pose 0x1C3, se levanta y vuelve a la acción 0). Con +0x2C bit0 (rival id 7, contra): 0x1214C, secuencia 0x1AD–0x1B1 en la que el rival le da la vuelta, él a la acción 8 sub 1 (+0x3E=6, 0x16488, sonido 0x2F) y el rival a la acción 0xC sub 0x8010. Si no: los dos enfrentados, rival a la acción 0x10; poses 0x12324[id del rival*6]+paso, duraciones 0x12316. Paso 3: voz 0x1C, salto z+0x10, sonido 0x50, 1C183E, +0xF6+=3; vuelo 0x3DCE hasta el suelo (paso 4). Paso 6: temblor, sonido 0x34, rival a la acción 8 sub 5 pose 0x1CF, +0x3E=0xC, 0x161C8. Paso 7: acción 5 (x∓0x20). |
| 012354 | sub_llave_sumision | C | R | Llave de sumisión de varias fases: 1C185A=0xC0 y despacha +0x34 con la tabla 0x1238E. |
| 01239E | sumision_f0 | C | R | Poses 0x125D2[id del rival]+paso, 12 frames por paso; tras 3 pasos, fase 1, sonido 0x51, 1C183E bit7. |
| 012404 | sumision_f1_forcejeo | C | R | Cada botón del rival suma +0x5D; si supera la tabla 0x124D6[0x1CE9C], fase 2 (escapa). Si no: alterna poses cada 8 frames; cada ciclo, +0x3E=4 y 0x161C8 (daño). A los 6 ciclos se escapa. Con +0x3C (energía) a 0 y los dos del bando: fase 3 (rendición). |
| 0124DA | sumision_f2_escape | C | R | Retrocede los pasos; al acabar, él a la acción 8 sub 1 pose 0x15, el rival a la acción 0xD pose 0x18, 1C185A=0xC1. |
| 01255C | anim_objeto_id | C | R | Pose = tabla 0x125DA[id del rival] + +0x37; a los 2 pasos, 0x16210 y prioridades 1C0BC2/1C0BDA (0x40/0x80 según +0x18 bit4). |
| 0125F0 | sub_salto_codazo | C | R | Salto colocado con 0x156FA (tabla 0x12A7C, +0x10 si el rival es el id 7); la sub 0x35 lo deja fuera (+0x19=1). Al bajar, si el rival está tumbado en el mismo plano: 0x12A9C y, cerca del suelo (+8), impacto (rival acción 8 sub 0xD, +0x38+=8, +0x3E=0xC o 8 sub 0x35, 0x161C8; rebote +0x28=0x300, sonido 0x48, temblor, 0xC6CA). Tras el rebote intenta cubrir (dentro y del bando): acción 0x17 (+0x2C byte 0x20), rival 0xB, +0x18 bit5, 0x11BC6/0x129A4. Al fallar en el suelo: acción 8 sub 5 (0x25 id 4), +0x3E=4 y 0x16488 (humano), sonido 0x34. Poses de las tablas 0x12A52 (id 4) / 0x12A60 según la altura. |
| 0129A4 | cubrir_iniciar_cuenta | C | R | Al cubrir: si +0x33 bit1 → 0xC554 con el compañero. Si el cubierto tiene energía 0 (+0x3C) o el compañero no puede (CPU +0x106 bit1 / humano +0x107 bit0, 3/16 de probabilidad) → sin salvamento. Si el compañero humano no es CPU: 0xAF9A; si no CC, 0xC554 y +0xC6 del cubridor = 2/bit7 (aviso de salvar). CPU: 0x1B7FA del compañero y borra +0xC6. |
| 012A9C | kickout_salto_cpu | C | R | Solo una vez (+0x2C bit0): si el rival es CPU, la sub 0x35, está por debajo a menos de 0x30 y no está cubierto: tirada 0x450A contra la tabla 0x12B0C[0x1CE9C] → el rival rueda (acción 0x19). |
| 012B10 | sub_correr_cuerdas | C | R | Corre a la cuerda (dirección 0x40/0xC0 según x≥0x300, 0x1979C, poses 2+paso). Al llegar a 0x298/0x328 rebota (+0x5C=1). Si el rival no está tumbado, acción 0x14. Si no: velocidad de la tabla 0x95BC[id], vuelve corriendo y en 0x288/0x378 salta (acción 0xC sub 0x35). Poses 0xA+paso. |
| 012C9E | sub_voltereta_atras | C | R | Pose 0x17F+paso, duraciones 0x12D2C, velocidad 0x10 hacia atrás; 4 pasos y acción 0. Cuerdas con 0x12DB0. |
| 012D30 | sub_voltereta_adelante | C | R | Pose 0x14B+paso, duraciones 0x12DAC; 4 pasos. 0x12DB0. |
| 012DB0 | chk_cuerda_rebote | C | R | Dentro: si choca con la cuerda (0x21E5A) → acción 2 (+0xA8=2). Fuera: (0x21ED0) → acción 8 sub 3. |
| 012DEE | sub_golpe_encadenable | C | R | Pose 0x15F+paso (tabla 0x12E76), acumula +0xC8 en +0x5C. Al acabar: con +0x5D bit3 y el rival no en la acción 8, acción 0xC sub 0 (encadena); si no, acción 0. |
| 012E7A | sub_carrera_hombro | C | R | Embestida (tabla 0x1302E, velocidad 0x10). Si conecta (+0xC9 bit3 y el rival bit4 o −2) antes del paso 0x10: pose 0x1D2+id del rival, 8 frames, +0xC9 bit4, +0x35 bit0 (pasos extra), enfrentados; el id 1 suena 0x50. En el paso 0xC suelta: rival a la acción 8 sub 0x17. Choque con la cuerda: dentro → acción 2 (y el rival sub 2); fuera → acción 8 sub 3. Al final, el id 1 con impacto llama a 0x15B90. |
| 01304E | sub_salto_patada | C | R | Voz 5, +0x18 bit7, suelo +0xF4 = 0xBB (0x80 fuera), tabla 0x1310C. En vuelo (pasos <8): 0x3DCE y 0x1600C; si choca con la cuerda, acción 8 sub d0. Al llegar al suelo: pose 0x61, sonido 0x2D. Al acabar: acción 0. |
| 013114 | sub_dropkick | C | R | Tabla 0x132B8, velocidad 0x20 hacia delante (0 si él mismo es el id 4, Bossman). Para conectar antes del paso 4 hace falta +0xC9 bit3 y que el rival tenga +0xC9 bit4 o +0x40 = −2; entonces: pose 0x1DE+id del rival, enfrentados, +0xC9 bit4. En el paso 8 suelta: el rival a la acción 8 sub 0x10, z+0x30, pose 0x9B, +0x2C bit0 (y = la suya +3 si +3=4). Cuerdas (como 0x12E7A): dentro → acción 2 con +0xA8=2; fuera → acción 8 sub 3; el rival recibe lo mismo. Frena 2/frame. |
| 0132C8 | sub_bulldog_salto | C | R | Rival a la acción 0x10. Pose 0x23E+id del rival*5, duraciones 0x134CC. Paso 2: sonido 0x51, 1C183E. Paso 3: voz 4, salto +0x18 bit7, z+0x20. Vuelo (0x3DCE, 0x1600C); si choca con la cuerda, los dos a la acción 8 sub d0 con la misma velocidad. Primer contacto con el suelo: sonido 0x34, temblor, rebote. Segundo: +0x3E=0xB y 0x161EC; dentro y del bando → cubre (acción 0x17, rival +0x18 bit5, 0x11BC6/0x129A4); si no, acción 5. Rival tumbado (0xB) detrás a ±0x20 con pose 0x17; él pose 0x65. |
| 0134D2 | sub_slam | C | R | Agarra (0x14222) y pone al rival delante (−0x10). Poses 0x13956[id del rival*0x1E], duraciones 0x13938. Rival id 7: secuencia de contra (0x1C6–0x1C9) en la que el rival lo tira (él a la acción 8 sub 0 pose 0xF2, +0x3E=6, 0x16488, sonido 0x2F) y el rival vuelve a la acción 0 con +3=7. Con +0xFC (rival resiste): poses alternativas +0x12 y 0x145F2 en el paso 0xC. Normal: paso 2 se giran; paso 0xC sonido 0x50 (0x51 id 6), 1C183E, +0xF6+=3, voz 0xC, salto; paso 0x10 rival a la acción 8 sub 0x12 pose 0x16 (x desplazada por la tabla 0x13918), temblor y sonido 0x34; paso 0x12: +0x3E=0xC, 0x161EC, acción 5, 0x15B90. Al bajar (z<0xBB) +2 paso. |
| 0138CA | contra_llave | C | R | El rival pasa a la acción 0xC sub 3 (pose 0x105D0); él a la acción 8 sub 9; +0xC9 bit5. |
| 013A46 | llave_slam | C | R | Pose 0x1DD + 6*id del rival, voz 6. Paso 3: sonido 0x50, 1C183E bit7, +0xF6 += 3. Paso 4: al tocar el suelo, daño 0xC al rival (0x161EC), 1C1858=0x80, sonido 0x31. Paso 6: él a la acción 5, el rival a la acción 8 sub 0x21 pose 0x1CF a ±0x30. Con +0xFC≠0 (contra) usa las tablas 0x13C64/0x13C70[id del rival*0xC]; al llegar al paso 0xC → 0x138CA y daño 6 a sí mismo (+0x3E=6, 0x16488). El bloque de 0x13C24 (daño 7 al rival) es código muerto: solo se evalúa con paso <0xC. |
| 013CD0 | sub_golpes_repetidos | C | R | Rival enfrentado; poses de la tabla 0x13E44[id del rival*10], 4 frames por paso (0xD si el rival es el id 7 (André) y el paso +0x37 < 3, es decir, pasos 0 y 2). Con +0x5C bit7 (puesto por 0x13DF6) repite los pasos 0–2 y cuenta en +0x5D; con +0x5D=2 al empezar el paso 0 → 0x145F2. Paso 6: rival a la acción 8 sub 0xA pose 0x9B, +0x3E=6, 0x161FE, a ±0x30 y z+0x20. Paso 0xA: acción 0. |
| 013DF6 | cpu_id7_tirada | C | R | Si el rival es la CPU con id 7: tabla 0x13E40[energía] frente a rng&7 → +0x5C bit7. |
| 013E94 | sub_body_slam | C | R | Agarre: x−0x20 (salvo con +0x2C bit5, que entra en el paso 2 con 0x14204) y 0x14222; el rival delante (+0x10). +0x108 bit6 sin id 7 anula la resistencia +0xFC. Tablas de duración 0x14108 y de pose 0x14124[id del rival*0x1C] (+0x10 si resiste). Paso 6: sonido 0x50 (0x51 id ≥6), 1C183E, +0xF6+=3. Paso 8: salto y voz 0xD. Al caer: paso 0xC, sonido 0x34, temblor. Paso 0x10: él a la acción 5, rival a la acción 8 sub 0xE pose 0x1CF (−0x20), +0xAE=0, +0x3E=0xC, 0x161DA, 0x15B90. Si resiste: paso 0xC → 0x145F2. |
| 0140E8 | anim_a3a4 | C | R | Pose/tiempo de a3/a4[+0x36]. |
| 014204 | agarre_reposicion | C | R | Variante de 0x14222 con la tabla 0x14378 (0x143DC CPU) para entrar desde el paso 2; continúa en el cuerpo común en 0x1423E. |
| 014222 | llave_tirada_exito | C | R | Éxito de la llave: tabla 0x14346 (0x143AA la CPU) + (1C0029>>1&0xF)*0xA, +5 si el DIP 0x180002 bit3=0. Índice por la cuenta +0xDC/+0xDD (máx. 4), según si +0x31 está en la lista 0x14338. Si rng>>1&7 < tabla y ≥ la racha +0xCC/+0xCD (con el id 7 solo las subs 0x18/0x32), suma la racha y da +0xFC=0; si no, +0xFC=1 (falla y el rival contraataca). |
| 01440E | sub_backbreaker | C | R | Igual que el body slam con las tablas 0x1465E (duraciones) / 0x14676[id*0x18] (poses), x−0x20, el rival a +8. Paso 4: sonido 0x50, 1C183E, +0xF6+=3. Paso 8: sonido 0x31. Paso 0xA: rival a la acción 8 sub 0xF pose 0x15 a ±0x30, z+0x10, +0x3E=0xC, 0x161DA. Paso 0xC: acción 0 y 0x15B90. Si resiste (+0xFC, tablas +0xC): paso 0xC → 0x145F2. |
| 0145D2 | anim_paso_a3a4 | C | R | Duración (a4) y pose (a3) del paso +0x36. |
| 0145F2 | contra_llave_mutua | C | R | Pone al rival la pose de la tabla 0x1464E[id]. Los dos pasan a la acción 0xC sub 0x26 (+0xAE 1/0), uno frente al otro. |
| 014736 | sub_golpe_corto | C | R | Pose 0x183+id del rival*2, 0x10 frames; paso 1 sonido 0x31. Paso 2: él a la acción 0; rival a la acción 8 sub 1 pose 0x15 a +0x10/+0x14, +0x3E=0xC, 0x161DA. |
| 01481C | sub_sumision_b | C | R | Llave de sumisión: rival a la acción 0x10, sonido 0x51, 1C183E, 1C185A=0xC0. Con +0x114 del rival ≠0 a partir del paso 2, cada frame suma +0x35; si supera la tabla 0x124D6[0x1CE9C del rival], se escapa. Poses 0x149AA[id del rival]+paso, duraciones 0x149A2; cada ciclo (pasos 2–3) +0x3E=4 y 0x161C8 al rival, +0x5C++. Si los dos tienen +0x2A bit1 y el rival tiene +0x3C=0: 0x16210 (rendición) y el resultado en 1C0BC2/1C0BDA (0x40/0x80 según +0x18 bit4). Escape o 6 ciclos terminan igual (0x14950): el rival a la acción 8 sub 0x15 pose 0x16 encima (z+0x40), él con la sub 0x3A, 1C185A=0xC1. |
| 0149B0 | llave_B | C | R | Poses de la tabla 0x14A82[id del rival] (stride 0x14). Paso 2: sonido 0x51 y 1C183E bit7. Paso 4: sonido 0x31. Al final, el rival pasa a la acción 8 sub 0x15 (z+0x10) con daño 0xB (0x161FE), y 0x15B90. |
| 014AFA | llave_C_aerea | C | R | Tabla 0x14C5C[id del rival*0x14] (pose+duración .l). Paso 1: sonido 0x51 y 1C183E. Paso 3: el rival a la acción 8 sub 0x10 (x±0x50, z+0x30, pose 0x9B) con daño 0xA (0x161FE). Paso 4: salta (+0x18 bit7, z+0x10, velocidades a 0, +0x22=0x20) y al caer a 0xBB (0x80 fuera) pasa al paso 5 con pose 0x17 (0x10 frames) y x+0x10. Paso 6: acción 5 y 0x15B90. |
| 014CFC | sub_contraataque_llave | C | R | La ejecuta el que contraataca (llamada con a0 = el rival desde 0x152BC cuando 0x14222 falla): se gira, pose 0x20+id del rival*2 (+1 por paso), el rival colocado con la tabla 0x14DD0. Paso 4: el rival a la acción 0x15 sub 0, él pose 0x30, +0x1C=0 en los dos. Paso 6: acción 0 (+0x5C=0xD si es CPU). |
| 014DD6 | sub_forcejeo_presa | C | R | Forcejeo del agarre: +0x28=0x80 frames, +0xDE = tabla 0x150E0[id&7] (tiempo de la CPU). Poses 0x150F6[id del rival*6], duraciones 0x150F0, alternando. Si no es CPU, 0x14FEE (entrada del humano); la CPU, al agotar +0xDE, 0x1E432. Con +0xAF bit0 (le toca al otro): 0x14F00. Si 0x2786 da CS (ruptura): los dos a la acción 0. |
| 014F00 | presa_contra_humano | C | R | Si +0x114≠0, no es CPU, +0x2A bit1, dentro, y el rival está en el paso 2/4 de +0x37, una sola vez (+0x108 bit7): tirada 0x450A&7 en la tabla 0x14FD8 (solo si el rival es CPU y 1C0029 < 2) o 0x14FE0 (resto). Con 0xFF: sub de la tabla 0x14FE8[id], acción 0xC, rival a la 0x10 (sub 0x1E contra el id 7), la sub 0x21 retrocede 0x20, +0x2C bit5 y +0x108 bit6 (salvo con la sub 0x1E). |
| 014FEE | presa_entrada_humano | C | R | Humano con +0x28<0x70 y botón 1/2: sub de la tabla 0x15126[id*3 + botón−1], acción 0xC, rival a la 0x10, separación ±8/∓0x10. Con +0x28=0: 0x1507C para él o para el rival (+0xAF bit0). |
| 01507C | tag_relevo_o_llave | C | R | Si 1C0026&3 = 2: acción 0xD y el compañero (a3) a la acción 0 a x±0x30. Si no: acción 0xC sub 0x27, el rival a la 0x10. |
| 01513E | sub_presa_cabeza | C | R | Pose 0x82+id*3 alternando con las tablas 0xB46C[id del rival]/0xB468, 0x20 frames. Al acabar, 0x145F2 desde el rival y rival +0x2C bit6. Ruptura con 0x2786 → los dos a la acción 0. |
| 0151F8 | sub_empujon | C | R | Pose 0x150F6[id del rival*6], 7 frames; luego acción 0, 0x19D1A, 0x15288; el rival a la acción 0xD a ±0x34, con los límites del ring. |
| 015288 | cpu_tras_llave | C | R | Con la acción 0 y 0x1D0E2 (tabla 0x152A4) → +0x5C=0xF (tabla 0x1B40C[0xF] = 0x1B486: ir junto al compañero que cubre, para romper/proteger la cuenta; sin compañero cubriendo → 0). |
| 0152BC | llave_D_salto | C | R | 0x14222 (si falla, contraataque 0x14CFC). Poses 0x154BC/0x154AE, sonido 5. Paso 1: sonido 0x50, 1C183E y +0xF6+=3. En el aire cae a 0xBB; el primer bote (vz 0x300) da daño 0xC, sonido 0x34 y 1C1858=0x80. Al final, el rival a la acción 0xB (tumbado, pose 0x17) y él a la 5. |
| 01552C | sub_salto_voz2 | C | R | Salto con la tabla 0x155EA, voz 2, +0x18 bit7. Vuelo (0x3DCE, 0x1600C), cuerda → acción 8 sub d0; al llegar al suelo (0x155C0), paso 0xC; a 0x10, acción 0. |
| 0155C0 | aterrizar | C | R | Si cae (+0x28<0) y z ≤ d0: z=d0, paso 0xC y su pose. |
| 0155FA | sub_golpe_objeto | C | R | Golpe con el objeto: sonido 0x25 (0x26 con +0x5F). Tabla 0x156C8[+0x5E&3*0xC] (3 sin +0x5E bit6). Si conecta (+0xC9 bit3) despacha +0x5E&3 por la tabla 0x15692: 0 → 0xE76E (suelta el objeto), 1 → 0xE6E0 y +0x5F=2. |
| 01569E | golpe_obj_0 | C | R | 0xE76E. |
| 0156A6 | golpe_obj_1 | C | R | 0xE6E0 y +0x5F=2. |
| 0156B4 | soltar_portado | C | R | El portado (+0x60) pasa a +0x2C=3; borra +0x5E bit6. |
| 0156FA | salto_preparar | C | R | Copia el bloque a6 a 1C00B4 (0x108B0), destino +0x68, 0x15B40 → +0x14, 0x159AC (calcula velocidades). Orienta, pose (a2), +1=2, +0x18 bit7, +0xF4 = 0xBB/0x80. |
| 01578E | cpu_combo_id | C | R | CPU (vía 0x15758, tabla 0x1576E por id): golpes de la tabla 0x15860 (0x15878 si 0x1CD80 da CC y sin +0xF9 bit0), 4 bytes por paso. Termina al pasar del paso 0x18 (0xC para el id 7 André: combo más corto). En el paso 0x10 sigue solo si la entrada de la tabla +0x6E del rival (+0x6C) tiene +9≠8, /dx/<0x40 y /dy/<8; si no, termina. Al terminar: el id 7 con el rival en la acción 0xA pasa a la acción 0xC sub 8; el resto, acción 0. |
| 015890 | golpe_rapido | C | R | Golpe en pasos de 4 (tabla 0x15944, o 0x15960 para la CPU que pierde la tirada 0x1CD80, sin +0xF9 bit0). En el paso 0xC (índice 3): si el estado del rival tiene entrada ≠0 en la tabla 0x1597C, salta al paso 0x18 (remate); si no, termina. El paso 0x14 y el ≥0x20 terminan (acción 0). Es decir: golpe de 3 pasos, más 2 pasos de remate si el rival está en un estado de la tabla. |
| 0159AC | calc_trayectoria | C | R | Bloque 1C00B4: +0 dx, +2 dx contra el tumbado, +4 dy, +6 z extra, +8 vz, +0xA gravedad, +0xC/+0xE máximos de vx/vy, +0x10 objetivo (−1 = punto fijo +0x16/+0x18), +0x14 z de destino. Simula la parábola (+0x28 −= +0x22 cada frame, mínimo −0x800) hasta bajar a la z de destino, cuenta los frames y pone +0x24/+0x26 = distancia·256/frames, limitado. |
| 015B40 | z_destino_salto | C | R | Tabla 0x15B70[zona propia*8 + zona del rival*2]. |
| 015B90 | cpu_provocar | C | R | Dentro y CPU: si 0x1CEF4≠0 y la tirada 0x450A&0xF < tabla 0x15BE4[id] → acción 0x12 (burla). |
| 015BEC | llave_E_secuencia | C | R | Llave por fases (+0x36/+0x37) con las tablas 0x15E7A/0x15EB2/0x15EE2/0x15F12, de stride 8 por id del rival. En la fase 2: sonido 0x50, 1C183E y +0xF6+=3. En la fase 8 lanza al rival (acción 8 sub 0xA, daño 0xD, z+0x40). Duraciones con rng&7. Si falla 0x14222 (o el rival es el id 7), termina en la contra mutua 0x145F2. |
| 015CC8 | warrior_33 | C(A) | A | Movimiento 0x33 de Warrior (vueltas, ver NOTES). |
| 015F1A | sub_rival_lanzado_id | C | R | Se coloca en el rival (x, y; la copia de z es un no-op: move $14(a1),$14(a1)), pose 0x209 y la tabla 0x15FFC cada 0xC frames. Paso 0xC: rival a la acción 8 sub 9 pose 0x9B, +0x3E=6, 0x161C8, a ±0x1E y z+0x10. Paso ≥0xE: acción 0, pose 0x1A, x+0x15. |
| 01600C | chk_cuerda_d0 | C | R | d0 = 0 sin choque, 2 = cuerda dentro, 3 = valla fuera. |
| 01603E | sub_esperar_tumbado | C | R | Pose 0; si el rival está tumbado, acción 0. |
| 016062 | sub_entrar_ring | C | R | Si el rival está dentro: +0x19=0, pose 0x105, avanza la tabla 0x160CC[id], 8 frames; luego acción 0 con +0x19=3 (delantal). |
| 0160D4 | sub_carrera_hacia_rival | C | R | Con +0x2C bit4 → 0x10A5E. Si no, corre (0x911E, 0x9202, 0x1617C, 0x1979C, 0x924A, 0x3DCE). Con la cuerda → acción 0xC sub 0x11. A una distancia de 0x50–0x5C delante del rival: si está tumbado → +0x2C bit4 (salto); si no, acción 0. |
| 01617C | dir_hacia_rival | C | R | +0x1E = 0x40 / (orientación del rival invertida); la invierte si está a ≥0x5C delante. |
| 0161C8 | danio_a1 | C | R | 0x16488 sobre a1. |
| 0161DA | danio_a2 | C | R | 0x16488 sobre a2. |
| 0161EC | danio_a3 | C | R | 0x16488 sobre a3. |
| 0161FE | danio_a4 | C | R | 0x16488 sobre a4. |
| 016210 | rendicion | C | R | Muestra el cartel fg0 1 (0x2660E con d0=1). |
| 01621A | temblor_pantalla | C | R | 1C1858 bit7 activa el temblor: 9 frames (3 si bit0, es decir 0x81 = corto). Suma la tabla 0x16286[frame] a 1C002E (scroll vertical); al acabar, borra 1C1858. |
| 0162A0 | procesar_impacto | C | R | Recibe el golpe (0x16340 filtra; +0xC9 bit0 = golpeado). +0x40 = reacción pendiente: 0xFFFE → 0x16468, acción 0x10 (agarrado), +0xC9 bit4. Agarre mutuo con la acción 0xC sub 0x14 → el otro +0x40=−1. Si no: 0x16468, 0x1638E (daño extra), acción = +0x40 (la 9 si el golpe es la sub 1 y está fuera), 0x16488 (aplica el daño), 0x16538. +0x46 temporiza el combo +0x48. |
| 016340 | filtro_impacto | C | R | Tabla 0x1636C[acción]: 0 = acepta; negativo = ignora el golpe; positivo = ignora solo con sub ≠0 (+0x31). |
| 01638E | danio_extra_tumbado | C | R | Si la víctima está en la acción 1/0x15/0x16: +0x3E += tabla 0x1642A[sub del atacante]&0x7F. Reacción 9/0xA (salvo con las subs 0x14/0x28/0x15) → 8; con el atacante en el estado 7, sub 0x23, y si no, +0x45=1. Con +0xF9 bit0 del atacante, daño ×2. |
| 016468 | soltar_si_tumbado | C | R | Acción 1/0x15/0x16 → 0x8EEA. |
| 016488 | aplicar_danio | C | R | +0x3C −= +0x3E (mínimo 0; si ya es 0 no cambia). Sonido 0x22 (0x23 si el banco gráfico +2 del atacante es ≥6: DiBiase y André) salvo con las subs 0/1. Con la tabla 0x164FA[sub] = 0xFF (o la víctima id 7 André con la sub 0x1F) → +0xF0 bit7 (golpe fuerte). |
| 016538 | limpia_f0_por_estado | C | R | Si la tabla 0x1655C[estado] es 0, borra +0xF0 bit7. |
| 01657E | colisiones_bucle | C | R | Bucle de colisiones: limpia +0x40 de los 4 luchadores; recorre las 6 parejas (0x165B2), 0x165FE, si están cerca (0x16634): 0x16716 (cajas) y 0x1675C (impactos en ambos sentidos). |
| 0165B2 | siguiente_pareja | C | R | Parejas (i<j) de la lista 0xEA4C (4 luchadores); CS al acabar. |
| 0165FE | reset_mascara_golpe | C | R | Si cambió la pose (+6 &0x3FFF vs +0x42): +0xCE=0 (máscara de a quién ha golpeado ya). |
| 016634 | pareja_cerca | C | R | CC si /dx/<0x60, /dy/<8, ninguno en la acción 0x10, ni la 0x1F sub 1, sin +0x2A bit2, los dos con +0x2C bit7 y sin bit6, pose ≠ −1, 0x166FC sin ruptura, los dos con +0x19<2 e iguales. |
| 0166FC | chk_ruptura_pareja | C | R | 0x2786 para los dos. |
| 016716 | cajas_pareja | C | R | a1/a4: cajas de golpe de los dos (0x1672C). |
| 01672C | caja_de_pose | C | R | Tabla 0x1761E[pose&0x3FFF] → la lista de frames [+2]; pose −1 → 0x18076. |
| 01675C | impactos_pareja | C | R | En los dos sentidos: 0x16796 (golpe); CC → 0x16CF4 (sonido/combo); CS → 0x172AA, que repite si sigue dando CS (cajas múltiples, +0xCA). |
| 016796 | chk_golpe | C | R | Ninguno con +0xC9 bit4/5 ni +0x40 −1/−2/−4, los dos activos, el atacante con prioridad (a1+0) ≥ la defensa (a3+0; 0x20 con 0x1688E), 0x16D9C (no le ha golpeado ya), cajas no nulas (0x18BF2/0x18AFE), solapamiento en x (0x16C60) y z (0x16CA8), golpe ≠ 0x18C72, tabla 0x172FA[pose de la víctima] ≠ 0xFF. Entonces (0x168B6): reacción y sub de la tabla de golpes (+2 si miran al mismo lado, es decir, la víctima de espaldas; +0xC8 bit1 = 1 si están de frente, 0 si de espaldas), +0xC9 bit3 al atacante, ajustes 0x169C2/0x16AA0/0x16BD2/0x16C04/0x16C14/0x16AD4/0x16B2A, 0x16B6A (contra). Con −4: 0x17136; con −2 (agarre): los dos enlazados (+0x68), 0x17228/0x17240 y el objeto del agarrado a la acción 4. Daño = a1+1 en +0x3E (0 a la CPU con las subs 0/1). +0xC0 bit0 = lado, +0xC9 bit0, 0x16DD2. Si falla: 0x16E48/0x16FAA/0x16DF8 (choque cuerpo a cuerpo). |
| 01688E | prioridad_defensa | C | R | Si la víctima tiene la sub 3 y el atacante la 0/1/8: d0=0x20. (Tras el rts, en 0x168B6, sigue el cuerpo de 0x16796.) |
| 0169C2 | ajuste_reaccion_id7 | C | R | Víctima id 7 (André) en las poses 0x18/0x19, o cualquier víctima con la reacción 0xF2 → 8. Reacción 0xF1 → 0xA (9 para André). Reacción 8 contra André: si el atacante está tumbado (acción 1/0x15/0x16) y no tiene la sub 0x20, el atacante pasa a la acción 8 sub 1 y André a 9; con las subs 0x2A/0x16/0x20/0x17/0x12/0xD del atacante → 0xA si su +0x44=1, si no 9; resto sin cambios. |
| 016AA0 | ajuste_sub15_cpu | C | R | Sub 0x15 contra el estado 7 con dificultad ≥2 → reacción 0xA, +0x48=0. |
| 016AD4 | ajuste_id7_accionC0 | C | R | Id 7 en la acción 0xC sub 0: víctima con +1=2 o la acción de la lista 0x16B20 → 8; si no, 0xA. |
| 016B2A | ajuste_id7_accionC8 | C | R | Id 7, acción 0xC sub 8: con +1=2 → 8; con la acción 0/9 → 0xA. |
| 016B6A | chk_choque_golpes | C | R | Reacción con sub 9: si la acción de la víctima está en la lista 0x16BCC (o la 0xC con la sub 0xE/0x14), se anulan (los dos 4 frames, enlazados, +0xC9 bit5) y devuelve CS. Si no, CC (sigue). |
| 016BD2 | ajuste_F0 | C | R | Reacción 0xF0 → 8; el atacante +0x116=0, +0x22=0, +8+=0xC (el id 4 avanza el paso +4). |
| 016C04 | ajuste_sub20 | C | R | Sub 0x20 → +0x44 de la víctima 0x23. |
| 016C14 | ajuste_sub31_id7 | C | R | Sub 0x31 contra el id 7 (no tumbado ni en las poses 0x18/0x19): el atacante a la acción 8 sub 1, la víctima a la reacción 9. |
| 016C60 | solape_x | C | R | Solapamiento de cajas en x (caja: +0 offset, +1 ancho). |
| 016CA8 | solape_z | C | R | Solapamiento en z (+2 offset, +3 alto). |
| 016CDE | x_caja | C | R | x de la caja según la orientación. |
| 016CF4 | sonido_y_combo | C | R | Acción 1 → sonido 0x48. Acción 0xC: sonido de la tabla 0x175CE[sub] (0x30 para el id 1 con la sub 0); combo de la víctima +0x48 += tabla 0x17590[sub] (+0x46=0x30); si la víctima es CPU dentro y el atacante no tiene +0xF8 bit7 ni +0xF9 bit0, también +0xF6. |
| 016D92 | acumular_mareo | C(A) | A | Suma daño a +0xF6 (medidor de mareo); ver NOTES s66. |
| 016D9C | chk_ya_golpeado | C | R | CS si el bit de la víctima (0x8000>>índice en 0xEA4C) está en +0xCE. |
| 016DD2 | marcar_golpeado | C | R | Pone ese bit en +0xCE. |
| 016DF8 | chk_choque_cuerpos | C | R | Acción 0/9 de los dos, 0x16E7E y 0x16F12 → los dos a la acción 0x11 (choque), se borra +0xC9 bit0, 0x170BA/0x170F0. |
| 016E48 | chk_bandos_opuestos | C | R | CC si a0 y a2 son de equipos distintos (1C0100/1C021A frente a ≥1C0334). |
| 016E7E | chk_choque_validable | C | R | CC si son de bandos distintos (+0x2A bit12), ninguno lleva objeto (+0x5E bit6), están en la misma zona +0x19 (si los dos están fuera, +0x19=1, además deben tener el mismo +0x2A bit1) y la acción de a2 lo permite según la tabla 0x1760C (<0x10; negativo = no, 0 = sí, positivo = solo con la sub 0/1 de a2; la acción 0x1F vale salvo con la sub 1 del atacante). |
| 016F12 | chk_cuerpos_cerca | C | R | CC si /dx/<0x20 (<0x28 entre dos id 7) y /dy/<0x10. |
| 016F58 | centrar_pareja | C | R | Coloca a los dos en el punto medio (x, y) y en orientaciones opuestas. |
| 016FAA | chk_agarre_carrera | C | R | El atacante en la acción 0 y la víctima corriendo (0xD) o rebotando (0xA) de frente: él pasa a la acción 0xC (+0x2C bit5) con la sub de la tabla 0x170B2[id] (0x1E contra el id 7), y la víctima a la 0x10. Fuera, o CPU en frames alternos (1C0046 bit1): sub 0x1E sin bit5. Id 6 con dificultad <2: sub 0x13. Enlaza (0x170F0). |
| 0170BA | soltar_objetos | C | R | Si llevan objeto (+0x5E bit6), lo sueltan (objeto +0x60 a la acción 4). |
| 0170F0 | enlazar_pareja | C | R | Cada uno pasa a tener al otro como rival (+0x68) y su índice +0x6C dentro del equipo contrario (lista 0xEA4C; +8 con +0x2A bit4). |
| 017106 | enlazar_uno | C | R | +0x68 = a4 y +0x6C = el índice de a4 en su equipo. |
| 017136 | reaccion_especial_m4 | C | R | Reacción −4 (contraataque) según +0x44 de la víctima, por la tabla 0x1715C: 0 suelta al agarrador (acción 0), la víctima a la 8; 1/2 → +0x40 −1; 3 los dos a la acción 8 sub 1; 4 suelta, la víctima a la 8 sub 1. El atacante +0x32 bit3. Daño +1 y 0x16488. CS. |
| 017168 | reac_m4_0 | C | R | Ver 0x17136. |
| 017198 | reac_m4_1 | C | R | Ver 0x17136. |
| 0171A2 | reac_m4_2 | C | R | Ver 0x17136. |
| 0171AA | reac_m4_3 | C | R | Ver 0x17136. |
| 0171D6 | reac_m4_4 | C | R | Ver 0x17136. |
| 017228 | ajuste_agarre_sub15 | C | R | Sub 0x15 en el paso ≥4 → paso 0. |
| 017240 | ajuste_agarre_id7 | C | R | Solo con las subs 0x14/0x28 (con otras sale sin hacer nada). Sub 0x28 con paso ≥2 → paso 0 (la 0x14 no reinicia). Si la víctima tiene el estado +3 = 7: tirada 0x450A&7 contra la tabla 0x172A6[dificultad 0x1CE9C del atacante]; si la tirada supera el valor, el atacante va a la acción 8 sub 1 y la víctima a la reacción 9 (se borra +0xC9 bit0 del atacante). |
| 0172AA | chk_pose_lista | C | R | Si +0xCA=0 y la pose del rival (+6 de a2) está en la lista 0x172DE: +0xCA=1 y CS. |
| 018E70 | cpu_ia_entrada | P(A) | A | Entrada a la IA de CPU (desde acción 00 y otros). |
| 018ECE | ia_principal | C | R | IA de la CPU: decrementa +0xF3; 0x1CCE8 puede abortar. Salvo con +0x5D=9/0xA/0xD, borra +0xB0 y elige la intención (0x1D1A8). Salta por +0x5C a la tabla 0x18F16. |
| 018F56 | ia_sub0 | C | R | Si 0x1D04C da CS → +0x5C=0xB. Si no, 0x19012 y 0x1907C, y despacha según la acción del rival por la tabla 0x18F92. |
| 019012 | cpu_pedir_relevo | C | R | CPU de equipo sin 1C00F2 ni +0xF9 bit0, rival no corriendo, compañero en el delantal (no en 0x13): si la dificultad < +0xDA y el compañero tiene ≥ energía → +0x5C=6 y compañero +0x5C=5 (relevo). |
| 01907C | cpu_rival_fuera | C | R | Rival fuera (+0x19=1): tirada (0x450A>>1)&0xF; con <8 consulta 0x1AE98, y si no da CS (o la tirada ≥8) → +0x5C=3 y compañero +0xC4=0x10. Si no: el id 7 (André) → +0x5C=4 (compañero +0xC4=0x7FFF); rival en la acción 8 → nada; rival tumbado (0xB, ya iniciado) → tabla 0x19132[rng&0xF]: 0 → +0x5C=4, 1 → +0x5C=2 (rival +0x38+=0x80, +0x34−=0x14), otro → acción 0xC sub 0x3B; resto → +0x5C=4. |
| 019142 | cpu_est_0 | C | R | Pose actual. |
| 01914A | cpu_est_andar | C | R | 0x19248, 0x19160, 0x196F8 (andar hacia el rival), límites, 0x1BE9C. |
| 019160 | cpu_decidir_correr | C | R | CPU con +0x2A bit1 sin cooldown (+0xA8 bit7), /dy/<8: según dx (≥0xE0/≥0xA0/≥0x60/≥0x40; <0x40 nunca) tabla 0x19228[banda*8+id&7] contra rng&0xF; si sale → acción 1 (carrera), salvo contra el rival tumbado (0xB): solo corre si miran al mismo lado y dx ≥0xA0. Cooldown +0xA8=0x809C (0x9C frames en +0xA9). El filtro de bits 8–9 (move.b + andi.w #$300) siempre da 0: no tiene efecto. |
| 019248 | cpu_elegir_paso | C | R | Si /dy/ ≥ 8: +0x34 = 0/1/2 aleatorio, +0x5C=0xE. |
| 01928A | cpu_lanzar_ataque | C | R | Con el ataque preparado (+0x2E bit7), sin ruptura y en la misma zona: si /dy/<0xC y 0x10 ≤ dx ≤ tabla 0x19310[id] → acción 0xC con la sub +0x2E (sub 4: el rival a la acción 0x10). |
| 019318 | cpu_est_andar2 | C | R | = 0x1914A. |
| 01931C | cpu_est_elegir | C | R | Rival activo: 0x19422 (¿subir al poste?) o 0x1935C (elige el ataque); si elige: +0x5C=0, +0x5D=+0xD9. Si no, anda. |
| 01935C | cpu_elegir_ataque | C | R | Rival dentro. Bando contra bando: rival con 0 de energía → +0x2E=0x8006; si no, 0x19406. Fuera de bando: subs 6/9 → 4. +0xD9 = tabla 0x193D6[+0x2E&0x3F] (5 por defecto), +0xD8 bit7. |
| 019406 | cpu_ataque_tras_golpe | C | R | Si +0xE2 bit0 y 0x1CEF4 del rival ≠0: +0x2E=0x8004. |
| 019422 | cpu_decidir_poste | C | R | Rival dentro, no el id 7, rival sin +0x104 y en la zona de la tabla 0x19528 (0x194B8), con energía, 0x1CEF4≠2, él en la zona (0x194F8) y tirada < tabla 0x19548[id]: +0xD9=2 (poste), rival +0x38+=0x80, +0x34−=0x14. |
| 0194B8 | chk_zona_rect_adelantado | C | R | Rectángulo de la tabla a2[(zona+0x18 bits8-9)>>5] con x adelantada ±0x30; CC si dentro. |
| 0194F8 | chk_zona_rect | C | R | Igual sin adelanto. |
| 019550 | cpu_est_combate | C | R | 0x1956A (esquivar), 0x19160, 0x196F8, límites, 0x1928A. |
| 01956A | cpu_esquivar | C | R | Una vez (+0xE2 bit4): rival atacando (0xC) cerca (dx<0x60, 0x38 con la sub 2; dy<8), de frente, con una sub de la lista 0x19644: tirada contra la tabla 0x19656[1C0028 y dificultad] (0x1966A para el id 7) → +0xF1 = la respuesta de la lista y acción 5 (agacharse/esquivar); tumbado: +0xF0 bit0 y 0x8EEA. |
| 01966E | cpu_est_seguir | C | R | 0x196F8, límites, 0x1BE9C. |
| 01967E | cpu_est_seguir2 | C | R | = 0x1966E. |
| 01968E | cpu_est_esperar_cerca | C | R | Cerca (dx<0x60, dy<0x50): se para mirando; si no, se acerca. |
| 0196C2 | cpu_est_ir_punto | C | R | Va al punto de la tabla 0x196F4 (0x1CF50). |
| 0196F8 | cpu_andar_hacia_rival | C | R | Si /dx/<5 y /dy/<5: solo se mueve (dirección 0) si el rival está tumbado (0xB) sin el bit6 de la entrada; en otro caso no hace nada. Si no: banda 0 (/dy/<4), 1 (dx<0x30), 3 (0x30–0x4F) o 2 (≥0x50); dirección = tabla 0x1977C[banda*8 + octante (bits 14–15 de la entrada)*2]. Luego 0x1979C, 0x924A, 0x3DCE. |
| 01979C | velocidad_por_dir | C | R | +0x21 = tabla 0x933E[id][dirección>>5 + 1] (velocidad por luchador). |
| 0197C4 | cpu_est_ir_tabla | C | R | Va al punto de la tabla 0x19808[índice +1 del rival] (0x1CFD8). |
| 019818 | cpu_comp_rodear | C | R | Rodea al rival (0x198B6 comprueba el poste 0x1A820) por el lado según la orientación; 0x198C6 o se acerca; con el rival corriendo sigue (si no, +0x5C=0). |
| 0198A2 | cpu_fin_si_no_corre | C | R | Rival ≠0xD → +0x5C=0. |
| 0198B6 | cpu_chk_poste | C | R | 0x1A7CE con la tabla 0x1A820 y la altura 0xBB. |
| 0198C6 | cpu_rodear_paso | C | R | Dirección de la tabla 0x19954[lado+zona], se aparta si dy≥0x10; +0xEA bit7 alterna el lado. |
| 019958 | cpu_ir_a_poste | C | R | Con el objetivo en las acciones 0xB/0xD/0xE: se orienta (+0xA, +0x18 bit6) y va al poste de la tabla 0x199FA; al llegar → acción 0xF (subir), +0xB8=0. 0xF81A sin CS → +0x5C=0. |
| 019A0A | cpu_ir_cuerda_rival_fuera | C | R | Rival fuera: va a la línea x=0x2D0/0x330 (o y=0x120 según +0x18 bit4) del lado del rival y se alinea. |
| 019AD4 | cpu_perseguir_fuera | C | R | Rival fuera: 0x19B8E calcula el punto de salida; con +0x32 bit6 espera la entrada 0x1A22C. Al llegar a la cuerda (+0x9F) con 0x1A25C: acción 3 (salir por las cuerdas), +0xAC = 0/1/2 según la cuerda (el id 7 se coloca en x 0x2A5/0x345). +0x5C=0. |
| 019B8E | cpu_punto_salida | C | R | Punto de salida (+0x24/+0x26) hacia el rival, limitado a x 0x280–0x380 o y 0x108–0x150 (tabla 0x19C20, 0x1D032); el id 7 usa unos puntos fijos. 0x1CFD8 da la dirección. |
| 019C28 | cpu_rodear_tumbado | C | R | Rival en la misma zona, tumbado/aturdido (0xB/8/5): elige un lado (+0x22 bit6) y va al punto de la tabla 0x19D12; si el rival corre (0xD), 0x19D1A o 0x19D5C según la distancia. Si no, +0x5C=0. |
| 019D1A | cpu_reaccion_carrera | C | R | Rival dentro en la zona 0x19D44 (0x1D0E2): +0x5C=1; si no, 0xF. |
| 019D5C | cpu_reaccion_carrera2 | C | R | Rival dentro en la zona 0x19D7E → acción 1 (carrera). |
| 019D96 | cpu_ir_relevo | C | R | Va a la esquina (tabla 0x19E32 por equipo). Al llegar, con el compañero en la acción 0, +0x5D=5 y +0xE2 bit3: los dos a la acción 0x1A (relevo) con +0x2A bit2; +0xDB = dificultad. La comprobación «compañero ya en 0x13 → +0x5C=0» usa movea.w $A4 (lee solo la palabra alta del puntero, a1=0x1C) y mira el byte de ROM 0x49, que vale 0: nunca se cumple (fallo del original). |
| 019E3A | cpu_volver_delantal | C | R | Va a su esquina (tabla 0x19ED6); al llegar, 0x1A25C / 0x1A22C → acción 6 (subir al delantal), +0x2A bit7=0. 0x1B3E4: si termina → acción 0 y, para el humano en modo 1C0026 bit0=0, +0xF2 bit7. |
| 019EDE | cpu_seguir_si_rebota | C | R | Rival dentro rebotando (0xA) o corriendo (0xD): le sigue; si no, +0x5C=0. |
| 019F0A | cpu_ir_a_tumbado | C | R | Rival dentro tumbado: va al punto fijo 0x19FE8 (0x19F92 siempre devuelve ese, ver 0x19F92). Al llegar: si el rival tiene +0x38 ≥0x10, acción 0xC con la sub +0x2F (sub 4 → el rival a la acción 0x10); si no, +0x5C=0. Si el rival deja de estar tumbado o dentro, +0x5C=0 (pero termina el frame). |
| 019F92 | cpu_punto_ataque | C | R | Lista 0x19FD6 (sub → índice) — el resultado se pisa: siempre devuelve 0x19FE8 (código muerto: el adda se sobrescribe). |
| 01A008 | cpu_nada | C | R | rts. |
| 01A00A | cpu_ir_centro | C | R | 0x1D04C; va al punto 0x1A056/0x1A05A según la y del rival (≥0x138). |
| 01A05E | cpu_dar_vueltas | C | R | Durante +0x24 frames (0x20; 0x10 fuera) y un número de pasos de la tabla 0x1A15E[1C0028&0xF]: se aleja del rival (dirección opuesta). Al chocar o acabar el tiempo: en equipo, en la zona 0x1A168 y con el compañero en el delantal → relevo (+0x5C=6/5). El id 6 usa otra animación (0x1A1C8). |
| 01A170 | anim_andar | C | R | Animación de andar: sin objeto, ciclo de 4 pasos de la tabla 0x93AE (+8 con +0x18 bit6). Con objeto: 0x924A. |
| 01A1C8 | anim_andar_id6 | C | R | Ciclo de 4 pasos de la tabla 0x1A20C. |
| 01A22C | chk_entrada_cuerda_lado | C | R | Entrada 1C1894/1C1896 (según +0x18 bit0) &3; sin pulsar borra +0x32 bit0, pulsada → CS. |
| 01A25C | chk_puede_cruzar | C | R | CS si la entrada del lado (1C1894/1C1896 &3) está activa, salvo en la zona 1 con +0x18 bit4. |
| 01A29A | cpu_esperar_levante | C | R | Rival tumbado/levantándose (1/2/0x15). Elige el ataque (0x1A33E); en la zona de la tabla 0x1A336 y con 0xA39A → +0x22 bit7 (desde el poste). Con +0x2E bit6: si está en el poste, cuenta +0x23 y salta (acción 0x16); si no, con el rival en 0x15 de espaldas → carrera (acción 1). |
| 01A33E | cpu_elegir_sub | C | R | Sub del ataque (+0x2F) de la tabla 0x1E8FC[posición x(0–2)*0xC0 + 0x1CEF4 del rival*0x40 + id*8 + tirada&7]. Fuera de bando: la sub 0xB → 0x1C. Bit7 de la sub → +0x2E bit6 (desde el poste). +0x2E bit7 = preparado. |
| 01A3EC | cpu_ir_poste_rival | C | R | Rival dentro: va al poste de la tabla 0x1A48C[+0x34&3]; al llegar, con el rival en la acción 0 a dx 0x20–0x40 y en la zona 0x1A49C → acción 0x16 (salto del poste). |
| 01A4B4 | cpu_entrar_ring | C | R | Rival dentro: va al punto de la tabla 0x1A512[id]; al llegar → acción 1. +0x5C=0. |
| 01A532 | ia_sub_5d | C | R | Despacha por +0x5D&0xF (<8) con la tabla 0x1A554. |
| 01A574 | cpu_fuera_principal | C | R | Fuera del ring: 0x1CDA4, 0x1A6B6 (objeto), 0x1AE44 (cuenta fuera). Con +0x5A bit7 (cuenta alta): con +0x5B=2 → acción 0x1C; si no, +0x5C=2 (3 en equipo) para volver. Si no: se orienta al rival; en el mismo lado: 0x1D04C → +0x5C=6, o ataca (0x1AF58; tumbado → 0x1A674), o anda. Si en otro lado: rodea el ring (0x1A742/0x1A772/0x1A79E). |
| 01A674 | cpu_atacar_fuera | C | R | Sin objeto: 0x1AF70 elige +0x2E; ≠0 → acción 0xC con esa sub (4 → el rival a 0x10). Con objeto: +0x5C=6. |
| 01A6B6 | cpu_buscar_objeto | C | R | Id <6, fuera de los modos 4/9 de 1C0029, con un objeto asignado (+0x5E bit7, +0x60) libre: si está más cerca del objeto (+0x64/+0x66) que del rival → +0x5C=5 (coger el objeto); si no, +0x5C=0. |
| 01A742 | dir_rodear_x | C | R | Dirección para rodear el ring por x (0x3E0/0x210 según el lado). |
| 01A772 | dir_rodear_y | C | R | Dirección por y (0xC0). |
| 01A79E | dir_rodear_x2 | C | R | Como 0x1A742, con el lado del rival. |
| 01A7CE | chk_rival_en_trapecio | C | R | CC si el rival está dentro del trapecio de la tabla a2 (y por debajo de d4, los bordes x se abren 1/6 por y). |
| 01A830 | cpu_volver_ring | C | R | Va a la cuerda (0x1A926 o 0x1A9C2 según el equipo +0x2A bit4) y, al llegar mirando a 0x40/0xC0 en su lado, con 0x1A25C → acción 4 (entrar), +0xAC=3/4. Si el compañero está fuera y el rival dentro → +0x5C=0. |
| 01A926 | dir_cuerda_eq0 | C | R | Dirección hacia la cuerda (x 0x210/0x3E0, y 0x160/0xC0 según +0x18). |
| 01A9C2 | dir_cuerda_eq1 | C | R | Ídem para el otro equipo. |
| 01AA5E | cpu_entrar_por_lado | C | R | Va a la línea de entrada (0x1AB0C/0x1AB34) y, al llegar con la entrada 0x1A25C, acción 4 con +0xAC 0/1/2. |
| 01AB0C | dir_entrada_y | C | R | Por y 0x130/0x180. |
| 01AB34 | dir_entrada_x | C | R | Por x 0x280/0x380; el id 7 en x 0x2A5/0x345 (se ajusta a menos de 5). |
| 01AB92 | cpu_coger_objeto | C | R | Máquina de +0xE6 (tabla 0x1ABCA): 0 ir a la mesa, 1 bajar a y<0x30 y coger el objeto, 2 volver. |
| 01ABDA | obj_ir_mesa | C | R | Hacia y 0xC8 y x 0x200/0x400; al llegar, +0xE6++. |
| 01AC22 | obj_bajar | C | R | Hacia y<0x30; coge el objeto (0x1AC42), +0xE6++. |
| 01AC42 | crear_objeto_en_mano | C | R | 1C1823 /= +0xE7. Objeto 0xEA60/0xEA64 (según +0xE7 bit0): +0x5F = tipo, +0x5E bit6, +0x60. El objeto: activo (0x8000), pose 0xF/8, sprite 0x17, en la posición del luchador, acción 1, dueño +0x60, +0x1A=0x8070. |
| 01ACE2 | obj_volver | C | R | Hacia y ≥0xC8 → +0x5C=0. |
| 01AD02 | cpu_ir_a_por_objeto | C | R | Fuera del ring, yendo a por el objeto asignado (+0x60): 0x1A6B6 y 0x1AE44 como 0x1A574 (con cuenta alta: +0x5B=2 → acción 0x1C; si no, +0x5C=2/3). Si está en el mismo lado que el objeto: 0x1AF58, 0x1AE3C (0xE462, intenta recogerlo) y 0x1ADD2 (se acerca); si no, rodea el ring (0x1A742/0x1A772/0x1A79E). |
| 01ADD2 | cpu_ir_al_objeto | C | R | Dirección de la tabla 0x1977C según la distancia (+0x64/+0x66) y el cuadrante respecto al objeto. |
| 01AE3C | cpu_recoger_objeto | C | R | 0xE462 (recoger_objeto). |
| 01AE44 | cpu_chk_cuenta_fuera | C | R | Fuera de la zona 1 → +0x5A=0. En la zona 1: si ninguno de los dos rivales (+0x6E/+0x7E) está en la zona 1 → volver (+0x5A=0x8001; 0x8002 con objeto). Si alguno lo está: sin +0x2A bit1, vuelve salvo que el compañero (+0xA4) esté también fuera (+0x19=1 → +0x5A=0); con +0x2A bit1, vuelve si la cuenta 1C0596 ≥ la tabla 0x1AED4[id] (0x1AE98) y, si no, +0x5A=0. |
| 01AE98 | chk_cuenta_vs_id | C | R | CC/CS: la cuenta fuera del árbitro 1C0596 contra el límite de la tabla 0x1AED4[id]. |
| 01AEE4 | cpu_fuera_ir_tumbado | C | R | Rival en la misma zona tumbado/aturdido/corriendo: va al punto 0x1AF50/0x1AF54; si no, +0x5C=0. |
| 01AF58 | cpu_planificar | C | R | Rival no tumbado → 0x1D1A8 (elige el ataque); tumbado → +0x2E=0. |
| 01AF70 | ia_elige_movimiento | C | R | 0x1E7DA(d1=2) → tabla 0x1AFA8[d0][id]; +0x2F = una de sus 8 entradas elegida con rng&7. |
| 01B010 | cpu_subir_poste | C | R | Acción 0xF, +0xB8=2. |
| 01B01E | cpu_delantal_espera | C | R | Con +0xC6 bit7 → +0x5C=0; luego 0x1BC3E. |
| 01B034 | cpu_delantal_disp | C | R | Despacha +0x5C&7 (<5) por la tabla 0x1B04E; si no, 0x1B06C y los límites. |
| 01B062 | cpu_delantal_def | C | R | 0x1B06C y los límites. |
| 01B06C | cpu_delantal_seguir | C | R | Compañero fuera → +0x5C=4; si no, 0x1B120 y se mueve. |
| 01B084 | cpu_seguir_objetivo8e | C | R | Se mueve hacia el objetivo +0x8E/+0x90/+0x92 (tabla 0x1977C); cerca (+0x92<8) con +0xF2 bit7 → acción 1 (dentro) o 0x15 (fuera). |
| 01B0FE | cpu_atacar_def | C | R | +0x2E=0x8005 y anda; 0x1BEE4 con la tabla 0x1BEB6. |
| 01B120 | cpu_chk_objetivo_cerca | C | R | Solo si la zona del objetivo (+0x8E&3) es la suya; lejos no hace nada. CPU: con /dx/<0x30 y /dy/<0x20 → borra +0xF2 bit7 y +0x5C. Humano: con /dx/<0x60 y /dy/<0x40 (además <0x30/<0x20 si +0x97=0xB y 1C0026 bit0=0): si 1C0026 bit0=1 o +0x97=0x17 → borra +0xF2 bit7 y +0x5C; en la acción 0x15/2 nada; en la acción 1 → acción 0x14 y +0x5C=1; si no → acción 0 y +0x5C=1, y si +0x97≠0xB también borra +0xF2 bit7 y +0x5C. |
| 01B1D6 | cpu_relevo_disp | C | R | Borra +0xE2 bit3; despacha +0x5D&7 (<4) por la tabla 0x1B1F8; si no, 0x1B208. |
| 01B208 | cpu_relevo_ir | C | R | Compañero fuera → +0x5C=3; si no, va hacia el compañero rodeando. |
| 01B2A0 | cpu_entrar_relevo | C | R | Copia la zona del compañero, acción 0xC con la sub de la tabla 0x1B2E8[id] (entrada), borra el bit de la esquina (tabla 0x1B2F8) de 1C1821, +0xB7 bit0. |
| 01B2FC | cpu_delantal_volver | C | R | Con +0xC6 bit7 → +0x5C=0. Compañero fuera → 0x1BBB4; si no, 0x1BC3E. |
| 01B37E | cpu_bucle_principal | C | R | Si nadie está cubriendo (acción 0x17) y 0x1B3E4 da CS → +0x5C=7. Salvo en los estados 9/0xA/0xD, planifica (0x1D1A8). Despacha +0x5C&0xF por la tabla 0x1B40C. |
| 01B3E4 | ia_compa_cubierto | C | R | CC si el compañero está tumbado (0xB) y cubierto (+0x18 bit5); si no, CS. |
| 01B44C | cpu_ayudar_pin | C | R | Compañero cubriendo (0x17) y cerca (0x1B46C) → +0x5C=0xF; si no, 0x18F56. |
| 01B46C | chk_cerca_60_40 | C | R | CS si dx ≥0x60 o dy ≥0x40. |
| 01B486 | cpu_ir_salvar_pin | C | R | Con el compañero cubriendo y cerca: va al punto (0x1B4D2) junto al compañero (x±0x60/0x40, y del rival); si no, +0x5C=0. |
| 01B4D2 | punto_salvar_pin | C | R | +0x24 = x del compañero −0x60/+0x40 según el equipo; +0x26 = y del rival; 0x1CFD8. |
| 01B504 | cpu_delantal_disp2 | C | R | +0xF3−− si ≠0; despacha +0x5D&0xF (<8) por la tabla 0x1B52A; si no, 0x1B54A. |
| 01B54A | cpu_delantal_pasear | C | R | En el delantal: se pasea en y entre 0x118 y 0x170 con giros aleatorios (+0xC3); con el compañero cerca (<0x40) y sin +0xE3 bit0 → +0x5C=5. 0x1B6F0 decide entrar. |
| 01B62E | limite_delantal | C | R | y limitada a 0x118–0x170 (para); si no, 0x220C4. |
| 01B656 | cpu_delantal_seguir_rival | C | R | Sigue la y del rival por el delantal. |
| 01B6F0 | cpu_delantal_decidir | C | R | Si 0x1BDCA da CS (alguien en la acción 1/2/0x15/0x16) → +0x5C=6. CPU con el compañero en la acción 0 y +0x5D=6 → +0x5C=5. Si no, toma la zona de la entrada +0x6E (si tiene el bit3; si no, la +0x7E): en la zona 0 → 0x1B756 y, si no ha entrado (+0x2A bit7), 0x1B942 (agarrar desde el delantal); en la zona 1 → 0x1BB92. |
| 01B756 | cpu_temporizador_entrada | C | R | Con +0xC6 bit7 cuenta +0xC7; al acabar: +0x2A bit7 (entra), +0x5C=4 (0 si no está en el delantal), +0xF2 bit7, +0xE0 = tabla 0x1B7E2[id]. Si no, despacha +0xC6 por la tabla 0x1B7C2. |
| 01B7F2 | nop | C | R | Nada. |
| 01B7FA | cpu_programar_entrada | C | R | Si el compañero tiene energía 0 y +0x106 bit1 ya está puesto: solo sigue con una tirada <3/16. Luego: en el modo 1C0026 bit0=1 durante el combate 0, o la primera vez (+0x106 bit1 estaba a 0, se pone) → +0xC6 bit7 y +0xC7 = tabla 0x1B938[1C0028&0xF]. Las veces siguientes → 0x1B8F4 con la tabla 0x1B862. |
| 01B880 | cpu_entrada_ya | C | R | +0xC6 bit7. |
| 01B888 | rts_1b888 | C | R | rts. |
| 01B88A | rts_1b88a | C | R | rts. |
| 01B88C | ia_tirada_tag | C | R | En el modo 1C0026 bit0=1 durante el combate 0, o la primera vez (+0x106 bit0 estaba a 0, se pone) → +0xC6 bit7 y +0xC7 = tabla 0x1B938[1C0028&0xF]. Las veces siguientes → 0x1B8F4 con la tabla 0x1B8D6. |
| 01B8F4 | cpu_tirada_entrada | C | R | Tirada contra la tabla a2[1C0028*3 + 0x1CEF4] → programa la entrada. |
| 01B942 | cpu_agarre_desde_delantal | C | R | Con 1C001A bit7 y el rival dentro a dx ≤0x50: si está pegado (dx≤0x2C, dy≤0x10, misma z), sin la cuerda vibrando (bit14 de 1C1898/1C189A), rival no en 0x1F, ni ninguno el id 7, rival rebotando/corriendo o (0x1BB0C/+0xE2 bit5) en la acción 0 de espaldas, sin ruptura: él a la acción 0x13 y el rival a la 0x1B (agarrado desde el delantal), enlazados. Humano con botón: acción 0xC sub 0x3C (tag). Si no se da: CPU → acción 0 con +0x5C=1. |
| 01BB0C | chk_humano_modo1 | C | R | CS si es humano con control y 1C0026 bit0. |
| 01BB32 | cpu_tirada_agarre_delantal | C | R | Una vez (+0xE2 bit6): tirada contra la tabla 0x1BB7E (0x1BB88 la CPU)[1C0028] → +0xE2 bit5. |
| 01BB92 | cpu_delantal_a_ring | C | R | Objetivo en la zona 1 → +0x2A bit7, acción 0, +0x5C=2. |
| 01BBB4 | cpu_bajar_delantal | C | R | Anda hacia fuera (0x40/0xC0 según el equipo); al chocar: acción 3 (bajar), +0xAC según el lado; con 1C0026 bit0 el humano recupera el control (+0x2A bit0). |
| 01BC3E | cpu_volver_esquina | C | R | Va hacia y 0x110–0x150 y, al tocar la cuerda con 0x1A25C, acción 7 (subir al delantal). |
| 01BCB6 | cpu_delantal_ir_esquina | C | R | Compañero dentro, cerca (<0x60) y sin +0xE3 bit0: va a la esquina (y 0x108/0x150) y se gira (+0xE2 bit3). |
| 01BD5C | cpu_delantal_mirar | C | R | Si 0x1BDCA da CS (alguien en la acción 1/2/0x15/0x16, ver 0x1BDCA): se orienta con la tabla 0x1BDC6 mientras y esté en 0x118–0x170; si no, +0x5C=0. Fallo del original: calcula la orientación del equipo en d1 pero escribe d0 (el índice que devolvió 0x1BDCA) en +0xA. |
| 01BDCA | chk_alguien_accion_1_2_15_16 | C | R | CS si alguno de los 3 (+0x68/+0xA0/+0xA4, tabla 0x1BE2A) está en la acción 1, 2, 0x15 o 0x16 con su orientación (+0xA bit15) distinta de la de su equipo (+0x2A bit4). Qué representan esas acciones aquí: SIN CONFIRMAR (no es el estado tumbado 0xB). |
| 01BE30 | cpu_carrera | P(A) | A | Carrera de la CPU (acción 01 con +0x2A bit3). |
| 01BE9C | ia_ejec_mov | C | R | Tabla 0x1BEB6 (0x1BECA si 0x1D136 da CS) → 0x1BEE4. |
| 01BEE4 | ia_iniciar_llave | C | R | Con +0x2E bit7, la misma zona que el rival y 0x2786 CC: busca +0x2F en la lista a2 → descriptor 0x1C028+6*n con flags: bit0 = no con la misma orientación que el rival, bit1 = contacto +0x6E bit6, bit2 = compara +0xA con el byte +0xA de a2 (cae en el descriptor siguiente; probable fallo del original), bit3 = lado. dy<8 y dx en [+2,+4) del descriptor; si está más cerca y está fuera → +0x5C=7. Si todo cuadra y 0x1C14E no lo impide → acción 0xC con la sub +0x2F; con las subs 4 y 0x1C, el rival pasa a la acción 0x10 y queda enlazado. |
| 01C14E | chk_sub_a_limite | C | R | Sub +0x2F=0xA: si x pasa de 0x330 (0x2E0 al otro lado) → +0x2E=0, CS. |
| 01C180 | acc_salir_ring | C | R | Borra el bando bit1 y recorre la tabla 0x1C26E (0x1C2AA para el id 7) según el lado (+0x18 bit0) con pasos (pose, dx, dy). Al acabar, +0x19=3 (fuera), acción 0, y borra +0x33 bit7 y +0x2A bit2. |
| 01C306 | acc_volver_ring | C | R | Igual con las tablas 0x1C3F6/0x1C432; si +0x2A bit2, recupera el bit1. Al acabar, +0x19=0 (dentro). |
| 01C4A2 | ent_esquina_2 | C | R | Entrada por la esquina: +0xB8 bit7, 1C1821 bit2 durante 4 frames, pose 0x1F, posición fija 0xF6CE; luego 0x1E8B0. |
| 01C4FA | ent_esquina_0 | C | R | Ídem bit0, posición 0xF6D4. |
| 01C552 | ent_esquina_3 | C | R | Ídem bit3, pose 0x69, posición 0xF6DA. |
| 01C5B0 | ent_esquina_1 | C | R | Ídem bit1, posición 0xF6E0. |
| 01C60E | acc_caer_init | C | R | 0x1C61A y 0x8EC8. |
| 01C61A | acc_caer_inicio | C | R | Primera vez: si 1C1828=0xFF anota el id (primer caído); estado 1, velocidad de la tabla 0x95BC[id], se gira de espaldas al rival, dirección ±0x40. |
| 01C68C | acc_burla | C | R | Burla: pose 0x1A (0 para las subs 0x32/0x18/0x33/0x14) 4 frames; luego despacha por id (tabla 0x1C6FA). |
| 01C71A | burla_fin | C | R | Acción 0, +0x5C=0. |
| 01C726 | burla_a | C | R | Sonido 0x22, +0xE2 bit0; 2 poses de la tabla 0x1C7B0 (el id 5 usa la del 2) repetidas 2 veces. |
| 01C7C8 | burla_b | C | R | Sonido 0x22, una de 3 poses al azar (tabla 0x1C818). |
| 01C824 | burla_c | C | R | Sonido 0x22, pose 0x103 (0x20 frames). |
| 01C85C | burla_d | C | R | Sonido 0x23, una de 2 secuencias de 4 poses al azar (tabla 0x1C8DE), 2 veces. |
| 01C906 | acc_coger_silla | C | R | Coge/usa el objeto (sonido 0x2C); en los combates 4/9 la CPU → 0x1CB16. Fuera: pose 0xEF y coloca al compañero a ±0x33, crea el objeto en la mano (0x1CA6A). Al acabar: fuera → acción 7 con +0xE3 bit0 (y el control si es humano); dentro → +0xC0 bit7, espera a que el compañero entre → acción 6. |
| 01CA6A | crear_obj_mano | C | R | 0x1D114 da un objeto libre a4: activo, x/y/z desde el luchador con los desfases de las tablas 0x1CB06/0x1CB0E[id], pose 0x7C, orientación. |
| 01CB16 | coger_silla_modo49 | C | R | En los combates 4/9 (CPU): coloca al compañero a ±0x18 y hace 4 poses (tablas 0x1CBF0 dentro / 0x1CC10 fuera, índice id−6: solo da datos válidos para DiBiase (6) y André (7)). Fuera → acción 7; dentro → espera a que entre el compañero → acción 6. |
| 01CC30 | acc_cc30 | C | R | Salta a 0xE604. Le sigue 0x1CC36: toma el objeto +0x60 (el objeto pasa a la acción 1 con dueño y bando), 2 poses de la tabla 0x1CCD0[tipo], luego acción 0 con +0x5C=0. |
| 01CCE8 | chk_furia | C | R | Si +0xF9 bit0=0 y (+0xF8 bit7 o el contador +0xF6 ≥ la tabla 0x1CD48[id]): +0xFA = duración de la tabla 0x1CD6C[1C0028], +0xF9 bit0, borra +0xF8 bit7 y +0xF6 → CS (entra en modo especial/furia). |
| 01CD50 | tick_furia | C | R | Con +0xF9 bit0: +0xFA−−; al acabar borra +0xF8/+0xF9 y +0xF6. |
| 01CD80 | chk_contador_f6 | C | R | CS si +0xF6 >= la tabla 0x1CD48[id] (cmp.b y luego eori 1 a CCR invierte el acarreo); CC si es menor. Corregido 31-10-2026: antes decía lo contrario. |
| 01CDA4 | cpu_decidir_ir_objeto | C | R | Nada en los combates 4/9, con ids ≥6 (DiBiase/André), con un objeto en uso (1C1822) o si ya lleva uno. +0xE4 funciona como historial: cada frame se desplaza 8 bits y +0xE5 bit7 se pone si está junto a la mesa (y<0x100 y x<0x250 o ≥0x3A8). +0xE4 == 0x80 es el flanco de llegada (junto a la mesa ahora y no en el frame anterior). En ese momento, si el rival está más lejos que la mesa (0x1CE24 ≥0) y la tirada 0x1CE6C sale menor que la tabla → +0xE6=1 y +0x5C=4 (ir a por el objeto). |
| 01CE24 | dist_rival_vs_mesa | C | R | d2 = dist²(rival) − dist²(mesa: x 0x200/0x400 según el lado, y 0xB0). |
| 01CE6C | tirada_objeto | C | R | Tirada &0xF contra la tabla 0x1CE92[1C0028]. |
| 01CE8C | tipo_objeto | C | R | d0=1. |
| 01CE9C | nivel_energia4 | C | R | Energía +0x3C dividida por (energía máxima de la tabla 0x7FEC, o, para la CPU (+0x2A bit3), 0x8190[nivel 1C0028*8 + hueco +0x2A&7]; niveles 0–3: 45/49/47/43/47/43, 60/64/62/58/60/58, 68/73/70/66/71/66, 72/76/74/70/74/70/88/96)/4 (mínimo 1); el resultado se limita a 3. |
| 01CEF4 | nivel_energia3 | C | R | Ídem con /3 → 0–2. |
| 01CF50 | dir_a_rival_offset | C | R | Dirección (tabla 0x1977C, banda por distancia) hacia el rival + desfase (a2: dx con bit15 = lado contrario a la orientación, dy). CS si llega (dy<5 y dx<9). |
| 01CFD8 | dir_a_punto | C | R | Ídem hacia el punto absoluto (a2). |
| 01D032 | x_trapecio | C | R | x de un borde del trapecio del ring según y (pendiente 1/6, signo por el lado). |
| 01D04C | chk_compañero_mismo_objetivo | C | R | CS si el compañero está en la misma zona, con el mismo rival y su acción es compatible según la tabla de bits 0x1D0A0 (bit0/bit1 por bando). |
| 01D0C2 | tirada_id | C | R | Tirada &0xF < a2[id] → CS. |
| 01D0E2 | tirada_por_energia_rival | C | R | Pretende tirar &0xF < a2[nivel_energía(rival)*8 + id] → CS. Fallo del original: suma el desplazamiento del nivel a a1 (el puntero del rival) en vez de a a2, así que en la práctica la tirada es contra a2[id] sin tener en cuenta la energía. |
| 01D114 | buscar_objeto_libre | C | R | Primer objeto libre (bit7=0) de los 4 de la tabla 0xBCB8. Si no hay ninguno libre, devuelve igualmente el último (a4) aunque esté ocupado. |
| 01D136 | chk_rival_accion_1_15_16 | C | R | CS si el rival está en la acción 1, 0x15 o 0x16 (no es el estado tumbado 0xB; qué representan esas acciones aquí: SIN CONFIRMAR). |
| 01D166 | ia_retardo | C | R | +0xF3 = tabla 0x1D18E[rng%4]. |
| 01D1A8 | ia_intencion | C | R | Elige +0x2E/+0x2F (intención de la CPU). Tabla 0x1D33A (0x1DD7E si él mismo está en la acción 1) indexada por el nivel de energía 0x1CEF4 del rival, que cuenta como 0 hasta que 1C1852 ≥ 0x258. Luego por la acción del rival (0x1F si está en la acción 0xC con la sub en la lista 0x1D2B0: 19 2F 24 2C 20 1A) y por el id propio. rng&0xF & la máscara 0x1D2FA (0x1D31A en la acción 1)[acción]; byte con signo, máscara 0x807F. Salvo que los dos tengan +0x2A bit1 y él no esté fuera (+0x19≠1), se remapea con la lista 0x1D2B8[id]. Si lleva un objeto (+0x5E bit6) → +0x2F=0x30 (+0x2E=0 si el rival está tumbado, 0xB). |
| 01E05C | ia_elegir_llave | C | R | Subacción +0x30: tabla 0x1E392 si está fuera (+0x19=1, índice 0x1E7DA d1=0, rng&7) o 0x1E1A6[nivel de energía del rival, 0 hasta 1C1852 ≥0x258][id][rng&0xF]. Sin +0x2A bit1: +0x31 = tabla 0x1E14E[id][1C0046 bit1]. Ajustes 0x1E826 (lista 0x1E15E) → 0x1E88A (lista 0x1E170); si la sub está en la lista 0x1E19A, gira. Acción 0xC y el rival a la 0x10. |
| 01E432 | ia_elegir_llave_b | C | R | Variante de 0x1E05C: tablas 0x1E74A (fuera, d1=1) y 0x1E55E[dificultad][id][rng], con ext. La sub 0x36 fuera de x 0x2C0–0x340 pasa a 0x1E. Ajustes 0x1E510/0x1E526; giro si está en la lista 0x1E55A. Acción 0xC y el rival a la 0x10. |
| 01E7DA | chk_lado_exterior | C | R | Fuera (+0x18 bit4): 1 si va hacia un borde según x (0x2A0/0x360) y la orientación. |
| 01E826 | chk_sub_fuera_ring | C | R | Busca la sub +0x31 en la lista a2 (sub, dx); CS si la x resultante sale del ring (≥0x380 / <0x280). |
| 01E88A | remap_sub_por_id | C | R | Busca +0x31 en la lista a2 (9 bytes); sustituye por el byte [id]. |
| 01E8B0 | ia_llave_suelo | C | R | Sub +0x31 = tabla 0x1E8EC[id + 8 si el rival no está tumbado]; acción 0xC en el mismo lado que el rival; +0x104 del rival = 1. |
| 01EB40 | camara_disp | C | R | Cámara: a0=1C18AC, a1=1C18B0 (los dos seguidos); despacha 1C18A8 por la tabla 0x1EB60. |
| 01EB68 | despacho_zonas | C | R | Salta a 0x1EB8A[(zona propia & 0xF)*0x10 + (zona del rival & 0xF)*4]. |
| 01EBCA | camara_normal | C | R | Centra x (0x1EEE0) con un salto máximo de 4; y (0x1EF2A); y no pasa de 0x15C. |
| 01EC44 | camara_seguir_uno | C | R | Si a0 es CPU (+0x2A bit3): si a1 también es CPU → 0x1EE9A; si no sigue a a1. Si a0 es humano y 1C0026 bit1: si a0 está fuera (+0x19==1) → 0x1EE9C; si lo está a1 → guarda 1C18AC/1C18B0, intercambia y 0x1EE9C. Resto: salto por +0xB8 del seguido (tabla 0x1EC96). |
| 01ECAA | camara_poste | C | R | Por +0x18&3 (tabla 0x1ECBE): cada esquina tiene su posición objetivo. |
| 01ECCE | cam_esq_0 | C | R | x → 0x302, y → 0x1FB (pasos de 2). |
| 01ED18 | cam_esq_1 | C | R | x → 0x1F9, y → 0x1FB. |
| 01ED62 | cam_esq_2 | C | R | x → 0x32D, y → 0x155. |
| 01EDAC | cam_esq_3 | C | R | x → 0x1F9, y → 0x1FA. |
| 01EDF6 | camara_delantal | C | R | x como la normal; y → 0x15B o 0x1CB según +0x18 bit1. |
| 01EE9A | rts_1ee9a | C | R | rts. |
| 01EE9C | camara_x_y | C | R | 0x1EEE0 y 0x1EF2A. |
| 01EEA6 | camara_los_dos_fuera | C | R | Los dos fuera: x normal; y baja hasta 0xEF. |
| 01EEE0 | camara_x | C | R | 1C002A = x(a0) − min(/dx//2, 0x50) hacia a1 − 0x80, limitada a 0x1A0–0x360. |
| 01EF2A | camara_y | C | R | 1C002E sigue a y+z del luchador con una ventana de 0x40–0x80; mínimo 0xEF. |
| 01EF78 | camara_transicion | C | R | Al cambiar de objetivo (1C18B5 bit3): mueve 1C002A 2 píxeles por frame hacia el objetivo (bit1 al llegar) y la y (bit0); con los dos bits → 1C18A8=0 (vuelve al modo normal). |
| 01F0B0 | camara_elegir | C | R | Con partida: despacha 1C0026&3 por la tabla 0x1F0D0. |
| 01F0E0 | cam_elegir_1p | C | R | 1C18AC = el humano (bit0), 1C18B0 = la CPU con bit1. |
| 01F11A | cam_elegir_bando | C | R | Por el bit1. |
| 01F154 | cam_elegir_2p | C | R | Dos humanos (a3/a4): reglas por acciones (0xF poste, 0x19, 0xC, fuera 0x3/0x6 con 0x1F340) para elegir cuál centrar; si cambia, transición (1C18B5 bit3, 1C18A8=1). |
| 01F340 | chk_fuera_o_cruzando | C | R | CS si está fuera o en la acción 3/6. |
| 01F364 | cam_saltar_delantal | C | R | Si el seguido tiene +0xF2 bit7 (en el delantal), lo cambia por su compañero (0x1F39C). |
| 01F39C | compañero_de | C | R | 1C0100↔1C021A, 1C0334↔1C044E. |
| 01F3CE | camara_a_hw | C | R | Scroll: 180004 = 1C002A−0x200 (bit9 → 1C2B9C bit5), 180006 = 0x200−1C002E (bit9 → bit4); 18000A = 1C2B9C. |
| 01F434 | fondo_cmd | C | R | 1C182C = d0; llama a la tabla 0x1F450[d0]. |
| 01F474 | fondo_init_ring | C | R | Copia 4 bloques de tilemap (0x1F72C/0x1F868/0x1F9D4/0x1FAD0) a 0xC0000/0xC0400/0xC0800/0xC0C00 con 0x203C2 y pone las celdas fijas 0xC01B0 y 0xC0A50. 1C1890=1, 1C1892=0, scroll 1C002A=0x280 y 1C002E=0x200. Puertos 0x180004=0x80 y 0x180006=0. 1C2B9C &= 0xCF y lo copia a 0x18000A. |
| 01F50C | marcadores_nombres | C | R | Escribe en la capa de texto (c00b4/c0174/c0484/c0544) los 3×2 tiles del luchador (tabla 0x2197A[id]); los dos de la izquierda en espejo. |
| 01F546 | nombre_derecha | C | R | 3 filas × 2 tiles, atributo 0x20. |
| 01F57E | nombre_izquierda | C | R | Ídem en espejo (bit7 del atributo). |
| 01F5C8 | fondo_scroll_columnas | C | R | Si 1C182D=0: según el scroll X 1C002A, busca la columna en los umbrales 0x1F726 (avanza de 1 en 1 frente a 1C1890) y copia 16 filas de tilemap (tabla 0x1F706) en dos mitades por frame (1C1860/62/66). Según 1C1891, ajusta las celdas fijas 0xC0B80/0xC0A50/0xC01B0. |
| 0201AC | esc_dibujar_a | C | R | Escena (tabla 0x1F43E): dibuja en la capa c0000 la lista 0x20D9E (0x203C2) y 7 columnas de la tabla 0x20F06; 0x207C6. |
| 0201F4 | esc_dibujar_b | C | R | Escena: rellena c0000 (0x4FFDC), dos bloques espejados de 0x20F3E (0x20314), filas c03C0/c03CC y 10 tiles de 0x20FC8; 0x207C6. |
| 0202A0 | esc_dibujar_c | C | R | Escena: relleno 0x6FF00, bloques espejados de 0x20FDC y 32 tiles de 0x21068 en c0380. |
| 020314 | blit_bloques | C | R | Dibuja bloques de tiles consecutivos (formato: filas, columnas, atributo^d7, tile, ancho) con paso d0 y salto d6. |
| 02034A | esc_dibujar_d | C | R | Escena: lista 0x210A8 y seis bloques de 4×4 tiles (0x20404); c0264=0x720043. |
| 0203C2 | blit_lista_rle | C | R | Dibuja una lista: filas; por fila (atributo, tile[, 0xFF = nuevo atributo], incremento con bit7 = espejo, cuenta). |
| 020404 | blit_4x4 | C | R | Bloque de 4×4 tiles consecutivos. |
| 020424 | esc_dibujar_e | C | R | Escena: 6 tiles de 0x21134, filas de tiles fijos y la lista 0x210EC (0x2048E). |
| 02048E | blit_lista_rect | C | R | Lista de rectángulos (destino, atributo, tile, alto, ancho, salto); d6 negativo = dibuja hacia atrás (espejo). |
| 0204DC | esc_dibujar_f | C | R | Escena: lista 0x2113A, bloques fijos; prepara la animación (1C1836=0x80008, 1C182E=0, 1C185E=0, 1C185C=0x10). |
| 02057A | esc_dibujar_g | C | R | Escena: lista 0x218D6 y dos bloques de 3 tiles × 4/3 filas. |
| 0205D6 | esc_dibujar_h | C | R | Ídem en espejo (lista 0x21928). |
| 020632 | esc_combates_4_9 | C | R | En los combates 4/9: 4 rectángulos (tabla 0x2069E) con tiles 0x60FFE1… saltando los huecos (0x2065A). |
| 02065A | blit_rect_saltos | C | R | Rectángulo con tiles consecutivos que salta de 0x60FFF4 a 0x62FF43 y se corta en 0x62FF47/0x62FF4E. |
| 0206BE | esc_anim_6 | C | R | Con la escena 6 (1C182D): cada 8 frames alterna dos versiones (0x211FA/0x2121C y 0x2123E/0x21272); y ciclo de 5 pasos (tabla 0x207F6 de duraciones, tiles 0x20800) en c00C0/c0100 en espejo. |
| 0207C6 | fondo_reset_scroll | C | R | Pone a cero 0x180004/0x180006 y 1C002A/1C002E; 1C2B9C &= 0xCF y lo copia a 0x18000A. |
| 020824 | esc_anim_7_8 | C | R | Escenas 7/8: avanza los contadores (0x208DA alterna cada 8 frames; 0x208FE ciclo de 3). |
| 0208DA | ctr_alterna8 | C | R | Alterna d1 cada 8 frames (init 1C182C bit7). |
| 0208FE | ctr_ciclo3 | C | R | d1 = 0,1,2 cada 8 frames (init 1C182C bit6). |
| 020928 | esc_anim_dibujar | C | R | Escenas 7/8: si cambia el frame, redibuja (0x209C6 / 0x20C72). |
| 0209C6 | esc_anim_a | C | R | Por frame (+2 en la escena 8), tabla 0x209E6. |
| 0209F6 | esc_anim_a0 | C | R | 4 bloques de tiles (0x20B1A). |
| 020A88 | esc_anim_a1 | C | R | Ídem, el otro frame. |
| 020B1A | blit_bloque_inc | C | R | Bloque de tiles crecientes. |
| 020B34 | esc_anim_a2 | C | R | 4 bloques en espejo (0x20C58). |
| 020BC6 | esc_anim_a3 | C | R | Ídem. |
| 020C58 | blit_bloque_dec | C | R | Bloque de tiles decrecientes, hacia atrás. |
| 020C72 | esc_anim_b | C | R | Por frame (+3 en la escena 8), tabla 0x20C92. |
| 020CAA | esc_anim_b0 | C | R | 2 bloques de 5×8 (0x20D04). |
| 020CC8 | esc_anim_b1 | C | R | Ídem. |
| 020CE6 | esc_anim_b2 | C | R | Ídem. |
| 020D04 | blit_5x8 | C | R | 5 filas × 8 tiles. |
| 020D24 | esc_anim_b3 | C | R | 2 bloques (0x20D7E). |
| 020D42 | esc_anim_b4 | C | R | Ídem. |
| 020D60 | esc_anim_b5 | C | R | 2 bloques con 0x20D7E: 0xC03E0 tile 0xCD006C y 0xC03C0 tile 0xCD0094. |
| 020D7E | blit_5x8_dec | C | R | 5×8 tiles decrecientes, filas hacia arriba. |
| 0212A6 | cuerdas_anim | C | R | Por lado (1C1898/1C189C/1C189E/1C18A4/1C1894 y el bloque 1C189A…1C1896): 0x21324. |
| 021324 | cuerda_vibrar | C | R | Bit15 (lo pide 0x9700) → empieza: sonido 0x2A y bit14 = vibrando. Si el nibble bajo ≠0, empieza en el paso 2 (frame 3); si es 0, en el paso 0 (frame 1). Avanza hasta 8 pasos con las duraciones de la tabla 0x213A4 y los frames 0x213AC (&3) en d4 → 1C1894/1C1896; en el paso 8 borra el bit14. |
| 0213B4 | cuerdas_a_video | C | R | Para 1C1898 con el bit14 (vibrando; btst.b #6 sobre el byte alto) y 1C1890<2, si cambió el frame (1C189C≠1C189E) → 0x21412. Para 1C189A con el bit14 y 1C1890≠0, si 1C18A0≠1C18A2 → 0x21420. |
| 021412 | cuerda_dibujar_0 | C | R | a0=c020C, tabla 0x21476 → 0x2142C. |
| 021420 | cuerda_dibujar_1 | C | R | Cuerda del otro lado: a0=0xC0620, tabla 0x216A6; entra en el código común 0x2142C, que copia el bloque a2[0x2146E[d0]*0x8C] (14 filas de 5 celdas, con un salto de 0x400 en la fila 6). No es un retrato: la llama 0x213B4 para 1C189A. 0x21412 usa el mismo código con 0xC020C/0x21476. |
| 0219AA | indicador_1a92 | C | R | Flanco de 1C1A92 bit7: dibuja (encendido/apagado) 2 filas de 4 tiles en c0C8C o c08A4 (según bit0) con los tiles de 0x21A4A. |
| 021A00 | ind_tiles | C | R | Elige el destino y los tiles. |
| 021A2E | ind_dibujar | C | R | 2 filas de 4. |
| 021A4E | textos_luchadores | C | R | Pinta los textos 0x21BB8[id] de los 4 luchadores (ids de 1C012A/244/35E/478). Si el segundo de una pareja tiene el id 6 (DiBiase), lo cambia con el primero. No es un retrato: 0x21BB8 apunta a cadenas de texto RLE (destino fg0 de 4 bytes y luego pares de tiles arriba/abajo) que pinta 0x21B4C con la fuente de dos filas. Que sean los nombres de los luchadores es SIN CONFIRMAR: la tabla de letras no está decodificada. |
| 021A9A | fg0_iconos_fijos | C | R | Escribe las celdas fg0 0x80838–0x808C4 con los tiles 0xFFE1–0xFFF8 (paleta 0x10). |
| 021AEC | texto_lucha_0 | C | R | Texto del luchador d0, sin desplazamiento extra (0x21B4C). |
| 021AFE | texto_lucha_1 | C | R | Texto del luchador d1, destino +0x180. |
| 021B10 | texto_lucha_2 | C | R | Texto del luchador d2, destino +0x580 (+0x100 si es el id 6, DiBiase). |
| 021B30 | fg0_texto_rle | C | R | Dibuja texto RLE de (a0)[d3] en fg0 (+0x700, o +0x800 si d2=6) en dos filas, con paleta 0x17. Códigos: 0 fin, 1 salto, 2 hueco, 0xEB media celda. |
| 021E06 | texto_id_1c0102 | C | R | Texto 0x21BB8 del id que hay en 1C0102. |
| 021E1A | texto_id | C | R | Texto 0x21BB8[d0] en su destino, sin desplazamiento extra. No es un retrato: 0x21BB8 apunta a cadenas de texto RLE (destino fg0 de 4 bytes y luego pares de tiles arriba/abajo) que pinta 0x21B4C con la fuente de dos filas. Que sean los nombres de los luchadores es SIN CONFIRMAR: la tabla de letras no está decodificada. |
| 021E30 | textos_intro | C | R | Textos 0xC, 8+(1C0028&0xF) y 0xB (o 0xD si ese índice es 0xA, es decir, en el combate 2). |
| 021E5A | lim_fuera | C | R | Límites fuera del ring (tabla 0x221AA, y 0xBB) con 0x22140; en el aire (+0x18 bit7) por encima de z 0xDB → +0x9E bit7. Aplica las correcciones de los bits de +0x9F (0x21EBA: x/y). |
| 021E9A | lim_aplicar | C | R | Para cada bit 0–3 de +0x9F aplica la corrección (x=d2 o y=d0). |
| 021EC4 | lim_x | C | R | x=d2. |
| 021ECA | lim_y | C | R | y=d0. |
| 021ED0 | lim_ring | C | R | Límites del ring (tabla 0x221B2) con 0x22140; fuera: bordes x 0x240/0x3C0 e y 0x158; dentro: cuerdas laterales ±0x30 → +0x9F bits 0/1/3. Sin contacto → 0x21FE6; con contacto en el aire → 0x22040 (golpe contra la cuerda/poste). |
| 021FB6 | marca_choque_on | C | R | 1C1A9A /= bit del luchador (índice en 0xEA4C). |
| 021FE6 | marca_choque_off | C | R | Borra el bit del luchador en 1C1A9A. |
| 022016 | chk_marca_choque | C | R | Prueba el bit del luchador en 1C1A9B. |
| 022040 | choque_poste | C | R | Una vez por contacto (+0x9E bits 0/1; 0x22016): si la acción +0x2D está en la lista 0x220BE: sonido 0x33 si (+0x18 bit0 y contacto bit0) o (+0x18 bit0=0 y contacto bit1), si no 0x47; 1C1854 bit7. Daño 5 (+0x3E=5, 0x16488) si la acción ≠8 O si es la acción 8 con sub +0x45 = 0xA (corregido en auditoría: antes decía lo contrario). Luego 0x21FB6. Sin contacto → 0x21FE6. Qué lado es cuerda o poste: SIN CONFIRMAR visualmente. |
| 0220C4 | lim_delantal | C | R | Límites del delantal (tablas 0x221C2/0x221BA) → +0x9F bit0/1; en el aire por encima de z 0xDB → +0x9E bit7. |
| 022140 | lim_trapecio | C | R | Contra la tabla a2 (yfondo, yfrente, xizq, xder) menos d4: +0x9F bit3 (fondo), bit2 (frente; desfase 0), bits 1/0 (lados con la pendiente 1/6 por y); d2/d0 = valores corregidos. |
| 0221CA | objs_extra_tick | C | R | Recorre los 5 pares de 0x221F2 (a0, a1) y, si a1 está activo, llama a 0x2221A. |
| 02221A | obj_sombra_tick | C | R | Objeto de apoyo del luchador a1: init (estado 0xA, z 0xBB, +0x1A=0x8040); por el lado (+0x18&3) llama a la tabla 0x222A0 (0x222AC con 1C00F0 bit7; dentro en las acciones 3/4 usa la entrada 0). Copia la orientación desde la pose salvo con 1C00F0 bit0. |
| 0222C4 | obj_sombra_ocultar | C | R | 1C00F0 bit0. |
| 0222D6 | sombra_cuerda | C | R | Objeto ligado a un luchador (a1): si la tabla 0x2535A[estado de a1] = 0, se oculta. Si no, +0x19=3 e y del escalón de la tabla 0x2237A. Pose de las tablas 0x22392[1C1894&3] (x=0x26E) o 0x223FA[1C1896&3] (x=0x38E, volteado) según el lado (a1+0x18 bit0). |
| 022462 | flash_1c183e | C | R | Con partida y sin 1C1854 bit7: si 1C183E bit6/7, arranca (1C1890/1C1892 a +4/+6, 0xA ciclos de 6 frames, 0xE5) y lo cuenta; al acabar → 0x80. Si no, 0x23406. |
| 0224E8 | flash_dibujar | C | R | En la escena 0 (1C182C=0): dibuja el mensaje 1C183E (3 filas de las tablas 0x22634/0x22640/0x230F0 según 1C1890 y la fase); el mensaje 0x15 en la fase 4 escribe c0414. Si no, 0x230FC. |
| 0225B0 | tilemap_rle | C | R | Escribe una cadena RLE en el tilemap: geometría de la tabla 0x22760[d1] (x0, ancho, salto) y destino 0x22640[d1*0x10]. Códigos 0x00: 0xFD fin, 0xFC cambia de paleta (d6), y si no, repetición. |
| 022848 | datos | C | R | Entrada falsa: son datos (dc.w 0xFCFD…), no código. |
| 023054 | datos_23054 | C | R | No es código: tabla de tiles (dc.w 0x0DFF, 0x00FC…) del mensaje 0x22640, decodificada por la semilla lineal. |
| 0230FC | fondo_anim_publico | C | R | Sale si 1C1890 == 1 o si 1C182C ≠ 0 (corregido en auditoría: antes decía «solo si 1C1890=1»). Con 1C1854 bit4 y 1C1857 == 1 dibuja 2 cadenas RLE (0x225B0) de la tabla 0x23170 + 1C1890*0xC + 1C1856*0xC. |
| 0232DE | luces_azar | C | R | 1C184A: una vez, elige al azar una posición (rng%4) y repeticiones (&3); ciclos de 10 frames de 2 fases (bits 5/4) hasta agotar. |
| 02336C | luces_dibujar | C | R | Con 1C184A activo (y sin 1C183E bit7): tiles de la tabla 0x233F6[posición][fase] en c0B70, c0F40, c0BB0, c0F80 (4 por sitio). |
| 0233DC | blit_4_tiles | C | R | 4 tiles consecutivos con atributo = byte alto. |
| 023406 | flash_1c1854 | C | R | Arranca con el bit6 de 1C1854, o con el bit7 si 1C1890≠1 (con el bit7 y 1C1890=1 no hace nada; corregido, antes decía lo contrario). Fase 0 de 4 frames y fase 1 de 0x21 frames; luego 1C1854=0. El bit4 marca que es visible. |
| 02347E | pantalla_versus_retratos | C | R | 0x23F10 y 0x207C6; elige la pareja 1C0100/21A (o 334/44E si 1C0BC2 bit6=0). Dibuja 4×4 tiles por id (tabla 0x23536) en 0xC01D4/0xC01E8 y un bloque de 4×8 de la tabla 0x2354E en 0xC0318. |
| 0235CE | pantalla_presentacion | C | R | Dibuja la presentación del combate d0 en la capa 0x80000: fondos 5×5 (0x236A2), la lista 0x23702[d0] (0x236BC; la entrada 0x237FE limpia antes con 0x2367A) y tiles fijos. |
| 02367A | limpiar_6x6 | C | R | Borra 6×6 tiles en 0x80B28. |
| 0236A2 | relleno_5x5 | C | R | 5×5 tiles iguales. |
| 0236BC | blit_lista_presentacion | C | R | Lista: destino, cuenta, tile; por elemento atributo (0xFF = repetir) y salto. |
| 0236F4 | fill_inc | C | R | Escribe d5+1 longs incrementando d2; a2 += d6. |
| 02387C | pantalla_titulo_seq | C | R | Secuencia de pantalla con fundido: escena 3, paleta 0x140200=0x900, cartel fg0 0x2660E(3), dibuja los marcos 0x23CEE, los textos 0x23757/0x237BD y la fila 0x23D2E; cámara a 0; 1C0568=0; sonido 0x45; 0x1D pasos de la tabla 0x23A0A (0x23A28) con espera (0x239DC); paleta a 0. |
| 0239DC | espera_bucle | C | R | Bucle de espera ocupado (d0 × 0x1B80). |
| 0239F4 | blit_texto | C | R | Tile inicial de a1 y lista (0x236CE). |
| 023A02 | fg0_dibujo_cont | C | R | Entrada intermedia de 0x23A28 (continúa con a0/a1/a2 ya cargados). |
| 023A28 | fg0_dibujo | C | R | Dibuja el gráfico d1 de la tabla 0x23AC4 en fg0 (0x80000 + desplazamiento). Rachas (inicio, fin) de tiles con paleta d4. Comandos tras 0xFF: 0 salto n celdas, 1 paleta, 2 nueva fila (+0x80), 3 repetición n, 0xFF fin. |
| 023F10 | fg0_marco_versus | C | R | 0x24E2, gráficos 0x18–0x1D (0x23A28) y bordes de tiles 0xA0–0xA8 (paletas 0x38/0x39) en fg0, más una columna de la tabla 0x23FF4. |
| 0240B6 | llave_por_sub | C | R | +0x9E=0. Busca +0x31 en la lista de 14 bytes 0x240F0; la entrada i salta a 0x240FE+(13−i)*4 (el índice va al revés porque usa el contador de dbra). |
| 024136 | llave_sub_0x24136 | C | R | 0x244EE con la tabla 0x24146 y d0=3. |
| 024168 | llave_sub_0x24168 | C | R | 0x244EE con la tabla 0x24178 y d0=1. |
| 02418A | hitbox_pose_a | C | R | Tabla 0x241AE: 0x24554 con 5 entradas, dx 0x10, dz 0x10; sin contacto → 0x24222. |
| 0241BA | llave_sub_multi | C | R | Prueba 0x24554 con 6 tablas (0x24254…0x2429C) y parámetros (d0, d1, d2); para en la primera que da CC. |
| 0242AC | hitbox_pose_b | C | R | Tres intentos (0x242F8/0x24306/0x24314) de desplazar el luchador según la pose. |
| 024322 | rts_24322 | C | R | rts. |
| 024324 | rts_24324 | C | R | rts. |
| 024326 | rts_24326 | C | R | rts. |
| 024328 | rts_24328 | C | R | rts. |
| 02432A | rts_2432a | C | R | rts. |
| 02432C | rts_2432c | C | R | rts. |
| 02432E | hitbox_pose_c | C | R | Seis intentos (tablas 0x243F8…0x243EC). |
| 024410 | hitbox_pose_d | C | R | Dos intentos (0x24442, 0x24452). |
| 024460 | hitbox_pose_e | C | R | Cuatro intentos (0x244C6…0x244EA). |
| 0244EE | ajuste_pose_lista | C | R | Busca la pose actual en la lista (pose, dx, dz, flip) y aplica dz a +0x14 y dx a x (con el signo según el flip respecto a +0xA). Si toca un límite (+0x9E&3≠0), restaura solo la z y se queda con la x que ha corregido la rutina de límites. Si no toca nada, restaura x y z, así que no se mueve (corregido: antes decía que deshacía x al chocar). Con +0x19=0 llama a 0x21E5A y con ≠0 a 0x21ED0. Con +0x19 0=dentro, eso choca con los nombres lim_fuera/lim_ring: SIN CONFIRMAR cuál está al revés. C=0 si la encuentra, C=1 si no. |
| 024554 | ajuste_pose | C | R | Igual con dx/dz fijos (d1/d2) y el flip en los 4 bits altos de la pose de la lista. Si toca un límite (+0x9E&3≠0), restaura solo la z y se queda con la x que ha corregido la rutina de límites. Si no toca nada, restaura x y z, así que no se mueve (corregido: antes decía que deshacía x al chocar). Con +0x19=0 llama a 0x21E5A y con ≠0 a 0x21ED0. Con +0x19 0=dentro, eso choca con los nombres lim_fuera/lim_ring: SIN CONFIRMAR cuál está al revés. C=0 si la encuentra. |
| 0245BE | secuencia_creditos_intro | C | R | 0x24C8/0x24E2/0x254E; 0x140200=0; sonido 0x14 y 0x24B38. 4 páginas con los gráficos fg0 7–0xE y los textos 0x29–0x31 (0x2549E), iconos 0x7C00DC–DE. Transiciones 0x24B54 y esperas 0x453A de 0x260/0x240/0x240/0x240 frames. |
| 024B38 | pal_buffer_borrar | C | R | Borra el buffer de paleta 1C198A (0x78 words). |
| 024B54 | pal_fundido | C | R | 16 pasos: acerca (a3=0) o aleja (a3≠0) cada componente RGB del buffer 1C198A a la paleta 0x37D0/0x37F0/0x3810 de d2 en d2; vuelca en el vblank (0x24C5C). |
| 024C5C | pal_volcar | C | R | Copia 1C198A a la paleta 140002 (8 filas de 15 colores). |
| 024C90 | marcador_inicio | C | R | Dibuja los dos marcadores (0x80084/0x800C0) según el +0x2A bit3 de 1C0100/1C0334 (tablas 0x24D86 CPU / 0x24D92 humano); 1C186C=0x8000, 1C186A=1. |
| 024D36 | fg0_fila_3partes | C | R | Escribe una fila fg0 (paleta 0x1F) de inicio, medio y fin. |
| 024D9E | marcador_modo | C | R | Para cada bando, si es CPU (+0x2A bit3) no dibuja nada. Humano: 0 (o 2 en el bando B) con bit1, 1 (o 3) sin bit1; en el modo 1C0026&0xF=1 usa 4, o 5 con bit5. Llama a 0x24E20 (izquierda) o 0x24E28 (derecha). |
| 024E20 | marcador_izq | C | R | Destino 0x80084. |
| 024E28 | fg0_bloque_2x4 | C | R | Escribe 4 filas × 2 celdas de la tabla 0x24E62[d0*8] en 0x800C0 (paleta 0x1F). |
| 024E92 | insert_coin_parpadeo | C | R | Por bando CPU (bit3): parpadeo (0x24EBC). |
| 024EBC | parpadeo_texto | C | R | Alterna cada 0x20/8 frames el texto (tabla 0x24FB4 o 0x24FBC con créditos) — p. ej. «insert coin / press start». |
| 024F6C | blit_texto2 | C | R | Filas de tiles con el atributo 0x1F. |
| 024F96 | fg0_borra_2x13 | C | R | Borra 2 filas de 13 celdas (0x1FFF00). |
| 025050 | ptr_1c0890 | C | R | a0 = 1C0890 + scroll x. |
| 025064 | ocultar_cuerda_frente | C | R | 0x251D2, 0x251F0; para los luchadores en la acción 4 o dentro con y<0x140: 0x2509E. |
| 02509E | cuerda_frente_por_luchador | C | R | Elige la tabla de anchura por acción (0x2535A → 0x25346): por la acción (0x252FE; el árbitro 1C0568 usa 0x25340), por la sub +0x30 (0x25286) o por +0x44 (0x2523C). Marca los segmentos (de 16 píxeles entre x 0x236 y 0x3B6) del array 1C155A que tapa; pose 0x3B/0x42 en los casos del estado 7. |
| 0250C6 | cf_por_accion | C | R | Tabla 0x252FE[acción] (el árbitro, 0x25340). |
| 0250E8 | cf_por_sub | C | R | Tabla 0x25286[+0x30&0x3F]. |
| 0250F8 | cf_por_44 | C | R | Tabla 0x2523C[+0x44]. |
| 0251D2 | cf_limpiar | C | R | Borra el bit de activo de los 23 segmentos de 1C155A. |
| 0251F0 | fg0_marcas_jugador | C | R | Pone los tiles 0x39/0x3A (si 1C1895 bit0) y 0x40/0x41 (si 1C1897 bit0) en el búfer 1C155A. |
| 02537C | cf_init | C | R | Crea los 23 segmentos de la cuerda delantera (1C155A, paso 0x1E): x desde 0x246 de 16 en 16, y 0xE0, z 0xC0, pose 0x3B; los extremos con las poses 0x39/0x3A y 0x40/0x41 (postes). |
| 025402 | cf_extremos | C | R | Rehace las poses de los extremos (0x253CE). |
| 025408 | cortinilla | C | R | Transición de pantalla: llena la capa 0x80000 con los tiles de la tabla 0x25492 por pasos (esperando 4 frames); al acabar borra (0x25474) o 0x24E2 según el sentido. |
| 025474 | capa_80000_borrar | C | R | Llena 0x80000 con 0x1F0000 (vacío). |
| 02549E | imprimir_texto | C | R | Imprime la cadena d0 (tabla 0x25600; con el bit7, la borra con espacios). Formato: atributo, destino long alineado y luego caracteres; ASCII−0x20+d2 = tile. Códigos <7 (tabla 0x2551A): 0 fin, 1 nuevo destino absoluto, 2 destino relativo, 3 atributo, 4 máquina de escribir (pausa de n frames por carácter), 5 fin de pausa, 6 desplazamiento de tile d2. |
| 025536 | txt_fin | C | R | Fin. |
| 02553C | txt_destino_abs | C | R | Código 1: alinea y lee un nuevo destino absoluto (0x254C2). |
| 02553E | txt_reubicar | C | R | Destino += long. |
| 02554C | txt_atributo | C | R | Nuevo atributo. |
| 025558 | txt_pausa_on | C | R | Modo máquina de escribir (d2 frames). |
| 025568 | txt_pausa_off | C | R | Fin del modo. |
| 025570 | txt_desplaz_tile | C | R | Código 6: d2 (low) = byte siguiente, que se suma a cada tile. |
| 0255A8 | capa_80000_marco | C | R | Borra las filas 0 y 31 y las columnas de los bordes de la capa 0x80000. |
| 0255F4 | fg0_borra_n | C | R | Borra d0+1 celdas fg0. |
| 025B96 | datos_25b96 | C | R | No es código: tabla de entradas de 10 bytes (0x0008, 0x08BC…), decodificada por error. |
| 025DA2 | datos | C | R | Entrada falsa: datos. |
| 026110 | frag_26110 | C | R | Fragmento de datos decodificado por error (sin entrada real). |
| 026120 | tilemap_fila_tabla | C | R | Escribe una fila del tilemap: destino de 0x26166[d2] y origen de 0x26176[d0], con la paleta de 0x261B6[d1]. Formato: longitud, tile inicial (dos bytes si d1=0) y tiles consecutivos. |
| 0261BC | imprimir_numero | C | R | Imprime el número BCD de la tabla 0x26244[d0] (cifras, destino, fuente) sin ceros a la izquierda (0x26218). |
| 026218 | cifra_bcd | C | R | Cifra → tile; los ceros a la izquierda se ponen como espacio. |
| 02626E | reloj_combate | C | R | Reloj del combate (1C1850). Al empezar: dibuja el marco (0x265F6), sonido de la música del combate (0x6DD4), tiempo = 0x708 ajustado por los DIP 180003 bits 4–5 (0: 0x708, 1: +0x96, 2: −0x96, 3: −0x12C). Cada 0x42 frames resta 0xA (décimas → 30:00 en el valor por defecto, mostrado como mm:ss con /0x3C). Al llegar a 0x12C (5:00): 1C1850 bit1, aviso con el comando 0x70 (en el Z80 no hace nada: solo escribe 0x821F, que nada lee) y la música 8 (prisa). Con menos de 0x12C parpadea el color 140036 (bit2). A 0: 1C1850=1, texto 0x9B («TIME UP»), cartel fg0 0x2660E(0) y, según el modo (1C0026&3, tabla 0x2653C), decide el resultado. |
| 026548 | tiempo_fin_1p | C | R | Fin de tiempo con un humano. Si el bando A es CPU (+0x2A bit3 de 1C0100), 1C0BC2=0x4000 y 1C0BDA=0x8000; si no, al revés. Sonido 0x21 y espera de 0x10. Qué significan 0x4000/0x8000 (perder o ganar): SIN CONFIRMAR. |
| 02657A | tiempo_fin_empate | C | R | Los dos con 0x8000 (empate/derrota doble); sonido 0x21. |
| 0265A0 | celda_doble | C | R | Escribe 2 celdas (arriba/abajo) de la tabla 0x265D2[d1] en el destino 0x265E6[d2] (paleta 0x10). |
| 02660E | cartel_fg0 | C | R | Cartel grande de 2 filas en la capa fg0: borra 2×19 celdas en 0x80720/0x807A0 y escribe el patrón 0x26696[d0] (longitud 0x26692[d0] = 0x12/0x10/0x10/0x1E bytes) como pares de tiles 0x10xxxx (0x80D04 si d0=3). Lo llaman: 0x1A64 (fin de combate), 0x16212 (rendición, d0=1), 0x238A0 (título, d0=3), 0x26522 (fin de tiempo, d0=0). No es sonido ni Z80. |
| 02EF54 | datos | C | R | Entrada falsa: datos. |
| 02F00C | datos | C | R | Entrada falsa: datos. |
| 02F068 | datos_2f068 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F070 | datos_2f070 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F106 | datos_2f106 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F14E | datos_2f14e | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F174 | datos | C | R | Entrada falsa: datos. |
| 02F254 | datos_2f254 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F256 | datos_2f256 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F262 | datos_2f262 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F266 | datos_2f266 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F3C6 | datos_2f3c6 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F3EA | datos_2f3ea | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F40C | datos_2f40c | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F410 | datos_2f410 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F50A | datos_2f50a | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F51E | datos_2f51e | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F522 | datos_2f522 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F548 | datos_2f548 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F614 | datos_2f614 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F648 | datos_2f648 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F668 | datos_2f668 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F68E | datos_2f68e | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 02F6AC | datos | C | R | Entrada falsa: datos. |
| 02F786 | datos_2f786 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6A8 | datos_3b6a8 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6B0 | datos_3b6b0 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6B8 | datos_3b6b8 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6C0 | datos_3b6c0 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6C8 | datos_3b6c8 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6D0 | datos_3b6d0 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6D8 | datos_3b6d8 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B6E0 | datos_3b6e0 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
| 03B7C6 | datos_3b7c6 | C | R | No es código: datos (tablas de sprites/punteros) que la semilla lineal decodificó como instrucciones (ori.b #xx,d3 = 0x0003xxxx = punteros a 0x3xxxx). Leídos y descartados como código. |
