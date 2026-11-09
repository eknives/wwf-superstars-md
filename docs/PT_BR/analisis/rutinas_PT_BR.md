# Rotinas (R = lida inteira; A = assinatura antiga sem reler)

> Versão em português do Brasil de `docs/analisis/rutinas.md` (o espanhol é o original). Endereços, nomes de rotinas, código e valores são mantidos como no original; só as descrições são traduzidas.

Cobertura lida inteira: 964 rotinas, 100.0% dos bytes (bytes por entrada = min(distância até a seguinte, 0x400)).

Estado: C = confirmado lendo o código inteiro; "SC: motivo" = SEM CONFIRMAR (SIN CONFIRMAR); P(A) = anotação antiga por assinatura, pendente de reler.

| Dir | Nome | Estado | Fonte | Função |
|---|---|---|---|---|
| 000E00 | reset_arranque | C | R | Vetor de reset: IPL 7, USP=1C3B00, apaga 1C180C, IRQ ack (180002/180000) e 1C2B9C; inicializa o vídeo (0x24AE/24C8/24E2/254E/25B8/29DC); baixa o IPL; 180008=0; volta a inicializar duas vezes (com 0x24FC); som 0xD (0x2549E), espera 0xFF frames (0x453A); 140200=0 → laço 0x1010. |
| 000EBA | irq_vblank | C | R | IRQ (vetor 30): se 1C180C bit7 e não reentrante (1C0019 bit7): 1C180D++; com 1C0019 bit0 (frame pronto): DMA/paletas/sprites (0x259A, 0x269A, 0x29F6, 0x2626E), 1C0019 bit1 e os ticks de frame: 0x20928, 0x55C6, 0x1F5C8, 0x213B4 (cordas para o vídeo), 0x224E8, 0x2336C, 0x206BE, 0x219AA, 0x1F3CE. Espera que 180009 bit0 baixe. ACK 180000. |
| 000F5C | irq_timer | C | R | IRQ (vetor 29), não reentrante (1C0019 bit5): 0x4A10 e 0xF92 (temporizador da demo/atração). ACK 180002. |
| 000F90 | irq_nula | C | R | rte. |
| 000F92 | tick_atraccion | C | R | Com 1C00E4 bit7: conta até 0x100 → 1C182A=2, 1C00E6=0x800083FE, som 2. Com 1C00E6 bit7: contador 1C00E8 em ciclo de 0x9ECF; em 0x860F e 0x8E7D dispara o som 0x22 (0x25E6). |
| 001010 | bucle_juego | C | R | Inicializa variáveis e o vídeo; som 0x22 (1C00E4=0x8000); paleta/cena (0x1F434 modo 3, 0x497C). Sem crédito: sons 0xE/0x37. 0x78FA (atração/créditos). Com partida (1C001A): 0x704E (seleção); 1C004B da tabela 0x139E segundo os DIP (180002 &3). Entre combates: intro com música da tabela 0x135C[1C0028], cena 0x1F434 modo 5, 0x1326 (objeto 1C0AB2), 0x43D4. Prepara o combate (tabela 0x1364/0x136E: música, paleta, cena, textos 0x24B38/0x24C5C/0x235CE, 0x1E62, salto para a rotina). Laço por frame (0x1502): lutadores (tabela 0x1DF0, 8 objetos, 0xEA74 para os ≥4), 0xC6C8 árbitro, 0x212A6 cordas, 0x25064, 0x22462, 0xF844, 0x232DE, 0x1676 (música), 0x6BA0, 0x7CAE, 0x17D2, 0x435C, 0x1657E colisões; marca o frame (1C0019 bit0) e espera a IRQ. Fim do combate (1C0BC2/1C0BDA bits 7/6) → 0x178C. 1C0046 = frames. |
| 001326 | init_obj_ab2 | C | R | Objeto 1C0AB2: ativo, pose 0x10, estado 8, pos (0xC6, 0x155, 0xBB). |
| 001676 | musica_combate | C | R | Na partida, ou na demo com 1C0026&0xF=2: música 0x27 (bit7 = sem loop se 1C0047 bit5=0). Se não: sons 0xA7, 0x261BC(0), 0x28. |
| 0017C6 | modo_attract_creditos | C | R | Caso da tabela 0x17B6: tst 0x1C0016 (créditos) e salta para 0x1DC8 (fim de partida → attract/0x1010). |
| 0017D2 | cargar_graf_luchadores | C | R | Para cada lutador não CPU (+0x2A bit3=0) chama 0x26120 com d0=+0x2B (id), d1=+0x2A bit1, d2=índice. |
| 001810 | gana_equipo_A | C | R | Caso de 0x17B6. d2=1 se na equipe B o legal (+0x2A bit1) tem +0x19==1 (ou 0x1C1852<0 → d2=0). Se 0x1C0026 bit6 (humano em B) → 0x1A30 (derrota do humano). Se não: 0x1AC8 (sequência de vitória); se devolve CC → 0x1DC8. Modo 2 jogadores → 0x1926. Resto: d0 = ids da tabela 0x1C7E dos lutadores vencedores, 0x1C0026 bit7, libera rivais (0x1CFA), avança combate (0x1D22) e guarda rivais novos em 0x1C0085/87; volta a 0x113C. |
| 0018D2 | gana_equipo_B | C | R | Simétrica de 0x1810 para a equipe B (bit7 → 0x1A30, ids 0x1C0479/0x1C035F, 0x1C0026 bit6, rivais em 0x1C006F/71). No modo 2 (versus) 0x1926: limpa telas, paleta 6 e modo 6 (0x1F434). |
| 0019C6 | empate_o_derrota | C | R | Se o líder da equipe A é CPU → 0x1810; se o de B é CPU → 0x18D2. Se não (ambos humanos): sons 0x15 e 0x23, 0x80 frames, 0x651C, apaga caixas e fim (0x1DC8). Em 0x1A30 (derrota humano): sons 0x15/0x23, no frame 0x3F se d2 texto 0x9B e 0x2660E; depois tela de continuar 0x853E: se continua restaura equipes (0x1EE8/0x1F22) e volta a 0x13A2. |
| 001AC8 | secuencia_victoria | C | R | 0x20 frames de combate (0x1C86). Combate 9 (final): sons 0x38, 0x09, 0x22; +0x40=0xC nos 4; 0xE8 iterações com recarga de energia 0x2060 e barras 0x7CAE; depois paletas 0, som 0x12, FINAL 0x2387C, limpeza, 0x245BE e CC (fim de jogo). Resto: som 0x38 se combate 4, se não 0x39; texto 0x0C; mesma recarga; combate 4: paleta 8, som 0x0D, cena 0x2347E, 0x100 frames puláveis, 0x2387C. Devolve CS (continua). |
| 001C86 | frames_combate | C | R | d6+1 frames: 0x221CA, 0x25064, 0x22462, 0x6BA0, 0x435C, copia contador de sprites, 0x455C, 0x2516; pede vblank (0x1C0019 bit0) e espera bit1; 0x1676; 0x1C0046++. |
| 001CFA | liberar_rivales | C | R | bclr bit7 de 0x1C00A2[d5&F] e [d6&F] (palavras). |
| 001D22 | avanzar_combate | C | R | 0x1C0029++ pulando 3→4 e 8→9; se chega a 0xA → fim (0x1DA4: limpa, 0x245BE, 0x1DC8). Combates 4 e 9: dupla fixa d2=0x706 ou 0x607 (rng bit2). Resto: 0x21AE por nível. 0x1DC8: limpa 0x1C0024/28, som 0, para 0x1010 se há créditos, se não para 0xE60. |
| 001E38 | esperar_saltable | C | R | Espera d1 frames (0x453A); após os primeiros 0x10 permite sair com botões (0x1E90 CS). |
| 001E62 | texto_y_esperar | C | R | Se d3==FFFF só espera; se não, fade de paleta 0x24B54 (d3=1, a3=0, d2=1) e espera d1-0x10. (Corrigido: 0x24B54 é o fade de paleta, não texto.) |
| 001E90 | boton_pulsado | C | R | CS se P1 ou P2 têm pressionado bit4 ou bit5 (ativo baixo). |
| 001EC4 | borrar_caja_fg0 | C | R | Apaga 20 linhas × 25 longs de fg0 a partir de 0x80390 (linha 0x80 B). |
| 001EE8 | guardar_equipos | C | R | Guarda +0x2A e +0x3C dos 4 e 0x1C0026 em d0-d7. |
| 001F22 | restaurar_equipos | C | R | Inversa de 0x1EE8. |
| 001F5C | indicador_activar | C | R | 0x1C1A7A[d0*4]: bit7, bit6 se obj+0 bit0, fase 2, duração 0x40. |
| 001F86 | destello_paleta_seleccion | SC: qual elemento da tela usa essa cor (moldura do retrato?); formato xBGR444 presumido | R | Tela de seleção: 6 indicadores (um por lutador, ativados por 0x1F5C a partir de 0x7552 ao confirmar, 0x40 frames; bit6 conforme o bit0 do cursor, provavelmente jogador). A cada 2 frames fase 0..2: NÃO são sprites nem tiles, escreve uma cor com 0x2636 na RAM de paleta 0x140200 (tabela 0x268E[1]) em (paleta,cor) de 0x2048: (0,15),(1,15),(2,1),(3,15),(4,15),(5,12). Cores 0x2054: 0x0F66/0x0F0F/0x00F0 (lilás-azul, magenta, verde); 0x205A em outra ordem. Ao terminar, restaura. Render: obj1f86/. |
| 002060 | recarga_energia | C | R | Se 0x1C0BC2≥0 recarrega os lutadores A (contadores +0x40); se 0x1C0BDA≥0 os B. 0x1C0BC2/0x1C0BDA são flags de equipe: sua origem está pendente. |
| 0020C2 | recarga_uno | C | R | Se d7≥0: d7-=4; se DSW2 bit7==0, +0x3C += 4; teto 0x30. |
| 0020EC | energia_llena_si_eliminado | C | R | Se 0x1C0BC2<0 põe +0x3C=0x30 em A; se 0x1C0BDA<0 em B. |
| 00211E | sonido_publico_fuera | C | R | Legal A (bit1 de +0x2A, ou o parceiro) e legal B: se ambos +0x19==1, ou algum ==2 → na primeira vez som 0x22 + 0x1C183E bit7; repete 0x22 a cada 0x50 frames (0x1C1A9D). Se não, limpa 0x1C1A9C. |
| 0021AE | elegir_rivales_nivel | C | R | jmp tabela 0x21C4[0x1C0028&F]. Devolve d2 = (id1<<8)/id2. |
| 0021EC | rivales_nada | C | R | rts |
| 0021EE | rivales_primeros_libres | C | R | Os 2 primeiros de 0x1C00A2 sem bit0 (derrotado); põe-lhes bit1. |
| 002228 | rivales_azar_a | C | R | Dois rng&1: o n-ésimo derrotado e o n-ésimo não derrotado sem bit7. |
| 002284 | rivales_por_seleccion | C | R | Marca bit0 dos que têm bit15 e usa 0x71E8 (escolha como a tela de seleção) com 0x1C0084/86 salvos. |
| 0022D2 | rivales_azar_uno | C | R | rng&7 (<6, se não 0) e avança até um não derrotado; d7=6 fixo. |
| 002308 | rivales_primero_y_azar | C | R | d6 = primeiro livre (bits 0-1 a 0); d7 = rng&7 (<6) sem bit7 e diferente de d6. O final comum 0x2352 troca d6/d7 com rng&1. |
| 002368 | limitar_6 | C | R | d0=0 se ≥6. |
| 002372 | fundido_paletas | C | R | 16 passos: em cada vblank (0x180009 bit0) subtrai 1 de R, G e B das paletas 0x140200/0x140000/0x140100 (64 cores cada uma). |
| 002422 | oscurecer_64 | C | R | Subtrai 1 de cada nibble de cor não nulo em 64 entradas. |
| 00246C | enlazar_rivales | C | R | +0x68 de 1C0334 e 1C044E = 1C0100; +0x68 de 1C0100 e 1C021A = 1C0334. |
| 0024AE | borrar_ram | C | R | 0x1C0014–0x1C1AAF. |
| 0024C8 | borrar_bg0 | C | R | 0xC0000–0xC0FFF. |
| 0024E2 | borrar_fg0 | C | R | 0x80000–0x80FFF. |
| 0024FC | borrar_objetos | C | R | 0x1C0100–0x1C1AAF. |
| 002516 | borrar_sprites_sobrantes | C | R | Apaga as peças entre o contador novo 0x1C208C e o anterior 0x1C208E. |
| 00254E | borrar_sprites | C | R | Contadores e buffer 0x1C1AB0 (75×10 B) e sprite RAM 0x100000 (0x400 B). |
| 00259A | copiar_sprites | C | R | 75×10 B de 0x1C1AB0 para 0x100000. |
| 0025B8 | flip_pantalla | C | R | DSW1 bit7 (ativo baixo) → bit0 de 0x1C2B9C → 0x18000A. |
| 0025E6 | pedir_sonido | C | R | Salvo 2 e 0x22 limpa 0x1C00E6. Envia só se 0x1C001A≠0 ou DSW2 bit2=1 (som na demo). 0x34→0x48 se a0+0x19==1. Escreve a palavra em 0x180008 e espera 0x81 voltas. O Z80 só vê o byte baixo (latch 0x180009 → NMI → fila 0x8400). Mapa de comandos em sistemas/sonido.md. |
| 002636 | encolar_escritura | C | R | Entrada 0x1C18BC: tabela, linha, col, valor. Dir = 0x268E[tabela] + linha*0x20 + col*2 (a tabela de bases está em 0x268E). Fila 0x1C18C4 (máx 0x20). |
| 00269A | aplicar_cola | C | R | Escreve as palavras enfileiradas e esvazia a fila. |
| 0026BC | delta_objetos | C | R | a0=*(0x1C004E), a1=*(0x1C0052): /dy/→0x1C0052, /dx/→0x1C0050, sinais em 0x1C004E bits 1/0. |
| 00270C | angulo_objetos | C | R | Ângulo aproximado (atan por quociente×0x40 / soma, tabela de octante 0x2782) de a0 para a1 → byte 0x1C004E. |
| 002786 | fuera_de_pantalla | C | R | CS se x ∉ (camx−0x30, camx+0x130) ou y+z ∉ (camy−0x40, camy+0x150). |
| 0027D2 | trayectoria | C | R | Velocidades +0x24/+0x26/+0x28 e gravidade +0x22 da tabela 0x2814[d0]; modo 2 (cartesiano); vx negada se olha para a esquerda (salvo d0=0x11). |
| 0029DC | forzar_paletas | C | R | 0x1C003E=0, 0x1C0042=FFFFFFFF, carga. |
| 0029F6 | cargar_paletas | C | R | Espera vblank; para 3 bancos, se 0x1C003E[i]≠0x1C0042[i] copia 8 paletas×15 cores da tabela 0x2A60[i][id] para 0x2A6C[i] (cor 0 a 0). |
| 003B42 | paletas_luchadores | C | R | Paleta de 15 cores da tabela 0x3BC8[+0x2A&FF] (alternativa 0x3BEE se o id está na lista 0x3BE8 e +0x32 bit7: cores do mesmo lutador repetido) → 0x140100+0x20*i; +0x1A=0x8000+0x10*i. |
| 003BFE | decorado_por_nivel | C | R | Nível 0x1C0028 (1..; 0 e 5 nada): blocos de tiles da tabela 0x3C5A enfileirados e aplicados. |
| 003DCE | mover | C | R | jsr tabela 0x3DEA[+1]. |
| 003DF0 | mover_polar | C | R | d0=+0x1E (velocidade.l: alto=direção, baixo=módulo; ×2 na palavra baixa), 0x3E8E → dx,dy (8.8) somados a x/y. |
| 003E20 | mover_cartesiano | C | R | x+=vx*2, y+=vy*2, z+=vz*2 (8.8); vz−=g*2 (+0x22); vz mínima 0xF800. |
| 003E8E | polar_a_xy | C | R | Octante = direção>>5 (8 de 32 passos). Casos 0x3EC4–0x3F6E: um eixo = 32·v e o outro = f·v (f = 0..31 ou 32−f), com os sinais de cada octante. É uma aproximação linear (losango/quadrado): não usa seno nem cosseno. |
| 003EC4 | oct0 | C | R | (+32v, +fv) |
| 003ED8 | oct1 | C | R | (+(32-f)v, +32v) |
| 003EF2 | oct2 | C | R | (−fv, +32v) |
| 003F06 | oct3 | C | R | (−32v, +(32−f)v) |
| 003F24 | oct4 | C | R | (−32v, −fv) |
| 003F3C | oct5 | C | R | (−(32−f)v, −32v) |
| 003F5A | oct6 | C | R | (+fv, −32v) |
| 003F6E | oct7 | C | R | (+32v, −(32−f)v) |
| 003F8C | leer_mandos | C | R | d0 = ~(P2<<8 / P1) & 0x3F3F (bits 0-3 direção, 4-5 botões). O tst 0x1C001A + nop é um resto remendado. |
| 003FAE | repartir_mandos | C | R | Lê os controles e salta pela tabela 0x3FC6[0x1C0026&3]. |
| 003FCC | mandos_tag | C | R | Modo tag: P1 → dupla A (1C0100, que copia para 1C021A) se 0x1C0027 bit0; P2 → dupla B (1C0334→1C044E) se bit1. |
| 004000 | mandos_individual | C | R | Se 1C0027 bit0: 0x40C0 para 1C0100 e 1C021A; se 1C0027 bit1: 0x40C0 para 1C0334 e 1C044E. 0x40C0 lê P1, ou P2 se +0x2A bit5. |
| 00403E | mando_compartido | C | R | 0x4066 em a1 e copia +0x10D, +0x110, +0x114 e +0x116 para a2. |
| 004066 | procesar_mando | C | R | +0x10E=+0x10C anterior; +0x10D = direção traduzida pela tabela 0x40DA; +0x110 = botões (bits 4-6); +0x114 = recém-pressionados ((ant^atu)&atu); +0x112 = atual; +0x116 = OR dos pressionamentos, apaga-se a cada 4 frames (0x1C0046&3). |
| 0040C0 | mando_por_bit5 | C | R | Usa o byte de P2 se +0x2A bit5. |
| 0040EA | relaciones_4 | C | R | 0x4100 para os 4 lutadores. |
| 004100 | relaciones_luchador | C | R | Se a0 é um dos 4, copia da tabela 0x42C2 os 3 "outros" para 1C1814 e chama 0x4166 para cada um. |
| 004166 | relacion_con_otro | C | R | Com o outro objeto a1 calcula em a0, nos deslocamentos das tabelas 0x42F2–0x4316: /dx/ (±0x20 se a ação é 0xB, conforme a orientação), /dy/ e /dz/, e uma palavra de flags (lado esq./dir., frente/atrás, posição em relação às constantes 0x4332/0x4334−0xBB, bits de +0x18 e +0x2A). Copia também +0x2C, +0x3C (energia) e +0x2A&FF do outro. É a "tabela de percepção" que a IA e as colisões usam. |
| 00435C | encolar_todos | C | R | Enfileira se visíveis: os 4 lutadores (0xEA4C), 4 objetos de 0xBCB8, 10 de 0x7E22, 1C0568 e 23 objetos a partir de 1C155A (passo 0x1E). Os objetos 1C0682/78E/89A não são desenhados com a ação 1. |
| 00439A | encolar_lista | C | R | Para d0+1 ponteiros de a1: se visíveis (0x2786 CC) e não são a exceção anterior → 0x43D4. |
| 0043CA | encolar_si_visible | C | R | 0x2786 e 0x43D4. |
| 0043D4 | encolar_dibujo | C | R | Se ativo, a ação ≠0x10, +0x2C bit6=0 e a pose ≠FFFF: entrada de 16 B em 1C2094 (máx 0x40). Camada = +0x18&3; a camada 1 é refinada: bit4→4; bit7 e z≥0xBB→3; z≥0xD3→0. Há 5 baldes (tabela 0x449A, máx 0x30) e o tipo de entrada vai por +0x1C&7 (0x44AE). |
| 0044BE | entrada_propia | C | R | banco(+2), pose(+4), anim(+6), x, y, z, attr(+0x1A). |
| 0044C6 | entrada_banco_rival | C | R | Banco do rival (+0x68)+2, resto próprio. |
| 0044DA | entrada_banco_rival_anim_rival | C | R | Banco +2 do rival e anim +6 do rival. |
| 0044E6 | entrada_anim_rival | C | R | Banco próprio e anim +6 do rival (chaves compartilhadas). |
| 00450A | rng | C | R | semente(1C003A) = d0+semente+a1+a2+a4+a5+a6+d2..d7 (d1 e a3 não são somados); devolve (semente+1)>>8. |
| 00453A | esperar_vblanks | C | R | Espera d0+1 bordas de vblank (0x180009 bit0). |
| 00455C | dibujar_cubos | C | R | Se há entradas: 4 baldes (tabela 0x457E) → 0x458E; contador a 0. |
| 00458E | dibujar_cubo | C | R | Ordena (0x45AE) e converte cada entrada (0x45FC). |
| 0045AE | ordenar_y | C | R | Bolha pela palavra +8 (y) da entrada, de maior para menor. |
| 0045FC | entrada_a_sprites | C | R | sx = x−camx, sy = y+z−camy. Pose da tabela 0x6CD8[banco][pose]; deslocamentos em 1C0000/2. Para os bancos ≤7 de várias peças atribui paleta (0x46A0). Peças com 0x46F4 (máx 0x4B). |
| 0046A0 | paleta_por_banco | C | R | Procura o banco do gráfico em 0x6CD8 e o lutador que o usa → paleta 0..3 (4 se não há; 7 se o gráfico < *(0x3B87E)) em +0xC. |
| 0046F4 | emitir_pieza | C | R | Peça em 1C1AB0 + n*10; tipo pelo bit0 do primeiro byte (0x4724: 0x472C ou 0x47D2). |
| 00472C | piezas_lista | C | R | Bloco com códigos de tile explícitos. |
| 0047D2 | piezas_consecutivas | C | R | Bloco de tiles consecutivos (+1, ou +2 se for de altura dupla). |
| 004878 | pieza_x | C | R | x com flip (+2 bit7 nega o deslocamento), +9, 9 bits; recorta fora de 0x108–0x1F8 (CS). |
| 0048D4 | pieza_y | C | R | y −8 (−16 se altura dupla); recorta em 0x110 (0xD8 na demo com 1C182C=0). |
| 004934 | pieza_cerrar | C | R | Marca a peça como visível; contador++; Z se ≥0x4B. |
| 004952 | pieza_color | C | R | d3 = paleta (+0xC, ou +0xD se bit7); d4 = flips (bits do gráfico XOR +2 bits 6-7). |
| 00497C | texto_0x20 | C | R | Texto 0x23A28 (d1=0x20) e uma palavra fixa em fg0 0x806DC. |
| 004A10 | monedas | C | R | Na IRQ: moedas em SYSTEM bits 1-3 (ativo baixo) com antirrebote de 0x23 frames e 4 leituras; som 0x2F; tarifa segundo DSW1 bits 0-2/3-5 (tabelas 0x4B6A moedas, 0x4B7A créditos); créditos BCD em 1C0016 (máx 99). Se não estava em jogo (1C001A bit7=0) reinicia a pilha e salta para 0x1010. |
| 004B4E | moneda_repetir | C | R | Espera e relê as moedas (AND com a primeira leitura). |
| 004C2E | escena_attract | C | R | Cena de roteiro com 1C182C=5: inicializa (0x4D4C) e repete o passo de 1C09D2 (tabela 0x4D24) até o passo 4 (ou 9 se 1C180C bit1), com a animação do objeto 1C0AB2 (0x4E8E) e a música 0x25408 na primeira vez. |
| 004D4C | escena_init | C | R | 1C0100 em (0x98, 0x154, 0xBB) e 1C0AB2 em (0xC6, 0x155, 0xBB), ambos banco 0x10. |
| 004DCE | escena_paso0 | C | R | Anima 1C0100 (tabelas 0x4E76/0x4E82), som 0x35 no passo 3; após 9 voltas passa para o passo 1. |
| 004E8E | escena_obj_ab2 | C | R | Roteiro de 1C0AB2 por +0x2C (tabela 0x4EC6) e o desenha. Que no combate seja o árbitro está NÃO CONFIRMADO: esta cena não o demonstra. |
| 004ECE | escena_ab2_quieto | C | R | anim 8 |
| 004ED6 | escena_ab2_anim | C | R | anim 9..11 a cada 8 frames |
| 004F08 | escena_paso1 | C | R | 1C021A: bloco de tiles 0 (0x5578) e 0x20 frames → passo 2. |
| 004F48 | escena_paso2 | C | R | 1C0334: bloco 1 e 0x20 frames → passo 3. |
| 004F88 | escena_paso3 | C | R | 1C0334: som 0x46 e 2 blocos por fase (tabela 0x5086); ao terminar, passo 4. |
| 0050B6 | escena_sub_021a | C | R | Blocos 0xA/0xB alternados de 1C021A. |
| 00512C | escena_paso4 | C | R | 0x10 frames → passo 5. |
| 00516C | escena_paso5 | C | R | 3 blocos por fase (0x5246) → passo 6. |
| 00526A | escena_paso6 | C | R | 4 blocos (0x52EE/0x52FE) → passo 7. |
| 00530E | escena_paso7 | C | R | Som 0x36, blocos 0x20+n e depois a sequência 0x545E/0x5436 → passo 8. |
| 00546E | escena_paso8 | C | R | 3 blocos por fase (0x551E) e escrita em bg0 0xC0358 → passo 9. |
| 00554E | escena_paso9 | C | R | 0x20 frames → passo 0xA. |
| 005578 | encolar_bloque | C | R | Põe (d0, +0x30, +0x5C) na primeira vaga livre (FFFF) de 1C186E/78/82 (5 vagas); 0x55C6 os desenha na IRQ. |
| 0055C6 | dibujar_bloques_escena | C | R | IRQ: se 1C182C==5 desenha os 5 blocos enfileirados por 0x5578. |
| 005D80 | presentacion_combate | C | R | Música: nos combates 4/9, 0xB se o rival é 7, se não 0x10; no resto 3 (não a repete se já está tocando). Paleta 7. Combate 0 (ou 4/9 com 1C0026 bit6/bit7): modos 7/8 (0x1F434), nomes 0x62B0, posicionamento 0x5F54/0x5FDE e 0x50 frames 0x5EC4. |
| 005EC4 | presentacion_bucle | C | R | 0x51 frames: som 0x22 (público), anima os 4 (0x6192), 0x20824, nomes 0x6256 e desenho. |
| 005F54 | colocar_humano_A | C | R | Ids da tabela 0x7FE2[1C0070/1C006E] → +0x2B de 1C0100/1C021A; B = id 6; posições de 0x60EE; banco 0x10; +0x1A = paleta id&7; os ids 0, 1 e 7 são virados; paletas 3; 0x611E. |
| 005FDE | colocar_humano_B | C | R | Igual com 1C0086/84 e posições 0x6106 (lado contrário). |
| 00611E | paleta_libre_cpu | C | R | Procura o primeiro id 0..7 não usado por A e dá a B sua paleta (tabela 0x6172) em 0x140100+id*0x20. |
| 006192 | anim_presentacion | C | R | Para d0≥2: animação cíclica da tabela 0x61F6[+0x2A&7]; depois +4=+0xA, mover (0x3DCE) e desenhar. |
| 006256 | nombres_actualizar | C | R | Nos modos 7/8 redesenha o nome se 1C1833/1C1835 mudou. |
| 0062B0 | dibujar_nombre | C | R | 3 linhas de 31 tiles da tabela 0x62EE (id*0x5D + lado*0x117) em fg0. |
| 00651C | escena_fin_partida | C | R | Após perder ou empatar: limpa e carrega paletas 6/4, coloca 6 objetos (0x65EC), 0x6796, modo 6, música 0x13, 0x101 frames animando (0x680A) e texto 0x84B8. |
| 0065EC | fin_partida_colocar | C | R | Nos combates 4/9 com rival 7 troca +0x2A/+0x2B de B; 1C0122 bit7 = modo 2 e bit6 = combate 4/9 (som 0x37; se não, 0x3C); desativa a equipe correspondente; 6 objetos da tabela 0x6766. |
| 006796 | paleta_libre_extra | C | R | Como 0x611E para os objetos 1C0568/1C0682. |
| 00680A | obj_fin_partida | C | R | Roteiro por +0x2C&7 (tabela 0x6834). |
| 006848 | fin_p0 | C | R | Passo 0 do roteiro de fim de partida. |
| 0068FE | fin_p1 | C | R | Passo 1 do roteiro de fim de partida. |
| 0069A4 | fin_p2 | C | R | Passo 2 do roteiro de fim de partida. |
| 006AA6 | fin_p3 | C | R | Passo 3 do roteiro de fim de partida. |
| 006B98 | fin_p4 | C | R | Oculta (+0x2C bit6). |
| 006BA0 | efecto_publico_azar | C | R | Objeto 1C09A6: se está livre, a cada 8 frames com rng&7 contra a máscara 0x6C76 aparece numa posição da tabela 0x6C78 (conforme a câmera e rng&0x38), com a variante 0x3A ou 0x40 escolhida por rng frente a 0x6C77, e dura 6 passos de animação. São os flashes de câmera do público (confirmado visualmente pelo Emilio no arcade, 31-10-2026). |
| 006D2C | musica_combate | C | R | Em jogo: se algum humano tem índice de energia 0 (0x1CE9C) → música 8; se não, a da tabela 0x6DC0[nível] (salvo 1C1850 bit1). Só muda se for diferente de 1C182A. |
| 006DD4 | musica_nivel | C | R | d0 = 0x6DC0[nível]. |
| 006DEE | unirse_partida | C | R | Em jogo com créditos e 1C0026&0x300=0: tabela 0x6E2E[1C0027&3]. |
| 006E3E | unirse_nada | C | R | rts |
| 006E40 | unirse_P1 | C | R | Se se pressiona start (1C1A95 bit2), o parceiro livre da equipe A passa a humano (/0x21) e o modo a 0x103; gasta um crédito. |
| 006EC6 | unirse_P2 | C | R | Igual para a equipe B. |
| 006F4C | gastar_credito | C | R | 1C0016 −= 1 (BCD). |
| 006F64 | comprar_energia | C | R | Em jogo com créditos e sem modo 2: start (0x7B1E) recarrega a energia da equipe humana (tabela 0x7FEC[+0x2A&7]), 1C1850=0x80, 0x7CA6 e gasta um crédito. |
| 006FEE | energia_A | C | R | +0x3C de A = 0x7FEC[+0x2A&7]. |
| 00701E | energia_B | C | R | +0x3C de B = 0x7FEC[+0x2A&7]. |
| 00704E | pantalla_seleccion | C | R | Limpa 1C00A2, música 0xA, paleta 4, modo 4; tempo 0x180; cursores. Laço: ler (0x7240), tick ou confirmação, retratos e 1F86. Ao terminar espera 0x40/0x70 frames, marca os escolhidos (0x71B4) e escolhe rivais CPU (0x71E8), ou os de P2 no modo 2. |
| 0071B4 | marcar_elegidos | C | R | Em 1C00A2[d0], [d1]: bit7 = em combate e bit0 = já usado. |
| 0071E8 | cpu_elige_pareja | C | R | 2 vezes: rng&7 (<6), o seguinte sem bit7 nem bit0 → bit0 e guarda-se no ponteiro da tabela 0x7FD4. |
| 007240 | seleccion_leer | C | R | P1 (0x180004) e P2 (0x180006) → 0x727E; resultados em 1C0072.. e 1C0088.. (6 palavras). |
| 00727E | flancos_mando | C | R | d1 = direção (bits 0-3, ativa alta), d3 = recém-pressionadas; d4 = botões (bits 4-5), d6 = recém-pressionados. |
| 00729C | seleccion_tick | C | R | Enquanto resta tempo (1C006A) move os cursores (0x749E); se acaba, 0x7328 (a CPU escolheu). Quando todos confirmam, o tempo passa a 1. |
| 007328 | seleccion_tiempo_fuera | C | R | Tabela 0x7340[modo&3]. |
| 007350 | tfuera_m0 | C | R | Modo 0: se não está confirmado, escolha ao acaso (0x73E8); se está, fim. |
| 00736E | tfuera_m1 | C | R | Modo 1: escolha de cada controle e passagem para a dupla. |
| 0073B0 | tfuera_m2 | C | R | Modo 2: igual ao modo 0 com dois jogadores. |
| 0073DE | seleccion_fin | C | R | 1C0067 bit0 = fim. |
| 0073E8 | tfuera_azar | C | R | Escolha ao acaso do lutador (modos 0 e 2). Sem confirmar (1C0066 bit7=0): a cada 16 frames (1C0046&0xF==0) escolhe; se não, salta para mostrar. Com 1C0066 bit7 escolhe só se 1C0047 bit0=0. Escolha: d0=(RNG 0x450A + 1C0046) mod 6, repete enquanto o bit d0 de 1C0069 estiver posto (ocupado); guarda d0 em +0x14 com bit15 de 'escolhido'. Mostrar: se +0x14 tem bit15 e seu byte baixo difere de +1, põe +0xB=tabela 0x747A[(+0 & 7)*6 + d0] e chama 0x74C4; a cada 64 frames (1C0046&0x3F==0x3F) chama 0x7552. Se os 6 bits de 1C0069 estão postos o laço não termina: se isso pode ocorrer, NÃO CONFIRMADO. O que fazem 0x74C4/0x7552 (atualização de retrato/som): NÃO CONFIRMADO. |
| 00749E | cursor_estado | C | R | Tabela 0x74B4[+0x10&3]; seus estados 0x75B2/0x75B4 são rts. |
| 0074C4 | cursor_mover | C | R | Se há direção: novo índice da tabela 0x74F2[pos*16+dir] (FF = não se move); retratos 0x762A. |
| 007552 | cursor_confirmar | C | R | Se o lutador não está tomado (bit em 1C0069): marca-o, guarda o histórico e sobe +0x12; no modo de 2 jogadores o anuncia (0x1F5C). |
| 0075B2 | rts_75b2 | C | R | rts. |
| 0075B4 | rts_75b4 | C | R | rts. |
| 0075B6 | retrato_dibujar | C | R | Moldura e nome do lutador sob o cursor, com piscada a cada 16 frames se estiver repetido. |
| 00762A | retrato_borrar | C | R | Apaga os dois blocos (tabela 0x78CA). |
| 007658 | cola_7658 | C | R | Continuação: d2=0x11 (segue na rotina seguinte). |
| 00765C | bloque_fg0 | C | R | Escreve uma lista (deslocamento, tile) em fg0 com a cor d2 (0x7658 usa d2=0x11). |
| 0078FA | attract_espera | C | R | Laço de título/créditos (0x2FF frames se não há créditos): 0x879A lê os start. bit1 e 1 crédito → modo 0x8001 (1 jogador); bit0 e ≥2 créditos → 0x8101; bit2 e ≥2 → 0x203 (2 jogadores); gastam-se 1 ou 2 créditos. Textos piscantes com 0x2549E (INSERT COIN / PRESS START segundo os créditos, com um ciclo de 3) e 2 objetos animados (0x7B6C). |
| 007B1E | start_pulsado | C | R | Z = !(1C1A95 bit1). |
| 007B32 | attract_init_objs | C | R | Apaga 1C0100 e 1C021A. |
| 007B6C | attract_obj | C | R | Com rng (máscara 0x7C34) aparece na posição da tabela 0x7C66/0x7C86 e faz 6 passos de animação (0x7C36/0x7C4E). |
| 007CA6 | musica_forzar | C | R | Entra em 0x6D2C sem a verificação de dano. |
| 007CAE | barras_energia | C | R | Para cada lutador sem +0x2A bit3: apaga (0x7CD2) e desenha (0x7CF2) sua barra. |
| 007CD2 | barra_borrar | C | R | 6 entradas (0x1F, 0) no buffer da tabela 0x7D6A[i]. |
| 007CF2 | barra_dibujar | C | R | segmentos = ceil(energia/4), máximo 12, em meios tiles; os inteiros saem de 0x7D92 e o meio da tabela 0x7D7A/82/8A segundo o modo e +0x2A bit5. A barra mostra energia/4, ou seja 48 pontos = barra cheia. |
| 007D92 | barra_enteros | C | R | d2 tiles da tabela 0x7DD8/0x7DE0/0x7DF0. |
| 007E00 | borrar_objs_extra | C | R | Apaga os 10 objetos de 0x7E22 (0x10C B) e 1C1822. |
| 007E4A | crear_obj_78e | C | R | Cria a MESA dobrável que se parte em duas (objeto 1C078E, id 1, fora do ringue em 0x300,0xC8, paleta 7; gráficos banco 8, poses 0x3B402). Não é criada nos combates 4/9 (os do André), que além disso desativam a lógica de objetos. Identidade CONFIRMADA pelo Emilio (vista no arcade) e pelo render do sprite (obj78e/). |
| 007EB6 | preparar_combate | C | R | 0x7EE6 e depois 0x7FFC com 1 (modo 2), 0 (combate 0 ou equipe B humana) ou 2. |
| 007EE6 | init_luchadores | C | R | 5 objetos (tabela 0x7F9A): apaga-os conservando +0x3C e +0x2A bit13; id = 0x7FE2[seleção]; +0x2A da tabela 0x7FAE; +0xDA=3; no combate 0, energia = 0x7FEC[+0x2A&7]. |
| 007FFC | colocar_combate | C | R | Atribui controle segundo o modo (tabela 0x805A) e a energia da CPU da tabela 0x8190[nível*16 + id*2] + (1C004A&3)*8; posições iniciais (x, y, z, +0x18, anim) da tabela 0x8230. |
| 008066 | ctrl_modo0 | C | R | A humano (+0x20 parceiro no combate 0 com modo bit0); à CPU de B dá-se energia por nível e +0x2A bit3. |
| 0080F6 | ctrl_modo1 | C | R | A1 humano; B1 /0x21 e B2 /0x20 (humano P2). |
| 008110 | ctrl_modo2 | C | R | Energia por nível para a equipe A da CPU; B humano. |
| 008276 | elegir_legales | C | R | Tabela 0x828E[modo]: o lutador "legal" de cada equipe (o de +0x2A bit0, ou o outro) → 1C18AC/1C18B0; +0x2A em 1C18AA. |
| 00829E | rts_829e | C | R | rts. |
| 0082A0 | asignar_controlados_a | C | R | Tabela 0x7F9A: 1C18AC = o lutador com controle (+0x2A bit0) do par 0/1 (1C18AA = seu +0x2A); 1C18B0 = o do lado (bit1) do par 2/3. |
| 0082DA | asignar_controlados_b | C | R | Idem com os pares trocados. |
| 008314 | asignar_controlados_c | C | R | Idem: os dois com +0x2A bit0. |
| 00834E | nada | C | R | rts |
| 008350 | inicio_combate | C | R | Tempo 1C002E=0x180; 2 frames de desenho; segundo a tabela 0x84AE[combate] e o modo tag, decide que parceiro começa fora (+0x5C=7, +0x33 bit7). Depois barras, placar, música 1, som 0x3B, espera 0xC0, som 0x20 e espera 8. O sino de início é o 0x20 (amostra OKI 1: pico espectral 2.360 Hz, decaimento exponencial de 1,5 s), não o 0x3B (amostra 0x1C). O 0x21 (amostra 2, mesma frequência, sustentada) é o sino repetido de musica_combate e do fim de tempo. Foi deduzido do espectro e do contexto de chamada, sem ouvi-lo. |
| 0084B8 | texto_fin_partida | C | R | Textos 0xF, 0x10 e 0x11 de 0x23A28, cada um com 4×(1 frame + 0x206BE). |
| 00850A | fg0_rellenar_area | C | R | 14×16 células de fg0 a partir de 0x80120 = 0x1100F3. |
| 00852A | espera_fundido | C | R | 4×(1 frame + 0x206BE). |
| 00853E | continuar | C | R | Contagem regressiva do CONTINUE: 1C001C=0x10 (BCD), a cada 0x30 frames desce 1 (0x870C); uma piscada (0x85D0) anima bg0. Se pressiona start com créditos suficientes (0x8758) → CS (continua); se chega a 0 → 0x886E e CC. |
| 0085D0 | continuar_anim | C | R | Alterna os gráficos 0x2123E/0x21272 a cada 8 frames e anima tiles em bg0 0xC00C0 com a tabela 0x207F6/0x20800. |
| 0086A2 | continuar_textos | C | R | Textos de preço/número (0x2549E com a tabela 0x89A4) e 0x34. |
| 00870C | continuar_tick | C | R | Desconta o número 1C001C a cada 0x30 frames; CC ao chegar a 0. |
| 008758 | continuar_start | C | R | Lê os start (0x879A); segundo o modo (tabela 0x878E) exige o botão correspondente e cobra 0x88E6 créditos. |
| 00879A | leer_starts | C | R | d0 = bit1 P1 start (0x180004 bit7), bit0/bit2 de P2 (0x180006 bits 6/7); borda em 1C1A94; 1C1A96 = estado. |
| 0087FC | cont_m0 | C | R | Start bit1 e créditos suficientes. |
| 008820 | cont_m1 | C | R | Start bit2 e créditos suficientes. |
| 008842 | cont_m2 | C | R | Start bit0 e créditos suficientes. |
| 00886E | game_over | C | R | Nos modos 0/1: texto 0xB e 0x100 frames de animação. No modo 2 (versus) não há fim: o modo passa a 1 jogador (0x4000 ou 0x8000 segundo 1C0BC2 bit7, ou seja, quem ganhou) e 1C001F bit4. |
| 0088E6 | precio_continuar | C | R | d1 = créditos por partida (tabela 0x4B7A segundo DSW1 e 1C0015), o dobro no modo 1; compara com 1C0016 (CS se não chega). |
| 00895C | bg0_limpiar_zona | C | R | 7×8 longs de 0xC0050 a 0. |
| 008980 | fg0_limpiar_zona | C | R | 14×16 longs de 0x80120 a 0. |
| 0089A8 | demo_preparar | C | R | Demo: ids da tabela 0x8AB0[nível] (4 colunas de 10), modo 0, 0x7EB6; controles CPU (+0x2A: 0xA/0x1A/8/0x18), energias 0xFFF/0xF00/0/0, rivais fixos, parceiros fora (pos 0x260/0x3B0) e duração 1C1984=0x400. |
| 008AD8 | intro_escena | C | R | Cortina 0x25408 (d0=1) e 0x25474, apaga bg0 e sprites, modo 1C0040=5 (0x29F6), espera 8, cena 0x1F434 com d0=5, 1C180C bit1 = NOT(1C0025 bit1), cena 0x4C2E, limpa 1C180C; se 1C0025 < 4: outra cortina, espera 8 e apaga bg0/sprites. (Corrigido: 0x25408 é a cortina, não a música 1.) |
| 008C82 | luchador_update | C(A) | A | Atualização por frame de um lutador: flags CPU/humano (+0x2A bits0/1/3), 0x162A0, e despacho da ação +0x2D pela tabela 0x8CE2 (33 ações). |
| 008D66 | acc0_cpu_comun | C | R | Ação 0 (em pé) no ramo CPU/parceiro: se +0xF2 bit6, +0x5C=0; inicializa 0x911E; tabela 0x8D8A por +0x18&3 (plano: ringue, fora, poste…). |
| 008D9A | acc0_plano0 | C | R | Se +0x5C&7≠7: orientar (0x919C), zona (0x9202), pose parada (0x92BE), 0x21E5A e 0x8E7A; se é 7, 0x8DC0. |
| 008DC0 | acc0_espera_tag | C | R | +0x5C=7: orienta por zona (0x91DC/0x9202) e chama 0x19E3A. |
| 008DD8 | acc0_plano1 | C | R | jmp 0x1A532 |
| 008DDE | acc0_plano_b | C | R | Se +0x5E bit6 → ação 0x1C; se não, 0x1A830. |
| 008DFE | acc0_plano3 | C | R | Subtabela 0x8E1E[+0x5D&7] → 0x1B54A/0x1B656/0x1BBB4/0x21ED0/0x1BCB6/0x1BD5C. |
| 008E2E | apron_cpu_0 | C | R | Zona 3 / +0x5D: 0x1B54A (passear pelo avental). |
| 008E40 | apron_cpu_1 | C | R | 0x1B656 (seguir o rival pelo avental). |
| 008E52 | apron_cpu_2 | C | R | 0x1BBB4 (descer do avental). |
| 008E5A | apron_cpu_3 | C | R | 0x919C, 0x9202, 0x92BE, 0x21ED0. |
| 008E6E | apron_cpu_4 | C | R | 0x1BCB6. |
| 008E74 | apron_cpu_5 | C | R | 0x1BD5C. |
| 008E7A | tag_contador | C | R | = 0x8E7E |
| 008E7E | tag_espera | C | R | Salvo se o rival legal está na ação 0xB (modo tag) ou o lutador é +0x2A bit1: no modo tag +0x10A++ e ao chegar a 0x60 (sem tag, imediato) +0x5C=7 e põe-se a 0. +0x5C=7 → tabela CPU 0x1B40C[7] = 0x19E3A: ir ao seu córner e subir ao avental (sair por revezamento). |
| 008EC8 | acc_correr_cpu | C | R | Apaga +0xA8 bit7 e segue em 0x8ECE. |
| 008ECE | correr_cuerpo | C | R | Init (0x945C), animação (0x94CE); se +0xF2 bit7, 0x9598; mover (0x953C). |
| 008EEA | pasos_liberar | C | R | Se 1C1828 == id, 1C1828=FF (deixa livre o som de passos). |
| 008F08 | acc0_humano | C | R | Ação 0 do humano: CPU (+0x2A bit3) ou +0xF2 bit7 → 0x18E70 (IA/automático); +0x2A bit0=0 → 0x8D66; +0x33 bit4 limpa bits 2-3; tabela 0x8F58 por plano. |
| 008F68 | acc0_h_ring | C | R | Subtabela 0x8F7E[+0x5C&7]. |
| 008F9E | acc0_h_andar | C | R | Andar com o controle: direção → velocidade (0x919C, 0x924A anim, 0x9310 velocidade, 0x3DCE) ou parado (0x92BE); 0x21E5A (limites); subir ao poste (0x9738); botões 0xF78E → 0xCD2C / 0xC706 (golpes com d3=0). Se algum rival está na ação 0x17 o contador de tag não corre. |
| 009014 | acc0_h_fuera | C | R | Subtabela 0x902A[+0x5C&7]. |
| 00904A | acc0_h_fuera_andar | C | R | Igual a andar, mas com os limites de fora do ringue (0x21ED0), 0xD2D6 e botões 0xC706 (d3=1). |
| 009094 | acc0_h_apron | C | R | Só no modo tag (se não, ação 7): andar com 0x220C4 e 0x1B942; 0x90DE. |
| 0090DE | tag_relevo_fin | C | R | Se o rival legal e seu parceiro estão no plano 1: apaga +0x2A bit0 (deixa de ser legal), ação 0 e +0x5C=2. |
| 00911E | acc_init_de_pie | C | R | Primeira vez (+0x2C bit7): apaga contadores (+0x36, +0xA8, +0xBE, +0x104, +0x102, +0x9E, +0x1C, +0xC8), anim 1, zona e pose parada. |
| 009184 | anim_reset | C | R | Apaga +0x36 e +8, marca init, apaga +0xA8 e +0xBE. |
| 00919C | orientar_y_dir | C | R | +0xA = sinal(x_rival − x) (olha para o rival +0x68). Com direção (+0x10C): ângulo da tabela 0x9334 → +0x1F, CC; sem direção: velocidade 0, CS. |
| 0091DC | orientar_zona | C | R | +0xA = bit15 da entrada +0x6E[+0x6C*16]; CS se é negativa. |
| 009202 | zona_flags | C | R | +0x18 bit6 ← bit14 da entrada de zona; se é 0 e o plano coincide e entrada+4 < 8 → bit6=1. |
| 00924A | anim_andar | C | R | Ciclo de 4 frames da tabela 0x93AE (+8 se +0x18 bit6, +0x10+n*0x10 se carrega alguém, +0x5E bit6). |
| 0092BE | pose_quieto | C | R | Pose da tabela 0x9308 conforme carregue alguém (+0x5E) e +0x18 bit6. |
| 009310 | velocidad_andar | C | R | +0x20 = tabela 0x933E[id][direção] (cada lutador tem a sua). |
| 0093EE | acc_correr | C | R | CPU → 0x1BE30. Não legal → 0x8EC8. Init, e se não há automático 0xCC26 (golpe correndo, CC → segue); animação, movimento; se a direção é a oposta (tabela 0x9600 frente a +0x1F) → ação 0x14 (frear). |
| 00945C | correr_init | C | R | Só na primeira vez (+0x2C bit7): limpa +0x22/24/26/36/104/A8, +8=1, +1=1, +0x18 bit7=0; velocidade 0x95BC[id] → byte +0x21; ângulo +0x1E = 0x40 ou 0xC0 segundo a orientação +0xA bit7 (corrigido: antes dizia 0/0x80); se 1C1828 == 0xFF, 1C1828 = id (+0x2B). |
| 0094CE | correr_anim | C | R | Animação da tabela 0x95C4[id]; som 0x24 (passos) nos frames 0 e 3 só para o lutador de 1C1828. |
| 00953C | correr_mover | C | R | Move. Fora do ringue: se bate (+0x9E&3) → ação 8 sub 7. No ringue: se toca a corda do lado para onde corre → +0xA8++ e +0x2C=2 (rebote). |
| 009598 | correr_auto | C | R | 0x1B120 (controle automático); se acaba, ação 0x14 e CC. |
| 00960A | acc_rebote_cuerdas | C | R | Gira (+0xA ^ 0x80), anim 0x10, velocidade 9 que desce 1 por frame; 0x9700 marca a corda tocada em 1C1898 (plano bit0) ou 1C189A. Após 2 passos segue segundo +0xA8 (tabela 0x96A4). |
| 0096AA | rebote_seguir | C | R | Ação 1 (correr), ou 0x15 se +0xA8 bit7, com a velocidade de correr. |
| 0096F0 | rebote_parar | C | R | Ação 0, +0x5C=0, libera os passos. |
| 0096FE | nada | C | R | rts |
| 009700 | marcar_cuerda | C | R | 1C1898/1C189A bit15 e nibble = d0. |
| 009738 | subir_poste_chk | C | R | Só se +0x2A bit1: segundo o córner tocado (+0x9E&0xF <0xB, tabela 0x975C) verifica a distância <8 aos córneres (constantes 0x6D24–0x6D2A, 0x281, 0x37F) e que a direção (+0x10C) seja a diagonal correta; se o poste está livre (bit em 1C1820), ação 0xF (subir) e o reserva. |
| 009788 | poste_chk_a | C | R | Distância ao córner em y. |
| 0097D4 | poste_chk_b | C | R | Distância ao córner em y. |
| 009820 | poste_chk_c | C | R | Distância ao córner em x. |
| 00986C | poste_chk_d | C | R | Distância ao córner em x (0x281/0x37F). |
| 0098B4 | poste_esq0 | C | R | Córner 2 (direção 6/5). |
| 0098D4 | poste_esq1 | C | R | Córner 8 (direção 4/5). |
| 0098F2 | poste_esq2 | C | R | Córner 1 (direção 1/8). |
| 009910 | poste_esq3 | C | R | Córner 4 (direção 1/2). |
| 009958 | nada | C | R | rts |
| 00995A | chk_tabla_umbral | C | R | Se +0x18 bit7 e /+0x24/ ≥ 0x400 → CC. Se não, compara +0x48 com a tabela 0x999E[d0][+2]. |
| 0099BE | acc_recibir | C | R | Ação "receber/cair". Se a subação anterior +0x45 é 0x1C ou 0x13 desativa o objeto 1C0AB2 (bit7 de +0). Primeiro frame: se +0x5E bit6, o carregado (+0x60) passa a +0x2C=4. Salta para a subação +0x44 (tabela 0x9A14) com os parâmetros da tabela 0xA74A[+0x44] em a2. |
| 009AAC | rec_s0 | C | R | Gira, som 0x14 (0x27D2) e cai até o chão (z 0xBB, ou 0x80 fora) → ação 0xB (no chão) e som 0x29; animação da tabela 0x9B3E/0x9B41. |
| 009B44 | rec_lanzado | C | R | Ramo da subação arremessado: impulso (0x9BBE). |
| 009B52 | rec_lanzado_girado | C | R | Igual, mas girado. |
| 009B66 | rec_lanzado_txt | C | R | Igual, com o texto 0x9B (0x2549E). |
| 009B7E | rec_lanzado_d7 | C | R | Igual, com d7=1. |
| 009B88 | rec_lanzado_10 | C | R | Impulso 0x10. |
| 009B9A | rec_lanzado_20 | C | R | Impulso 0x20. |
| 009BBE | impulso_lanzado | C | R | x += ±d0; +0x18 bit7 (no ar); +8 de a2+0x10; som de a2+0x12 (0x23 se é o id 7 na subação 1, ou 0x12 se o rival é o 7); z += a2+0xE; anim a2+0. |
| 009CD0 | caida_cuerda_ring | C | R | Se bate na corda (+0x9E&3) → ação 8 com a subação 1 ou 2. |
| 009CFC | caida_cuerda_fuera | C | R | Fora: subação 3. |
| 009D18 | rec_rodar | C | R | Som 0x34 e o da tabela 0x9E38; avança 0x30 por passo com choque de cordas (0x9700); ao tocar o chão, ação 0xB e som 0x29. |
| 009E4C | anim_por_altura | C | R | Escolhe a anim de a2+8.. segundo a altura sobre o chão (limiares a2+2..). |
| 009E78 | empuje_ring | C | R | x ±0x10 com limites 0x21E5A; desfaz se bate (salvo poses 0x9A/0xA1). |
| 009EC2 | empuje_fuera | C | R | x ±0x20 com limites 0x21ED0. |
| 009F02 | rec_contra_cuerda | C | R | Marca a corda, z ≥ 0xCB, som 0x11, rebate (+0x24 negado); ao cair a 0xBB → 0xB e som 0x29. |
| 009F74 | rec_rebote_suelo_fuera | C | R | Velocidade z/4 negada; ao chegar a 0x80 → ação 0xB. |
| 009FCC | rec_empujado | C | R | Som 0x25/0x1D/0x1B/0x19 segundo a subação e id; avança 0x30 com choque; ao chão → 0xB e som 0x29. |
| 00A16E | rec_caer_fuera | C | R | Cai até 0x80 → ação 0xB. |
| 00A196 | rec_sobre_rival | C | R | Coloca-se sobre o rival (+0x68): x±0x10, y−2, z+0x28 (salvo +0x31 do rival =0x34) e cai (0xA230). |
| 00A230 | caida_general | C | R | Move. No ringue com corda → subação 2. Se cruza as cordas por cima (0xA39A) → passa para fora (+0x19=1, +0x33 bit0). Ao tocar 0xBB: 1C1858=0x81 (0x80 se id 7), ação 8 sub 0x20, som 0x29 se +2=7 e 0x3E (sub 0xA) ou 0x34. Fora: chão 0x80. 1C1858 = tremor de tela, confirmado em 0x1621A (0x81 = curto, 3 frames; 0x80 = 9 frames, id 7). |
| 00A358 | caida_pose | C | R | Pose 0x17, x += tabela 0xA392[id]. |
| 00A39A | cruza_cuerda_chk | C | R | Z se o lado (+0x18 bit8) coincide com a orientação. |
| 00A3BC | nada | C | R | rts |
| 00A3BE | rec_suplex | C | R | Impulso 0/−0x10 e queda; na sub 0xA anima as poses 0x9B+n com os tempos da tabela 0xA43C. |
| 00A440 | rec_vertical | C | R | Pose 0x9C, vz=0x10; ao chão: 1C1858, ação 0xB, gira e som 0x29. |
| 00A4C8 | rec_elevado | C | R | Som 0x29, vz=0x30 e +0x28=0x100; ao chão → 0xB e som 0x29. |
| 00A540 | rec_soltado | C | R | 0xA554; se termina em 0xB apaga +0x2C bit1. |
| 00A554 | rec_soltado_cuerpo | C | R | Som 8, anim 0xA2/4. Se o rival estava em 0x17 (chave) com ele, solta-o (ação 8 sub 0x13) e limpa as células fg0 0x808BC/0x808C0. Ao chão → 0xB. |
| 00A612 | rec_tumbado_por | C | R | Olha como o rival, som 0xE; cai com choque de cordas. |
| 00A6BC | rec_aturdido | C | R | Som 0x15, pose 0x14F; ao chão, som 0x29; quando +8 termina → ação 5. |
| 00A748 | nada | C | R | rts |
| 00A90E | acc_levantarse | C | R | z ao chão, pose 0x1A, tempo da tabela 0xAA00[+0xF0&7]. Ao terminar, se é CPU e está junto ao poste (zona tipo 0xC, dist <0x30/<8): com rng&0xF < tabela 0xAA20[id] sobe ao poste (ação 0xC, +0x30 da tabela 0xAA10, olha para o lado oposto ao rival); se não, ação 0 (ou 0xD se +0xF0 bit7). +0xF0 bit0 freia a velocidade 8 por frame. |
| 00AA28 | acc_bloqueo | C | R | Solta quem carrega; se não está fora (ou o rival não está em 0x31=1) e 0x995A dá CC → ação 0xA. Se não, pose 0x11 (0x12 se o rival tem +0xC1 bit0) durante 6 frames e volta a 0. |
| 00AA9C | acc_aturdido_corto | C | R | 0xC6CA, solta, pose 0x14 durante 0xC frames → ação 0xE. |
| 00AAF2 | acc_aturdido_fin | C | R | Pose 0x14/8 até terminar → ação 0 e 0xB16A. |
| 00AB1E | acc_en_suelo | C | R | Ação 0xB (deitado). Init: z ao chão, pose 0x17, ajuste contra as cordas (0xACA4). Tempo no chão +0x38 = tabela 0xAF66[índice de energia 0x1CE9C]; para a CPU divide-se por 2 se 0x1CD80 dá CS, e +0x20 se vinha de fora. Marca +0xD6 bit7 no rival e seu parceiro (podem cobrir). Humano: martelar botões (+0x116) adianta o levantar (0xAD12, limiar 0xAF6A[energia] → ação 0x19). Com +0x18 bit5 (estão cobrindo-o) vai para a saída do pin: 0xADEA o humano, 0xAE7E a CPU. Ao acabar o tempo → ação 5 (levantar) salvo que o rival esteja em 0x12/0x17/0xC-6. |
| 00ABA0 | tumbado_cpu_div2 | C(A) | A | Divide +0x38 por 2 se CPU atordoada/≥limiar. |
| 00AC88 | suelo_ajuste_x | C | R | x ±0x38 |
| 00ACA4 | suelo_chk_cuerdas | C | R | Testa os limites 0x30/8 pela frente e deixa o resultado em d7. |
| 00AD12 | suelo_machacar | C | R | Humano: cada pressionamento sobe +0x34; ao chegar à tabela 0xAF6A[energia] → ação 0x19 (levantar rápido). CPU: se o rival cai sobre ele a partir do poste (ação 0xC com uma subação da lista 0xAF76, descendo, a uma altura relativa de 0x10–0x30), com rng < tabela 0xAF82[nível][energia] (0xAF96 para o id 7) esquiva (ação 0x19), e o rival na sub 4 passa para a ação 5. |
| 00ADEA | pin_salida_humano | C | R | Humano coberto: limiar = 0xAF72[energia]/2. Se a contagem do objeto 1C0568 (+0x2F = 1C0597) ainda não o alcança, cada pressionamento (+0x114) soma; com 0x30−energia pressionamentos → liberta-se (ação 0x1E). Se a contagem chega ao limiar (e em 1C0595=2 com 1C059E≠0) também sai. Ao sair, cancela os agarres (0xC554). |
| 00AE7E | pin_salida_cpu | C | R | CPU coberta, enquanto 1C05A5 bit2 (contagem em andamento): nível de energia d1 (0xAF26). d1=6 (energia 0) nunca sai. d1=0 sai se 1C0595=2, 1C059F≥1 e 1C0570≠0. Nos demais, sai quando contagem*2+(1C059E bit0 negado) ≥ d1 e 1C059F≥2 e 1C0570≥4 → ação 0x1E e solta o rival. |
| 00AF26 | nivel_energia_pin | C | R | d1 segundo a energia: ≥0x36→0, ≥0x30→1, ≥0x24→2, ≥0x19→3, ≥0xE→4, >0→5, 0→6. |
| 00AF9A | cpu_tirada_nivel | C | R | No modo tag fora do combate 0, na primeira vez (+0x107 bit0) dá CC. Se não, rng&0xF frente à tabela 0xAFF4[nível*3 + 0x1CEF4] (CS se o sorteio se cumpre). |
| 00B012 | acc_alzar_lanzar | C | R | Desativa 1C0AB2 (bit7). Anima com as poses da tabela 0xB0EA e leva o rival em cima (pose 0x9B, x±0x28, y−1, z+4). Após 2 passos o rival passa para a ação 8 sub 0x1C e gira, 1C185A=0x81 (ativa a mensagem piscante fg0, ver 0xF844), e o texto 0x9B (0x2549E); ele vai para a ação 5. |
| 00B0F2 | acc_provocar | C | R | Fora do ringue → ação 0 e 0x8F08. Se não, alterna as poses de 0xB162 três vezes e volta a 0 (mais 0xB16A). |
| 00B16A | cpu_tras_accion | C | R | CPU: se 0x1D0E2 com a tabela 0xB188 dá CS → +0x5C=0xC (tabela 0x1B40C[0xC] = 0x1A05E: afastar-se do rival dando voltas e pedir revezamento). |
| 00B1A0 | acc_espera | C | R | Marca +0x2C bit6. |
| 00B1A8 | acc_espera_rival_1b | C | R | Espera enquanto o rival está em 0x1B; depois ação 0 e apaga +0x1C em ambos. |
| 00B1D0 | acc_forcejeo | C | R | Disputa de força (lock-up) com o rival, que deve estar na ação 0x11; se não, volta a 0. Init: velocidades a 0; +0xFF conta as disputas (sem +0xFE bits5/6); +0xAE=2; 0x16F58 e 0xB670. A direção do humano (+0x116&3) vai para +0x28. +0x26 conta frames. Se +0xAF bit1 → 0xB5C2. Janela: CPU 0x20 frames; humano 0x10 (ou 8/0x11 segundo o bit1 de +0x2A; 0x30 se 1C001A≠0). No frame 0x10, em tag (1C0026 bit1) ou com o rival CPU que ganha o sorteio 0x1CD80, entra no modo puxar/empurrar (+0xAF=3/2). Ao fechar a janela com direção → 0xB48C (ganha a chave). Se não, alterna as poses da tabela 0xB46C[id do rival] com os tempos 0xB468. Quando 0x2786 dá CS, ambos se separam 0x18 e voltam à ação 0 (+0xFF a 0 se +0xFE bit7). |
| 00B2DC | presa_tick16 | C(A) | A | Pegada: no tick 16 ganha o humano se CPU atordoada/≥limiar. |
| 00B422 | forcejeo_limite | C | R | Se +0xFF > 3 → +0xFE bit7 e CS. |
| 00B442 | forcejeo_anim | C | R | Alterna 2 poses/tempos das tabelas a3/a1. |
| 00B48C | forcejeo_resolver | C | R | O rival passa para a ação 0x10 e ele para a 0xC. A CPU escolhe a chave com 0x1E05C. O humano a escolhe pela entrada +0x28 com a tabela 0xB5B2 (lado 1) ou 0xB5BA (+4 fora); se dir bit0 e +0x10D∈{1,2,8}, usa o índice 3. Sem entrada, os dois vão para 0x8011 (+0xAF 3/2). Com a sub 0x26 → contra mútuo 0x145F2. Apaga +0xAA, +0xFE bits5–6 e +0xFF. |
| 00B5C2 | forcejeo_anim | C | R | 2 passos de 4 frames com as poses da tabela 0xB650[id do rival]; ao terminar apaga +0xAE/+0xAF bits. |
| 00B670 | forcejeo_ganador | C | R | Decide quem ganha a disputa (+0xAF bit0). +0xFE bit6 dá a vitória direta. Sem 1C001A, ganha 1C0100. Em tag, decide 1C0046 bit1. Se não, contra a CPU (rng>>1&7) com a tabela 0xB74A[nível*8] (+0x50 se +0xFF≠2); com +0xF8 bit7 ou +0xF9 bit0 do rival, ou +0xFF>3, ganha o outro. No final 0xB7EA. |
| 00B7EA | ajuste_x_limites | C | R | Testa x±0x24 com 0xB822 e copia x para o rival. |
| 00B822 | limites_x | C | R | 0x21E5A dentro do ringue; 0x21ED0 fora. |
| 00B838 | acc_presa_mantenida | C | R | Pegada sobre um rival na ação 0x13. Ao começar: som 0x2D, pose 0x105, +0x34=0xFF (−4/frame com +0x117), rival de frente a x±0x10 e 0xBBB2. Ao acabar o tempo, sub 3. Despacha +0x44 pela tabela 0xB91E. A sub 0 alterna as poses 0xBCCC/0xBCC8; com 1C1898/1C189A (por lado) bit14 = corda vibrando (0x21324) → 0x2786 → solta (os dois para a ação 0, +0x5C=0). Se o rival deixa a 0x13 → solta e ele vai para a 0xD. |
| 00B92E | presa_sub0 | C | R | A sub 0 de 0xB838: alterna 2 poses (tabelas a5/a3) e verifica 0xB988 (corda vibrando) → 0x2786 → solta (os dois para a ação 0, +0x5C=0). |
| 00B988 | presa_chk_salida | C | R | Lê 1C1898 (lado 1) ou 1C189A; com bit14, solta: o rival para a ação 0 e ele para a 0xD (CC). Se não, CS. Bit14 = a corda desse lado está vibrando (animação de 0x21324; não é uma entrada). |
| 00B9D0 | borra_objs_efecto | C | R | Com +0x5C=0, libera os objetos +0x22/+0x26 e põe +0x5C=1. |
| 00BA18 | presa_sub_golpe | C | R | Testa 0x995A(d0=2): se falha, ele vai para a ação 8, 0xC6CA, o rival para a 0. Se não: pose 0xBE+id*2−(+0xC0&1), 16 frames e depois 0xBA8C. |
| 00BA8C | presa_vuelta_sub0 | C | R | Temporizador; ao terminar, sub 0 e pose 0xBCCC[id]. |
| 00BAC2 | presa_sub_golpe2 | C | R | Como 0xBA18 com d0=3 e a pose 0x125+(id&0xF), 8 frames. |
| 00BB2A | presa_sub_final | C | R | Poses 0xBCEC/0xBD0C, 2 passos; depois solta e ele vai para a 0xD. |
| 00BBB2 | crear_objs_llave | C | R | Toma 2 objetos livres da lista 0xBCB8 (4 ponteiros) e os liga (+0x26 e +0x22) aos dois lutadores: um com pose 0 a x±0x10, e o outro com pose 0xBC a y−2/z+2. Copiam id, controle e estado. |
| 00BD10 | acc_cubrir_pin | C | R | Ação 0x17 (tabela de ações 0x8CE2: entrada 0x8D3E) = COBRIR (pin). Posta por 0x12972 ao mesmo tempo que marca o rival com +0x18 bit5 (coberto), que é o que faz passar o árbitro ao estado 2 (0xD7D8 → contagem do pin 0xDD4E). Ação de colocar-se em cima do rival (a2=+0x68, ligação mútua). Se é a CPU: +0xC6=0x80 de um lutador fixo por slot (1C02E0/1C01C6/1C0514/1C03FA). Se o rival é humano: 1C185A bit7 (mensagem fg0). Pose 0x65 (0x7F para os ids 0/4), ou 0x188 com +0x2C bit5. Posição a partir da tabela 0xBEF2[id*0x10][id do rival] (dx, dz) e y do rival−1. Ativa o objeto 1C0AB2 (pose 0x80) com a mesma posição. Ao terminar (dentro ou sem lado 1): z=0x80, ação 5, apaga 1C0AB2. |
| 00BF72 | acc_ir_a_punto | C | R | Calcula a zona com 0xC018; se é 0xFF, ação 6. Se não, +0x1E=direção e anima com as tabelas 0xC072/0xC082 (4 passos de 5 frames). |
| 00BFC4 | anim_ciclo4 | C | R | Ciclo de 4 poses (tabela 0xC072, 5 frames) e orientação (0xC082) segundo 0xC058; 0xC00A: ação 6 e apaga +0xC0 bit6. |
| 00C018 | zona_destino | C | R | Compara x e y+z com o ponto da tabela 0xC094[0xC058] e devolve a direção da tabela 0xC084. |
| 00C058 | es_bit4_ctrl | C | R | d0 = +0x2A bit4. |
| 00C09C | acc_15_correr | C | R | 0x8ECE. Na ação 0x15: +0xA8 bit7 e +0x24++. Fora (+0x19=1), após 0x15 frames a CPU faz 0x8EEA e passa para a ação 0x14. Dentro, com +0xA8&0x8001 → 0xC116; fora dos limites x 0x2F1/0x30F → ação 1. |
| 00C116 | cpu_reaccion_carrera | C | R | Só a CPU. Se o rival faz uma chave da lista 0xC2AA e está perto (hitbox dz<8, dx<0x50) → sorteio 0xC34C → ação 5 (+0xF1=3). A média distância (0x20–0x40, ou 0x40–0x68 segundo o id) → sorteio 0xC308 → ação 0xC sub 0xC326[id]. A 0x30–0x4A (0x3B para ids 4/7) → sorteio 0xC32E → +0x26 bit4. |
| 00C2B4 | tirada_nivel3 | C | R | rng&7 frente a a2[nível*3 + 0x1CEF4]. |
| 00C36A | acc_rodar_fuera_ring | C | R | Ação 0x19 (entrada 0x8D46). Postas pelas saídas do pin (0xAD3A, 0xADD2), 0x11610/0x118A6 (ao rival) e 0x12B00 (ao coberto ao terminar a contagem). Poses 0xC54C, som 0x32. Sub 0: anima dentro até +0x9F bit2 (contato com a corda) → sub 1: trepa até y<0xD8 e cai fora do ringue deitado. Se já estava fora, termina na ação 5. O nome é descritivo: o código não contém nomes de movimentos. |
| 00C3DE | c36a_sub0 | C | R | Dentro: anima 2 passos e depois ação 5. |
| 00C444 | c36a_sub1 | C | R | Despacha +0x34 pela tabela 0xC458. |
| 00C45C | c36a_trepar | C | R | Anima em laço com a física 0x3DCE; quando y<0xD8 → +0x34=1. |
| 00C4A6 | c36a_caer_fuera | C | R | y−8, z+8, som 7 (0x27D2), +0x18 bit7, pose 0x16, +0x19=1 (fora). Cai com 0x3DCE; ao chegar a z<0x80 → ação 0xB (deitado) com bit1 e +0xAE=0. No ramo de fora, anima com os limites 0x21ED0 e depois ação 5. |
| 00C554 | tag_cambio_control | C | R | Com o lado bit1: alterna +0x33 bit1. Se os dois são humanos e 1C0026&3≠1: troca o bit0 de controle entre ele e seu parceiro (a1) e apaga +0x10C/+0x110/+0x114/+0x116. Calcula se o parceiro está na tela (câmera 1C002A/1C002E) → +0xF2 bit7 (fora da tela) e bit6. |
| 00C628 | acc_deslizar | C | R | +0x22=2; freia +0x20 em 4 por frame com 0x3DCE e a pose 0xB. Contra a corda (+0x9E&3): dentro → ação 2 (+0xA8=2); fora → ação 8 sub 7. Parado: conta +0x23 e passa para a ação 0; +0x5C=1 se +0xF2 bit7 e não 1C0026 bit0. |
| 00C6C8 | nop | C | R | rts. |
| 00C6CA | sonido_44_2b | C | R | Som 0x44, ou 0x2B com +0x2A bit4 (modo 1C0026 bit1) ou bit3 (CPU). |
| 00C706 | humano_golpe_boton | C | R | Com o botão +0x116&3 na ação 0, ou na 0xC com sub<9 e a tabela 0xCC1C. Com +0x5E bit6 (carrega alguém): sub da tabela 0xCB16. Se não, a tabela 0xCADE (0xCAFE fora)[id][deslocamento+botão]. Deslocamento segundo o rival (tabela 0xCB1A[ação do rival]): +0xC se está deitado perto (0xFE), +6 na frente (<0x20/0x28) ou +9 atrás (<0x30/0x38), com dz<0x18. 0xFF → ação 1 e reinicia a entrada. Ajustes das subs 6/9 e 0xC9E2/0xCA4E. Ação 0xC; a sub 4 liga o rival na ação 0x10 (salvo que o parceiro o esteja segurando, ação 0x17); 0xE462. |
| 00C9E2 | chk_sub3_alcance | C | R | A sub 3 só vale com o rival a dx<0x70 e dz<0x10, de frente, e o rival na ação 1/2/0x15/0x16; se não, restaura a ação (d4=0x80). |
| 00CA4E | cpu_chk_alcance | C | R | CPU (ou humano na sub 0x10): se está a menos de 0x70 (0x30 na sub 0x10) em x e 0x10 em y, olhando-se, e o rival não está nas ações 1/2/0x15/0x16 → +0x2C=d6, d4=0x80. Sub 0x10 com o rival com energia ≥0x16 → +0x30=3. |
| 00CC26 | cpu_boton_a_sub | C | R | Com um botão em +0x116: sub = tabela 0xCD14[id*3+botão−1] e ação 0xC; 0xCC8A; CS. |
| 00CC8A | chk_golpe_por_cuerdas | C | R | Se ele está dentro e o rival fora (sem bit4), dz<0x20 e do lado correto: testa x±0x80 com 0x21E5A; se toca a corda e dx<0x100 → +0x30=0x35. |
| 00CD2C | chk_cuerdas_salir | C | R | Despacha +0x9E&0xF (<5) pela tabela 0xCD48. |
| 00CD5C | cuerda_lateral_izq | C | R | Sem 1C1898 bit6, com a direção 7 no lado 1 e y+z em 0x1E0–0x230 → ação 3 (+0xAC=0). O humano de equipe precisa de 12 frames (+0x102). Sem bit4/lado e dentro → ação 6. CS. |
| 00CDF8 | cuerda_lateral_der | C | R | Simétrica: 1C189A, direção 3, +0xAC=1. |
| 00CE8E | cuerda_frontal | C | R | Direção 5 com x 0x280–0x380 → ação 3, +0xAC=2. CS. |
| 00CEC2 | cuerda_no | C | R | Apaga +0x102 e CC. |
| 00CECC | acc_cruzar_cuerdas | C | R | Ação 3: trajetória da tabela 0xD0AE (0xD1AA para o id 7)[+0xAC] (+3 se +0x19=3), com passos (pose, dx, dy). Ao começar copia os parâmetros para +0x22..+0x28 e 0xD00A. Entre os passos d0 e d1 salta (voo com 0x3DCE, +0x18 bit7) até z<0x80. Ao terminar: ação 0, +0x5C=0, z=0x80; 0xD04A. |
| 00D00A | cuerda_interp_x | C | R | Salvo com +0xAD 2/5: x = x0 ± (y−y0)/6 (corda em diagonal). Se não, y=y0. |
| 00D04A | marca_pose_especial_id7 | C | R | Id 7: se a pose está na lista 0xD092 (2 entradas), 1C1A92 bit7 = 1 e 1C1A93 = +0x18 bit0; se não, apaga o bit. |
| 00D2D6 | humano_salir_ring | C | R | Com contato +0x9F e a direção (+0x10C=7/3, sem 1C189A/1C1898 bit6) e y+z em 0x1A0–0x210 → +0xAC=0/1 (+3 com bit4/sem lado) e ação 4 (7 se +0x19=3; 0x20 se carrega alguém). Corda frontal: bit3, direção 1, x 0x280–0x380 → +0xAC=2. CS. |
| 00D400 | acc_entrar_ring | C | R | Sequência guiada pela tabela 0xD54C[+0xAC&0xF] (0xD646 para o id 7): (pose, dx, dy) por passo; +0x19=3 salvo na entrada 2. Ao terminar: +0x19 /= tabela 0xD52E, volta à ação 0 e, em tag com o parceiro dentro, texto 0x9B. |
| 00D7D8 | arbitro_elige_estado | C | R | Árbitro (1C0568), salvo no estado 4 com id 1. Toma o lutador ativo (lado bit1) de cada equipe: 1C0100/1C021A e 1C0334/1C044E. Estado novo: 2 se algum está coberto (+0x18 bit5); 3 se algum está fora (+0x19=1) ou na ação 4; 1 se algum faz a sub 0x13/0x2E (ação 0xC) ou a ação 0x1B (guarda o lutador em 1C05D0); 0 em outro caso. Se muda, escreve-o em +0x2D e apaga +0x2C. |
| 00D8F4 | arbitro_e0_seguir | C | R | Vai ao ponto médio entre os dois lutadores (0xDFE0), com y forçada a 0x175 ou 0x118 segundo o lado de 0x148. Direção com 0x270C (1C004E→1C0052), velocidade 8. Se o destino muda de lado: +0x3D bit4 e o quadrante em +0x3C → contorna pelas cordas com a tabela 0xDB44. Olha para o centro; se está a mais de ±4, move-se (0x3DCE) e anda (0xDA38). Limites 0x21E5A. |
| 00DA38 | anim_8dir | C | R | Animação de 4 frames a cada 8 ticks; escolhe a pose por direção (+0xA em 8 setores) na tabela 0xDAC4 (0xDB04 no estado 3, ou o 4 com controle 2). |
| 00DB54 | arbitro_rodear_q0 | C | R | Contorno: y mínima 6D26+0x38−0xBB (sai do bit4); com contato +0x9F bit0 → direção 0x80, se não 0xC0. |
| 00DB8E | arbitro_rodear_q1 | C | R | Igual com +0x9F bit1 → 0x80/0x40. |
| 00DBCE | arbitro_rodear_q2 | C | R | Com +0x9F bit3 termina; bit0 → direção 0, se não 0xC0. |
| 00DBF8 | arbitro_rodear_q3 | C | R | Com +0x9F bit3 termina; bit1 → direção 0, se não 0x40. |
| 00DC22 | arbitro_e1_vigilar | C | R | Vai junto ao lutador +0x68, a x±0x30 (lado segundo x≥0x300), e quando chega (±4) alterna as poses 0x12/0x13 a cada 4 frames, olhando-o. |
| 00DD4E | arbitro_e2_cuenta_pin | C | R | Contagem do pin: aproxima-se do ponto médio (±0x20 x, ±0x30 y) e depois dá batidas com as poses da tabela 0xDED4 e as durações 0xDEDC (laço dos passos 2–3). No passo 3, frame 1: +0x2E++ e 0xE02C (mostra/soa a contagem). Ao chegar a 3: escreve o resultado em 1C0BBE+4 e 1C0BD6+4 (bit6/bit7 segundo que lado está coberto, a1+0x18 bit5). |
| 00DEE4 | arbitro_e3_cuenta_fuera | C | R | Contagem fora do ringue em BCD (abcd) até 0x20 (20). Olha para o lutador que está fora (+0x18&3=1). Cada ciclo da animação: +1 e 0xE02C. Ao chegar a 20: 1C0BBE+4 / 1C0BD6+4 bit7 se esse lutador está fora (+0x18&3 ∈ {1,3}), se não bit6. Permite a dupla desqualificação por contagem fora. |
| 00DFDE | arbitro_nop | C | R | rts (estado vazio da tabela 0xD7AE). |
| 00DFE0 | punto_medio | C | R | a2 = ponto médio entre a2 e a1 (x e y). |
| 00E016 | arbitro_reset | C | R | Apaga +8, +0x36, +0x2E, +0x2A e +0x18. |
| 00E02C | sonido_texto_estado | C | R | Som da tabela 0xE0A8[+0x2E] (salvo 0xFF, ou no estado 3 com +0x2E<4), texto 0x9B e o texto de 0xE086[+0x2E]. |
| 00E132 | obj_nop | C | R | rts. |
| 00E134 | obj_seguir_portador | C | R | Copia a posição do portador (+0x60) com x±0x10 e sua orientação. |
| 00E172 | obj_reposo | C | R | Pose 0xE1B6[id]; 0xE1BC; na primeira vez, 0xE7E8. |
| 00E1BC | obj_ofrecerse | C | R | Para cada lutador (tabela 0xE224) que esteja fora (+0x19=1) e sem carregar nada: se é o objeto mais próximo em x, marca-o como disponível (+0x5E bit7, +0x60=objeto, +0x64/+0x66 distância). |
| 00E234 | obj_romper | C | R | Som 0x28; x±0x20, z+0x20; 5 passos de pose (0xE2B8) e desaparece (apaga bit7 de +0 e 1C1823 bit1 ou bit2). |
| 00E2CC | obj_lanzado | C | R | Voo com 0x3DCE (velocidades 0xE374), pose 0xE37C[id] (+2 segundo o lançador +0x18 bit6). Ao cair (z<0x80): som 0x27, ação 2 e volta a estar disponível (+0x5E bits 7/6). |
| 00E388 | obj_caida_desp | C | R | Despacha +0x44&1 pela tabela 0xE39E. |
| 00E3A6 | obj_rebote | C | R | Trajetória 0xE45A; pose 6/0xA (1 para o id 0). Ao cair: som 0x27, ação 2 sub 3. |
| 00E462 | recoger_objeto | C | R | Procura entre os 3 objetos (1C0682, stride 0x10C) um na ação 2, na mesma z, dentro da caixa 0xE542 e disponível. A CPU só pega seu alvo (+0x60). Se o encontra: ação 0x1D, ligação mútua por +0x60, +0x5F=id do objeto, +0x5E bit6 e o objeto para a ação 1. Se não: a CPU põe +0x5C=0. |
| 00E572 | acc_coger_obj | C | R | A CPU vai para 0x1CC36. O humano: 0x9184 e 2 passos de 8 frames, pose base da tabela 0xE5F0[+0x5E&3]; depois ação 0. |
| 00E5F6 | acc_soltar_obj | C | R | A CPU vai para 0x1B326. Se não: 2 passos de 8 frames e depois a ação 4 (0 sem lado). O objeto passa para a ação 2, a x±0x20, disponível; apaga +0x5E bit6. |
| 00E6E0 | crear_obj_2 | C | R | Cria o objeto 1C089A (id 2, 0x8002, ação 5, disponível) na posição de 1C078E com z+0x20 e x±0x20; 1C1823 bit2. |
| 00E76E | soltar_obj_682 | C | R | O objeto 1C0682 aparece onde ele está (z+0x20, x±0x20), ação 5; 1C1823 bit2; apaga +0x5E bit6. |
| 00E7E8 | obj_evitar_pared | C | R | Desloca x segundo a tabela 0xE874 (0xE880 na ação 2) com os limites de fora 0x21ED0; se bate (+0x9E&3), desfaz. |
| 00E88C | zonas_todos | C | R | Para os 10 objetos da tabela 0xEA4C (salvo o árbitro) chama 0xE8A6. |
| 00E8A6 | calc_zona_18 | C | R | Salvo nas ações 3/4/6/7 recalcula os bits 0–4 de +0x18. bit0: x ≤ [0x4332]. bit1: y+0xBB < [0x4334]. bit2/bit3: córneres/avental segundo as caixas 0xEA34 (lado 1) ou 0xEA40 (sem bit2, apaga +0xE3 bit0). bit4: +0x18&3=1 com y+0x80 ≤ 0x158. |
| 00EA74 | elegir_rival | C | R | Com 1C001A≠0 e fora dos estados da tabela 0xEBCC/+0xC8: toma os dois rivais possíveis da tabela 0xEBBC[slot] e despacha pela zona +0x18 (tabela 0xEAF0). Preferência: o que segura (0x17) ou faz a sub 6, o não coberto, o que está na mesma zona, o do lado ativo. Escreve +0x68 (rival), +0xA0 (o outro) e +0x6C (0/1). |
| 00EB00 | elegir_rival_z0 | C | R | Preferências de 0xEA74 para a zona 0 (ver lá). |
| 00EB60 | elegir_rival_z1 | C | R | Escolhe por coincidência do lado bit1. |
| 00EB72 | elegir_rival_z2 | C | R | Escolhe o de lado bit1. |
| 00EBA0 | cmp_bando | C | R | Compara o bit1 de +0x2A (lado) de a0 e a2; ramos da tabela 0xEAE6. |
| 00EBEE | acc_subtabla_b8 | C | R | Salta por +0xB8 para a tabela 0xEBFE. |
| 00EC12 | acc_subir_esquina | C | R | Sobe ao córner (+0x19=2) por passos da tabela 0xED20 (0xED40 para a CPU id 2, que além disso alonga +8 do rival deitado para 0x40). Lado/posição por +0xB4 (cópia de +0x18) com 0xECB8 e 0xECE2. Ao terminar, +0xB8=2 (3 para a CPU no lado bit1). |
| 00ECB8 | esquina_tablas | C | R | Seleciona as tabelas de pose (a2) e posição (a3[id]) segundo +0xB4>>8&3; y a partir da tabela. |
| 00ECE2 | cpu_id2_sonido22 | C | R | CPU id 2: com d0=5 (ou 3 se +0xB4 bit1) → +0xE2 bit0 e som 0x22. |
| 00F018 | acc_bajar_esquina | C | R | Percorre os passos ao contrário. Ao terminar: z=0xBB, ação 0, +0x5C=0, libera seu bit de 1C1820 (+0x34), +0x19=+0xB5. Se é humano sem controle bit0, +0x5C=7. |
| 00F098 | esquina_paso | C | R | Pose, x e z do passo d0. A CPU id 2 no lado não-bit1 gira a partir do passo 5. |
| 00F0DE | esquina_esperar | C | R | A CPU vai para 0x1C47E. O humano despacha pelo córner (+0x18&3) com a tabela 0xF100. |
| 00F110 | esquina_q0 | C | R | Olha para 0x80, pose 0x1F, posição 0xF280. Com controle: remapeia a direção (tabela 0xF6BA → +0x10D) e 0xF35A; se não, 0xF2B0. |
| 00F15E | esquina_q1 | C | R | Igual olhando para 0 com a tabela 0xF6C4. |
| 00F1AC | esquina_q2 | C | R | Olha para 0, pose 0xF0DA[+0xBE&1]; sem direção põe 4 (ou 8 com +0xBF bit0); 0xF35A → 0xF2FA, 0xF2B0. |
| 00F218 | esquina_q3 | C | R | Igual olhando para 0x80, direção 6 (ou 2). |
| 00F280 | esquina_posicion | C | R | x, y, z da tabela 0xF6CE[córner]; +0x5C=0x7F (tempo máximo no córner). |
| 00F2B0 | esquina_chk_bajar | C | R | Humano: a direção 5 (ou 1 no lado bit1) → +0xB8=1 (descer). Se não, decrementa +0x5C; em 0 (ou sem controle) → descer. |
| 00F2FA | esquina_elige_salto | C | R | Se não está nas ações 3/4/6/7: segundo o rival (ou +0xA0 se não é o do lado) a y≥0xDD → +0xB8=3, se não 4 (salvo poses 0x69/0x1F). |
| 00F35A | esquina_boton | C | R | Despacha pelo córner com a tabela 0xF37A. |
| 00F38A | esquina_boton_q0 | C | R | Com um botão em +0x114: 0xF636, 0xF684 e a tabela 0xF3A6. |
| 00F3B6 | esquina_boton_q1 | C | R | Igual com a tabela 0xF3D2. |
| 00F3E2 | esquina_boton_q2 | C | R | Igual (ou com +0xBA bit7) com a tabela 0xF406. |
| 00F416 | esquina_boton_q3 | C | R | Igual com a tabela 0xF43A. |
| 00F44A | dir_rotar_mas | C | R | +0x10C++ circular 1..8. |
| 00F466 | dir_rotar_menos | C | R | +0x10C-- circular 8..1. |
| 00F47A | salto_destino_q0 | C | R | Tabela 0xF6FE → 0xF498. |
| 00F482 | salto_destino_q1 | C | R | Tabela 0xF721. |
| 00F48A | salto_destino_q2 | C | R | Tabela 0xF746. |
| 00F492 | salto_destino_q3 | C | R | Tabela 0xF76A. Comum: destino do salto em 1C00B4 (+0x16 x+dx, +0x18 y+dy, +0x14) segundo a direção +0x10C; +0xB6=1; +0x10=−1; continua em 0xF564. |
| 00F4DA | cpu_objetivo | C | R | Escreve o alvo em 1C00B4: rival (+0x10), x/y; se está a ≥0x30, o destino é ±0x30 a partir dele (+0x10 = −1). z do rival para +0xBE. Despacha por +0x30 com a lista 0xF594 e a tabela 0xF59C. |
| 00F636 | esquina_salto_sub | C | R | Sub da tabela 0xF6E6[id*3 + (rival não deitado)]; ação 0xC; libera seu bit de 1C1820. |
| 00F684 | const1 | C | R | d0=1. |
| 00F68A | b8_sub_pose68 | C | R | Pose 0x68 durante 8; ao terminar, +0xBE^=1 e +0xB8=2. |
| 00F78E | tag_chk_relevo | C | R | Dentro, do lado, com um botão (+0x115), no córner (+0x18 bit2, sem +0xE3 bit0), com o parceiro no córner bit2, e a 0x150 (0x108 com bit4) ±0x10. Se o parceiro está fora (+0x19=3) e na ação 0: os dois +0x2A bit2 e ação 0x1A (revezamento). CC. |
| 00F81A | esquina_ocupada | C | R | CC se o bit da tabela 0xF840[córner] está posto em 1C1821. |
| 00F844 | flash_fg0 | C | R | Com 1C001A≠0, gerencia 1C185A. bit7 → passa a bit1 com um temporizador de 3 (1C185B). bit1: a cada 2 frames alterna bit2 e desenha o texto 0x1E/0x1F (0x23A28); com bit6 apaga as células fg0 0x80B04–0x80B18. bit0: apaga 9 linhas de fg0 a partir de 0x80B04 e põe 1C185A a 0. Então 1C185A=0x81 é uma mensagem piscante em fg0 (o texto 0x1E/0x1F), não um tremor. |
| 00F94C | acc_0c_llave | C | R | Ação 0xC: 0x240B6 (chaves por sub); dentro, se bate na corda, 0xF9B0. Despacha +0x30 pela tabela 0xFB58. Ao sair da 0xC apaga +0x33 bit3 dos dois. |
| 00F9B0 | llave_fuera_ring | C | R | Se o rival não está na ação 0x10 → ação 8 sub 1. Segundo a subação +0x31: 0x1B/0x21/0x22/7 colocam os dois em x=0x280/0x390 (segundo +0x9F bit0) e lhes dão a ação 8; 0x29 e 0x28 são variantes desse posicionamento. |
| 00FC4C | nop | C | R | rts. |
| 00FC4E | despacho_id | C | R | Chama a tabela 0xFC64[id]. |
| 00FC84 | sub_combo_golpes | C | R | A CPU vai para 0x15758. Três passos da tabela 0xFD70 (0xFD88 para o id 7; 0xFD7C/0xFD94 com +0xC0 bit0). Nos passos 0xB/0xC acumula os botões em +0x22. Com o botão 1 alterna +0xC0 bit0 e repete (combo); se não, ação 0. |
| 00FDA0 | sub_combo_golpes2 | C | R | Como 0xFC84, com a tabela 0xFE88 (0xFEAC para o id 2) e 10 passos. Nos passos 0x10/0x1C alterna +0xC1 bit0 e verifica o botão 1 para encadear; acumula +0x114 em +0x22 salvo nos passos 0/0xC/0x18. Sem botão: ação 0. |
| 00FED0 | sub_golpe_simple | C | R | Três passos da tabela 0xFF3A (0xFF4A com +0x2A=7); no passo 0xC termina se +0xC9 bit2. Depois ação 0. |
| 00FF5A | sub_proyeccion_salto | C | R | Se o rival é o id 7: rival para a ação 0xC sub 0x1E, ele para a ação 0x10, e executa-se 0x14CFC como o rival (contra-ataque). Se não: gira, 0x14222, +0x5C=1 se +0xFC; rival para a ação 0x10. Animação da tabela 0x10136[id do rival]+passo, durações 0x1013E/0x10146. Passo 2: som 0x50, 1C183E bit7, salto (+0x22=0x40, z+0x10). Passo 4: ele para a ação 5, o rival para a ação 8 sub 0x1F pose 0x1CF a x±0x40, +0x3E=0xC, 0x161C8, +0xF6+=3, 0x15B90. Na queda (z≤0xBB): 1C1858=0x80 (tremor) e som 0x48. Com +0x5C: 3 repetições e 0x145F2. |
| 01014A | sub_embestida | C | R | Pose 0x1D0 e voz 3 (0x27D2); +0x18 bit7. Se conecta (+0xC9 bit3 e o rival +0xC9 bit4 ou +0x40=−2): som 0x2F e +0x34=1 (com o rival). Move-se (0x3DCE, 0x1600C); se bate na corda: ação 8 (e o rival também se +0x34). Ao acabar os passos (durações 0x10340): ação 5 a x±0x30; se +0x34, o rival para a ação 0xB pose 0x17. Ao cair (z≤0xBB, ou 0x80 fora): som 0x34 e tremor; sem conectar, ação 8 sub 0x22 pose 0x1CF; se conectou, rebote (passo 6, velocidade /4, +0x28=0x200). |
| 01031C | anim_tablas_a2a4 | C | R | Pose/tempo a partir de a2/a4[+0x36] (a2 = 0x10348 se +0x34 = 0). |
| 01037E | sub_salto_voz_b | C | R | Como 0x103A8 com a voz 0xB. |
| 0103A8 | sub_salto_aereo | C | R | Salto com a tabela 0x104FE e a voz 1; +0x18 bit7. Avança ±8 com os limites dentro (0x21E5A) ou fora (0x21ED0). Ao bater na corda: ação 8 sub 2 (ou 3 fora, se vai em direção a essa corda). Ao cair (z ≤ 0xBB, ou 0x80 fora): pose 0x15F, som 0x29 (0x48 fora), passo 0x10. Ao terminar: ação 5 e gira. |
| 01050E | sub_salto_hacia_rival | C | R | Igual a 0x103A8, mas orienta-se como o rival, coloca a trajetória com 0x156FA (tabela 0x1599C, ±0x20) e 0x110E4 (velocidade 0x180/0x180) em direção ao rival. |
| 01055A | sub_golpe_rival_8_9 | C | R | Três passos da tabela 0x105D0. No passo 4 apaga +0xC9 bit5 e, se o rival está na ação 8, iguala-lhe o x. Depois ação 0. |
| 0105DC | llave_lanzamiento_A | C | R | Se 0x14222 dá falha (+0xFC≠0), o rival contra-ataca (ação 0xC sub 0x1E). Se não, 4 passos de pose (tabela 0x106F8[id do rival]) com som 0x2F; no final o rival passa para a ação 8 sub 1, dano +0x3E=8 (0x161DA) e +0xF6 += 3. |
| 0107CA | chk_caer_sobre_rival | C | R | Se está no mesmo plano que o rival e o rival está deitado (0xB) ou seguro (0x17), e z ≤ chão+0x10: pose 0x1D2, coloca-se sobre ele com a tabela 0x10920[id] (orientação). Se está deitado: rival para a ação 8 sub 0xD, +0x3E=1 e 0x161EC; se não, 0x108E2 com o parceiro. Se não: ao chegar ao chão d0, ação 5. |
| 0108B0 | copiar_8w | C | R | Copia 8 words de a6 para a1. |
| 0108E2 | soltar_llave | C | R | O rival passa para a ação 8 sub 0x13; cancela os agarres (0xC554). |
| 010950 | sub_levantarse_rapido | C | R | Começa no passo 0x10 da tabela 0x10A4A (continua em 0x10976). |
| 010976 | sub_rodar | C | R | Rola com a tabela 0x10A4A: +0x20=0x11 velocidade, +0x1E direção (±0x40). A partir do passo 0x10 freia 2/frame. Com a corda: fora → ação 8 sub 3; dentro, se vai em direção à corda → ação 2 com +0xA8=2. Em 0x14 termina: ação 0. |
| 010A5E | sub_salto_esquina_ataque | C | R | Ataque a partir do córner/ar. Trajetória da tabela 0x11150[id*16 + ar*8 + variante] (com a sub 0x1A, segundo a zona x≥0x300/y<0x120) colocada com 0x156FA. +0x34 = 1 a partir do córner (2 no lado bit1); +0x5C=1 se o rival está mais acima ou (id 6 com a sub 0x11). Com +0x34, 0x110E4 (0x200/0x100). O id 1 no chão dobra a velocidade. Em voo: se o rival está deitado no mesmo plano e a z chega a +0xF4+0x10 → 0x10FCC. Se chega ao chão sem rival: ação 8 sub 5, tremor 0x81, pose 0x1CF (0x14F id 7), som 0x34, +0x3E=2 e 0x16488 (humano). Se impacta (passo 4): rival para a ação 8 sub 0xD, +0x3E = 5/0xA/+1 id1/0xB sub 0x1A/6 sub 0xF/0xC id 7; 0x161C8, tremor, som 0x49, 0xC6CA do rival; o id 1 acrescenta a voz 8 e rebate (0x10EA8). Ao terminar: ação 5, apaga 1C0AB2/1C144E. |
| 010EA8 | sprite_efecto_144e | C | R | Objeto efeito 1C144E (0x8000) junto ao lutador: y−2, z+6, pose 0x1CC, +3=1. |
| 010F04 | ajuste_y_impacto | C | R | id 0 sem +0x5D bit0: y+0xA e 0x1152A. Para o id 1 com +0x5C, a sub 0x1A sem +0x5C ou o id 6 com a sub 0xF: y+2. |
| 010FCC | chk_impacto_aereo | C | R | Caixa do rival: tabela 0x11084[id] (x±, com margens 0x10/0x30 segundo a orientação; y±8). Ponto de impacto do atacante: tabela 0x110A4[id*2+córner]. Se está dentro: passo 4 (impacto) e som 0x22 (0x23 para os id ≥ 6). |
| 0110E4 | cpu_ajuste_vel | C | R | Limita a velocidade em direção ao rival: dx<0x60 (±0x40 se está deitado) e dy<0x50/0x70. |
| 01143A | llave_10a5e | C | R | bsr 0x10A5E |
| 01152A | sprite_efecto_0ab2 | C | R | Objeto efeito 1C0AB2: y−0xA, x∓4, z+0xA, pose 0x7D, orientação invertida. |
| 011598 | sub_presa_intento | C | R | Se o rival está coberto: ação 0. A CPU rival sorteia 0x450A contra a tabela 0x11726[dificuldade 1C0028 + 0x1CE9C]; se resiste, ele vai para a ação 5 e o rival para a 0x19. Se não: rival para a ação 0x10, pose 0x31+id*3, 3 passos (duração 0x11724). Depois os dois para a ação 0x11 (disputa de força: +0xFE bit6 / bit5), +0xAA = +0x3C+0x30 (0x50 CPU), poses −1, de frente. No modo 1C0026 bit1, com 1/4 de probabilidade, +0x2C bit4 nos dois. |
| 01173A | sub_pisoton | C | R | Dois passos da tabela 0x118BC; no passo 4: 0x1185A e 0x1179A. |
| 01179A | pisoton_impacto | C | R | Mesmo plano. Se o rival está deitado: ação 8 sub 0xD, som 0x49, 0xC6CA, +0x3E=1 (3 se +3=7), 0x161DA, +0xBF++ (máx. 4). Se o rival segura (0x17): 1C185A=0x81, ação 8 sub 0x13, apaga o coberto do parceiro; os que tenham +0x33 bit1 → 0xC554. |
| 01185A | pisoton_rival_levanta | C | R | No modo 1C0026 bit1 (ou CPU), rival deitado sem cobrir: sorteio 0x450A contra a tabela 0x118B6[+0xBE] → o rival passa para a ação 0x19 (levanta-se) e apaga +0xBE. |
| 0118D8 | despacho_id2 | C | R | Salta para a tabela 0x118EC[id]. |
| 01190C | sub_salto_cubrir | C | R | Salto em direção ao rival: 1C00B4 com a altura da tabela 0xBEF2[id][id do rival], velocidade 0x380/0x50, gravidade 0x4000/0x80, destino +0x68, 0x15B40 → +0x14, 0x159AC. Quando desce: pose 0x64; se o rival está deitado dentro, sem cobrir e ele não está fora, com z<0xC3: ação 0x17 (cobrir), rival +0x18 bit5 e +0x68=ele; 0x11BC6 e, se não CC, 0x129A4. Se não: ao chão, ação 8 sub 0. |
| 011A72 | sub_cubrir | C | R | Coloca-se sobre o rival (x da tabela 0xBEF2[id][id do rival], −4 para o id 4; z de +8), pose 0x7E (id 0/4) ou a tabela 0x11BBE. No passo 8, se o rival está deitado dentro, sem cobrir e ele não está fora: ação 0x17 e cobrir como em 0x1190C. Se não, tenta de novo. No passo 0xC: ação 0. |
| 011BC6 | cubrir_chk_kickout_inmediato | C | R | Só o modo normal (não 1C0026 bit1; com bit0, 1C0029≠0) com +0x107 bit0: sorteio 0x450A&0xF contra a tabela 0x11C30[dificuldade*3 + 0x1CEF4]. CC/CS invertido (CS = cobre). |
| 011C4E | sub_lanzar_por_encima | C | R | Agarra (0x14222), o rival na frente a ±8. Se o rival é o id 7: ação 0xC sub 0x34 (contra). Poses 0x11E1E[id do rival]+passo (passo 5 pose 0x20E), 4 frames (8 com +0x5C). Passo 2: som 0x50, 1C183E bit7, +0xF6+=3. Passo 5: rival para a ação 8 sub 0x1E a ±0x80, pose 0x1CF. Passo 6: ele para a ação 5 (x∓0x20), +0x3E=0xC, 0x161C8, tremor, 0x15B90, som 0x34. Com +0x5C: 3 repetições e 0x145F2. |
| 011E2E | sub_golpe_cabeza | C | R | Com +0xFC: contra (rival para a ação 0xC sub 0x1E, 0x14CFC). Poses 0x11F52[id do rival]+passo, durações 0x11F62. Passo 1: som 0x49. Passo 2: ele para a ação 0; rival para a ação 8 sub 1 pose 0x15 a x−0x10; som 0x50, 1C183E bit7, +0xF6+=3, 0x15B90, +0x3E=8, 0x161C8. |
| 011F66 | sub_suplex | C | R | Com +0x30 bit7: 0x1229C (o rival, na pose 0x1C3, levanta-se e volta à ação 0). Com +0x2C bit0 (rival id 7, contra): 0x1214C, sequência 0x1AD–0x1B1 em que o rival a inverte, ele para a ação 8 sub 1 (+0x3E=6, 0x16488, som 0x2F) e o rival para a ação 0xC sub 0x8010. Se não: os dois de frente, rival para a ação 0x10; poses 0x12324[id do rival*6]+passo, durações 0x12316. Passo 3: voz 0x1C, salto z+0x10, som 0x50, 1C183E, +0xF6+=3; voo 0x3DCE até o chão (passo 4). Passo 6: tremor, som 0x34, rival para a ação 8 sub 5 pose 0x1CF, +0x3E=0xC, 0x161C8. Passo 7: ação 5 (x∓0x20). |
| 012354 | sub_llave_sumision | C | R | Chave de submissão de várias fases: 1C185A=0xC0 e despacha +0x34 com a tabela 0x1238E. |
| 01239E | sumision_f0 | C | R | Poses 0x125D2[id do rival]+passo, 12 frames por passo; após 3 passos, fase 1, som 0x51, 1C183E bit7. |
| 012404 | sumision_f1_forcejeo | C | R | Cada botão do rival soma +0x5D; se supera a tabela 0x124D6[0x1CE9C], fase 2 (escapa). Se não: alterna poses a cada 8 frames; cada ciclo, +0x3E=4 e 0x161C8 (dano). Aos 6 ciclos escapa. Com +0x3C (energia) a 0 e os dois do lado: fase 3 (rendição). |
| 0124DA | sumision_f2_escape | C | R | Retrocede os passos; ao terminar, ele para a ação 8 sub 1 pose 0x15, o rival para a ação 0xD pose 0x18, 1C185A=0xC1. |
| 01255C | anim_objeto_id | C | R | Pose = tabela 0x125DA[id do rival] + +0x37; após 2 passos, 0x16210 e prioridades 1C0BC2/1C0BDA (0x40/0x80 segundo +0x18 bit4). |
| 0125F0 | sub_salto_codazo | C | R | Salto colocado com 0x156FA (tabela 0x12A7C, +0x10 se o rival é o id 7); a sub 0x35 o deixa fora (+0x19=1). Ao descer, se o rival está deitado no mesmo plano: 0x12A9C e, perto do chão (+8), impacto (rival ação 8 sub 0xD, +0x38+=8, +0x3E=0xC ou 8 sub 0x35, 0x161C8; rebote +0x28=0x300, som 0x48, tremor, 0xC6CA). Após o rebote tenta cobrir (dentro e do lado): ação 0x17 (+0x2C byte 0x20), rival 0xB, +0x18 bit5, 0x11BC6/0x129A4. Ao falhar no chão: ação 8 sub 5 (0x25 id 4), +0x3E=4 e 0x16488 (humano), som 0x34. Poses das tabelas 0x12A52 (id 4) / 0x12A60 segundo a altura. |
| 0129A4 | cubrir_iniciar_cuenta | C | R | Ao cobrir: se +0x33 bit1 → 0xC554 com o parceiro. Se o coberto tem energia 0 (+0x3C) ou o parceiro não pode (CPU +0x106 bit1 / humano +0x107 bit0, 3/16 de probabilidade) → sem salvamento. Se o parceiro humano não é CPU: 0xAF9A; se não CC, 0xC554 e +0xC6 de quem cobre = 2/bit7 (aviso de salvar). CPU: 0x1B7FA do parceiro e apaga +0xC6. |
| 012A9C | kickout_salto_cpu | C | R | Só uma vez (+0x2C bit0): se o rival é CPU, a sub 0x35, está abaixo a menos de 0x30 e não está coberto: sorteio 0x450A contra a tabela 0x12B0C[0x1CE9C] → o rival rola (ação 0x19). |
| 012B10 | sub_correr_cuerdas | C | R | Corre até a corda (direção 0x40/0xC0 segundo x≥0x300, 0x1979C, poses 2+passo). Ao chegar a 0x298/0x328 rebate (+0x5C=1). Se o rival não está deitado, ação 0x14. Se não: velocidade da tabela 0x95BC[id], volta correndo e em 0x288/0x378 salta (ação 0xC sub 0x35). Poses 0xA+passo. |
| 012C9E | sub_voltereta_atras | C | R | Pose 0x17F+passo, durações 0x12D2C, velocidade 0x10 para trás; 4 passos e ação 0. Cordas com 0x12DB0. |
| 012D30 | sub_voltereta_adelante | C | R | Pose 0x14B+passo, durações 0x12DAC; 4 passos. 0x12DB0. |
| 012DB0 | chk_cuerda_rebote | C | R | Dentro: se bate na corda (0x21E5A) → ação 2 (+0xA8=2). Fora: (0x21ED0) → ação 8 sub 3. |
| 012DEE | sub_golpe_encadenable | C | R | Pose 0x15F+passo (tabela 0x12E76), acumula +0xC8 em +0x5C. Ao terminar: com +0x5D bit3 e o rival não na ação 8, ação 0xC sub 0 (encadeia); se não, ação 0. |
| 012E7A | sub_carrera_hombro | C | R | Investida (tabela 0x1302E, velocidade 0x10). Se conecta (+0xC9 bit3 e o rival bit4 ou −2) antes do passo 0x10: pose 0x1D2+id do rival, 8 frames, +0xC9 bit4, +0x35 bit0 (passos extras), de frente; o id 1 soa 0x50. No passo 0xC solta: rival para a ação 8 sub 0x17. Choque com a corda: dentro → ação 2 (e o rival sub 2); fora → ação 8 sub 3. No final, o id 1 com impacto chama 0x15B90. |
| 01304E | sub_salto_patada | C | R | Voz 5, +0x18 bit7, chão +0xF4 = 0xBB (0x80 fora), tabela 0x1310C. Em voo (passos <8): 0x3DCE e 0x1600C; se bate na corda, ação 8 sub d0. Ao chegar ao chão: pose 0x61, som 0x2D. Ao terminar: ação 0. |
| 013114 | sub_dropkick | C | R | Tabela 0x132B8, velocidade 0x20 para a frente (0 se ele mesmo é o id 4, Bossman). Para conectar antes do passo 4 é preciso +0xC9 bit3 e que o rival tenha +0xC9 bit4 ou +0x40 = −2; então: pose 0x1DE+id do rival, de frente, +0xC9 bit4. No passo 8 solta: o rival para a ação 8 sub 0x10, z+0x30, pose 0x9B, +0x2C bit0 (y = a sua +3 se +3=4). Cordas (como 0x12E7A): dentro → ação 2 com +0xA8=2; fora → ação 8 sub 3; o rival recebe o mesmo. Freia 2/frame. |
| 0132C8 | sub_bulldog_salto | C | R | Rival para a ação 0x10. Pose 0x23E+id do rival*5, durações 0x134CC. Passo 2: som 0x51, 1C183E. Passo 3: voz 4, salto +0x18 bit7, z+0x20. Voo (0x3DCE, 0x1600C); se bate na corda, os dois para a ação 8 sub d0 com a mesma velocidade. Primeiro contato com o chão: som 0x34, tremor, rebote. Segundo: +0x3E=0xB e 0x161EC; dentro e do lado → cobre (ação 0x17, rival +0x18 bit5, 0x11BC6/0x129A4); se não, ação 5. Rival deitado (0xB) atrás a ±0x20 com pose 0x17; ele pose 0x65. |
| 0134D2 | sub_slam | C | R | Agarra (0x14222) e põe o rival na frente (−0x10). Poses 0x13956[id do rival*0x1E], durações 0x13938. Rival id 7: sequência de contra (0x1C6–0x1C9) em que o rival o derruba (ele para a ação 8 sub 0 pose 0xF2, +0x3E=6, 0x16488, som 0x2F) e o rival volta à ação 0 com +3=7. Com +0xFC (rival resiste): poses alternativas +0x12 e 0x145F2 no passo 0xC. Normal: passo 2 giram; passo 0xC som 0x50 (0x51 id 6), 1C183E, +0xF6+=3, voz 0xC, salto; passo 0x10 rival para a ação 8 sub 0x12 pose 0x16 (x deslocado pela tabela 0x13918), tremor e som 0x34; passo 0x12: +0x3E=0xC, 0x161EC, ação 5, 0x15B90. Ao descer (z<0xBB) passo +2. |
| 0138CA | contra_llave | C | R | O rival passa para a ação 0xC sub 3 (pose 0x105D0); ele para a ação 8 sub 9; +0xC9 bit5. |
| 013A46 | llave_slam | C | R | Pose 0x1DD + 6*id do rival, voz 6. Passo 3: som 0x50, 1C183E bit7, +0xF6 += 3. Passo 4: ao tocar o chão, dano 0xC ao rival (0x161EC), 1C1858=0x80, som 0x31. Passo 6: ele para a ação 5, o rival para a ação 8 sub 0x21 pose 0x1CF a ±0x30. Com +0xFC≠0 (contra) usa as tabelas 0x13C64/0x13C70[id do rival*0xC]; ao chegar ao passo 0xC → 0x138CA e dano 6 a si mesmo (+0x3E=6, 0x16488). O bloco de 0x13C24 (dano 7 ao rival) é código morto: só é avaliado com passo <0xC. |
| 013CD0 | sub_golpes_repetidos | C | R | Rival de frente; poses da tabela 0x13E44[id do rival*10], 4 frames por passo (0xD se o rival é o id 7 (André) e o passo +0x37 < 3, ou seja, passos 0 e 2). Com +0x5C bit7 (posto por 0x13DF6) repete os passos 0–2 e conta em +0x5D; com +0x5D=2 ao começar o passo 0 → 0x145F2. Passo 6: rival para a ação 8 sub 0xA pose 0x9B, +0x3E=6, 0x161FE, a ±0x30 e z+0x20. Passo 0xA: ação 0. |
| 013DF6 | cpu_id7_tirada | C | R | Se o rival é a CPU com id 7: tabela 0x13E40[energia] contra rng&7 → +0x5C bit7. |
| 013E94 | sub_body_slam | C | R | Agarre: x−0x20 (salvo com +0x2C bit5, que entra no passo 2 com 0x14204) e 0x14222; o rival na frente (+0x10). +0x108 bit6 sem id 7 anula a resistência +0xFC. Tabelas de duração 0x14108 e de pose 0x14124[id do rival*0x1C] (+0x10 se resiste). Passo 6: som 0x50 (0x51 id ≥6), 1C183E, +0xF6+=3. Passo 8: salto e voz 0xD. Ao cair: passo 0xC, som 0x34, tremor. Passo 0x10: ele para a ação 5, rival para a ação 8 sub 0xE pose 0x1CF (−0x20), +0xAE=0, +0x3E=0xC, 0x161DA, 0x15B90. Se resiste: passo 0xC → 0x145F2. |
| 0140E8 | anim_a3a4 | C | R | Pose/tempo a partir de a3/a4[+0x36]. |
| 014204 | agarre_reposicion | C | R | Variante de 0x14222 com a tabela 0x14378 (0x143DC CPU) para entrar a partir do passo 2; continua no corpo comum em 0x1423E. |
| 014222 | llave_tirada_exito | C | R | Sucesso da chave: tabela 0x14346 (0x143AA para a CPU) + (1C0029>>1&0xF)*0xA, +5 se o DIP 0x180002 bit3=0. Índice pela contagem +0xDC/+0xDD (máx. 4), segundo se +0x31 está na lista 0x14338. Se rng>>1&7 < tabela e ≥ a sequência +0xCC/+0xCD (com o id 7 só as subs 0x18/0x32), soma à sequência e dá +0xFC=0; se não, +0xFC=1 (falha e o rival contra-ataca). |
| 01440E | sub_backbreaker | C | R | Igual ao body slam com as tabelas 0x1465E (durações) / 0x14676[id*0x18] (poses), x−0x20, o rival a +8. Passo 4: som 0x50, 1C183E, +0xF6+=3. Passo 8: som 0x31. Passo 0xA: rival para a ação 8 sub 0xF pose 0x15 a ±0x30, z+0x10, +0x3E=0xC, 0x161DA. Passo 0xC: ação 0 e 0x15B90. Se resiste (+0xFC, tabelas +0xC): passo 0xC → 0x145F2. |
| 0145D2 | anim_paso_a3a4 | C | R | Duração (a4) e pose (a3) do passo +0x36. |
| 0145F2 | contra_llave_mutua | C | R | Põe no rival a pose da tabela 0x1464E[id]. Os dois passam para a ação 0xC sub 0x26 (+0xAE 1/0), um de frente para o outro. |
| 014736 | sub_golpe_corto | C | R | Pose 0x183+id do rival*2, 0x10 frames; passo 1 som 0x31. Passo 2: ele para a ação 0; rival para a ação 8 sub 1 pose 0x15 a +0x10/+0x14, +0x3E=0xC, 0x161DA. |
| 01481C | sub_sumision_b | C | R | Chave de submissão: rival para a ação 0x10, som 0x51, 1C183E, 1C185A=0xC0. Com +0x114 do rival ≠0 a partir do passo 2, cada frame soma +0x35; se supera a tabela 0x124D6[0x1CE9C do rival], escapa. Poses 0x149AA[id do rival]+passo, durações 0x149A2; cada ciclo (passos 2–3) +0x3E=4 e 0x161C8 ao rival, +0x5C++. Se os dois têm +0x2A bit1 e o rival tem +0x3C=0: 0x16210 (rendição) e o resultado em 1C0BC2/1C0BDA (0x40/0x80 segundo +0x18 bit4). Escape ou 6 ciclos terminam igual (0x14950): o rival para a ação 8 sub 0x15 pose 0x16 por cima (z+0x40), ele com a sub 0x3A, 1C185A=0xC1. |
| 0149B0 | llave_B | C | R | Poses da tabela 0x14A82[id do rival] (stride 0x14). Passo 2: som 0x51 e 1C183E bit7. Passo 4: som 0x31. No final, o rival passa para a ação 8 sub 0x15 (z+0x10) com dano 0xB (0x161FE), e 0x15B90. |
| 014AFA | llave_C_aerea | C | R | Tabela 0x14C5C[id do rival*0x14] (pose+duração .l). Passo 1: som 0x51 e 1C183E. Passo 3: o rival para a ação 8 sub 0x10 (x±0x50, z+0x30, pose 0x9B) com dano 0xA (0x161FE). Passo 4: salta (+0x18 bit7, z+0x10, velocidades a 0, +0x22=0x20) e ao cair a 0xBB (0x80 fora) passa ao passo 5 com pose 0x17 (0x10 frames) e x+0x10. Passo 6: ação 5 e 0x15B90. |
| 014CFC | sub_contraataque_llave | C | R | Executa-a quem contra-ataca (chamada com a0 = o rival a partir de 0x152BC quando 0x14222 falha): gira, pose 0x20+id do rival*2 (+1 por passo), o rival colocado com a tabela 0x14DD0. Passo 4: o rival para a ação 0x15 sub 0, ele pose 0x30, +0x1C=0 nos dois. Passo 6: ação 0 (+0x5C=0xD se é CPU). |
| 014DD6 | sub_forcejeo_presa | C | R | Disputa do agarre: +0x28=0x80 frames, +0xDE = tabela 0x150E0[id&7] (tempo da CPU). Poses 0x150F6[id do rival*6], durações 0x150F0, alternando. Se não é CPU, 0x14FEE (entrada do humano); a CPU, ao esgotar +0xDE, 0x1E432. Com +0xAF bit0 (é a vez do outro): 0x14F00. Se 0x2786 dá CS (ruptura): os dois para a ação 0. |
| 014F00 | presa_contra_humano | C | R | Se +0x114≠0, não é CPU, +0x2A bit1, dentro, e o rival está no passo 2/4 de +0x37, uma só vez (+0x108 bit7): sorteio 0x450A&7 na tabela 0x14FD8 (só se o rival é CPU e 1C0029 < 2) ou 0x14FE0 (resto). Com 0xFF: sub da tabela 0x14FE8[id], ação 0xC, rival para a 0x10 (sub 0x1E contra o id 7), a sub 0x21 recua 0x20, +0x2C bit5 e +0x108 bit6 (salvo com a sub 0x1E). |
| 014FEE | presa_entrada_humano | C | R | Humano com +0x28<0x70 e botão 1/2: sub da tabela 0x15126[id*3 + botão−1], ação 0xC, rival para a 0x10, separação ±8/∓0x10. Com +0x28=0: 0x1507C para ele ou para o rival (+0xAF bit0). |
| 01507C | tag_relevo_o_llave | C | R | Se 1C0026&3 = 2: ação 0xD e o parceiro (a3) para a ação 0 a x±0x30. Se não: ação 0xC sub 0x27, o rival para a 0x10. |
| 01513E | sub_presa_cabeza | C | R | Pose 0x82+id*3 alternando com as tabelas 0xB46C[id do rival]/0xB468, 0x20 frames. Ao terminar, 0x145F2 a partir do rival e rival +0x2C bit6. Ruptura com 0x2786 → os dois para a ação 0. |
| 0151F8 | sub_empujon | C | R | Pose 0x150F6[id do rival*6], 7 frames; depois ação 0, 0x19D1A, 0x15288; o rival para a ação 0xD a ±0x34, com os limites do ringue. |
| 015288 | cpu_tras_llave | C | R | Com a ação 0 e 0x1D0E2 (tabela 0x152A4) → +0x5C=0xF (tabela 0x1B40C[0xF] = 0x1B486: ir para junto do parceiro que cobre, para quebrar/proteger a contagem; sem parceiro cobrindo → 0). |
| 0152BC | llave_D_salto | C | R | 0x14222 (se falha, contra-ataque 0x14CFC). Poses 0x154BC/0x154AE, som 5. Passo 1: som 0x50, 1C183E e +0xF6+=3. No ar cai a 0xBB; o primeiro quique (vz 0x300) dá dano 0xC, som 0x34 e 1C1858=0x80. No final, o rival para a ação 0xB (deitado, pose 0x17) e ele para a 5. |
| 01552C | sub_salto_voz2 | C | R | Salto com a tabela 0x155EA, voz 2, +0x18 bit7. Voo (0x3DCE, 0x1600C), corda → ação 8 sub d0; ao chegar ao chão (0x155C0), passo 0xC; em 0x10, ação 0. |
| 0155C0 | aterrizar | C | R | Se cai (+0x28<0) e z ≤ d0: z=d0, passo 0xC e a sua pose. |
| 0155FA | sub_golpe_objeto | C | R | Golpe com o objeto: som 0x25 (0x26 com +0x5F). Tabela 0x156C8[+0x5E&3*0xC] (3 sem +0x5E bit6). Se conecta (+0xC9 bit3) despacha +0x5E&3 pela tabela 0x15692: 0 → 0xE76E (solta o objeto), 1 → 0xE6E0 e +0x5F=2. |
| 01569E | golpe_obj_0 | C | R | 0xE76E. |
| 0156A6 | golpe_obj_1 | C | R | 0xE6E0 e +0x5F=2. |
| 0156B4 | soltar_portado | C | R | O objeto carregado (+0x60) passa a +0x2C=3; apaga +0x5E bit6. |
| 0156FA | salto_preparar | C | R | Copia o bloco a6 para 1C00B4 (0x108B0), destino +0x68, 0x15B40 → +0x14, 0x159AC (calcula velocidades). Orienta, pose (a2), +1=2, +0x18 bit7, +0xF4 = 0xBB/0x80. |
| 01578E | cpu_combo_id | C | R | CPU (via 0x15758, tabela 0x1576E por id): golpes da tabela 0x15860 (0x15878 se 0x1CD80 dá CC e sem +0xF9 bit0), 4 bytes por passo. Termina ao passar do passo 0x18 (0xC para o id 7 André: combo mais curto). No passo 0x10 continua só se a entrada da tabela +0x6E do rival (+0x6C) tem +9≠8, /dx/<0x40 e /dy/<8; se não, termina. Ao terminar: o id 7 com o rival na ação 0xA passa para a ação 0xC sub 8; o resto, ação 0. |
| 015890 | golpe_rapido | C | R | Golpe em passos de 4 (tabela 0x15944, ou 0x15960 para a CPU que perde o sorteio 0x1CD80, sem +0xF9 bit0). No passo 0xC (índice 3): se o estado do rival tem entrada ≠0 na tabela 0x1597C, salta para o passo 0x18 (finalização); se não, termina. O passo 0x14 e o ≥0x20 terminam (ação 0). Ou seja: golpe de 3 passos, mais 2 passos de finalização se o rival está num estado da tabela. |
| 0159AC | calc_trayectoria | C | R | Bloco 1C00B4: +0 dx, +2 dx contra o deitado, +4 dy, +6 z extra, +8 vz, +0xA gravidade, +0xC/+0xE máximos de vx/vy, +0x10 alvo (−1 = ponto fixo +0x16/+0x18), +0x14 z de destino. Simula a parábola (+0x28 −= +0x22 a cada frame, mínimo −0x800) até descer à z de destino, conta os frames e põe +0x24/+0x26 = distância·256/frames, limitado. |
| 015B40 | z_destino_salto | C | R | Tabela 0x15B70[zona própria*8 + zona do rival*2]. |
| 015B90 | cpu_provocar | C | R | Dentro e CPU: se 0x1CEF4≠0 e o sorteio 0x450A&0xF < tabela 0x15BE4[id] → ação 0x12 (provocação). |
| 015BEC | llave_E_secuencia | C | R | Chave por fases (+0x36/+0x37) com as tabelas 0x15E7A/0x15EB2/0x15EE2/0x15F12, de stride 8 por id do rival. Na fase 2: som 0x50, 1C183E e +0xF6+=3. Na fase 8 lança o rival (ação 8 sub 0xA, dano 0xD, z+0x40). Durações com rng&7. Se 0x14222 falha (ou o rival é o id 7), termina na contra mútua 0x145F2. |
| 015CC8 | warrior_33 | C(A) | A | Movimento 0x33 do Warrior (giros, ver NOTES). |
| 015F1A | sub_rival_lanzado_id | C | R | Coloca-se no rival (x, y; a cópia de z é um no-op: move $14(a1),$14(a1)), pose 0x209 e a tabela 0x15FFC a cada 0xC frames. Passo 0xC: rival para a ação 8 sub 9 pose 0x9B, +0x3E=6, 0x161C8, a ±0x1E e z+0x10. Passo ≥0xE: ação 0, pose 0x1A, x+0x15. |
| 01600C | chk_cuerda_d0 | C | R | d0 = 0 sem choque, 2 = corda dentro, 3 = grade fora. |
| 01603E | sub_esperar_tumbado | C | R | Pose 0; se o rival está deitado, ação 0. |
| 016062 | sub_entrar_ring | C | R | Se o rival está dentro: +0x19=0, pose 0x105, avança a tabela 0x160CC[id], 8 frames; depois ação 0 com +0x19=3 (avental). |
| 0160D4 | sub_carrera_hacia_rival | C | R | Com +0x2C bit4 → 0x10A5E. Se não, corre (0x911E, 0x9202, 0x1617C, 0x1979C, 0x924A, 0x3DCE). Com a corda → ação 0xC sub 0x11. A uma distância de 0x50–0x5C na frente do rival: se está deitado → +0x2C bit4 (salto); se não, ação 0. |
| 01617C | dir_hacia_rival | C | R | +0x1E = 0x40 / (orientação do rival invertida); inverte-a se está a ≥0x5C na frente. |
| 0161C8 | danio_a1 | C | R | 0x16488 sobre a1. |
| 0161DA | danio_a2 | C | R | 0x16488 sobre a2. |
| 0161EC | danio_a3 | C | R | 0x16488 sobre a3. |
| 0161FE | danio_a4 | C | R | 0x16488 sobre a4. |
| 016210 | rendicion | C | R | Mostra o letreiro fg0 1 (0x2660E com d0=1). |
| 01621A | temblor_pantalla | C | R | 1C1858 bit7 ativa o tremor: 9 frames (3 se bit0, ou seja 0x81 = curto). Soma a tabela 0x16286[frame] a 1C002E (scroll vertical); ao terminar, apaga 1C1858. |
| 0162A0 | procesar_impacto | C | R | Recebe o golpe (0x16340 filtra; +0xC9 bit0 = golpeado). +0x40 = reação pendente: 0xFFFE → 0x16468, ação 0x10 (agarrado), +0xC9 bit4. Agarre mútuo com a ação 0xC sub 0x14 → o outro +0x40=−1. Se não: 0x16468, 0x1638E (dano extra), ação = +0x40 (a 9 se o golpe é a sub 1 e está fora), 0x16488 (aplica o dano), 0x16538. +0x46 temporiza o combo +0x48. |
| 016340 | filtro_impacto | C | R | Tabela 0x1636C[ação]: 0 = aceita; negativo = ignora o golpe; positivo = ignora só com sub ≠0 (+0x31). |
| 01638E | danio_extra_tumbado | C | R | Se a vítima está na ação 1/0x15/0x16: +0x3E += tabela 0x1642A[sub do atacante]&0x7F. Reação 9/0xA (salvo com as subs 0x14/0x28/0x15) → 8; com o atacante no estado 7, sub 0x23, e se não, +0x45=1. Com +0xF9 bit0 do atacante, dano ×2. |
| 016468 | soltar_si_tumbado | C | R | Ação 1/0x15/0x16 → 0x8EEA. |
| 016488 | aplicar_danio | C | R | +0x3C −= +0x3E (mínimo 0; se já é 0 não muda). Som 0x22 (0x23 se o banco gráfico +2 do atacante é ≥6: DiBiase e André) salvo com as subs 0/1. Com a tabela 0x164FA[sub] = 0xFF (ou a vítima id 7 André com a sub 0x1F) → +0xF0 bit7 (golpe forte). |
| 016538 | limpia_f0_por_estado | C | R | Se a tabela 0x1655C[estado] é 0, apaga +0xF0 bit7. |
| 01657E | colisiones_bucle | C | R | Laço de colisões: limpa +0x40 dos 4 lutadores; percorre os 6 pares (0x165B2), 0x165FE, se estão perto (0x16634): 0x16716 (caixas) e 0x1675C (impactos nos dois sentidos). |
| 0165B2 | siguiente_pareja | C | R | Pares (i<j) da lista 0xEA4C (4 lutadores); CS ao terminar. |
| 0165FE | reset_mascara_golpe | C | R | Se a pose mudou (+6 &0x3FFF vs +0x42): +0xCE=0 (máscara de quem já golpeou). |
| 016634 | pareja_cerca | C | R | CC se /dx/<0x60, /dy/<8, nenhum na ação 0x10, nem na 0x1F sub 1, sem +0x2A bit2, os dois com +0x2C bit7 e sem bit6, pose ≠ −1, 0x166FC sem ruptura, os dois com +0x19<2 e iguais. |
| 0166FC | chk_ruptura_pareja | C | R | 0x2786 para os dois. |
| 016716 | cajas_pareja | C | R | a1/a4: caixas de golpe dos dois (0x1672C). |
| 01672C | caja_de_pose | C | R | Tabela 0x1761E[pose&0x3FFF] → a lista de frames [+2]; pose −1 → 0x18076. |
| 01675C | impactos_pareja | C | R | Nos dois sentidos: 0x16796 (golpe); CC → 0x16CF4 (som/combo); CS → 0x172AA, que repete enquanto continuar dando CS (caixas múltiplas, +0xCA). |
| 016796 | chk_golpe | C | R | Nenhum com +0xC9 bit4/5 nem +0x40 −1/−2/−4, os dois ativos, o atacante com prioridade (a1+0) ≥ a defesa (a3+0; 0x20 com 0x1688E), 0x16D9C (ainda não o golpeou), caixas não nulas (0x18BF2/0x18AFE), sobreposição em x (0x16C60) e z (0x16CA8), golpe ≠ 0x18C72, tabela 0x172FA[pose da vítima] ≠ 0xFF. Então (0x168B6): reação e sub da tabela de golpes (+2 se olham para o mesmo lado, ou seja, a vítima de costas; +0xC8 bit1 = 1 se estão de frente, 0 se de costas), +0xC9 bit3 ao atacante, ajustes 0x169C2/0x16AA0/0x16BD2/0x16C04/0x16C14/0x16AD4/0x16B2A, 0x16B6A (contra). Com −4: 0x17136; com −2 (agarre): os dois ligados (+0x68), 0x17228/0x17240 e o objeto do agarrado para a ação 4. Dano = a1+1 em +0x3E (0 à CPU com as subs 0/1). +0xC0 bit0 = lado, +0xC9 bit0, 0x16DD2. Se falha: 0x16E48/0x16FAA/0x16DF8 (choque corpo a corpo). |
| 01688E | prioridad_defensa | C | R | Se a vítima tem a sub 3 e o atacante a 0/1/8: d0=0x20. (Após o rts, em 0x168B6, segue o corpo de 0x16796.) |
| 0169C2 | ajuste_reaccion_id7 | C | R | Vítima id 7 (André) nas poses 0x18/0x19, ou qualquer vítima com a reação 0xF2 → 8. Reação 0xF1 → 0xA (9 para André). Reação 8 contra André: se o atacante está deitado (ação 1/0x15/0x16) e não tem a sub 0x20, o atacante passa para a ação 8 sub 1 e André para 9; com as subs 0x2A/0x16/0x20/0x17/0x12/0xD do atacante → 0xA se o seu +0x44=1, se não 9; resto sem mudanças. |
| 016AA0 | ajuste_sub15_cpu | C | R | Sub 0x15 contra o estado 7 com dificuldade ≥2 → reação 0xA, +0x48=0. |
| 016AD4 | ajuste_id7_accionC0 | C | R | Id 7 na ação 0xC sub 0: vítima com +1=2 ou a ação da lista 0x16B20 → 8; se não, 0xA. |
| 016B2A | ajuste_id7_accionC8 | C | R | Id 7, ação 0xC sub 8: com +1=2 → 8; com a ação 0/9 → 0xA. |
| 016B6A | chk_choque_golpes | C | R | Reação com a sub 9: se a ação da vítima está na lista 0x16BCC (ou a 0xC com a sub 0xE/0x14), anulam-se (os dois 4 frames, ligados, +0xC9 bit5) e devolve CS. Se não, CC (continua). |
| 016BD2 | ajuste_F0 | C | R | Reação 0xF0 → 8; o atacante +0x116=0, +0x22=0, +8+=0xC (o id 4 avança o passo +4). |
| 016C04 | ajuste_sub20 | C | R | Sub 0x20 → +0x44 da vítima 0x23. |
| 016C14 | ajuste_sub31_id7 | C | R | Sub 0x31 contra o id 7 (não deitado nem nas poses 0x18/0x19): o atacante para a ação 8 sub 1, a vítima para a reação 9. |
| 016C60 | solape_x | C | R | Sobreposição de caixas em x (caixa: +0 offset, +1 largura). |
| 016CA8 | solape_z | C | R | Sobreposição em z (+2 offset, +3 altura). |
| 016CDE | x_caja | C | R | x da caixa segundo a orientação. |
| 016CF4 | sonido_y_combo | C | R | Ação 1 → som 0x48. Ação 0xC: som da tabela 0x175CE[sub] (0x30 para o id 1 com a sub 0); combo da vítima +0x48 += tabela 0x17590[sub] (+0x46=0x30); se a vítima é CPU dentro e o atacante não tem +0xF8 bit7 nem +0xF9 bit0, também +0xF6. |
| 016D92 | acumular_mareo | C(A) | A | Soma dano a +0xF6 (medidor de tontura); ver NOTES s66. |
| 016D9C | chk_ya_golpeado | C | R | CS se o bit da vítima (0x8000>>índice em 0xEA4C) está em +0xCE. |
| 016DD2 | marcar_golpeado | C | R | Põe esse bit em +0xCE. |
| 016DF8 | chk_choque_cuerpos | C | R | Ação 0/9 dos dois, 0x16E7E e 0x16F12 → os dois para a ação 0x11 (choque), apaga-se +0xC9 bit0, 0x170BA/0x170F0. |
| 016E48 | chk_bandos_opuestos | C | R | CC se a0 e a2 são de equipes diferentes (1C0100/1C021A frente a ≥1C0334). |
| 016E7E | chk_choque_validable | C | R | CC se são de lados diferentes (+0x2A bit12), nenhum carrega objeto (+0x5E bit6), estão na mesma zona +0x19 (se os dois estão fora, +0x19=1, além disso devem ter o mesmo +0x2A bit1) e a ação de a2 o permite segundo a tabela 0x1760C (<0x10; negativo = não, 0 = sim, positivo = só com a sub 0/1 de a2; a ação 0x1F vale salvo com a sub 1 do atacante). |
| 016F12 | chk_cuerpos_cerca | C | R | CC se /dx/<0x20 (<0x28 entre dois id 7) e /dy/<0x10. |
| 016F58 | centrar_pareja | C | R | Coloca os dois no ponto médio (x, y) e em orientações opostas. |
| 016FAA | chk_agarre_carrera | C | R | O atacante na ação 0 e a vítima correndo (0xD) ou rebatendo (0xA) de frente: ele passa para a ação 0xC (+0x2C bit5) com a sub da tabela 0x170B2[id] (0x1E contra o id 7), e a vítima para a 0x10. Fora, ou CPU em frames alternados (1C0046 bit1): sub 0x1E sem bit5. Id 6 com dificuldade <2: sub 0x13. Liga (0x170F0). |
| 0170BA | soltar_objetos | C | R | Se carregam objeto (+0x5E bit6), soltam-no (objeto +0x60 para a ação 4). |
| 0170F0 | enlazar_pareja | C | R | Cada um passa a ter o outro como rival (+0x68) e o seu índice +0x6C dentro da equipe contrária (lista 0xEA4C; +8 com +0x2A bit4). |
| 017106 | enlazar_uno | C | R | +0x68 = a4 e +0x6C = o índice de a4 na sua equipe. |
| 017136 | reaccion_especial_m4 | C | R | Reação −4 (contra-ataque) segundo +0x44 da vítima, pela tabela 0x1715C: 0 solta o agarrador (ação 0), a vítima para a 8; 1/2 → +0x40 −1; 3 os dois para a ação 8 sub 1; 4 solta, a vítima para a 8 sub 1. O atacante +0x32 bit3. Dano +1 e 0x16488. CS. |
| 017168 | reac_m4_0 | C | R | Ver 0x17136. |
| 017198 | reac_m4_1 | C | R | Ver 0x17136. |
| 0171A2 | reac_m4_2 | C | R | Ver 0x17136. |
| 0171AA | reac_m4_3 | C | R | Ver 0x17136. |
| 0171D6 | reac_m4_4 | C | R | Ver 0x17136. |
| 017228 | ajuste_agarre_sub15 | C | R | Sub 0x15 no passo ≥4 → passo 0. |
| 017240 | ajuste_agarre_id7 | C | R | Só com as subs 0x14/0x28 (com outras sai sem fazer nada). Sub 0x28 com passo ≥2 → passo 0 (a 0x14 não reinicia). Se a vítima tem o estado +3 = 7: sorteio 0x450A&7 contra a tabela 0x172A6[dificuldade 0x1CE9C do atacante]; se o sorteio supera o valor, o atacante vai para a ação 8 sub 1 e a vítima para a reação 9 (apaga-se +0xC9 bit0 do atacante). |
| 0172AA | chk_pose_lista | C | R | Se +0xCA=0 e a pose do rival (+6 de a2) está na lista 0x172DE: +0xCA=1 e CS. |
| 018E70 | cpu_ia_entrada | P(A) | A | Entrada da IA da CPU (a partir da ação 00 e outras). |
| 018ECE | ia_principal | C | R | IA da CPU: decrementa +0xF3; 0x1CCE8 pode abortar. Salvo com +0x5D=9/0xA/0xD, apaga +0xB0 e escolhe a intenção (0x1D1A8). Salta por +0x5C para a tabela 0x18F16. |
| 018F56 | ia_sub0 | C | R | Se 0x1D04C dá CS → +0x5C=0xB. Se não, 0x19012 e 0x1907C, e despacha segundo a ação do rival pela tabela 0x18F92. |
| 019012 | cpu_pedir_relevo | C | R | CPU de equipe sem 1C00F2 nem +0xF9 bit0, rival não correndo, parceiro no avental (não em 0x13): se a dificuldade < +0xDA e o parceiro tem ≥ energia → +0x5C=6 e parceiro +0x5C=5 (revezamento). |
| 01907C | cpu_rival_fuera | C | R | Rival fora (+0x19=1): sorteio (0x450A>>1)&0xF; com <8 consulta 0x1AE98, e se não dá CS (ou o sorteio ≥8) → +0x5C=3 e parceiro +0xC4=0x10. Se não: o id 7 (André) → +0x5C=4 (parceiro +0xC4=0x7FFF); rival na ação 8 → nada; rival deitado (0xB, já iniciado) → tabela 0x19132[rng&0xF]: 0 → +0x5C=4, 1 → +0x5C=2 (rival +0x38+=0x80, +0x34−=0x14), outro → ação 0xC sub 0x3B; resto → +0x5C=4. |
| 019142 | cpu_est_0 | C | R | Pose atual. |
| 01914A | cpu_est_andar | C | R | 0x19248, 0x19160, 0x196F8 (andar em direção ao rival), limites, 0x1BE9C. |
| 019160 | cpu_decidir_correr | C | R | CPU com +0x2A bit1 sem cooldown (+0xA8 bit7), /dy/<8: segundo dx (≥0xE0/≥0xA0/≥0x60/≥0x40; <0x40 nunca) tabela 0x19228[faixa*8+id&7] contra rng&0xF; se sai → ação 1 (corrida), salvo contra o rival deitado (0xB): só corre se olham para o mesmo lado e dx ≥0xA0. Cooldown +0xA8=0x809C (0x9C frames em +0xA9). O filtro dos bits 8–9 (move.b + andi.w #$300) sempre dá 0: não tem efeito. |
| 019248 | cpu_elegir_paso | C | R | Se /dy/ ≥ 8: +0x34 = 0/1/2 aleatório, +0x5C=0xE. |
| 01928A | cpu_lanzar_ataque | C | R | Com o ataque preparado (+0x2E bit7), sem ruptura e na mesma zona: se /dy/<0xC e 0x10 ≤ dx ≤ tabela 0x19310[id] → ação 0xC com a sub +0x2E (sub 4: o rival para a ação 0x10). |
| 019318 | cpu_est_andar2 | C | R | = 0x1914A. |
| 01931C | cpu_est_elegir | C | R | Rival ativo: 0x19422 (subir no poste?) ou 0x1935C (escolhe o ataque); se escolhe: +0x5C=0, +0x5D=+0xD9. Se não, anda. |
| 01935C | cpu_elegir_ataque | C | R | Rival dentro. Lado contra lado: rival com 0 de energia → +0x2E=0x8006; se não, 0x19406. Fora do lado: subs 6/9 → 4. +0xD9 = tabela 0x193D6[+0x2E&0x3F] (5 por padrão), +0xD8 bit7. |
| 019406 | cpu_ataque_tras_golpe | C | R | Se +0xE2 bit0 e 0x1CEF4 do rival ≠0: +0x2E=0x8004. |
| 019422 | cpu_decidir_poste | C | R | Rival dentro, não o id 7, rival sem +0x104 e na zona da tabela 0x19528 (0x194B8), com energia, 0x1CEF4≠2, ele na zona (0x194F8) e sorteio < tabela 0x19548[id]: +0xD9=2 (poste), rival +0x38+=0x80, +0x34−=0x14. |
| 0194B8 | chk_zona_rect_adelantado | C | R | Retângulo da tabela a2[(zona+0x18 bits8-9)>>5] com x adiantado ±0x30; CC se dentro. |
| 0194F8 | chk_zona_rect | C | R | Igual sem adiantamento. |
| 019550 | cpu_est_combate | C | R | 0x1956A (esquivar), 0x19160, 0x196F8, limites, 0x1928A. |
| 01956A | cpu_esquivar | C | R | Uma vez (+0xE2 bit4): rival atacando (0xC) perto (dx<0x60, 0x38 com a sub 2; dy<8), de frente, com uma sub da lista 0x19644: sorteio contra a tabela 0x19656[1C0028 e dificuldade] (0x1966A para o id 7) → +0xF1 = a resposta da lista e ação 5 (agachar/esquivar); deitado: +0xF0 bit0 e 0x8EEA. |
| 01966E | cpu_est_seguir | C | R | 0x196F8, limites, 0x1BE9C. |
| 01967E | cpu_est_seguir2 | C | R | = 0x1966E. |
| 01968E | cpu_est_esperar_cerca | C | R | Perto (dx<0x60, dy<0x50): para olhando; se não, aproxima-se. |
| 0196C2 | cpu_est_ir_punto | C | R | Vai ao ponto da tabela 0x196F4 (0x1CF50). |
| 0196F8 | cpu_andar_hacia_rival | C | R | Se /dx/<5 e /dy/<5: só se move (direção 0) se o rival está deitado (0xB) sem o bit6 da entrada; em outro caso não faz nada. Se não: faixa 0 (/dy/<4), 1 (dx<0x30), 3 (0x30–0x4F) ou 2 (≥0x50); direção = tabela 0x1977C[faixa*8 + octante (bits 14–15 da entrada)*2]. Depois 0x1979C, 0x924A, 0x3DCE. |
| 01979C | velocidad_por_dir | C | R | +0x21 = tabela 0x933E[id][direção>>5 + 1] (velocidade por lutador). |
| 0197C4 | cpu_est_ir_tabla | C | R | Vai ao ponto da tabela 0x19808[índice +1 do rival] (0x1CFD8). |
| 019818 | cpu_comp_rodear | C | R | Rodeia o rival (0x198B6 verifica o poste 0x1A820) pelo lado segundo a orientação; 0x198C6 ou aproxima-se; com o rival correndo continua (se não, +0x5C=0). |
| 0198A2 | cpu_fin_si_no_corre | C | R | Rival ≠0xD → +0x5C=0. |
| 0198B6 | cpu_chk_poste | C | R | 0x1A7CE com a tabela 0x1A820 e a altura 0xBB. |
| 0198C6 | cpu_rodear_paso | C | R | Direção da tabela 0x19954[lado+zona], afasta-se se dy≥0x10; +0xEA bit7 alterna o lado. |
| 019958 | cpu_ir_a_poste | C | R | Com o alvo nas ações 0xB/0xD/0xE: orienta-se (+0xA, +0x18 bit6) e vai ao poste da tabela 0x199FA; ao chegar → ação 0xF (subir), +0xB8=0. 0xF81A sem CS → +0x5C=0. |
| 019A0A | cpu_ir_cuerda_rival_fuera | C | R | Rival fora: vai à linha x=0x2D0/0x330 (ou y=0x120 segundo +0x18 bit4) do lado do rival e alinha-se. |
| 019AD4 | cpu_perseguir_fuera | C | R | Rival fora: 0x19B8E calcula o ponto de saída; com +0x32 bit6 espera a entrada 0x1A22C. Ao chegar à corda (+0x9F) com 0x1A25C: ação 3 (sair pelas cordas), +0xAC = 0/1/2 segundo a corda (o id 7 coloca-se em x 0x2A5/0x345). +0x5C=0. |
| 019B8E | cpu_punto_salida | C | R | Ponto de saída (+0x24/+0x26) em direção ao rival, limitado a x 0x280–0x380 ou y 0x108–0x150 (tabela 0x19C20, 0x1D032); o id 7 usa uns pontos fixos. 0x1CFD8 dá a direção. |
| 019C28 | cpu_rodear_tumbado | C | R | Rival na mesma zona, deitado/atordoado (0xB/8/5): escolhe um lado (+0x22 bit6) e vai ao ponto da tabela 0x19D12; se o rival corre (0xD), 0x19D1A ou 0x19D5C segundo a distância. Se não, +0x5C=0. |
| 019D1A | cpu_reaccion_carrera | C | R | Rival dentro na zona 0x19D44 (0x1D0E2): +0x5C=1; se não, 0xF. |
| 019D5C | cpu_reaccion_carrera2 | C | R | Rival dentro na zona 0x19D7E → ação 1 (corrida). |
| 019D96 | cpu_ir_relevo | C | R | Vai ao córner (tabela 0x19E32 por equipe). Ao chegar, com o parceiro na ação 0, +0x5D=5 e +0xE2 bit3: os dois para a ação 0x1A (revezamento) com +0x2A bit2; +0xDB = dificuldade. A verificação «parceiro já em 0x13 → +0x5C=0» usa movea.w $A4 (lê só a palavra alta do ponteiro, a1=0x1C) e olha o byte de ROM 0x49, que vale 0: nunca se cumpre (falha do original). |
| 019E3A | cpu_volver_delantal | C | R | Vai ao seu córner (tabela 0x19ED6); ao chegar, 0x1A25C / 0x1A22C → ação 6 (subir ao avental), +0x2A bit7=0. 0x1B3E4: se termina → ação 0 e, para o humano no modo 1C0026 bit0=0, +0xF2 bit7. |
| 019EDE | cpu_seguir_si_rebota | C | R | Rival dentro rebatendo (0xA) ou correndo (0xD): segue-o; se não, +0x5C=0. |
| 019F0A | cpu_ir_a_tumbado | C | R | Rival dentro deitado: vai ao ponto fixo 0x19FE8 (0x19F92 sempre devolve esse, ver 0x19F92). Ao chegar: se o rival tem +0x38 ≥0x10, ação 0xC com a sub +0x2F (sub 4 → o rival para a ação 0x10); se não, +0x5C=0. Se o rival deixa de estar deitado ou dentro, +0x5C=0 (mas termina o frame). |
| 019F92 | cpu_punto_ataque | C | R | Lista 0x19FD6 (sub → índice) — o resultado é sobrescrito: sempre devolve 0x19FE8 (código morto: o adda é sobrescrito). |
| 01A008 | cpu_nada | C | R | rts. |
| 01A00A | cpu_ir_centro | C | R | 0x1D04C; vai ao ponto 0x1A056/0x1A05A segundo a y do rival (≥0x138). |
| 01A05E | cpu_dar_vueltas | C | R | Durante +0x24 frames (0x20; 0x10 fora) e um número de passos da tabela 0x1A15E[1C0028&0xF]: afasta-se do rival (direção oposta). Ao chocar ou acabar o tempo: em equipe, na zona 0x1A168 e com o parceiro no avental → revezamento (+0x5C=6/5). O id 6 usa outra animação (0x1A1C8). |
| 01A170 | anim_andar | C | R | Animação de andar: sem objeto, ciclo de 4 passos da tabela 0x93AE (+8 com +0x18 bit6). Com objeto: 0x924A. |
| 01A1C8 | anim_andar_id6 | C | R | Ciclo de 4 passos da tabela 0x1A20C. |
| 01A22C | chk_entrada_cuerda_lado | C | R | Entrada 1C1894/1C1896 (segundo +0x18 bit0) &3; sem pressionar apaga +0x32 bit0, pressionada → CS. |
| 01A25C | chk_puede_cruzar | C | R | CS se a entrada do lado (1C1894/1C1896 &3) está ativa, salvo na zona 1 com +0x18 bit4. |
| 01A29A | cpu_esperar_levante | C | R | Rival deitado/levantando-se (1/2/0x15). Escolhe o ataque (0x1A33E); na zona da tabela 0x1A336 e com 0xA39A → +0x22 bit7 (a partir do poste). Com +0x2E bit6: se está no poste, conta +0x23 e salta (ação 0x16); se não, com o rival em 0x15 de costas → corrida (ação 1). |
| 01A33E | cpu_elegir_sub | C | R | Sub do ataque (+0x2F) da tabela 0x1E8FC[posição x(0–2)*0xC0 + 0x1CEF4 do rival*0x40 + id*8 + sorteio&7]. Fora do lado: a sub 0xB → 0x1C. Bit7 da sub → +0x2E bit6 (a partir do poste). +0x2E bit7 = preparado. |
| 01A3EC | cpu_ir_poste_rival | C | R | Rival dentro: vai ao poste da tabela 0x1A48C[+0x34&3]; ao chegar, com o rival na ação 0 a dx 0x20–0x40 e na zona 0x1A49C → ação 0x16 (salto do poste). |
| 01A4B4 | cpu_entrar_ring | C | R | Rival dentro: vai ao ponto da tabela 0x1A512[id]; ao chegar → ação 1. +0x5C=0. |
| 01A532 | ia_sub_5d | C | R | Despacha por +0x5D&0xF (<8) com a tabela 0x1A554. |
| 01A574 | cpu_fuera_principal | C | R | Fora do ringue: 0x1CDA4, 0x1A6B6 (objeto), 0x1AE44 (contagem fora). Com +0x5A bit7 (contagem alta): com +0x5B=2 → ação 0x1C; se não, +0x5C=2 (3 em equipe) para voltar. Se não: orienta-se para o rival; no mesmo lado: 0x1D04C → +0x5C=6, ou ataca (0x1AF58; deitado → 0x1A674), ou anda. Se em outro lado: rodeia o ringue (0x1A742/0x1A772/0x1A79E). |
| 01A674 | cpu_atacar_fuera | C | R | Sem objeto: 0x1AF70 escolhe +0x2E; ≠0 → ação 0xC com essa sub (4 → o rival para a 0x10). Com objeto: +0x5C=6. |
| 01A6B6 | cpu_buscar_objeto | C | R | Id <6, fora dos modos 4/9 de 1C0029, com um objeto atribuído (+0x5E bit7, +0x60) livre: se está mais perto do objeto (+0x64/+0x66) que do rival → +0x5C=5 (pegar o objeto); se não, +0x5C=0. |
| 01A742 | dir_rodear_x | C | R | Direção para rodear o ringue por x (0x3E0/0x210 segundo o lado). |
| 01A772 | dir_rodear_y | C | R | Direção por y (0xC0). |
| 01A79E | dir_rodear_x2 | C | R | Como 0x1A742, com o lado do rival. |
| 01A7CE | chk_rival_en_trapecio | C | R | CC se o rival está dentro do trapézio da tabela a2 (e abaixo de d4, as bordas x abrem 1/6 por y). |
| 01A830 | cpu_volver_ring | C | R | Vai à corda (0x1A926 ou 0x1A9C2 segundo a equipe +0x2A bit4) e, ao chegar olhando para 0x40/0xC0 no seu lado, com 0x1A25C → ação 4 (entrar), +0xAC=3/4. Se o parceiro está fora e o rival dentro → +0x5C=0. |
| 01A926 | dir_cuerda_eq0 | C | R | Direção em direção à corda (x 0x210/0x3E0, y 0x160/0xC0 segundo +0x18). |
| 01A9C2 | dir_cuerda_eq1 | C | R | Idem para a outra equipe. |
| 01AA5E | cpu_entrar_por_lado | C | R | Vai à linha de entrada (0x1AB0C/0x1AB34) e, ao chegar com a entrada 0x1A25C, ação 4 com +0xAC 0/1/2. |
| 01AB0C | dir_entrada_y | C | R | Por y 0x130/0x180. |
| 01AB34 | dir_entrada_x | C | R | Por x 0x280/0x380; o id 7 em x 0x2A5/0x345 (ajusta-se a menos de 5). |
| 01AB92 | cpu_coger_objeto | C | R | Máquina de +0xE6 (tabela 0x1ABCA): 0 ir à mesa, 1 descer a y<0x30 e pegar o objeto, 2 voltar. |
| 01ABDA | obj_ir_mesa | C | R | Em direção a y 0xC8 e x 0x200/0x400; ao chegar, +0xE6++. |
| 01AC22 | obj_bajar | C | R | Em direção a y<0x30; pega o objeto (0x1AC42), +0xE6++. |
| 01AC42 | crear_objeto_en_mano | C | R | 1C1823 /= +0xE7. Objeto 0xEA60/0xEA64 (segundo +0xE7 bit0): +0x5F = tipo, +0x5E bit6, +0x60. O objeto: ativo (0x8000), pose 0xF/8, sprite 0x17, na posição do lutador, ação 1, dono +0x60, +0x1A=0x8070. |
| 01ACE2 | obj_volver | C | R | Em direção a y ≥0xC8 → +0x5C=0. |
| 01AD02 | cpu_ir_a_por_objeto | C | R | Fora do ringue, indo atrás do objeto atribuído (+0x60): 0x1A6B6 e 0x1AE44 como 0x1A574 (com contagem alta: +0x5B=2 → ação 0x1C; se não, +0x5C=2/3). Se está no mesmo lado que o objeto: 0x1AF58, 0x1AE3C (0xE462, tenta recolhê-lo) e 0x1ADD2 (aproxima-se); se não, rodeia o ringue (0x1A742/0x1A772/0x1A79E). |
| 01ADD2 | cpu_ir_al_objeto | C | R | Direção da tabela 0x1977C segundo a distância (+0x64/+0x66) e o quadrante em relação ao objeto. |
| 01AE3C | cpu_recoger_objeto | C | R | 0xE462 (recoger_objeto). |
| 01AE44 | cpu_chk_cuenta_fuera | C | R | Fora da zona 1 → +0x5A=0. Na zona 1: se nenhum dos dois rivais (+0x6E/+0x7E) está na zona 1 → voltar (+0x5A=0x8001; 0x8002 com objeto). Se algum está: sem +0x2A bit1, volta salvo se o parceiro (+0xA4) também está fora (+0x19=1 → +0x5A=0); com +0x2A bit1, volta se a contagem 1C0596 ≥ a tabela 0x1AED4[id] (0x1AE98) e, se não, +0x5A=0. |
| 01AE98 | chk_cuenta_vs_id | C | R | CC/CS: a contagem fora do árbitro 1C0596 contra o limite da tabela 0x1AED4[id]. |
| 01AEE4 | cpu_fuera_ir_tumbado | C | R | Rival na mesma zona deitado/atordoado/correndo: vai ao ponto 0x1AF50/0x1AF54; se não, +0x5C=0. |
| 01AF58 | cpu_planificar | C | R | Rival não deitado → 0x1D1A8 (escolhe o ataque); deitado → +0x2E=0. |
| 01AF70 | ia_elige_movimiento | C | R | 0x1E7DA(d1=2) → tabela 0x1AFA8[d0][id]; +0x2F = uma das suas 8 entradas escolhida com rng&7. |
| 01B010 | cpu_subir_poste | C | R | Ação 0xF, +0xB8=2. |
| 01B01E | cpu_delantal_espera | C | R | Com +0xC6 bit7 → +0x5C=0; depois 0x1BC3E. |
| 01B034 | cpu_delantal_disp | C | R | Despacha +0x5C&7 (<5) pela tabela 0x1B04E; se não, 0x1B06C e os limites. |
| 01B062 | cpu_delantal_def | C | R | 0x1B06C e os limites. |
| 01B06C | cpu_delantal_seguir | C | R | Parceiro fora → +0x5C=4; se não, 0x1B120 e move-se. |
| 01B084 | cpu_seguir_objetivo8e | C | R | Move-se em direção ao alvo +0x8E/+0x90/+0x92 (tabela 0x1977C); perto (+0x92<8) com +0xF2 bit7 → ação 1 (dentro) ou 0x15 (fora). |
| 01B0FE | cpu_atacar_def | C | R | +0x2E=0x8005 e anda; 0x1BEE4 com a tabela 0x1BEB6. |
| 01B120 | cpu_chk_objetivo_cerca | C | R | Só se a zona do alvo (+0x8E&3) é a sua; longe não faz nada. CPU: com /dx/<0x30 e /dy/<0x20 → apaga +0xF2 bit7 e +0x5C. Humano: com /dx/<0x60 e /dy/<0x40 (além disso <0x30/<0x20 se +0x97=0xB e 1C0026 bit0=0): se 1C0026 bit0=1 ou +0x97=0x17 → apaga +0xF2 bit7 e +0x5C; na ação 0x15/2 nada; na ação 1 → ação 0x14 e +0x5C=1; se não → ação 0 e +0x5C=1, e se +0x97≠0xB também apaga +0xF2 bit7 e +0x5C. |
| 01B1D6 | cpu_relevo_disp | C | R | Apaga +0xE2 bit3; despacha +0x5D&7 (<4) pela tabela 0x1B1F8; se não, 0x1B208. |
| 01B208 | cpu_relevo_ir | C | R | Parceiro fora → +0x5C=3; se não, vai em direção ao parceiro rodeando. |
| 01B2A0 | cpu_entrar_relevo | C | R | Copia a zona do parceiro, ação 0xC com a sub da tabela 0x1B2E8[id] (entrada), apaga o bit do córner (tabela 0x1B2F8) de 1C1821, +0xB7 bit0. |
| 01B2FC | cpu_delantal_volver | C | R | Com +0xC6 bit7 → +0x5C=0. Parceiro fora → 0x1BBB4; se não, 0x1BC3E. |
| 01B37E | cpu_bucle_principal | C | R | Se ninguém está cobrindo (ação 0x17) e 0x1B3E4 dá CS → +0x5C=7. Salvo nos estados 9/0xA/0xD, planeja (0x1D1A8). Despacha +0x5C&0xF pela tabela 0x1B40C. |
| 01B3E4 | ia_compa_cubierto | C | R | CC se o parceiro está deitado (0xB) e coberto (+0x18 bit5); se não, CS. |
| 01B44C | cpu_ayudar_pin | C | R | Parceiro cobrindo (0x17) e perto (0x1B46C) → +0x5C=0xF; se não, 0x18F56. |
| 01B46C | chk_cerca_60_40 | C | R | CS se dx ≥0x60 ou dy ≥0x40. |
| 01B486 | cpu_ir_salvar_pin | C | R | Com o parceiro cobrindo e perto: vai ao ponto (0x1B4D2) junto ao parceiro (x±0x60/0x40, y do rival); se não, +0x5C=0. |
| 01B4D2 | punto_salvar_pin | C | R | +0x24 = x do parceiro −0x60/+0x40 segundo a equipe; +0x26 = y do rival; 0x1CFD8. |
| 01B504 | cpu_delantal_disp2 | C | R | +0xF3−− se ≠0; despacha +0x5D&0xF (<8) pela tabela 0x1B52A; se não, 0x1B54A. |
| 01B54A | cpu_delantal_pasear | C | R | No avental: passeia em y entre 0x118 e 0x170 com giros aleatórios (+0xC3); com o parceiro perto (<0x40) e sem +0xE3 bit0 → +0x5C=5. 0x1B6F0 decide entrar. |
| 01B62E | limite_delantal | C | R | y limitada a 0x118–0x170 (para); se não, 0x220C4. |
| 01B656 | cpu_delantal_seguir_rival | C | R | Segue a y do rival pelo avental. |
| 01B6F0 | cpu_delantal_decidir | C | R | Se 0x1BDCA dá CS (alguém na ação 1/2/0x15/0x16) → +0x5C=6. CPU com o parceiro na ação 0 e +0x5D=6 → +0x5C=5. Se não, toma a zona da entrada +0x6E (se tem o bit3; se não, a +0x7E): na zona 0 → 0x1B756 e, se não entrou (+0x2A bit7), 0x1B942 (agarrar a partir do avental); na zona 1 → 0x1BB92. |
| 01B756 | cpu_temporizador_entrada | C | R | Com +0xC6 bit7 conta +0xC7; ao terminar: +0x2A bit7 (entra), +0x5C=4 (0 se não está no avental), +0xF2 bit7, +0xE0 = tabela 0x1B7E2[id]. Se não, despacha +0xC6 pela tabela 0x1B7C2. |
| 01B7F2 | nop | C | R | Nada. |
| 01B7FA | cpu_programar_entrada | C | R | Se o parceiro tem energia 0 e +0x106 bit1 já está posto: só continua com um sorteio <3/16. Depois: no modo 1C0026 bit0=1 durante a luta 0, ou na primeira vez (+0x106 bit1 estava a 0, é posto) → +0xC6 bit7 e +0xC7 = tabela 0x1B938[1C0028&0xF]. Nas vezes seguintes → 0x1B8F4 com a tabela 0x1B862. |
| 01B880 | cpu_entrada_ya | C | R | +0xC6 bit7. |
| 01B888 | rts_1b888 | C | R | rts. |
| 01B88A | rts_1b88a | C | R | rts. |
| 01B88C | ia_tirada_tag | C | R | No modo 1C0026 bit0=1 durante a luta 0, ou na primeira vez (+0x106 bit0 estava a 0, é posto) → +0xC6 bit7 e +0xC7 = tabela 0x1B938[1C0028&0xF]. Nas vezes seguintes → 0x1B8F4 com a tabela 0x1B8D6. |
| 01B8F4 | cpu_tirada_entrada | C | R | Sorteio contra a tabela a2[1C0028*3 + 0x1CEF4] → programa a entrada. |
| 01B942 | cpu_agarre_desde_delantal | C | R | Com 1C001A bit7 e o rival dentro a dx ≤0x50: se está colado (dx≤0x2C, dy≤0x10, mesma z), sem a corda vibrando (bit14 de 1C1898/1C189A), rival não em 0x1F, nem nenhum o id 7, rival rebatendo/correndo ou (0x1BB0C/+0xE2 bit5) na ação 0 de costas, sem ruptura: ele para a ação 0x13 e o rival para a 0x1B (agarrado a partir do avental), ligados. Humano com botão: ação 0xC sub 0x3C (revezamento). Se não ocorre: CPU → ação 0 com +0x5C=1. |
| 01BB0C | chk_humano_modo1 | C | R | CS se é humano com controle e 1C0026 bit0. |
| 01BB32 | cpu_tirada_agarre_delantal | C | R | Uma vez (+0xE2 bit6): sorteio contra a tabela 0x1BB7E (0x1BB88 para a CPU)[1C0028] → +0xE2 bit5. |
| 01BB92 | cpu_delantal_a_ring | C | R | Alvo na zona 1 → +0x2A bit7, ação 0, +0x5C=2. |
| 01BBB4 | cpu_bajar_delantal | C | R | Anda para fora (0x40/0xC0 segundo a equipe); ao chocar: ação 3 (descer), +0xAC segundo o lado; com 1C0026 bit0 o humano recupera o controle (+0x2A bit0). |
| 01BC3E | cpu_volver_esquina | C | R | Vai em direção a y 0x110–0x150 e, ao tocar a corda com 0x1A25C, ação 7 (subir ao avental). |
| 01BCB6 | cpu_delantal_ir_esquina | C | R | Parceiro dentro, perto (<0x60) e sem +0xE3 bit0: vai ao córner (y 0x108/0x150) e gira (+0xE2 bit3). |
| 01BD5C | cpu_delantal_mirar | C | R | Se 0x1BDCA dá CS (alguém na ação 1/2/0x15/0x16, ver 0x1BDCA): orienta-se com a tabela 0x1BDC6 enquanto y estiver em 0x118–0x170; se não, +0x5C=0. Falha do original: calcula a orientação da equipe em d1 mas escreve d0 (o índice que 0x1BDCA devolveu) em +0xA. |
| 01BDCA | chk_alguien_accion_1_2_15_16 | C | R | CS se algum dos 3 (+0x68/+0xA0/+0xA4, tabela 0x1BE2A) está na ação 1, 2, 0x15 ou 0x16 com a sua orientação (+0xA bit15) diferente da da sua equipe (+0x2A bit4). O que essas ações representam aqui: SEM CONFIRMAR (não é o estado deitado 0xB). |
| 01BE30 | cpu_carrera | P(A) | A | Corrida da CPU (ação 01 com +0x2A bit3). |
| 01BE9C | ia_ejec_mov | C | R | Tabela 0x1BEB6 (0x1BECA se 0x1D136 dá CS) → 0x1BEE4. |
| 01BEE4 | ia_iniciar_llave | C | R | Com +0x2E bit7, a mesma zona que o rival e 0x2786 CC: procura +0x2F na lista a2 → descritor 0x1C028+6*n com flags: bit0 = não com a mesma orientação que o rival, bit1 = contato +0x6E bit6, bit2 = compara +0xA com o byte +0xA de a2 (cai no descritor seguinte; provável falha do original), bit3 = lado. dy<8 e dx em [+2,+4) do descritor; se está mais perto e está fora → +0x5C=7. Se tudo bate e 0x1C14E não o impede → ação 0xC com a sub +0x2F; com as subs 4 e 0x1C, o rival passa para a ação 0x10 e fica ligado. |
| 01C14E | chk_sub_a_limite | C | R | Sub +0x2F=0xA: se x passa de 0x330 (0x2E0 do outro lado) → +0x2E=0, CS. |
| 01C180 | acc_salir_ring | C | R | Apaga o lado bit1 e percorre a tabela 0x1C26E (0x1C2AA para o id 7) segundo o lado (+0x18 bit0) com passos (pose, dx, dy). Ao terminar, +0x19=3 (fora), ação 0, e apaga +0x33 bit7 e +0x2A bit2. |
| 01C306 | acc_volver_ring | C | R | Igual com as tabelas 0x1C3F6/0x1C432; se +0x2A bit2, recupera o bit1. Ao terminar, +0x19=0 (dentro). |
| 01C4A2 | ent_esquina_2 | C | R | Entrada pelo córner: +0xB8 bit7, 1C1821 bit2 durante 4 frames, pose 0x1F, posição fixa 0xF6CE; depois 0x1E8B0. |
| 01C4FA | ent_esquina_0 | C | R | Idem bit0, posição 0xF6D4. |
| 01C552 | ent_esquina_3 | C | R | Idem bit3, pose 0x69, posição 0xF6DA. |
| 01C5B0 | ent_esquina_1 | C | R | Idem bit1, posição 0xF6E0. |
| 01C60E | acc_caer_init | C | R | 0x1C61A e 0x8EC8. |
| 01C61A | acc_caer_inicio | C | R | Primeira vez: se 1C1828=0xFF anota o id (primeiro caído); estado 1, velocidade da tabela 0x95BC[id], vira-se de costas para o rival, direção ±0x40. |
| 01C68C | acc_burla | C | R | Provocação: pose 0x1A (0 para as subs 0x32/0x18/0x33/0x14) 4 frames; depois despacha por id (tabela 0x1C6FA). |
| 01C71A | burla_fin | C | R | Ação 0, +0x5C=0. |
| 01C726 | burla_a | C | R | Som 0x22, +0xE2 bit0; 2 poses da tabela 0x1C7B0 (o id 5 usa a do 2) repetidas 2 vezes. |
| 01C7C8 | burla_b | C | R | Som 0x22, uma de 3 poses ao acaso (tabela 0x1C818). |
| 01C824 | burla_c | C | R | Som 0x22, pose 0x103 (0x20 frames). |
| 01C85C | burla_d | C | R | Som 0x23, uma de 2 sequências de 4 poses ao acaso (tabela 0x1C8DE), 2 vezes. |
| 01C906 | acc_coger_silla | C | R | Pega/usa o objeto (som 0x2C); nas lutas 4/9 a CPU → 0x1CB16. Fora: pose 0xEF e coloca o parceiro a ±0x33, cria o objeto na mão (0x1CA6A). Ao terminar: fora → ação 7 com +0xE3 bit0 (e o controle se é humano); dentro → +0xC0 bit7, espera que o parceiro entre → ação 6. |
| 01CA6A | crear_obj_mano | C | R | 0x1D114 dá um objeto livre a4: ativo, x/y/z a partir do lutador com os deslocamentos das tabelas 0x1CB06/0x1CB0E[id], pose 0x7C, orientação. |
| 01CB16 | coger_silla_modo49 | C | R | Nas lutas 4/9 (CPU): coloca o parceiro a ±0x18 e faz 4 poses (tabelas 0x1CBF0 dentro / 0x1CC10 fora, índice id−6: só dá dados válidos para DiBiase (6) e André (7)). Fora → ação 7; dentro → espera que o parceiro entre → ação 6. |
| 01CC30 | acc_cc30 | C | R | Salta para 0xE604. Segue-o 0x1CC36: toma o objeto +0x60 (o objeto passa para a ação 1 com dono e lado), 2 poses da tabela 0x1CCD0[tipo], depois ação 0 com +0x5C=0. |
| 01CCE8 | chk_furia | C | R | Se +0xF9 bit0=0 e (+0xF8 bit7 ou o contador +0xF6 ≥ a tabela 0x1CD48[id]): +0xFA = duração da tabela 0x1CD6C[1C0028], +0xF9 bit0, apaga +0xF8 bit7 e +0xF6 → CS (entra em modo especial/fúria). |
| 01CD50 | tick_furia | C | R | Com +0xF9 bit0: +0xFA−−; ao terminar apaga +0xF8/+0xF9 e +0xF6. |
| 01CD80 | chk_contador_f6 | C | R | CS se +0xF6 >= a tabela 0x1CD48[id] (cmp.b e depois eori 1 ao CCR inverte o carry); CC se é menor. Corrigido em 31-10-2026: antes dizia o contrário. |
| 01CDA4 | cpu_decidir_ir_objeto | C | R | Nada nas lutas 4/9, com ids ≥6 (DiBiase/André), com um objeto em uso (1C1822) ou se já carrega um. +0xE4 funciona como histórico: a cada frame desloca-se 8 bits e +0xE5 bit7 é posto se está junto à mesa (y<0x100 e x<0x250 ou ≥0x3A8). +0xE4 == 0x80 é a borda de chegada (junto à mesa agora e não no frame anterior). Nesse momento, se o rival está mais longe que a mesa (0x1CE24 ≥0) e o sorteio 0x1CE6C sai menor que a tabela → +0xE6=1 e +0x5C=4 (ir atrás do objeto). |
| 01CE24 | dist_rival_vs_mesa | C | R | d2 = dist²(rival) − dist²(mesa: x 0x200/0x400 segundo o lado, y 0xB0). |
| 01CE6C | tirada_objeto | C | R | Sorteio &0xF contra a tabela 0x1CE92[1C0028]. |
| 01CE8C | tipo_objeto | C | R | d0=1. |
| 01CE9C | nivel_energia4 | C | R | Energia +0x3C dividida por (energia máxima da tabela 0x7FEC, ou, para a CPU (+0x2A bit3), 0x8190[nível 1C0028*8 + vaga +0x2A&7]; níveis 0–3: 45/49/47/43/47/43, 60/64/62/58/60/58, 68/73/70/66/71/66, 72/76/74/70/74/70/88/96)/4 (mínimo 1); o resultado é limitado a 3. |
| 01CEF4 | nivel_energia3 | C | R | Idem com /3 → 0–2. |
| 01CF50 | dir_a_rival_offset | C | R | Direção (tabela 0x1977C, faixa por distância) em direção ao rival + deslocamento (a2: dx com bit15 = lado contrário à orientação, dy). CS se chega (dy<5 e dx<9). |
| 01CFD8 | dir_a_punto | C | R | Idem em direção ao ponto absoluto (a2). |
| 01D032 | x_trapecio | C | R | x de uma borda do trapézio do ringue segundo y (inclinação 1/6, sinal pelo lado). |
| 01D04C | chk_compañero_mismo_objetivo | C | R | CS se o parceiro está na mesma zona, com o mesmo rival e a sua ação é compatível segundo a tabela de bits 0x1D0A0 (bit0/bit1 por lado). |
| 01D0C2 | tirada_id | C | R | Sorteio &0xF < a2[id] → CS. |
| 01D0E2 | tirada_por_energia_rival | C | R | Pretende sortear &0xF < a2[nível_energia(rival)*8 + id] → CS. Falha do original: soma o deslocamento do nível a a1 (o ponteiro do rival) em vez de a a2, então na prática o sorteio é contra a2[id] sem levar em conta a energia. |
| 01D114 | buscar_objeto_libre | C | R | Primeiro objeto livre (bit7=0) dos 4 da tabela 0xBCB8. Se não há nenhum livre, devolve mesmo assim o último (a4) ainda que esteja ocupado. |
| 01D136 | chk_rival_accion_1_15_16 | C | R | CS se o rival está na ação 1, 0x15 ou 0x16 (não é o estado deitado 0xB; o que essas ações representam aqui: SEM CONFIRMAR). |
| 01D166 | ia_retardo | C | R | +0xF3 = tabela 0x1D18E[rng%4]. |
| 01D1A8 | ia_intencion | C | R | Escolhe +0x2E/+0x2F (intenção da CPU). Tabela 0x1D33A (0x1DD7E se ele mesmo está na ação 1) indexada pelo nível de energia 0x1CEF4 do rival, que conta como 0 até que 1C1852 ≥ 0x258. Depois pela ação do rival (0x1F se está na ação 0xC com a sub na lista 0x1D2B0: 19 2F 24 2C 20 1A) e pelo id próprio. rng&0xF & a máscara 0x1D2FA (0x1D31A na ação 1)[ação]; byte com sinal, máscara 0x807F. Salvo se os dois têm +0x2A bit1 e ele não está fora (+0x19≠1), remapeia-se com a lista 0x1D2B8[id]. Se carrega um objeto (+0x5E bit6) → +0x2F=0x30 (+0x2E=0 se o rival está deitado, 0xB). |
| 01E05C | ia_elegir_llave | C | R | Subação +0x30: tabela 0x1E392 se está fora (+0x19=1, índice 0x1E7DA d1=0, rng&7) ou 0x1E1A6[nível de energia do rival, 0 até 1C1852 ≥0x258][id][rng&0xF]. Sem +0x2A bit1: +0x31 = tabela 0x1E14E[id][1C0046 bit1]. Ajustes 0x1E826 (lista 0x1E15E) → 0x1E88A (lista 0x1E170); se a sub está na lista 0x1E19A, gira. Ação 0xC e o rival para a 0x10. |
| 01E432 | ia_elegir_llave_b | C | R | Variante de 0x1E05C: tabelas 0x1E74A (fora, d1=1) e 0x1E55E[dificuldade][id][rng], com ext. A sub 0x36 fora de x 0x2C0–0x340 passa a 0x1E. Ajustes 0x1E510/0x1E526; giro se está na lista 0x1E55A. Ação 0xC e o rival para a 0x10. |
| 01E7DA | chk_lado_exterior | C | R | Fora (+0x18 bit4): 1 se vai em direção a uma borda segundo x (0x2A0/0x360) e a orientação. |
| 01E826 | chk_sub_fuera_ring | C | R | Procura a sub +0x31 na lista a2 (sub, dx); CS se a x resultante sai do ringue (≥0x380 / <0x280). |
| 01E88A | remap_sub_por_id | C | R | Procura +0x31 na lista a2 (9 bytes); substitui pelo byte [id]. |
| 01E8B0 | ia_llave_suelo | C | R | Sub +0x31 = tabela 0x1E8EC[id + 8 se o rival não está deitado]; ação 0xC no mesmo lado que o rival; +0x104 do rival = 1. |
| 01EB40 | camara_disp | C | R | Câmera: a0=1C18AC, a1=1C18B0 (os dois seguidos); despacha 1C18A8 pela tabela 0x1EB60. |
| 01EB68 | despacho_zonas | C | R | Salta para 0x1EB8A[(zona própria & 0xF)*0x10 + (zona do rival & 0xF)*4]. |
| 01EBCA | camara_normal | C | R | Centraliza x (0x1EEE0) com um salto máximo de 4; y (0x1EF2A); y não passa de 0x15C. |
| 01EC44 | camara_seguir_uno | C | R | Se a0 é CPU (+0x2A bit3): se a1 também é CPU → 0x1EE9A; se não, segue a1. Se a0 é humano e 1C0026 bit1: se a0 está fora (+0x19==1) → 0x1EE9C; se a1 está → guarda 1C18AC/1C18B0, troca e 0x1EE9C. Resto: salto por +0xB8 do seguido (tabela 0x1EC96). |
| 01ECAA | camara_poste | C | R | Por +0x18&3 (tabela 0x1ECBE): cada córner tem a sua posição alvo. |
| 01ECCE | cam_esq_0 | C | R | x → 0x302, y → 0x1FB (passos de 2). |
| 01ED18 | cam_esq_1 | C | R | x → 0x1F9, y → 0x1FB. |
| 01ED62 | cam_esq_2 | C | R | x → 0x32D, y → 0x155. |
| 01EDAC | cam_esq_3 | C | R | x → 0x1F9, y → 0x1FA. |
| 01EDF6 | camara_delantal | C | R | x como a normal; y → 0x15B ou 0x1CB segundo +0x18 bit1. |
| 01EE9A | rts_1ee9a | C | R | rts. |
| 01EE9C | camara_x_y | C | R | 0x1EEE0 e 0x1EF2A. |
| 01EEA6 | camara_los_dos_fuera | C | R | Os dois fora: x normal; y desce até 0xEF. |
| 01EEE0 | camara_x | C | R | 1C002A = x(a0) − min(/dx//2, 0x50) em direção a a1 − 0x80, limitada a 0x1A0–0x360. |
| 01EF2A | camara_y | C | R | 1C002E segue a y+z do lutador com uma janela de 0x40–0x80; mínimo 0xEF. |
| 01EF78 | camara_transicion | C | R | Ao mudar de alvo (1C18B5 bit3): move 1C002A 2 pixels por frame em direção ao alvo (bit1 ao chegar) e a y (bit0); com os dois bits → 1C18A8=0 (volta ao modo normal). |
| 01F0B0 | camara_elegir | C | R | Com partida: despacha 1C0026&3 pela tabela 0x1F0D0. |
| 01F0E0 | cam_elegir_1p | C | R | 1C18AC = o humano (bit0), 1C18B0 = a CPU com bit1. |
| 01F11A | cam_elegir_bando | C | R | Pelo bit1. |
| 01F154 | cam_elegir_2p | C | R | Dois humanos (a3/a4): regras por ações (0xF poste, 0x19, 0xC, fora 0x3/0x6 com 0x1F340) para escolher qual centralizar; se muda, transição (1C18B5 bit3, 1C18A8=1). |
| 01F340 | chk_fuera_o_cruzando | C | R | CS se está fora ou na ação 3/6. |
| 01F364 | cam_saltar_delantal | C | R | Se o seguido tem +0xF2 bit7 (no avental), troca-o pelo seu parceiro (0x1F39C). |
| 01F39C | compañero_de | C | R | 1C0100↔1C021A, 1C0334↔1C044E. |
| 01F3CE | camara_a_hw | C | R | Scroll: 180004 = 1C002A−0x200 (bit9 → 1C2B9C bit5), 180006 = 0x200−1C002E (bit9 → bit4); 18000A = 1C2B9C. |
| 01F434 | fondo_cmd | C | R | 1C182C = d0; chama a tabela 0x1F450[d0]. |
| 01F474 | fondo_init_ring | C | R | Copia 4 blocos de tilemap (0x1F72C/0x1F868/0x1F9D4/0x1FAD0) para 0xC0000/0xC0400/0xC0800/0xC0C00 com 0x203C2 e põe as células fixas 0xC01B0 e 0xC0A50. 1C1890=1, 1C1892=0, scroll 1C002A=0x280 e 1C002E=0x200. Portas 0x180004=0x80 e 0x180006=0. 1C2B9C &= 0xCF e copia-o para 0x18000A. |
| 01F50C | marcadores_nombres | C | R | Escreve na camada de texto (c00b4/c0174/c0484/c0544) os 3×2 tiles do lutador (tabela 0x2197A[id]); os dois da esquerda espelhados. |
| 01F546 | nombre_derecha | C | R | 3 linhas × 2 tiles, atributo 0x20. |
| 01F57E | nombre_izquierda | C | R | Idem espelhado (bit7 do atributo). |
| 01F5C8 | fondo_scroll_columnas | C | R | Se 1C182D=0: segundo o scroll X 1C002A, procura a coluna nos limiares 0x1F726 (avança de 1 em 1 frente a 1C1890) e copia 16 linhas de tilemap (tabela 0x1F706) em duas metades por frame (1C1860/62/66). Segundo 1C1891, ajusta as células fixas 0xC0B80/0xC0A50/0xC01B0. |
| 0201AC | esc_dibujar_a | C | R | Cena (tabela 0x1F43E): desenha na camada c0000 a lista 0x20D9E (0x203C2) e 7 colunas da tabela 0x20F06; 0x207C6. |
| 0201F4 | esc_dibujar_b | C | R | Cena: preenche c0000 (0x4FFDC), dois blocos espelhados de 0x20F3E (0x20314), linhas c03C0/c03CC e 10 tiles de 0x20FC8; 0x207C6. |
| 0202A0 | esc_dibujar_c | C | R | Cena: preenchimento 0x6FF00, blocos espelhados de 0x20FDC e 32 tiles de 0x21068 em c0380. |
| 020314 | blit_bloques | C | R | Desenha blocos de tiles consecutivos (formato: linhas, colunas, atributo^d7, tile, largura) com passo d0 e salto d6. |
| 02034A | esc_dibujar_d | C | R | Cena: lista 0x210A8 e seis blocos de 4×4 tiles (0x20404); c0264=0x720043. |
| 0203C2 | blit_lista_rle | C | R | Desenha uma lista: linhas; por linha (atributo, tile[, 0xFF = novo atributo], incremento com bit7 = espelho, contagem). |
| 020404 | blit_4x4 | C | R | Bloco de 4×4 tiles consecutivos. |
| 020424 | esc_dibujar_e | C | R | Cena: 6 tiles de 0x21134, linhas de tiles fixos e a lista 0x210EC (0x2048E). |
| 02048E | blit_lista_rect | C | R | Lista de retângulos (destino, atributo, tile, altura, largura, salto); d6 negativo = desenha para trás (espelho). |
| 0204DC | esc_dibujar_f | C | R | Cena: lista 0x2113A, blocos fixos; prepara a animação (1C1836=0x80008, 1C182E=0, 1C185E=0, 1C185C=0x10). |
| 02057A | esc_dibujar_g | C | R | Cena: lista 0x218D6 e dois blocos de 3 tiles × 4/3 linhas. |
| 0205D6 | esc_dibujar_h | C | R | Idem espelhado (lista 0x21928). |
| 020632 | esc_combates_4_9 | C | R | Nas lutas 4/9: 4 retângulos (tabela 0x2069E) com tiles 0x60FFE1… pulando os buracos (0x2065A). |
| 02065A | blit_rect_saltos | C | R | Retângulo com tiles consecutivos que salta de 0x60FFF4 para 0x62FF43 e corta-se em 0x62FF47/0x62FF4E. |
| 0206BE | esc_anim_6 | C | R | Com a cena 6 (1C182D): a cada 8 frames alterna duas versões (0x211FA/0x2121C e 0x2123E/0x21272); e ciclo de 5 passos (tabela 0x207F6 de durações, tiles 0x20800) em c00C0/c0100 espelhados. |
| 0207C6 | fondo_reset_scroll | C | R | Zera 0x180004/0x180006 e 1C002A/1C002E; 1C2B9C &= 0xCF e copia-o para 0x18000A. |
| 020824 | esc_anim_7_8 | C | R | Cenas 7/8: avança os contadores (0x208DA alterna a cada 8 frames; 0x208FE ciclo de 3). |
| 0208DA | ctr_alterna8 | C | R | Alterna d1 a cada 8 frames (init 1C182C bit7). |
| 0208FE | ctr_ciclo3 | C | R | d1 = 0,1,2 a cada 8 frames (init 1C182C bit6). |
| 020928 | esc_anim_dibujar | C | R | Cenas 7/8: se o frame muda, redesenha (0x209C6 / 0x20C72). |
| 0209C6 | esc_anim_a | C | R | Por frame (+2 na cena 8), tabela 0x209E6. |
| 0209F6 | esc_anim_a0 | C | R | 4 blocos de tiles (0x20B1A). |
| 020A88 | esc_anim_a1 | C | R | Idem, o outro frame. |
| 020B1A | blit_bloque_inc | C | R | Bloco de tiles crescentes. |
| 020B34 | esc_anim_a2 | C | R | 4 blocos espelhados (0x20C58). |
| 020BC6 | esc_anim_a3 | C | R | Idem. |
| 020C58 | blit_bloque_dec | C | R | Bloco de tiles decrescentes, para trás. |
| 020C72 | esc_anim_b | C | R | Por frame (+3 na cena 8), tabela 0x20C92. |
| 020CAA | esc_anim_b0 | C | R | 2 blocos de 5×8 (0x20D04). |
| 020CC8 | esc_anim_b1 | C | R | Idem. |
| 020CE6 | esc_anim_b2 | C | R | Idem. |
| 020D04 | blit_5x8 | C | R | 5 linhas × 8 tiles. |
| 020D24 | esc_anim_b3 | C | R | 2 blocos (0x20D7E). |
| 020D42 | esc_anim_b4 | C | R | Idem. |
| 020D60 | esc_anim_b5 | C | R | 2 blocos com 0x20D7E: 0xC03E0 tile 0xCD006C e 0xC03C0 tile 0xCD0094. |
| 020D7E | blit_5x8_dec | C | R | 5×8 tiles decrescentes, linhas para cima. |
| 0212A6 | cuerdas_anim | C | R | Por lado (1C1898/1C189C/1C189E/1C18A4/1C1894 e o bloco 1C189A…1C1896): 0x21324. |
| 021324 | cuerda_vibrar | C | R | Bit15 (pedido por 0x9700) → começa: som 0x2A e bit14 = vibrando. Se o nibble baixo ≠0, começa no passo 2 (frame 3); se é 0, no passo 0 (frame 1). Avança até 8 passos com as durações da tabela 0x213A4 e os frames 0x213AC (&3) em d4 → 1C1894/1C1896; no passo 8 apaga o bit14. |
| 0213B4 | cuerdas_a_video | C | R | Para 1C1898 com o bit14 (vibrando; btst.b #6 sobre o byte alto) e 1C1890<2, se o frame mudou (1C189C≠1C189E) → 0x21412. Para 1C189A com o bit14 e 1C1890≠0, se 1C18A0≠1C18A2 → 0x21420. |
| 021412 | cuerda_dibujar_0 | C | R | a0=c020C, tabela 0x21476 → 0x2142C. |
| 021420 | cuerda_dibujar_1 | C | R | Corda do outro lado: a0=0xC0620, tabela 0x216A6; entra no código comum 0x2142C, que copia o bloco a2[0x2146E[d0]*0x8C] (14 linhas de 5 células, com um salto de 0x400 na linha 6). Não é um retrato: chama-a 0x213B4 para 1C189A. 0x21412 usa o mesmo código com 0xC020C/0x21476. |
| 0219AA | indicador_1a92 | C | R | Borda de 1C1A92 bit7: desenha (aceso/apagado) 2 linhas de 4 tiles em c0C8C ou c08A4 (segundo bit0) com os tiles de 0x21A4A. |
| 021A00 | ind_tiles | C | R | Escolhe o destino e os tiles. |
| 021A2E | ind_dibujar | C | R | 2 linhas de 4. |
| 021A4E | textos_luchadores | C | R | Pinta os textos 0x21BB8[id] dos 4 lutadores (ids de 1C012A/244/35E/478). Se o segundo de uma dupla tem o id 6 (DiBiase), troca-o com o primeiro. Não é um retrato: 0x21BB8 aponta para cadeias de texto RLE (destino fg0 de 4 bytes e depois pares de tiles acima/abaixo) que 0x21B4C pinta com a fonte de duas linhas. Que sejam os nomes dos lutadores é SEM CONFIRMAR: a tabela de letras não está decodificada. |
| 021A9A | fg0_iconos_fijos | C | R | Escreve as células fg0 0x80838–0x808C4 com os tiles 0xFFE1–0xFFF8 (paleta 0x10). |
| 021AEC | texto_lucha_0 | C | R | Texto do lutador d0, sem deslocamento extra (0x21B4C). |
| 021AFE | texto_lucha_1 | C | R | Texto do lutador d1, destino +0x180. |
| 021B10 | texto_lucha_2 | C | R | Texto do lutador d2, destino +0x580 (+0x100 se é o id 6, DiBiase). |
| 021B30 | fg0_texto_rle | C | R | Desenha texto RLE de (a0)[d3] em fg0 (+0x700, ou +0x800 se d2=6) em duas linhas, com paleta 0x17. Códigos: 0 fim, 1 salto, 2 espaço, 0xEB meia célula. |
| 021E06 | texto_id_1c0102 | C | R | Texto 0x21BB8 do id que há em 1C0102. |
| 021E1A | texto_id | C | R | Texto 0x21BB8[d0] no seu destino, sem deslocamento extra. Não é um retrato: 0x21BB8 aponta para cadeias de texto RLE (destino fg0 de 4 bytes e depois pares de tiles acima/abaixo) que 0x21B4C pinta com a fonte de duas linhas. Que sejam os nomes dos lutadores é SEM CONFIRMAR: a tabela de letras não está decodificada. |
| 021E30 | textos_intro | C | R | Textos 0xC, 8+(1C0028&0xF) e 0xB (ou 0xD se esse índice é 0xA, ou seja, na luta 2). |
| 021E5A | lim_fuera | C | R | Limites fora do ringue (tabela 0x221AA, e 0xBB) com 0x22140; no ar (+0x18 bit7) acima de z 0xDB → +0x9E bit7. Aplica as correções dos bits de +0x9F (0x21EBA: x/y). |
| 021E9A | lim_aplicar | C | R | Para cada bit 0–3 de +0x9F aplica a correção (x=d2 ou y=d0). |
| 021EC4 | lim_x | C | R | x=d2. |
| 021ECA | lim_y | C | R | y=d0. |
| 021ED0 | lim_ring | C | R | Limites do ringue (tabela 0x221B2) com 0x22140; fora: bordas x 0x240/0x3C0 e y 0x158; dentro: cordas laterais ±0x30 → +0x9F bits 0/1/3. Sem contato → 0x21FE6; com contato no ar → 0x22040 (golpe contra a corda/poste). |
| 021FB6 | marca_choque_on | C | R | 1C1A9A /= bit do lutador (índice em 0xEA4C). |
| 021FE6 | marca_choque_off | C | R | Apaga o bit do lutador em 1C1A9A. |
| 022016 | chk_marca_choque | C | R | Testa o bit do lutador em 1C1A9B. |
| 022040 | choque_poste | C | R | Uma vez por contato (+0x9E bits 0/1; 0x22016): se a ação +0x2D está na lista 0x220BE: som 0x33 se (+0x18 bit0 e contato bit0) ou (+0x18 bit0=0 e contato bit1), se não 0x47; 1C1854 bit7. Dano 5 (+0x3E=5, 0x16488) se a ação ≠8 OU se é a ação 8 com sub +0x45 = 0xA (corrigido na auditoria: antes dizia o contrário). Depois 0x21FB6. Sem contato → 0x21FE6. Qual lado é corda ou poste: SEM CONFIRMAR visualmente. |
| 0220C4 | lim_delantal | C | R | Limites do avental (tabelas 0x221C2/0x221BA) → +0x9F bit0/1; no ar acima de z 0xDB → +0x9E bit7. |
| 022140 | lim_trapecio | C | R | Contra a tabela a2 (yfundo, yfrente, xesq, xdir) menos d4: +0x9F bit3 (fundo), bit2 (frente; deslocamento 0), bits 1/0 (lados com a inclinação 1/6 por y); d2/d0 = valores corrigidos. |
| 0221CA | objs_extra_tick | C | R | Percorre os 5 pares de 0x221F2 (a0, a1) e, se a1 está ativo, chama 0x2221A. |
| 02221A | obj_sombra_tick | C | R | Objeto de apoio do lutador a1: init (estado 0xA, z 0xBB, +0x1A=0x8040); pelo lado (+0x18&3) chama a tabela 0x222A0 (0x222AC com 1C00F0 bit7; dentro nas ações 3/4 usa a entrada 0). Copia a orientação a partir da pose salvo com 1C00F0 bit0. |
| 0222C4 | obj_sombra_ocultar | C | R | 1C00F0 bit0. |
| 0222D6 | sombra_cuerda | C | R | Objeto ligado a um lutador (a1): se a tabela 0x2535A[estado de a1] = 0, oculta-se. Se não, +0x19=3 e y do degrau da tabela 0x2237A. Pose das tabelas 0x22392[1C1894&3] (x=0x26E) ou 0x223FA[1C1896&3] (x=0x38E, invertido) segundo o lado (a1+0x18 bit0). |
| 022462 | flash_1c183e | C | R | Com partida e sem 1C1854 bit7: se 1C183E bit6/7, arranca (1C1890/1C1892 para +4/+6, 0xA ciclos de 6 frames, 0xE5) e conta-o; ao terminar → 0x80. Se não, 0x23406. |
| 0224E8 | flash_dibujar | C | R | Na cena 0 (1C182C=0): desenha a mensagem 1C183E (3 linhas das tabelas 0x22634/0x22640/0x230F0 segundo 1C1890 e a fase); a mensagem 0x15 na fase 4 escreve c0414. Se não, 0x230FC. |
| 0225B0 | tilemap_rle | C | R | Escreve uma cadeia RLE no tilemap: geometria da tabela 0x22760[d1] (x0, largura, salto) e destino 0x22640[d1*0x10]. Códigos 0x00: 0xFD fim, 0xFC muda de paleta (d6), e se não, repetição. |
| 022848 | datos | C | R | Entrada falsa: são dados (dc.w 0xFCFD…), não código. |
| 023054 | datos_23054 | C | R | Não é código: tabela de tiles (dc.w 0x0DFF, 0x00FC…) da mensagem 0x22640, decodificada pela semente linear. |
| 0230FC | fondo_anim_publico | C | R | Sai se 1C1890 == 1 ou se 1C182C ≠ 0 (corrigido na auditoria: antes dizia «só se 1C1890=1»). Com 1C1854 bit4 e 1C1857 == 1 desenha 2 cadeias RLE (0x225B0) da tabela 0x23170 + 1C1890*0xC + 1C1856*0xC. |
| 0232DE | luces_azar | C | R | 1C184A: uma vez, escolhe ao acaso uma posição (rng%4) e repetições (&3); ciclos de 10 frames de 2 fases (bits 5/4) até esgotar. |
| 02336C | luces_dibujar | C | R | Com 1C184A ativo (e sem 1C183E bit7): tiles da tabela 0x233F6[posição][fase] em c0B70, c0F40, c0BB0, c0F80 (4 por lugar). |
| 0233DC | blit_4_tiles | C | R | 4 tiles consecutivos com atributo = byte alto. |
| 023406 | flash_1c1854 | C | R | Arranca com o bit6 de 1C1854, ou com o bit7 se 1C1890≠1 (com o bit7 e 1C1890=1 não faz nada; corrigido, antes dizia o contrário). Fase 0 de 4 frames e fase 1 de 0x21 frames; depois 1C1854=0. O bit4 marca que é visível. |
| 02347E | pantalla_versus_retratos | C | R | 0x23F10 e 0x207C6; escolhe a dupla 1C0100/21A (ou 334/44E se 1C0BC2 bit6=0). Desenha 4×4 tiles por id (tabela 0x23536) em 0xC01D4/0xC01E8 e um bloco de 4×8 da tabela 0x2354E em 0xC0318. |
| 0235CE | pantalla_presentacion | C | R | Desenha a apresentação da luta d0 na camada 0x80000: fundos 5×5 (0x236A2), a lista 0x23702[d0] (0x236BC; a entrada 0x237FE limpa antes com 0x2367A) e tiles fixos. |
| 02367A | limpiar_6x6 | C | R | Apaga 6×6 tiles em 0x80B28. |
| 0236A2 | relleno_5x5 | C | R | 5×5 tiles iguais. |
| 0236BC | blit_lista_presentacion | C | R | Lista: destino, contagem, tile; por elemento atributo (0xFF = repetir) e salto. |
| 0236F4 | fill_inc | C | R | Escreve d5+1 longs incrementando d2; a2 += d6. |
| 02387C | pantalla_titulo_seq | C | R | Sequência de tela com fade: cena 3, paleta 0x140200=0x900, letreiro fg0 0x2660E(3), desenha as molduras 0x23CEE, os textos 0x23757/0x237BD e a linha 0x23D2E; câmera a 0; 1C0568=0; som 0x45; 0x1D passos da tabela 0x23A0A (0x23A28) com espera (0x239DC); paleta a 0. |
| 0239DC | espera_bucle | C | R | Laço de espera ocupada (d0 × 0x1B80). |
| 0239F4 | blit_texto | C | R | Tile inicial de a1 e lista (0x236CE). |
| 023A02 | fg0_dibujo_cont | C | R | Entrada intermediária de 0x23A28 (continua com a0/a1/a2 já carregados). |
| 023A28 | fg0_dibujo | C | R | Desenha o gráfico d1 da tabela 0x23AC4 em fg0 (0x80000 + deslocamento). Sequências (início, fim) de tiles com paleta d4. Comandos após 0xFF: 0 salto n células, 1 paleta, 2 nova linha (+0x80), 3 repetição n, 0xFF fim. |
| 023F10 | fg0_marco_versus | C | R | 0x24E2, gráficos 0x18–0x1D (0x23A28) e bordas de tiles 0xA0–0xA8 (paletas 0x38/0x39) em fg0, mais uma coluna da tabela 0x23FF4. |
| 0240B6 | llave_por_sub | C | R | +0x9E=0. Procura +0x31 na lista de 14 bytes 0x240F0; a entrada i salta para 0x240FE+(13−i)*4 (o índice vai ao contrário porque usa o contador de dbra). |
| 024136 | llave_sub_0x24136 | C | R | 0x244EE com a tabela 0x24146 e d0=3. |
| 024168 | llave_sub_0x24168 | C | R | 0x244EE com a tabela 0x24178 e d0=1. |
| 02418A | hitbox_pose_a | C | R | Tabela 0x241AE: 0x24554 com 5 entradas, dx 0x10, dz 0x10; sem contato → 0x24222. |
| 0241BA | llave_sub_multi | C | R | Testa 0x24554 com 6 tabelas (0x24254…0x2429C) e parâmetros (d0, d1, d2); para na primeira que dá CC. |
| 0242AC | hitbox_pose_b | C | R | Três tentativas (0x242F8/0x24306/0x24314) de deslocar o lutador segundo a pose. |
| 024322 | rts_24322 | C | R | rts. |
| 024324 | rts_24324 | C | R | rts. |
| 024326 | rts_24326 | C | R | rts. |
| 024328 | rts_24328 | C | R | rts. |
| 02432A | rts_2432a | C | R | rts. |
| 02432C | rts_2432c | C | R | rts. |
| 02432E | hitbox_pose_c | C | R | Seis tentativas (tabelas 0x243F8…0x243EC). |
| 024410 | hitbox_pose_d | C | R | Duas tentativas (0x24442, 0x24452). |
| 024460 | hitbox_pose_e | C | R | Quatro tentativas (0x244C6…0x244EA). |
| 0244EE | ajuste_pose_lista | C | R | Procura a pose atual na lista (pose, dx, dz, flip) e aplica dz a +0x14 e dx a x (com o sinal segundo o flip em relação a +0xA). Se toca um limite (+0x9E&3≠0), restaura só a z e fica com a x que a rotina de limites corrigiu. Se não toca nada, restaura x e z, então não se move (corrigido: antes dizia que desfazia x ao chocar). Com +0x19=0 chama 0x21E5A e com ≠0 0x21ED0. Com +0x19 0=dentro, isso choca com os nomes lim_fuera/lim_ring: SEM CONFIRMAR qual está ao contrário. C=0 se a encontra, C=1 se não. |
| 024554 | ajuste_pose | C | R | Igual com dx/dz fixos (d1/d2) e o flip nos 4 bits altos da pose da lista. Se toca um limite (+0x9E&3≠0), restaura só a z e fica com a x que a rotina de limites corrigiu. Se não toca nada, restaura x e z, então não se move (corrigido: antes dizia que desfazia x ao chocar). Com +0x19=0 chama 0x21E5A e com ≠0 0x21ED0. Com +0x19 0=dentro, isso choca com os nomes lim_fuera/lim_ring: SEM CONFIRMAR qual está ao contrário. C=0 se a encontra. |
| 0245BE | secuencia_creditos_intro | C | R | 0x24C8/0x24E2/0x254E; 0x140200=0; som 0x14 e 0x24B38. 4 páginas com os gráficos fg0 7–0xE e os textos 0x29–0x31 (0x2549E), ícones 0x7C00DC–DE. Transições 0x24B54 e esperas 0x453A de 0x260/0x240/0x240/0x240 frames. |
| 024B38 | pal_buffer_borrar | C | R | Apaga o buffer de paleta 1C198A (0x78 words). |
| 024B54 | pal_fundido | C | R | 16 passos: aproxima (a3=0) ou afasta (a3≠0) cada componente RGB do buffer 1C198A da paleta 0x37D0/0x37F0/0x3810 de d2 em d2; descarrega no vblank (0x24C5C). |
| 024C5C | pal_volcar | C | R | Copia 1C198A para a paleta 140002 (8 linhas de 15 cores). |
| 024C90 | marcador_inicio | C | R | Desenha os dois marcadores (0x80084/0x800C0) segundo o +0x2A bit3 de 1C0100/1C0334 (tabelas 0x24D86 CPU / 0x24D92 humano); 1C186C=0x8000, 1C186A=1. |
| 024D36 | fg0_fila_3partes | C | R | Escreve uma linha fg0 (paleta 0x1F) de início, meio e fim. |
| 024D9E | marcador_modo | C | R | Para cada lado, se é CPU (+0x2A bit3) não desenha nada. Humano: 0 (ou 2 no lado B) com bit1, 1 (ou 3) sem bit1; no modo 1C0026&0xF=1 usa 4, ou 5 com bit5. Chama 0x24E20 (esquerda) ou 0x24E28 (direita). |
| 024E20 | marcador_izq | C | R | Destino 0x80084. |
| 024E28 | fg0_bloque_2x4 | C | R | Escreve 4 linhas × 2 células da tabela 0x24E62[d0*8] em 0x800C0 (paleta 0x1F). |
| 024E92 | insert_coin_parpadeo | C | R | Por lado CPU (bit3): piscar (0x24EBC). |
| 024EBC | parpadeo_texto | C | R | Alterna a cada 0x20/8 frames o texto (tabela 0x24FB4 ou 0x24FBC com créditos) — p. ex. «insert coin / press start». |
| 024F6C | blit_texto2 | C | R | Linhas de tiles com o atributo 0x1F. |
| 024F96 | fg0_borra_2x13 | C | R | Apaga 2 linhas de 13 células (0x1FFF00). |
| 025050 | ptr_1c0890 | C | R | a0 = 1C0890 + scroll x. |
| 025064 | ocultar_cuerda_frente | C | R | 0x251D2, 0x251F0; para os lutadores na ação 4 ou dentro com y<0x140: 0x2509E. |
| 02509E | cuerda_frente_por_luchador | C | R | Escolhe a tabela de largura por ação (0x2535A → 0x25346): pela ação (0x252FE; o árbitro 1C0568 usa 0x25340), pela sub +0x30 (0x25286) ou por +0x44 (0x2523C). Marca os segmentos (de 16 pixels entre x 0x236 e 0x3B6) do array 1C155A que cobre; pose 0x3B/0x42 nos casos do estado 7. |
| 0250C6 | cf_por_accion | C | R | Tabela 0x252FE[ação] (o árbitro, 0x25340). |
| 0250E8 | cf_por_sub | C | R | Tabela 0x25286[+0x30&0x3F]. |
| 0250F8 | cf_por_44 | C | R | Tabela 0x2523C[+0x44]. |
| 0251D2 | cf_limpiar | C | R | Apaga o bit de ativo dos 23 segmentos de 1C155A. |
| 0251F0 | fg0_marcas_jugador | C | R | Põe os tiles 0x39/0x3A (se 1C1895 bit0) e 0x40/0x41 (se 1C1897 bit0) no buffer 1C155A. |
| 02537C | cf_init | C | R | Cria os 23 segmentos da corda da frente (1C155A, passo 0x1E): x a partir de 0x246 de 16 em 16, y 0xE0, z 0xC0, pose 0x3B; as pontas com as poses 0x39/0x3A e 0x40/0x41 (postes). |
| 025402 | cf_extremos | C | R | Refaz as poses das pontas (0x253CE). |
| 025408 | cortinilla | C | R | Transição de tela: preenche a camada 0x80000 com os tiles da tabela 0x25492 por passos (esperando 4 frames); ao terminar apaga (0x25474) ou 0x24E2 segundo o sentido. |
| 025474 | capa_80000_borrar | C | R | Preenche 0x80000 com 0x1F0000 (vazio). |
| 02549E | imprimir_texto | C | R | Imprime a cadeia d0 (tabela 0x25600; com o bit7, apaga-a com espaços). Formato: atributo, destino long alinhado e depois caracteres; ASCII−0x20+d2 = tile. Códigos <7 (tabela 0x2551A): 0 fim, 1 novo destino absoluto, 2 destino relativo, 3 atributo, 4 máquina de escrever (pausa de n frames por caractere), 5 fim de pausa, 6 deslocamento de tile d2. |
| 025536 | txt_fin | C | R | Fim. |
| 02553C | txt_destino_abs | C | R | Código 1: alinha e lê um novo destino absoluto (0x254C2). |
| 02553E | txt_reubicar | C | R | Destino += long. |
| 02554C | txt_atributo | C | R | Novo atributo. |
| 025558 | txt_pausa_on | C | R | Modo máquina de escrever (d2 frames). |
| 025568 | txt_pausa_off | C | R | Fim do modo. |
| 025570 | txt_desplaz_tile | C | R | Código 6: d2 (low) = byte seguinte, que se soma a cada tile. |
| 0255A8 | capa_80000_marco | C | R | Apaga as linhas 0 e 31 e as colunas das bordas da camada 0x80000. |
| 0255F4 | fg0_borra_n | C | R | Apaga d0+1 células fg0. |
| 025B96 | datos_25b96 | C | R | Não é código: tabela de entradas de 10 bytes (0x0008, 0x08BC…), decodificada por engano. |
| 025DA2 | datos | C | R | Entrada falsa: dados. |
| 026110 | frag_26110 | C | R | Fragmento de dados decodificado por engano (sem entrada real). |
| 026120 | tilemap_fila_tabla | C | R | Escreve uma linha do tilemap: destino de 0x26166[d2] e origem de 0x26176[d0], com a paleta de 0x261B6[d1]. Formato: comprimento, tile inicial (dois bytes se d1=0) e tiles consecutivos. |
| 0261BC | imprimir_numero | C | R | Imprime o número BCD da tabela 0x26244[d0] (dígitos, destino, fonte) sem zeros à esquerda (0x26218). |
| 026218 | cifra_bcd | C | R | Dígito → tile; os zeros à esquerda são postos como espaço. |
| 02626E | reloj_combate | C | R | Relógio da luta (1C1850). Ao começar: desenha a moldura (0x265F6), som da música da luta (0x6DD4), tempo = 0x708 ajustado pelos DIP 180003 bits 4–5 (0: 0x708, 1: +0x96, 2: −0x96, 3: −0x12C). A cada 0x42 frames subtrai 0xA (décimos → 30:00 no valor padrão, mostrado como mm:ss com /0x3C). Ao chegar a 0x12C (5:00): 1C1850 bit1, aviso com o comando 0x70 (no Z80 não faz nada: só escreve 0x821F, que nada lê) e a música 8 (pressa). Com menos de 0x12C pisca a cor 140036 (bit2). Em 0: 1C1850=1, texto 0x9B («TIME UP»), letreiro fg0 0x2660E(0) e, segundo o modo (1C0026&3, tabela 0x2653C), decide o resultado. |
| 026548 | tiempo_fin_1p | C | R | Fim de tempo com um humano. Se o lado A é CPU (+0x2A bit3 de 1C0100), 1C0BC2=0x4000 e 1C0BDA=0x8000; se não, ao contrário. Som 0x21 e espera de 0x10. O que significam 0x4000/0x8000 (perder ou ganhar): SEM CONFIRMAR. |
| 02657A | tiempo_fin_empate | C | R | Os dois com 0x8000 (empate/derrota dupla); som 0x21. |
| 0265A0 | celda_doble | C | R | Escreve 2 células (acima/abaixo) da tabela 0x265D2[d1] no destino 0x265E6[d2] (paleta 0x10). |
| 02660E | cartel_fg0 | C | R | Letreiro grande de 2 linhas na camada fg0: apaga 2×19 células em 0x80720/0x807A0 e escreve o padrão 0x26696[d0] (comprimento 0x26692[d0] = 0x12/0x10/0x10/0x1E bytes) como pares de tiles 0x10xxxx (0x80D04 se d0=3). Chamam-no: 0x1A64 (fim de luta), 0x16212 (rendição, d0=1), 0x238A0 (título, d0=3), 0x26522 (fim de tempo, d0=0). Não é som nem Z80. |
| 02EF54 | datos | C | R | Entrada falsa: dados. |
| 02F00C | datos | C | R | Entrada falsa: dados. |
| 02F068 | datos_2f068 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F070 | datos_2f070 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F106 | datos_2f106 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F14E | datos_2f14e | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F174 | datos | C | R | Entrada falsa: dados. |
| 02F254 | datos_2f254 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F256 | datos_2f256 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F262 | datos_2f262 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F266 | datos_2f266 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F3C6 | datos_2f3c6 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F3EA | datos_2f3ea | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F40C | datos_2f40c | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F410 | datos_2f410 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F50A | datos_2f50a | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F51E | datos_2f51e | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F522 | datos_2f522 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F548 | datos_2f548 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F614 | datos_2f614 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F648 | datos_2f648 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F668 | datos_2f668 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F68E | datos_2f68e | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 02F6AC | datos | C | R | Entrada falsa: dados. |
| 02F786 | datos_2f786 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6A8 | datos_3b6a8 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6B0 | datos_3b6b0 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6B8 | datos_3b6b8 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6C0 | datos_3b6c0 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6C8 | datos_3b6c8 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6D0 | datos_3b6d0 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6D8 | datos_3b6d8 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B6E0 | datos_3b6e0 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
| 03B7C6 | datos_3b7c6 | C | R | Não é código: dados (tabelas de sprites/ponteiros) que a semente linear decodificou como instruções (ori.b #xx,d3 = 0x0003xxxx = ponteiros para 0x3xxxx). Lidos e descartados como código. |
