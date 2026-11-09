# Routines (R = read in full; A = old signature, not re-read)

> English version of `docs/analisis/rutinas.md` (Spanish is the original). Addresses, routine names, code and values are kept as in the original; only the descriptions are translated.

Coverage read in full: 964 routines, 100.0% of bytes (bytes per entry = min(distance to the next one, 0x400)).

Status: C = confirmed by reading the whole code; "SC: reason" = UNCONFIRMED (SIN CONFIRMAR); P(A) = old annotation by signature, pending re-reading.

| Addr | Name | Status | Source | Function |
|---|---|---|---|---|
| 000E00 | reset_arranque | C | R | Reset vector: IPL 7, USP=1C3B00, clears 1C180C, IRQ ack (180002/180000) and 1C2B9C; initialises video (0x24AE/24C8/24E2/254E/25B8/29DC); lowers IPL; 180008=0; reinitialises twice (with 0x24FC); sound 0xD (0x2549E), waits 0xFF frames (0x453A); 140200=0 → loop 0x1010. |
| 000EBA | irq_vblank | C | R | IRQ (vector 30): if 1C180C bit7 and not reentrant (1C0019 bit7): 1C180D++; with 1C0019 bit0 (frame ready): DMA/palettes/sprites (0x259A, 0x269A, 0x29F6, 0x2626E), 1C0019 bit1 and the frame ticks: 0x20928, 0x55C6, 0x1F5C8, 0x213B4 (ropes to video), 0x224E8, 0x2336C, 0x206BE, 0x219AA, 0x1F3CE. Waits for 180009 bit0 to drop. ACK 180000. |
| 000F5C | irq_timer | C | R | IRQ (vector 29), not reentrant (1C0019 bit5): 0x4A10 and 0xF92 (demo/attract timer). ACK 180002. |
| 000F90 | irq_nula | C | R | rte. |
| 000F92 | tick_atraccion | C | R | With 1C00E4 bit7: counts to 0x100 → 1C182A=2, 1C00E6=0x800083FE, sound 2. With 1C00E6 bit7: counter 1C00E8 cycling over 0x9ECF; at 0x860F and 0x8E7D it fires sound 0x22 (0x25E6). |
| 001010 | bucle_juego | C | R | Initialises variables and video; sound 0x22 (1C00E4=0x8000); palette/scene (0x1F434 mode 3, 0x497C). No credit: sounds 0xE/0x37. 0x78FA (attract/credits). With a game (1C001A): 0x704E (selection); 1C004B from table 0x139E according to the DIPs (180002 &3). Between matches: intro with music from table 0x135C[1C0028], scene 0x1F434 mode 5, 0x1326 (object 1C0AB2), 0x43D4. Prepares the match (table 0x1364/0x136E: music, palette, scene, texts 0x24B38/0x24C5C/0x235CE, 0x1E62, jump to the routine). Per-frame loop (0x1502): wrestlers (table 0x1DF0, 8 objects, 0xEA74 for those ≥4), 0xC6C8 referee, 0x212A6 ropes, 0x25064, 0x22462, 0xF844, 0x232DE, 0x1676 (music), 0x6BA0, 0x7CAE, 0x17D2, 0x435C, 0x1657E collisions; marks the frame (1C0019 bit0) and waits for the IRQ. End of match (1C0BC2/1C0BDA bits 7/6) → 0x178C. 1C0046 = frames. |
| 001326 | init_obj_ab2 | C | R | Object 1C0AB2: active, pose 0x10, state 8, pos (0xC6, 0x155, 0xBB). |
| 001676 | musica_combate | C | R | In a game, or in the demo with 1C0026&0xF=2: music 0x27 (bit7 = no loop if 1C0047 bit5=0). Otherwise: sounds 0xA7, 0x261BC(0), 0x28. |
| 0017C6 | modo_attract_creditos | C | R | Case of table 0x17B6: tst 0x1C0016 (credits) and jumps to 0x1DC8 (end of game → attract/0x1010). |
| 0017D2 | cargar_graf_luchadores | C | R | For each non-CPU wrestler (+0x2A bit3=0) calls 0x26120 with d0=+0x2B (id), d1=+0x2A bit1, d2=index. |
| 001810 | gana_equipo_A | C | R | Case of 0x17B6. d2=1 if in team B the legal one (+0x2A bit1) has +0x19==1 (or 0x1C1852<0 → d2=0). If 0x1C0026 bit6 (human in B) → 0x1A30 (human's defeat). Otherwise: 0x1AC8 (victory sequence); if it returns CC → 0x1DC8. 2-player mode → 0x1926. Rest: d0 = ids from table 0x1C7E of the winning wrestlers, 0x1C0026 bit7, frees opponents (0x1CFA), advances match (0x1D22) and stores new opponents in 0x1C0085/87; returns to 0x113C. |
| 0018D2 | gana_equipo_B | C | R | Symmetric to 0x1810 for team B (bit7 → 0x1A30, ids 0x1C0479/0x1C035F, 0x1C0026 bit6, opponents in 0x1C006F/71). In mode 2 (versus) 0x1926: clears screens, palette 6 and mode 6 (0x1F434). |
| 0019C6 | empate_o_derrota | C | R | If team A's leader is CPU → 0x1810; if B's is CPU → 0x18D2. Otherwise (both human): sounds 0x15 and 0x23, 0x80 frames, 0x651C, clears boxes and ends (0x1DC8). At 0x1A30 (human defeat): sounds 0x15/0x23, at frame 0x3F if d2 text 0x9B and 0x2660E; then continue screen 0x853E: if continuing restores teams (0x1EE8/0x1F22) and returns to 0x13A2. |
| 001AC8 | secuencia_victoria | C | R | 0x20 match frames (0x1C86). Match 9 (final): sounds 0x38, 0x09, 0x22; +0x40=0xC on all 4; 0xE8 iterations with energy refill 0x2060 and bars 0x7CAE; then palettes 0, sound 0x12, FINAL 0x2387C, cleanup, 0x245BE and CC (end of game). Rest: sound 0x38 if match 4, otherwise 0x39; text 0x0C; same refill; match 4: palette 8, sound 0x0D, scene 0x2347E, 0x100 skippable frames, 0x2387C. Returns CS (continues). |
| 001C86 | frames_combate | C | R | d6+1 frames: 0x221CA, 0x25064, 0x22462, 0x6BA0, 0x435C, copies sprite counter, 0x455C, 0x2516; requests vblank (0x1C0019 bit0) and waits for bit1; 0x1676; 0x1C0046++. |
| 001CFA | liberar_rivales | C | R | bclr bit7 of 0x1C00A2[d5&F] and [d6&F] (words). |
| 001D22 | avanzar_combate | C | R | 0x1C0029++ skipping 3→4 and 8→9; if it reaches 0xA → end (0x1DA4: clears, 0x245BE, 0x1DC8). Matches 4 and 9: fixed pair d2=0x706 or 0x607 (rng bit2). Rest: 0x21AE by level. 0x1DC8: clears 0x1C0024/28, sound 0, to 0x1010 if there are credits, otherwise to 0xE60. |
| 001E38 | esperar_saltable | C | R | Waits d1 frames (0x453A); after the first 0x10 it allows exiting with buttons (0x1E90 CS). |
| 001E62 | texto_y_esperar | C | R | If d3==FFFF only waits; otherwise, palette fade 0x24B54 (d3=1, a3=0, d2=1) and waits d1-0x10. (Corrected: 0x24B54 is the palette fade, not text.) |
| 001E90 | boton_pulsado | C | R | CS if P1 or P2 have bit4 or bit5 pressed (active low). |
| 001EC4 | borrar_caja_fg0 | C | R | Clears 20 rows × 25 longs of fg0 from 0x80390 (row 0x80 B). |
| 001EE8 | guardar_equipos | C | R | Stores +0x2A and +0x3C of the 4 and 0x1C0026 in d0-d7. |
| 001F22 | restaurar_equipos | C | R | Inverse of 0x1EE8. |
| 001F5C | indicador_activar | C | R | 0x1C1A7A[d0*4]: bit7, bit6 if obj+0 bit0, phase 2, duration 0x40. |
| 001F86 | destello_paleta_seleccion | SC: which screen element uses that colour (portrait frame?); xBGR444 format assumed | R | Selection screen: 6 indicators (one per wrestler, activated by 0x1F5C from 0x7552 on confirming, 0x40 frames; bit6 according to the cursor's bit0, probably player). Every 2 frames phase 0..2: they are NOT sprites or tiles, it writes a colour with 0x2636 into palette RAM 0x140200 (table 0x268E[1]) at (palette,colour) from 0x2048: (0,15),(1,15),(2,1),(3,15),(4,15),(5,12). Colours 0x2054: 0x0F66/0x0F0F/0x00F0 (lilac-blue, magenta, green); 0x205A in another order. When finished, it restores. Render: obj1f86/. |
| 002060 | recarga_energia | C | R | If 0x1C0BC2≥0 refills team A's wrestlers (counters +0x40); if 0x1C0BDA≥0 team B's. 0x1C0BC2/0x1C0BDA are team flags: their origin is pending. |
| 0020C2 | recarga_uno | C | R | If d7≥0: d7-=4; if DSW2 bit7==0, +0x3C += 4; cap 0x30. |
| 0020EC | energia_llena_si_eliminado | C | R | If 0x1C0BC2<0 sets +0x3C=0x30 in A; if 0x1C0BDA<0 in B. |
| 00211E | sonido_publico_fuera | C | R | Legal A (bit1 of +0x2A, or the partner) and legal B: if both +0x19==1, or either ==2 → the first time sound 0x22 + 0x1C183E bit7; repeats 0x22 every 0x50 frames (0x1C1A9D). Otherwise, clears 0x1C1A9C. |
| 0021AE | elegir_rivales_nivel | C | R | jmp table 0x21C4[0x1C0028&F]. Returns d2 = (id1<<8)/id2. |
| 0021EC | rivales_nada | C | R | rts |
| 0021EE | rivales_primeros_libres | C | R | The first 2 of 0x1C00A2 without bit0 (defeated); sets bit1 on them. |
| 002228 | rivales_azar_a | C | R | Two rng&1: the n-th defeated and the n-th undefeated without bit7. |
| 002284 | rivales_por_seleccion | C | R | Marks bit0 of those with bit15 and uses 0x71E8 (choice like the selection screen) with 0x1C0084/86 saved. |
| 0022D2 | rivales_azar_uno | C | R | rng&7 (<6, otherwise 0) and advances to an undefeated one; d7=6 fixed. |
| 002308 | rivales_primero_y_azar | C | R | d6 = first free (bits 0-1 at 0); d7 = rng&7 (<6) without bit7 and different from d6. The common ending 0x2352 swaps d6/d7 with rng&1. |
| 002368 | limitar_6 | C | R | d0=0 if ≥6. |
| 002372 | fundido_paletas | C | R | 16 steps: on each vblank (0x180009 bit0) subtracts 1 from R, G and B of palettes 0x140200/0x140000/0x140100 (64 colours each). |
| 002422 | oscurecer_64 | C | R | Subtracts 1 from each non-zero colour nibble in 64 entries. |
| 00246C | enlazar_rivales | C | R | +0x68 of 1C0334 and 1C044E = 1C0100; +0x68 of 1C0100 and 1C021A = 1C0334. |
| 0024AE | borrar_ram | C | R | 0x1C0014–0x1C1AAF. |
| 0024C8 | borrar_bg0 | C | R | 0xC0000–0xC0FFF. |
| 0024E2 | borrar_fg0 | C | R | 0x80000–0x80FFF. |
| 0024FC | borrar_objetos | C | R | 0x1C0100–0x1C1AAF. |
| 002516 | borrar_sprites_sobrantes | C | R | Clears the pieces between the new counter 0x1C208C and the previous one 0x1C208E. |
| 00254E | borrar_sprites | C | R | Counters and buffer 0x1C1AB0 (75×10 B) and sprite RAM 0x100000 (0x400 B). |
| 00259A | copiar_sprites | C | R | 75×10 B from 0x1C1AB0 to 0x100000. |
| 0025B8 | flip_pantalla | C | R | DSW1 bit7 (active low) → bit0 of 0x1C2B9C → 0x18000A. |
| 0025E6 | pedir_sonido | C | R | Except for 2 and 0x22 it clears 0x1C00E6. Sends only if 0x1C001A≠0 or DSW2 bit2=1 (sound in demo). 0x34→0x48 if a0+0x19==1. Writes the word to 0x180008 and waits 0x81 loops. The Z80 only sees the low byte (latch 0x180009 → NMI → queue 0x8400). Command map in sistemas/sonido.md. |
| 002636 | encolar_escritura | C | R | Entry 0x1C18BC: table, row, col, value. Addr = 0x268E[table] + row*0x20 + col*2 (the base table is at 0x268E). Queue 0x1C18C4 (max 0x20). |
| 00269A | aplicar_cola | C | R | Writes the queued words and empties the queue. |
| 0026BC | delta_objetos | C | R | a0=*(0x1C004E), a1=*(0x1C0052): /dy/→0x1C0052, /dx/→0x1C0050, signs in 0x1C004E bits 1/0. |
| 00270C | angulo_objetos | C | R | Approximate angle (atan by quotient×0x40 / sum, octant table 0x2782) from a0 to a1 → byte 0x1C004E. |
| 002786 | fuera_de_pantalla | C | R | CS if x ∉ (camx−0x30, camx+0x130) or y+z ∉ (camy−0x40, camy+0x150). |
| 0027D2 | trayectoria | C | R | Velocities +0x24/+0x26/+0x28 and gravity +0x22 from table 0x2814[d0]; mode 2 (cartesian); vx negated if facing left (except d0=0x11). |
| 0029DC | forzar_paletas | C | R | 0x1C003E=0, 0x1C0042=FFFFFFFF, load. |
| 0029F6 | cargar_paletas | C | R | Waits for vblank; for 3 banks, if 0x1C003E[i]≠0x1C0042[i] copies 8 palettes×15 colours from table 0x2A60[i][id] to 0x2A6C[i] (colour 0 to 0). |
| 003B42 | paletas_luchadores | C | R | 15-colour palette from table 0x3BC8[+0x2A&FF] (alternative 0x3BEE if the id is in list 0x3BE8 and +0x32 bit7: colours for the same wrestler repeated) → 0x140100+0x20*i; +0x1A=0x8000+0x10*i. |
| 003BFE | decorado_por_nivel | C | R | Level 0x1C0028 (1..; 0 and 5 nothing): tile blocks from table 0x3C5A queued and applied. |
| 003DCE | mover | C | R | jsr table 0x3DEA[+1]. |
| 003DF0 | mover_polar | C | R | d0=+0x1E (speed.l: high=direction, low=magnitude; ×2 in the low word), 0x3E8E → dx,dy (8.8) added to x/y. |
| 003E20 | mover_cartesiano | C | R | x+=vx*2, y+=vy*2, z+=vz*2 (8.8); vz−=g*2 (+0x22); minimum vz 0xF800. |
| 003E8E | polar_a_xy | C | R | Octant = direction>>5 (8 of 32 steps). Cases 0x3EC4–0x3F6E: one axis = 32·v and the other = f·v (f = 0..31 or 32−f), with the signs of each octant. It is a linear approximation (rhombus/square): it uses neither sine nor cosine. |
| 003EC4 | oct0 | C | R | (+32v, +fv) |
| 003ED8 | oct1 | C | R | (+(32-f)v, +32v) |
| 003EF2 | oct2 | C | R | (−fv, +32v) |
| 003F06 | oct3 | C | R | (−32v, +(32−f)v) |
| 003F24 | oct4 | C | R | (−32v, −fv) |
| 003F3C | oct5 | C | R | (−(32−f)v, −32v) |
| 003F5A | oct6 | C | R | (+fv, −32v) |
| 003F6E | oct7 | C | R | (+32v, −(32−f)v) |
| 003F8C | leer_mandos | C | R | d0 = ~(P2<<8 / P1) & 0x3F3F (bits 0-3 direction, 4-5 buttons). The tst 0x1C001A + nop is a patched leftover. |
| 003FAE | repartir_mandos | C | R | Reads the pads and jumps via table 0x3FC6[0x1C0026&3]. |
| 003FCC | mandos_tag | C | R | Tag mode: P1 → pair A (1C0100, which copies to 1C021A) if 0x1C0027 bit0; P2 → pair B (1C0334→1C044E) if bit1. |
| 004000 | mandos_individual | C | R | If 1C0027 bit0: 0x40C0 for 1C0100 and 1C021A; if 1C0027 bit1: 0x40C0 for 1C0334 and 1C044E. 0x40C0 reads P1, or P2 if +0x2A bit5. |
| 00403E | mando_compartido | C | R | 0x4066 on a1 and copies +0x10D, +0x110, +0x114 and +0x116 to a2. |
| 004066 | procesar_mando | C | R | +0x10E=previous +0x10C; +0x10D = direction translated by table 0x40DA; +0x110 = buttons (bits 4-6); +0x114 = newly pressed ((prev^cur)&cur); +0x112 = current; +0x116 = OR of presses, cleared every 4 frames (0x1C0046&3). |
| 0040C0 | mando_por_bit5 | C | R | Uses P2's byte if +0x2A bit5. |
| 0040EA | relaciones_4 | C | R | 0x4100 for the 4 wrestlers. |
| 004100 | relaciones_luchador | C | R | If a0 is one of the 4, copies from table 0x42C2 the 3 "others" to 1C1814 and calls 0x4166 for each. |
| 004166 | relacion_con_otro | C | R | With the other object a1 it computes into a0, at the offsets of tables 0x42F2–0x4316: /dx/ (±0x20 if the action is 0xB, according to orientation), /dy/ and /dz/, and a flags word (left/right side, in front/behind, position relative to constants 0x4332/0x4334−0xBB, bits of +0x18 and +0x2A). Also copies +0x2C, +0x3C (energy) and +0x2A&FF of the other. It is the "perception table" used by the AI and collisions. |
| 00435C | encolar_todos | C | R | Queues if visible: the 4 wrestlers (0xEA4C), 4 objects from 0xBCB8, 10 from 0x7E22, 1C0568 and 23 objects from 1C155A (stride 0x1E). Objects 1C0682/78E/89A are not drawn with action 1. |
| 00439A | encolar_lista | C | R | For d0+1 pointers of a1: if visible (0x2786 CC) and not the previous exception → 0x43D4. |
| 0043CA | encolar_si_visible | C | R | 0x2786 and 0x43D4. |
| 0043D4 | encolar_dibujo | C | R | If active, action ≠0x10, +0x2C bit6=0 and pose ≠FFFF: 16 B entry in 1C2094 (max 0x40). Layer = +0x18&3; layer 1 is refined: bit4→4; bit7 and z≥0xBB→3; z≥0xD3→0. There are 5 buckets (table 0x449A, max 0x30) and the entry type goes by +0x1C&7 (0x44AE). |
| 0044BE | entrada_propia | C | R | bank(+2), pose(+4), anim(+6), x, y, z, attr(+0x1A). |
| 0044C6 | entrada_banco_rival | C | R | Opponent's (+0x68) bank +2, the rest own. |
| 0044DA | entrada_banco_rival_anim_rival | C | R | Opponent's bank +2 and opponent's anim +6. |
| 0044E6 | entrada_anim_rival | C | R | Own bank and opponent's anim +6 (shared holds). |
| 00450A | rng | C | R | seed(1C003A) = d0+seed+a1+a2+a4+a5+a6+d2..d7 (d1 and a3 are not added); returns (seed+1)>>8. |
| 00453A | esperar_vblanks | C | R | Waits d0+1 vblank edges (0x180009 bit0). |
| 00455C | dibujar_cubos | C | R | If there are entries: 4 buckets (table 0x457E) → 0x458E; counter to 0. |
| 00458E | dibujar_cubo | C | R | Sorts (0x45AE) and converts each entry (0x45FC). |
| 0045AE | ordenar_y | C | R | Bubble sort by the entry's word +8 (y), from highest to lowest. |
| 0045FC | entrada_a_sprites | C | R | sx = x−camx, sy = y+z−camy. Pose from table 0x6CD8[bank][pose]; offsets in 1C0000/2. For multi-piece banks ≤7 it assigns a palette (0x46A0). Pieces with 0x46F4 (max 0x4B). |
| 0046A0 | paleta_por_banco | C | R | Looks up the graphic's bank in 0x6CD8 and the wrestler using it → palette 0..3 (4 if none; 7 if the graphic < *(0x3B87E)) in +0xC. |
| 0046F4 | emitir_pieza | C | R | Piece in 1C1AB0 + n*10; type by bit0 of the first byte (0x4724: 0x472C or 0x47D2). |
| 00472C | piezas_lista | C | R | Block with explicit tile codes. |
| 0047D2 | piezas_consecutivas | C | R | Block of consecutive tiles (+1, or +2 if double height). |
| 004878 | pieza_x | C | R | x with flip (+2 bit7 negates the offset), +9, 9 bits; clips outside 0x108–0x1F8 (CS). |
| 0048D4 | pieza_y | C | R | y −8 (−16 if double height); clips at 0x110 (0xD8 in demo with 1C182C=0). |
| 004934 | pieza_cerrar | C | R | Marks the piece as visible; counter++; Z if ≥0x4B. |
| 004952 | pieza_color | C | R | d3 = palette (+0xC, or +0xD if bit7); d4 = flips (graphic bits XOR +2 bits 6-7). |
| 00497C | texto_0x20 | C | R | Text 0x23A28 (d1=0x20) and a fixed word in fg0 0x806DC. |
| 004A10 | monedas | C | R | In the IRQ: coins in SYSTEM bits 1-3 (active low) with 0x23-frame debounce and 4 reads; sound 0x2F; pricing according to DSW1 bits 0-2/3-5 (tables 0x4B6A coins, 0x4B7A credits); BCD credits in 1C0016 (max 99). If not in a game (1C001A bit7=0) resets the stack and jumps to 0x1010. |
| 004B4E | moneda_repetir | C | R | Waits and rereads the coins (AND with the first read). |
| 004C2E | escena_attract | C | R | Scripted scene with 1C182C=5: initialises (0x4D4C) and repeats the step of 1C09D2 (table 0x4D24) up to step 4 (or 9 if 1C180C bit1), with the animation of object 1C0AB2 (0x4E8E) and music 0x25408 the first time. |
| 004D4C | escena_init | C | R | 1C0100 at (0x98, 0x154, 0xBB) and 1C0AB2 at (0xC6, 0x155, 0xBB), both bank 0x10. |
| 004DCE | escena_paso0 | C | R | Animates 1C0100 (tables 0x4E76/0x4E82), sound 0x35 at step 3; after 9 loops goes to step 1. |
| 004E8E | escena_obj_ab2 | C | R | Script of 1C0AB2 by +0x2C (table 0x4EC6) and draws it. That in the match it is the referee is UNCONFIRMED: this scene does not prove it. |
| 004ECE | escena_ab2_quieto | C | R | anim 8 |
| 004ED6 | escena_ab2_anim | C | R | anim 9..11 every 8 frames |
| 004F08 | escena_paso1 | C | R | 1C021A: tile block 0 (0x5578) and 0x20 frames → step 2. |
| 004F48 | escena_paso2 | C | R | 1C0334: block 1 and 0x20 frames → step 3. |
| 004F88 | escena_paso3 | C | R | 1C0334: sound 0x46 and 2 blocks per phase (table 0x5086); when finished, step 4. |
| 0050B6 | escena_sub_021a | C | R | Alternating blocks 0xA/0xB of 1C021A. |
| 00512C | escena_paso4 | C | R | 0x10 frames → step 5. |
| 00516C | escena_paso5 | C | R | 3 blocks per phase (0x5246) → step 6. |
| 00526A | escena_paso6 | C | R | 4 blocks (0x52EE/0x52FE) → step 7. |
| 00530E | escena_paso7 | C | R | Sound 0x36, blocks 0x20+n and then the sequence 0x545E/0x5436 → step 8. |
| 00546E | escena_paso8 | C | R | 3 blocks per phase (0x551E) and a write to bg0 0xC0358 → step 9. |
| 00554E | escena_paso9 | C | R | 0x20 frames → step 0xA. |
| 005578 | encolar_bloque | C | R | Puts (d0, +0x30, +0x5C) into the first free slot (FFFF) of 1C186E/78/82 (5 slots); 0x55C6 draws them in the IRQ. |
| 0055C6 | dibujar_bloques_escena | C | R | IRQ: if 1C182C==5 draws the 5 blocks queued by 0x5578. |
| 005D80 | presentacion_combate | C | R | Music: in matches 4/9, 0xB if the opponent is 7, otherwise 0x10; in the rest 3 (does not repeat it if already playing). Palette 7. Match 0 (or 4/9 with 1C0026 bit6/bit7): modes 7/8 (0x1F434), names 0x62B0, placement 0x5F54/0x5FDE and 0x50 frames 0x5EC4. |
| 005EC4 | presentacion_bucle | C | R | 0x51 frames: sound 0x22 (crowd), animates the 4 (0x6192), 0x20824, names 0x6256 and drawing. |
| 005F54 | colocar_humano_A | C | R | Ids from table 0x7FE2[1C0070/1C006E] → +0x2B of 1C0100/1C021A; B = id 6; positions from 0x60EE; bank 0x10; +0x1A = palette id&7; ids 0, 1 and 7 are flipped; palettes 3; 0x611E. |
| 005FDE | colocar_humano_B | C | R | Same with 1C0086/84 and positions 0x6106 (opposite side). |
| 00611E | paleta_libre_cpu | C | R | Finds the first id 0..7 not used by A and gives B its palette (table 0x6172) at 0x140100+id*0x20. |
| 006192 | anim_presentacion | C | R | For d0≥2: cyclic animation from table 0x61F6[+0x2A&7]; then +4=+0xA, move (0x3DCE) and draw. |
| 006256 | nombres_actualizar | C | R | In modes 7/8 redraws the name if 1C1833/1C1835 changed. |
| 0062B0 | dibujar_nombre | C | R | 3 rows of 31 tiles from table 0x62EE (id*0x5D + side*0x117) in fg0. |
| 00651C | escena_fin_partida | C | R | After losing or drawing: clears and loads palettes 6/4, places 6 objects (0x65EC), 0x6796, mode 6, music 0x13, 0x101 frames animating (0x680A) and text 0x84B8. |
| 0065EC | fin_partida_colocar | C | R | In matches 4/9 with opponent 7 swaps B's +0x2A/+0x2B; 1C0122 bit7 = mode 2 and bit6 = match 4/9 (sound 0x37; otherwise 0x3C); deactivates the corresponding team; 6 objects from table 0x6766. |
| 006796 | paleta_libre_extra | C | R | Like 0x611E for objects 1C0568/1C0682. |
| 00680A | obj_fin_partida | C | R | Script by +0x2C&7 (table 0x6834). |
| 006848 | fin_p0 | C | R | Step 0 of the end-of-game script. |
| 0068FE | fin_p1 | C | R | Step 1 of the end-of-game script. |
| 0069A4 | fin_p2 | C | R | Step 2 of the end-of-game script. |
| 006AA6 | fin_p3 | C | R | Step 3 of the end-of-game script. |
| 006B98 | fin_p4 | C | R | Hides (+0x2C bit6). |
| 006BA0 | efecto_publico_azar | C | R | Object 1C09A6: if free, every 8 frames with rng&7 against mask 0x6C76 it appears at a position from table 0x6C78 (according to the camera and rng&0x38), with variant 0x3A or 0x40 chosen by rng against 0x6C77, and lasts 6 animation steps. They are the crowd's camera flashes (visually confirmed by Emilio in the arcade, 31-10-2026). |
| 006D2C | musica_combate | C | R | In game: if any human has energy index 0 (0x1CE9C) → music 8; otherwise, the one from table 0x6DC0[level] (except 1C1850 bit1). Only changes if different from 1C182A. |
| 006DD4 | musica_nivel | C | R | d0 = 0x6DC0[level]. |
| 006DEE | unirse_partida | C | R | In game with credits and 1C0026&0x300=0: table 0x6E2E[1C0027&3]. |
| 006E3E | unirse_nada | C | R | rts |
| 006E40 | unirse_P1 | C | R | If start is pressed (1C1A95 bit2), team A's free partner becomes human (/0x21) and the mode 0x103; spends a credit. |
| 006EC6 | unirse_P2 | C | R | Same for team B. |
| 006F4C | gastar_credito | C | R | 1C0016 −= 1 (BCD). |
| 006F64 | comprar_energia | C | R | In game with credits and not mode 2: start (0x7B1E) refills the human team's energy (table 0x7FEC[+0x2A&7]), 1C1850=0x80, 0x7CA6 and spends a credit. |
| 006FEE | energia_A | C | R | A's +0x3C = 0x7FEC[+0x2A&7]. |
| 00701E | energia_B | C | R | B's +0x3C = 0x7FEC[+0x2A&7]. |
| 00704E | pantalla_seleccion | C | R | Clears 1C00A2, music 0xA, palette 4, mode 4; time 0x180; cursors. Loop: read (0x7240), tick or confirmation, portraits and 1F86. When finished waits 0x40/0x70 frames, marks the chosen ones (0x71B4) and picks CPU opponents (0x71E8), or P2's in mode 2. |
| 0071B4 | marcar_elegidos | C | R | In 1C00A2[d0], [d1]: bit7 = in match and bit0 = already used. |
| 0071E8 | cpu_elige_pareja | C | R | Twice: rng&7 (<6), the next one without bit7 or bit0 → bit0 and it is stored in the pointer of table 0x7FD4. |
| 007240 | seleccion_leer | C | R | P1 (0x180004) and P2 (0x180006) → 0x727E; results in 1C0072.. and 1C0088.. (6 words). |
| 00727E | flancos_mando | C | R | d1 = direction (bits 0-3, active high), d3 = newly pressed; d4 = buttons (bits 4-5), d6 = newly pressed. |
| 00729C | seleccion_tick | C | R | While time remains (1C006A) moves the cursors (0x749E); if it runs out, 0x7328 (the CPU chose). When everyone confirms, the time becomes 1. |
| 007328 | seleccion_tiempo_fuera | C | R | Table 0x7340[mode&3]. |
| 007350 | tfuera_m0 | C | R | Mode 0: if not confirmed, random choice (0x73E8); if confirmed, end. |
| 00736E | tfuera_m1 | C | R | Mode 1: each pad's choice and move to the pair. |
| 0073B0 | tfuera_m2 | C | R | Mode 2: same as mode 0 with two players. |
| 0073DE | seleccion_fin | C | R | 1C0067 bit0 = end. |
| 0073E8 | tfuera_azar | C | R | Random wrestler choice (modes 0 and 2). Not confirmed (1C0066 bit7=0): every 16 frames (1C0046&0xF==0) it chooses; otherwise, jumps to display. With 1C0066 bit7 it chooses only if 1C0047 bit0=0. Choice: d0=(RNG 0x450A + 1C0046) mod 6, repeats while bit d0 of 1C0069 is set (taken); stores d0 in +0x14 with bit15 of 'chosen'. Display: if +0x14 has bit15 and its low byte differs from +1, sets +0xB=table 0x747A[(+0 & 7)*6 + d0] and calls 0x74C4; every 64 frames (1C0046&0x3F==0x3F) calls 0x7552. If all 6 bits of 1C0069 are set the loop does not end: whether that can happen is UNCONFIRMED. What 0x74C4/0x7552 do (portrait/sound refresh): UNCONFIRMED. |
| 00749E | cursor_estado | C | R | Table 0x74B4[+0x10&3]; its states 0x75B2/0x75B4 are rts. |
| 0074C4 | cursor_mover | C | R | If there is a direction: new index from table 0x74F2[pos*16+dir] (FF = does not move); portraits 0x762A. |
| 007552 | cursor_confirmar | C | R | If the wrestler is not taken (bit in 1C0069): marks it, stores the history and increments +0x12; in 2-player mode announces it (0x1F5C). |
| 0075B2 | rts_75b2 | C | R | rts. |
| 0075B4 | rts_75b4 | C | R | rts. |
| 0075B6 | retrato_dibujar | C | R | Frame and name of the wrestler under the cursor, flashing every 16 frames if repeated. |
| 00762A | retrato_borrar | C | R | Clears both blocks (table 0x78CA). |
| 007658 | cola_7658 | C | R | Continuation: d2=0x11 (continues in the next routine). |
| 00765C | bloque_fg0 | C | R | Writes a list (offset, tile) into fg0 with colour d2 (0x7658 uses d2=0x11). |
| 0078FA | attract_espera | C | R | Title/credits loop (0x2FF frames if there are no credits): 0x879A reads the starts. bit1 and 1 credit → mode 0x8001 (1 player); bit0 and ≥2 credits → 0x8101; bit2 and ≥2 → 0x203 (2 players); 1 or 2 credits are spent. Flashing texts with 0x2549E (INSERT COIN / PRESS START according to credits, with a cycle of 3) and 2 animated objects (0x7B6C). |
| 007B1E | start_pulsado | C | R | Z = !(1C1A95 bit1). |
| 007B32 | attract_init_objs | C | R | Clears 1C0100 and 1C021A. |
| 007B6C | attract_obj | C | R | With rng (mask 0x7C34) it appears at the position from table 0x7C66/0x7C86 and does 6 animation steps (0x7C36/0x7C4E). |
| 007CA6 | musica_forzar | C | R | Enters 0x6D2C without the damage check. |
| 007CAE | barras_energia | C | R | For each wrestler without +0x2A bit3: clears (0x7CD2) and draws (0x7CF2) its bar. |
| 007CD2 | barra_borrar | C | R | 6 entries (0x1F, 0) in the buffer of table 0x7D6A[i]. |
| 007CF2 | barra_dibujar | C | R | segments = ceil(energy/4), maximum 12, in half tiles; the whole ones come from 0x7D92 and the half from table 0x7D7A/82/8A according to mode and +0x2A bit5. The bar shows energy/4, i.e. 48 points = full bar. |
| 007D92 | barra_enteros | C | R | d2 tiles from table 0x7DD8/0x7DE0/0x7DF0. |
| 007E00 | borrar_objs_extra | C | R | Clears the 10 objects of 0x7E22 (0x10C B) and 1C1822. |
| 007E4A | crear_obj_78e | C | R | Creates the folding TABLE that breaks in two (object 1C078E, id 1, outside the ring at 0x300,0xC8, palette 7; graphics bank 8, poses 0x3B402). It is not created in matches 4/9 (André's), which also disable the object logic. Identity CONFIRMED by Emilio (seen in the arcade) and by the sprite render (obj78e/). |
| 007EB6 | preparar_combate | C | R | 0x7EE6 and then 0x7FFC with 1 (mode 2), 0 (match 0 or human team B) or 2. |
| 007EE6 | init_luchadores | C | R | 5 objects (table 0x7F9A): clears them keeping +0x3C and +0x2A bit13; id = 0x7FE2[selection]; +0x2A from table 0x7FAE; +0xDA=3; in match 0, energy = 0x7FEC[+0x2A&7]. |
| 007FFC | colocar_combate | C | R | Assigns control according to the mode (table 0x805A) and the CPU's energy from table 0x8190[level*16 + id*2] + (1C004A&3)*8; initial positions (x, y, z, +0x18, anim) from table 0x8230. |
| 008066 | ctrl_modo0 | C | R | A human (+0x20 partner in match 0 with mode bit0); B's CPU is given energy by level and +0x2A bit3. |
| 0080F6 | ctrl_modo1 | C | R | A1 human; B1 /0x21 and B2 /0x20 (human P2). |
| 008110 | ctrl_modo2 | C | R | Energy by level for CPU team A; B human. |
| 008276 | elegir_legales | C | R | Table 0x828E[mode]: the "legal" wrestler of each team (the one with +0x2A bit0, or the other) → 1C18AC/1C18B0; +0x2A in 1C18AA. |
| 00829E | rts_829e | C | R | rts. |
| 0082A0 | asignar_controlados_a | C | R | Table 0x7F9A: 1C18AC = the wrestler in control (+0x2A bit0) of pair 0/1 (1C18AA = its +0x2A); 1C18B0 = the one of the side (bit1) of pair 2/3. |
| 0082DA | asignar_controlados_b | C | R | Same with the pairs swapped. |
| 008314 | asignar_controlados_c | C | R | Same: both with +0x2A bit0. |
| 00834E | nada | C | R | rts |
| 008350 | inicio_combate | C | R | Time 1C002E=0x180; 2 drawing frames; according to table 0x84AE[match] and tag mode, decides which partner starts outside (+0x5C=7, +0x33 bit7). Then bars, scoreboard, music 1, sound 0x3B, waits 0xC0, sound 0x20 and waits 8. The start bell is 0x20 (OKI sample 1: spectral peak 2,360 Hz, exponential decay of 1.5 s), not 0x3B (sample 0x1C). 0x21 (sample 2, same frequency, sustained) is the repeated bell of musica_combate and the end of time. Deduced from the spectrum and the call context, without listening to it. |
| 0084B8 | texto_fin_partida | C | R | Texts 0xF, 0x10 and 0x11 of 0x23A28, each with 4×(1 frame + 0x206BE). |
| 00850A | fg0_rellenar_area | C | R | 14×16 fg0 cells from 0x80120 = 0x1100F3. |
| 00852A | espera_fundido | C | R | 4×(1 frame + 0x206BE). |
| 00853E | continuar | C | R | CONTINUE countdown: 1C001C=0x10 (BCD), every 0x30 frames decreases by 1 (0x870C); a flash (0x85D0) animates bg0. If start is pressed with enough credits (0x8758) → CS (continues); if it reaches 0 → 0x886E and CC. |
| 0085D0 | continuar_anim | C | R | Alternates graphics 0x2123E/0x21272 every 8 frames and animates tiles in bg0 0xC00C0 with table 0x207F6/0x20800. |
| 0086A2 | continuar_textos | C | R | Price/number texts (0x2549E with table 0x89A4) and 0x34. |
| 00870C | continuar_tick | C | R | Decrements the number 1C001C every 0x30 frames; CC on reaching 0. |
| 008758 | continuar_start | C | R | Reads the starts (0x879A); according to the mode (table 0x878E) requires the corresponding button and charges 0x88E6 credits. |
| 00879A | leer_starts | C | R | d0 = bit1 P1 start (0x180004 bit7), bit0/bit2 of P2 (0x180006 bits 6/7); edge in 1C1A94; 1C1A96 = state. |
| 0087FC | cont_m0 | C | R | Start bit1 and enough credits. |
| 008820 | cont_m1 | C | R | Start bit2 and enough credits. |
| 008842 | cont_m2 | C | R | Start bit0 and enough credits. |
| 00886E | game_over | C | R | In modes 0/1: text 0xB and 0x100 animation frames. In mode 2 (versus) there is no end: the mode becomes 1 player (0x4000 or 0x8000 according to 1C0BC2 bit7, i.e. who won) and 1C001F bit4. |
| 0088E6 | precio_continuar | C | R | d1 = credits per game (table 0x4B7A according to DSW1 and 1C0015), double in mode 1; compares with 1C0016 (CS if not enough). |
| 00895C | bg0_limpiar_zona | C | R | 7×8 longs of 0xC0050 to 0. |
| 008980 | fg0_limpiar_zona | C | R | 14×16 longs of 0x80120 to 0. |
| 0089A8 | demo_preparar | C | R | Demo: ids from table 0x8AB0[level] (4 columns of 10), mode 0, 0x7EB6; CPU controls (+0x2A: 0xA/0x1A/8/0x18), energies 0xFFF/0xF00/0/0, fixed opponents, partners outside (pos 0x260/0x3B0) and duration 1C1984=0x400. |
| 008AD8 | intro_escena | C | R | Wipe 0x25408 (d0=1) and 0x25474, clears bg0 and sprites, mode 1C0040=5 (0x29F6), waits 8, scene 0x1F434 with d0=5, 1C180C bit1 = NOT(1C0025 bit1), scene 0x4C2E, clears 1C180C; if 1C0025 < 4: another wipe, waits 8 and clears bg0/sprites. (Corrected: 0x25408 is the wipe, not music 1.) |
| 008C82 | luchador_update | C(A) | A | Per-frame update of a wrestler: CPU/human flags (+0x2A bits0/1/3), 0x162A0, and dispatch of action +0x2D via table 0x8CE2 (33 actions). |
| 008D66 | acc0_cpu_comun | C | R | Action 0 (standing) in the CPU/partner branch: if +0xF2 bit6, +0x5C=0; initialises 0x911E; table 0x8D8A by +0x18&3 (plane: ring, outside, post…). |
| 008D9A | acc0_plano0 | C | R | If +0x5C&7≠7: orient (0x919C), zone (0x9202), idle pose (0x92BE), 0x21E5A and 0x8E7A; if it is 7, 0x8DC0. |
| 008DC0 | acc0_espera_tag | C | R | +0x5C=7: orients by zone (0x91DC/0x9202) and calls 0x19E3A. |
| 008DD8 | acc0_plano1 | C | R | jmp 0x1A532 |
| 008DDE | acc0_plano_b | C | R | If +0x5E bit6 → action 0x1C; otherwise, 0x1A830. |
| 008DFE | acc0_plano3 | C | R | Subtable 0x8E1E[+0x5D&7] → 0x1B54A/0x1B656/0x1BBB4/0x21ED0/0x1BCB6/0x1BD5C. |
| 008E2E | apron_cpu_0 | C | R | Zone 3 / +0x5D: 0x1B54A (walk along the apron). |
| 008E40 | apron_cpu_1 | C | R | 0x1B656 (follow the opponent along the apron). |
| 008E52 | apron_cpu_2 | C | R | 0x1BBB4 (get down from the apron). |
| 008E5A | apron_cpu_3 | C | R | 0x919C, 0x9202, 0x92BE, 0x21ED0. |
| 008E6E | apron_cpu_4 | C | R | 0x1BCB6. |
| 008E74 | apron_cpu_5 | C | R | 0x1BD5C. |
| 008E7A | tag_contador | C | R | = 0x8E7E |
| 008E7E | tag_espera | C | R | Unless the legal opponent is in action 0xB (tag mode) or the wrestler is +0x2A bit1: in tag mode +0x10A++ and on reaching 0x60 (without tag, immediately) +0x5C=7 and it is set to 0. +0x5C=7 → CPU table 0x1B40C[7] = 0x19E3A: go to his corner and climb onto the apron (leave by tagging). |
| 008EC8 | acc_correr_cpu | C | R | Clears +0xA8 bit7 and continues at 0x8ECE. |
| 008ECE | correr_cuerpo | C | R | Init (0x945C), animation (0x94CE); if +0xF2 bit7, 0x9598; move (0x953C). |
| 008EEA | pasos_liberar | C | R | If 1C1828 == id, 1C1828=FF (frees the footsteps sound). |
| 008F08 | acc0_humano | C | R | Human's action 0: CPU (+0x2A bit3) or +0xF2 bit7 → 0x18E70 (AI/automatic); +0x2A bit0=0 → 0x8D66; +0x33 bit4 clears bits 2-3; table 0x8F58 by plane. |
| 008F68 | acc0_h_ring | C | R | Subtable 0x8F7E[+0x5C&7]. |
| 008F9E | acc0_h_andar | C | R | Walking with the pad: direction → velocity (0x919C, 0x924A anim, 0x9310 velocity, 0x3DCE) or idle (0x92BE); 0x21E5A (limits); climbing the post (0x9738); buttons 0xF78E → 0xCD2C / 0xC706 (strikes with d3=0). If any opponent is in action 0x17 the tag counter does not run. |
| 009014 | acc0_h_fuera | C | R | Subtable 0x902A[+0x5C&7]. |
| 00904A | acc0_h_fuera_andar | C | R | Same as walking, but with the outside-the-ring limits (0x21ED0), 0xD2D6 and buttons 0xC706 (d3=1). |
| 009094 | acc0_h_apron | C | R | Only in tag mode (otherwise, action 7): walking with 0x220C4 and 0x1B942; 0x90DE. |
| 0090DE | tag_relevo_fin | C | R | If the legal opponent and his partner are on plane 1: clears +0x2A bit0 (stops being legal), action 0 and +0x5C=2. |
| 00911E | acc_init_de_pie | C | R | First time (+0x2C bit7): clears counters (+0x36, +0xA8, +0xBE, +0x104, +0x102, +0x9E, +0x1C, +0xC8), anim 1, zone and idle pose. |
| 009184 | anim_reset | C | R | Clears +0x36 and +8, marks init, clears +0xA8 and +0xBE. |
| 00919C | orientar_y_dir | C | R | +0xA = sign(x_opponent − x) (faces the opponent +0x68). With direction (+0x10C): angle from table 0x9334 → +0x1F, CC; without direction: velocity 0, CS. |
| 0091DC | orientar_zona | C | R | +0xA = bit15 of entry +0x6E[+0x6C*16]; CS if negative. |
| 009202 | zona_flags | C | R | +0x18 bit6 ← bit14 of the zone entry; if 0 and the plane matches and entry+4 < 8 → bit6=1. |
| 00924A | anim_andar | C | R | 4-frame cycle from table 0x93AE (+8 if +0x18 bit6, +0x10+n*0x10 if carrying someone, +0x5E bit6). |
| 0092BE | pose_quieto | C | R | Pose from table 0x9308 according to whether carrying someone (+0x5E) and +0x18 bit6. |
| 009310 | velocidad_andar | C | R | +0x20 = table 0x933E[id][direction] (each wrestler has his own). |
| 0093EE | acc_correr | C | R | CPU → 0x1BE30. Not legal → 0x8EC8. Init, and if no automatic 0xCC26 (running strike, CC → continues); animation, movement; if the direction is the opposite one (table 0x9600 versus +0x1F) → action 0x14 (brake). |
| 00945C | correr_init | C | R | Only the first time (+0x2C bit7): clears +0x22/24/26/36/104/A8, +8=1, +1=1, +0x18 bit7=0; velocity 0x95BC[id] → byte +0x21; angle +0x1E = 0x40 or 0xC0 according to orientation +0xA bit7 (corrected: it used to say 0/0x80); if 1C1828 == 0xFF, 1C1828 = id (+0x2B). |
| 0094CE | correr_anim | C | R | Animation from table 0x95C4[id]; sound 0x24 (footsteps) on frames 0 and 3 only for the wrestler of 1C1828. |
| 00953C | correr_mover | C | R | Moves. Outside the ring: if it crashes (+0x9E&3) → action 8 sub 7. In the ring: if it touches the rope on the side it is running towards → +0xA8++ and +0x2C=2 (bounce). |
| 009598 | correr_auto | C | R | 0x1B120 (automatic control); if it finishes, action 0x14 and CC. |
| 00960A | acc_rebote_cuerdas | C | R | Turns (+0xA ^ 0x80), anim 0x10, velocity 9 decreasing by 1 per frame; 0x9700 marks the touched rope in 1C1898 (plane bit0) or 1C189A. After 2 steps continues according to +0xA8 (table 0x96A4). |
| 0096AA | rebote_seguir | C | R | Action 1 (run), or 0x15 if +0xA8 bit7, with the running speed. |
| 0096F0 | rebote_parar | C | R | Action 0, +0x5C=0, frees the footsteps. |
| 0096FE | nada | C | R | rts |
| 009700 | marcar_cuerda | C | R | 1C1898/1C189A bit15 and nibble = d0. |
| 009738 | subir_poste_chk | C | R | Only if +0x2A bit1: according to the touched corner (+0x9E&0xF <0xB, table 0x975C) checks distance <8 to the corners (constants 0x6D24–0x6D2A, 0x281, 0x37F) and that the direction (+0x10C) is the correct diagonal; if the post is free (bit in 1C1820), action 0xF (climb) and reserves it. |
| 009788 | poste_chk_a | C | R | Distance to the corner in y. |
| 0097D4 | poste_chk_b | C | R | Distance to the corner in y. |
| 009820 | poste_chk_c | C | R | Distance to the corner in x. |
| 00986C | poste_chk_d | C | R | Distance to the corner in x (0x281/0x37F). |
| 0098B4 | poste_esq0 | C | R | Corner 2 (direction 6/5). |
| 0098D4 | poste_esq1 | C | R | Corner 8 (direction 4/5). |
| 0098F2 | poste_esq2 | C | R | Corner 1 (direction 1/8). |
| 009910 | poste_esq3 | C | R | Corner 4 (direction 1/2). |
| 009958 | nada | C | R | rts |
| 00995A | chk_tabla_umbral | C | R | If +0x18 bit7 and /+0x24/ ≥ 0x400 → CC. Otherwise, compares +0x48 with table 0x999E[d0][+2]. |
| 0099BE | acc_recibir | C | R | "Receive/fall" action. If the previous sub-action +0x45 is 0x1C or 0x13 it deactivates object 1C0AB2 (bit7 of +0). First frame: if +0x5E bit6, the carried one (+0x60) goes to +0x2C=4. Jumps to sub-action +0x44 (table 0x9A14) with the parameters from table 0xA74A[+0x44] in a2. |
| 009AAC | rec_s0 | C | R | Turns, sound 0x14 (0x27D2) and falls to the floor (z 0xBB, or 0x80 outside) → action 0xB (on the floor) and sound 0x29; animation from table 0x9B3E/0x9B41. |
| 009B44 | rec_lanzado | C | R | Thrown sub-action branch: impulse (0x9BBE). |
| 009B52 | rec_lanzado_girado | C | R | Same, but turned. |
| 009B66 | rec_lanzado_txt | C | R | Same, with text 0x9B (0x2549E). |
| 009B7E | rec_lanzado_d7 | C | R | Same, with d7=1. |
| 009B88 | rec_lanzado_10 | C | R | Impulse 0x10. |
| 009B9A | rec_lanzado_20 | C | R | Impulse 0x20. |
| 009BBE | impulso_lanzado | C | R | x += ±d0; +0x18 bit7 (in the air); +8 from a2+0x10; sound from a2+0x12 (0x23 if it is id 7 in sub-action 1, or 0x12 if the opponent is 7); z += a2+0xE; anim a2+0. |
| 009CD0 | caida_cuerda_ring | C | R | If it hits a rope (+0x9E&3) → action 8 with sub-action 1 or 2. |
| 009CFC | caida_cuerda_fuera | C | R | Outside: sub-action 3. |
| 009D18 | rec_rodar | C | R | Sound 0x34 and the one from table 0x9E38; advances 0x30 per step with rope crash (0x9700); on touching the floor, action 0xB and sound 0x29. |
| 009E4C | anim_por_altura | C | R | Chooses the anim from a2+8.. according to the height above the floor (thresholds a2+2..). |
| 009E78 | empuje_ring | C | R | x ±0x10 with limits 0x21E5A; undoes if it crashes (except poses 0x9A/0xA1). |
| 009EC2 | empuje_fuera | C | R | x ±0x20 with limits 0x21ED0. |
| 009F02 | rec_contra_cuerda | C | R | Marks the rope, z ≥ 0xCB, sound 0x11, bounces (+0x24 negated); on falling to 0xBB → 0xB and sound 0x29. |
| 009F74 | rec_rebote_suelo_fuera | C | R | Velocity z/4 negated; on reaching 0x80 → action 0xB. |
| 009FCC | rec_empujado | C | R | Sound 0x25/0x1D/0x1B/0x19 according to sub-action and id; advances 0x30 with crash; to the floor → 0xB and sound 0x29. |
| 00A16E | rec_caer_fuera | C | R | Falls to 0x80 → action 0xB. |
| 00A196 | rec_sobre_rival | C | R | Places itself over the opponent (+0x68): x±0x10, y−2, z+0x28 (except opponent's +0x31 =0x34) and falls (0xA230). |
| 00A230 | caida_general | C | R | Moves. In the ring with rope → sub-action 2. If it crosses the ropes over the top (0xA39A) → goes outside (+0x19=1, +0x33 bit0). On touching 0xBB: 1C1858=0x81 (0x80 if id 7), action 8 sub 0x20, sound 0x29 if +2=7 and 0x3E (sub 0xA) or 0x34. Outside: floor 0x80. 1C1858 = screen shake, confirmed at 0x1621A (0x81 = short, 3 frames; 0x80 = 9 frames, id 7). |
| 00A358 | caida_pose | C | R | Pose 0x17, x += table 0xA392[id]. |
| 00A39A | cruza_cuerda_chk | C | R | Z if the side (+0x18 bit8) matches the orientation. |
| 00A3BC | nada | C | R | rts |
| 00A3BE | rec_suplex | C | R | Impulse 0/−0x10 and fall; in sub 0xA animates poses 0x9B+n with the times from table 0xA43C. |
| 00A440 | rec_vertical | C | R | Pose 0x9C, vz=0x10; to the floor: 1C1858, action 0xB, turns and sound 0x29. |
| 00A4C8 | rec_elevado | C | R | Sound 0x29, vz=0x30 and +0x28=0x100; to the floor → 0xB and sound 0x29. |
| 00A540 | rec_soltado | C | R | 0xA554; if it ends in 0xB clears +0x2C bit1. |
| 00A554 | rec_soltado_cuerpo | C | R | Sound 8, anim 0xA2/4. If the opponent was in 0x17 (hold) with him, releases him (action 8 sub 0x13) and clears fg0 cells 0x808BC/0x808C0. To the floor → 0xB. |
| 00A612 | rec_tumbado_por | C | R | Faces like the opponent, sound 0xE; falls with rope crash. |
| 00A6BC | rec_aturdido | C | R | Sound 0x15, pose 0x14F; to the floor, sound 0x29; when +8 ends → action 5. |
| 00A748 | nada | C | R | rts |
| 00A90E | acc_levantarse | C | R | z to the floor, pose 0x1A, time from table 0xAA00[+0xF0&7]. When finished, if CPU and next to the post (zone type 0xC, dist <0x30/<8): with rng&0xF < table 0xAA20[id] climbs the post (action 0xC, +0x30 from table 0xAA10, faces the side opposite the opponent); otherwise, action 0 (or 0xD if +0xF0 bit7). +0xF0 bit0 brakes the velocity by 8 per frame. |
| 00AA28 | acc_bloqueo | C | R | Releases whoever he carries; if not outside (or the opponent is not at 0x31=1) and 0x995A gives CC → action 0xA. Otherwise, pose 0x11 (0x12 if the opponent has +0xC1 bit0) for 6 frames and returns to 0. |
| 00AA9C | acc_aturdido_corto | C | R | 0xC6CA, releases, pose 0x14 for 0xC frames → action 0xE. |
| 00AAF2 | acc_aturdido_fin | C | R | Pose 0x14/8 until finished → action 0 and 0xB16A. |
| 00AB1E | acc_en_suelo | C | R | Action 0xB (downed). Init: z to the floor, pose 0x17, adjustment against the ropes (0xACA4). Time on the floor +0x38 = table 0xAF66[energy index 0x1CE9C]; for the CPU it is halved if 0x1CD80 gives CS, and +0x20 if coming from outside. Marks +0xD6 bit7 on the opponent and his partner (they can cover). Human: button mashing (+0x116) brings the getting up forward (0xAD12, threshold 0xAF6A[energy] → action 0x19). With +0x18 bit5 (being covered) goes to the pin exit: 0xADEA the human, 0xAE7E the CPU. When the time ends → action 5 (get up) unless the opponent is in 0x12/0x17/0xC-6. |
| 00ABA0 | tumbado_cpu_div2 | C(A) | A | Halves +0x38 if CPU dazed/≥threshold. |
| 00AC88 | suelo_ajuste_x | C | R | x ±0x38 |
| 00ACA4 | suelo_chk_cuerdas | C | R | Tests limits 0x30/8 in front and leaves the result in d7. |
| 00AD12 | suelo_machacar | C | R | Human: each press increases +0x34; on reaching table 0xAF6A[energy] → action 0x19 (quick get-up). CPU: if the opponent falls on him from the post (action 0xC with a sub-action from list 0xAF76, descending, at a relative height of 0x10–0x30), with rng < table 0xAF82[level][energy] (0xAF96 for id 7) dodges (action 0x19), and the opponent in sub 4 goes to action 5. |
| 00ADEA | pin_salida_humano | C | R | Covered human: threshold = 0xAF72[energy]/2. If the count of object 1C0568 (+0x2F = 1C0597) has not reached it yet, each press (+0x114) adds; with 0x30−energy presses → he escapes (action 0x1E). If the count reaches the threshold (and at 1C0595=2 with 1C059E≠0) he also gets out. On getting out, cancels the grabs (0xC554). |
| 00AE7E | pin_salida_cpu | C | R | Covered CPU, while 1C05A5 bit2 (count running): energy level d1 (0xAF26). d1=6 (energy 0) never gets out. d1=0 gets out if 1C0595=2, 1C059F≥1 and 1C0570≠0. In the others, gets out when count*2+(1C059E bit0 negated) ≥ d1 and 1C059F≥2 and 1C0570≥4 → action 0x1E and releases the opponent. |
| 00AF26 | nivel_energia_pin | C | R | d1 according to energy: ≥0x36→0, ≥0x30→1, ≥0x24→2, ≥0x19→3, ≥0xE→4, >0→5, 0→6. |
| 00AF9A | cpu_tirada_nivel | C | R | In tag mode outside match 0, the first time (+0x107 bit0) gives CC. Otherwise, rng&0xF against table 0xAFF4[level*3 + 0x1CEF4] (CS if the roll succeeds). |
| 00B012 | acc_alzar_lanzar | C | R | Deactivates 1C0AB2 (bit7). Animates with the poses from table 0xB0EA and carries the opponent on top (pose 0x9B, x±0x28, y−1, z+4). After 2 steps the opponent goes to action 8 sub 0x1C and turns, 1C185A=0x81 (activates the fg0 flashing message, see 0xF844), and text 0x9B (0x2549E); he goes to action 5. |
| 00B0F2 | acc_provocar | C | R | Outside the ring → action 0 and 0x8F08. Otherwise, alternates the poses of 0xB162 three times and returns to 0 (plus 0xB16A). |
| 00B16A | cpu_tras_accion | C | R | CPU: if 0x1D0E2 with table 0xB188 gives CS → +0x5C=0xC (table 0x1B40C[0xC] = 0x1A05E: move away from the opponent circling and ask for a tag). |
| 00B1A0 | acc_espera | C | R | Marks +0x2C bit6. |
| 00B1A8 | acc_espera_rival_1b | C | R | Waits while the opponent is in 0x1B; then action 0 and clears +0x1C on both. |
| 00B1D0 | acc_forcejeo | C | R | Lock-up with the opponent, who must be in action 0x11; otherwise, returns to 0. Init: velocities to 0; +0xFF counts the lock-ups (without +0xFE bits5/6); +0xAE=2; 0x16F58 and 0xB670. The human's direction (+0x116&3) goes to +0x28. +0x26 counts frames. If +0xAF bit1 → 0xB5C2. Window: CPU 0x20 frames; human 0x10 (or 8/0x11 according to bit1 of +0x2A; 0x30 if 1C001A≠0). At frame 0x10, in tag (1C0026 bit1) or with the CPU opponent winning roll 0x1CD80, enters pull/push mode (+0xAF=3/2). On closing the window with a direction → 0xB48C (wins the hold). Otherwise, alternates the poses from table 0xB46C[opponent id] with times 0xB468. When 0x2786 gives CS, both separate by 0x18 and return to action 0 (+0xFF to 0 if +0xFE bit7). |
| 00B2DC | presa_tick16 | C(A) | A | Grapple: at tick 16 the human wins if CPU dazed/≥threshold. |
| 00B422 | forcejeo_limite | C | R | If +0xFF > 3 → +0xFE bit7 and CS. |
| 00B442 | forcejeo_anim | C | R | Alternates 2 poses/times from tables a3/a1. |
| 00B48C | forcejeo_resolver | C | R | The opponent goes to action 0x10 and he to 0xC. The CPU chooses the hold with 0x1E05C. The human chooses it by input +0x28 with table 0xB5B2 (side 1) or 0xB5BA (+4 outside); if dir bit0 and +0x10D∈{1,2,8}, uses index 3. Without input, both go to 0x8011 (+0xAF 3/2). With sub 0x26 → mutual counter 0x145F2. Clears +0xAA, +0xFE bits5–6 and +0xFF. |
| 00B5C2 | forcejeo_anim | C | R | 2 steps of 4 frames with the poses from table 0xB650[opponent id]; when finished clears +0xAE/+0xAF bits. |
| 00B670 | forcejeo_ganador | C | R | Decides who wins the lock-up (+0xAF bit0). +0xFE bit6 gives direct victory. Without 1C001A, 1C0100 wins. In tag, 1C0046 bit1 decides. Otherwise, against the CPU (rng>>1&7) with table 0xB74A[level*8] (+0x50 if +0xFF≠2); with the opponent's +0xF8 bit7 or +0xF9 bit0, or +0xFF>3, the other wins. At the end 0xB7EA. |
| 00B7EA | ajuste_x_limites | C | R | Tests x±0x24 with 0xB822 and copies x to the opponent. |
| 00B822 | limites_x | C | R | 0x21E5A inside the ring; 0x21ED0 outside. |
| 00B838 | acc_presa_mantenida | C | R | Grapple on an opponent in action 0x13. At start: sound 0x2D, pose 0x105, +0x34=0xFF (−4/frame with +0x117), opponent facing at x±0x10 and 0xBBB2. When time ends, sub 3. Dispatches +0x44 via table 0xB91E. Sub 0 alternates poses 0xBCCC/0xBCC8; with 1C1898/1C189A (by side) bit14 = rope vibrating (0x21324) → 0x2786 → releases (both to action 0, +0x5C=0). If the opponent leaves 0x13 → releases and he goes to 0xD. |
| 00B92E | presa_sub0 | C | R | Sub 0 of 0xB838: alternates 2 poses (tables a5/a3) and checks 0xB988 (rope vibrating) → 0x2786 → releases (both to action 0, +0x5C=0). |
| 00B988 | presa_chk_salida | C | R | Reads 1C1898 (side 1) or 1C189A; with bit14, releases: the opponent to action 0 and he to 0xD (CC). Otherwise, CS. Bit14 = the rope on that side is vibrating (animation of 0x21324; it is not an input). |
| 00B9D0 | borra_objs_efecto | C | R | With +0x5C=0, frees objects +0x22/+0x26 and sets +0x5C=1. |
| 00BA18 | presa_sub_golpe | C | R | Tests 0x995A(d0=2): if it fails, he goes to action 8, 0xC6CA, the opponent to 0. Otherwise: pose 0xBE+id*2−(+0xC0&1), 16 frames and then 0xBA8C. |
| 00BA8C | presa_vuelta_sub0 | C | R | Timer; when finished, sub 0 and pose 0xBCCC[id]. |
| 00BAC2 | presa_sub_golpe2 | C | R | Like 0xBA18 with d0=3 and pose 0x125+(id&0xF), 8 frames. |
| 00BB2A | presa_sub_final | C | R | Poses 0xBCEC/0xBD0C, 2 steps; then releases and he goes to 0xD. |
| 00BBB2 | crear_objs_llave | C | R | Takes 2 free objects from list 0xBCB8 (4 pointers) and links them (+0x26 and +0x22) to the two wrestlers: one with pose 0 at x±0x10, and the other with pose 0xBC at y−2/z+2. They copy id, control and state. |
| 00BD10 | acc_cubrir_pin | C | R | Action 0x17 (action table 0x8CE2: entry 0x8D3E) = COVER (pin). Set by 0x12972 at the same time as it marks the opponent with +0x18 bit5 (covered), which is what moves the referee to state 2 (0xD7D8 → pin count 0xDD4E). Action of placing oneself on top of the opponent (a2=+0x68, mutual link). If it is the CPU: +0xC6=0x80 of a fixed wrestler per slot (1C02E0/1C01C6/1C0514/1C03FA). If the opponent is human: 1C185A bit7 (fg0 message). Pose 0x65 (0x7F for ids 0/4), or 0x188 with +0x2C bit5. Position from table 0xBEF2[id*0x10][opponent id] (dx, dz) and the opponent's y−1. Activates object 1C0AB2 (pose 0x80) with the same position. When finished (inside or without side 1): z=0x80, action 5, turns off 1C0AB2. |
| 00BF72 | acc_ir_a_punto | C | R | Computes the zone with 0xC018; if it is 0xFF, action 6. Otherwise, +0x1E=direction and animates with tables 0xC072/0xC082 (4 steps of 5 frames). |
| 00BFC4 | anim_ciclo4 | C | R | Cycle of 4 poses (table 0xC072, 5 frames) and orientation (0xC082) according to 0xC058; 0xC00A: action 6 and clears +0xC0 bit6. |
| 00C018 | zona_destino | C | R | Compares x and y+z with the point from table 0xC094[0xC058] and returns the direction from table 0xC084. |
| 00C058 | es_bit4_ctrl | C | R | d0 = +0x2A bit4. |
| 00C09C | acc_15_correr | C | R | 0x8ECE. In action 0x15: +0xA8 bit7 and +0x24++. Outside (+0x19=1), after 0x15 frames the CPU does 0x8EEA and goes to action 0x14. Inside, with +0xA8&0x8001 → 0xC116; outside the x limits 0x2F1/0x30F → action 1. |
| 00C116 | cpu_reaccion_carrera | C | R | CPU only. If the opponent does a hold from list 0xC2AA and is close (hitbox dz<8, dx<0x50) → roll 0xC34C → action 5 (+0xF1=3). At medium distance (0x20–0x40, or 0x40–0x68 according to id) → roll 0xC308 → action 0xC sub 0xC326[id]. At 0x30–0x4A (0x3B for ids 4/7) → roll 0xC32E → +0x26 bit4. |
| 00C2B4 | tirada_nivel3 | C | R | rng&7 against a2[level*3 + 0x1CEF4]. |
| 00C36A | acc_rodar_fuera_ring | C | R | Action 0x19 (entry 0x8D46). Set by the pin exits (0xAD3A, 0xADD2), 0x11610/0x118A6 (to the opponent) and 0x12B00 (to the covered wrestler when the count ends). Poses 0xC54C, sound 0x32. Sub 0: animates inside until +0x9F bit2 (contact with the rope) → sub 1: climbs until y<0xD8 and falls outside the ring downed. If already outside, ends in action 5. The name is descriptive: the code contains no move names. |
| 00C3DE | c36a_sub0 | C | R | Inside: animates 2 steps and then action 5. |
| 00C444 | c36a_sub1 | C | R | Dispatches +0x34 via table 0xC458. |
| 00C45C | c36a_trepar | C | R | Animates in a loop with physics 0x3DCE; when y<0xD8 → +0x34=1. |
| 00C4A6 | c36a_caer_fuera | C | R | y−8, z+8, sound 7 (0x27D2), +0x18 bit7, pose 0x16, +0x19=1 (outside). Falls with 0x3DCE; on reaching z<0x80 → action 0xB (downed) with bit1 and +0xAE=0. In the outside branch, animates with limits 0x21ED0 and then action 5. |
| 00C554 | tag_cambio_control | C | R | With side bit1: toggles +0x33 bit1. If both are human and 1C0026&3≠1: swaps the control bit0 between him and his partner (a1) and clears +0x10C/+0x110/+0x114/+0x116. Computes whether the partner is on screen (camera 1C002A/1C002E) → +0xF2 bit7 (off screen) and bit6. |
| 00C628 | acc_deslizar | C | R | +0x22=2; brakes +0x20 by 4 per frame with 0x3DCE and pose 0xB. Against the rope (+0x9E&3): inside → action 2 (+0xA8=2); outside → action 8 sub 7. Stopped: counts +0x23 and goes to action 0; +0x5C=1 if +0xF2 bit7 and not 1C0026 bit0. |
| 00C6C8 | nop | C | R | rts. |
| 00C6CA | sonido_44_2b | C | R | Sound 0x44, or 0x2B with +0x2A bit4 (mode 1C0026 bit1) or bit3 (CPU). |
| 00C706 | humano_golpe_boton | C | R | With button +0x116&3 in action 0, or in 0xC with sub<9 and table 0xCC1C. With +0x5E bit6 (carrying someone): sub from table 0xCB16. Otherwise, table 0xCADE (0xCAFE outside)[id][offset+button]. Offset according to the opponent (table 0xCB1A[opponent's action]): +0xC if downed nearby (0xFE), +6 in front (<0x20/0x28) or +9 behind (<0x30/0x38), with dz<0x18. 0xFF → action 1 and resets the input. Adjustments of subs 6/9 and 0xC9E2/0xCA4E. Action 0xC; sub 4 links the opponent in action 0x10 (unless the partner is holding him, action 0x17); 0xE462. |
| 00C9E2 | chk_sub3_alcance | C | R | Sub 3 is only valid with the opponent at dx<0x70 and dz<0x10, facing each other, and the opponent in action 1/2/0x15/0x16; otherwise, restores the action (d4=0x80). |
| 00CA4E | cpu_chk_alcance | C | R | CPU (or human in sub 0x10): if within 0x70 (0x30 in sub 0x10) in x and 0x10 in y, facing each other, and the opponent is not in actions 1/2/0x15/0x16 → +0x2C=d6, d4=0x80. Sub 0x10 with the opponent at energy ≥0x16 → +0x30=3. |
| 00CC26 | cpu_boton_a_sub | C | R | With a button in +0x116: sub = table 0xCD14[id*3+button−1] and action 0xC; 0xCC8A; CS. |
| 00CC8A | chk_golpe_por_cuerdas | C | R | If he is inside and the opponent outside (without bit4), dz<0x20 and on the correct side: tests x±0x80 with 0x21E5A; if it touches the rope and dx<0x100 → +0x30=0x35. |
| 00CD2C | chk_cuerdas_salir | C | R | Dispatches +0x9E&0xF (<5) via table 0xCD48. |
| 00CD5C | cuerda_lateral_izq | C | R | Without 1C1898 bit6, with direction 7 on side 1 and y+z in 0x1E0–0x230 → action 3 (+0xAC=0). A team human needs 12 frames (+0x102). Without bit4/side and inside → action 6. CS. |
| 00CDF8 | cuerda_lateral_der | C | R | Symmetric: 1C189A, direction 3, +0xAC=1. |
| 00CE8E | cuerda_frontal | C | R | Direction 5 with x 0x280–0x380 → action 3, +0xAC=2. CS. |
| 00CEC2 | cuerda_no | C | R | Clears +0x102 and CC. |
| 00CECC | acc_cruzar_cuerdas | C | R | Action 3: trajectory from table 0xD0AE (0xD1AA for id 7)[+0xAC] (+3 if +0x19=3), with steps (pose, dx, dy). At start copies the parameters to +0x22..+0x28 and 0xD00A. Between steps d0 and d1 it jumps (flight with 0x3DCE, +0x18 bit7) until z<0x80. When finished: action 0, +0x5C=0, z=0x80; 0xD04A. |
| 00D00A | cuerda_interp_x | C | R | Except with +0xAD 2/5: x = x0 ± (y−y0)/6 (diagonal rope). Otherwise, y=y0. |
| 00D04A | marca_pose_especial_id7 | C | R | Id 7: if the pose is in list 0xD092 (2 entries), 1C1A92 bit7 = 1 and 1C1A93 = +0x18 bit0; otherwise, clears the bit. |
| 00D2D6 | humano_salir_ring | C | R | With contact +0x9F and the direction (+0x10C=7/3, without 1C189A/1C1898 bit6) and y+z in 0x1A0–0x210 → +0xAC=0/1 (+3 with bit4/no side) and action 4 (7 if +0x19=3; 0x20 if carrying someone). Front rope: bit3, direction 1, x 0x280–0x380 → +0xAC=2. CS. |
| 00D400 | acc_entrar_ring | C | R | Sequence guided by table 0xD54C[+0xAC&0xF] (0xD646 for id 7): (pose, dx, dy) per step; +0x19=3 except in entry 2. When finished: +0x19 /= table 0xD52E, returns to action 0 and, in tag with the partner inside, text 0x9B. |
| 00D7D8 | arbitro_elige_estado | C | R | Referee (1C0568), except in state 4 with id 1. Takes the active wrestler (side bit1) of each team: 1C0100/1C021A and 1C0334/1C044E. New state: 2 if anyone is covered (+0x18 bit5); 3 if anyone is outside (+0x19=1) or in action 4; 1 if anyone does sub 0x13/0x2E (action 0xC) or action 0x1B (stores the wrestler in 1C05D0); 0 otherwise. If it changes, writes it to +0x2D and clears +0x2C. |
| 00D8F4 | arbitro_e0_seguir | C | R | Goes to the midpoint between the two wrestlers (0xDFE0), with y forced to 0x175 or 0x118 according to the side of 0x148. Direction with 0x270C (1C004E→1C0052), velocity 8. If the target changes side: +0x3D bit4 and the quadrant in +0x3C → goes around by the ropes with table 0xDB44. Faces the centre; if more than ±4 away, moves (0x3DCE) and walks (0xDA38). Limits 0x21E5A. |
| 00DA38 | anim_8dir | C | R | 4-frame animation every 8 ticks; chooses the pose by direction (+0xA in 8 sectors) in table 0xDAC4 (0xDB04 in state 3, or 4 with control 2). |
| 00DB54 | arbitro_rodear_q0 | C | R | Going around: minimum y 6D26+0x38−0xBB (leaves bit4); with contact +0x9F bit0 → direction 0x80, otherwise 0xC0. |
| 00DB8E | arbitro_rodear_q1 | C | R | Same with +0x9F bit1 → 0x80/0x40. |
| 00DBCE | arbitro_rodear_q2 | C | R | With +0x9F bit3 ends; bit0 → direction 0, otherwise 0xC0. |
| 00DBF8 | arbitro_rodear_q3 | C | R | With +0x9F bit3 ends; bit1 → direction 0, otherwise 0x40. |
| 00DC22 | arbitro_e1_vigilar | C | R | Goes next to wrestler +0x68, at x±0x30 (side according to x≥0x300), and on arriving (±4) alternates poses 0x12/0x13 every 4 frames, facing him. |
| 00DD4E | arbitro_e2_cuenta_pin | C | R | Pin count: approaches the midpoint (±0x20 x, ±0x30 y) and then slaps with the poses from table 0xDED4 and durations 0xDEDC (loop of steps 2–3). At step 3, frame 1: +0x2E++ and 0xE02C (shows/sounds the count). On reaching 3: writes the result to 1C0BBE+4 and 1C0BD6+4 (bit6/bit7 according to which side is covered, a1+0x18 bit5). |
| 00DEE4 | arbitro_e3_cuenta_fuera | C | R | Count-out outside the ring in BCD (abcd) up to 0x20 (20). Faces the wrestler who is outside (+0x18&3=1). Each animation cycle: +1 and 0xE02C. On reaching 20: 1C0BBE+4 / 1C0BD6+4 bit7 if that wrestler is outside (+0x18&3 ∈ {1,3}), otherwise bit6. Allows double disqualification by count-out. |
| 00DFDE | arbitro_nop | C | R | rts (empty state of table 0xD7AE). |
| 00DFE0 | punto_medio | C | R | a2 = midpoint between a2 and a1 (x and y). |
| 00E016 | arbitro_reset | C | R | Clears +8, +0x36, +0x2E, +0x2A and +0x18. |
| 00E02C | sonido_texto_estado | C | R | Sound from table 0xE0A8[+0x2E] (except 0xFF, or in state 3 with +0x2E<4), text 0x9B and the text of 0xE086[+0x2E]. |
| 00E132 | obj_nop | C | R | rts. |
| 00E134 | obj_seguir_portador | C | R | Copies the carrier's position (+0x60) with x±0x10 and his orientation. |
| 00E172 | obj_reposo | C | R | Pose 0xE1B6[id]; 0xE1BC; the first time, 0xE7E8. |
| 00E1BC | obj_ofrecerse | C | R | For each wrestler (table 0xE224) who is outside (+0x19=1) and not carrying anything: if it is the closest object in x, marks it as available (+0x5E bit7, +0x60=object, +0x64/+0x66 distance). |
| 00E234 | obj_romper | C | R | Sound 0x28; x±0x20, z+0x20; 5 pose steps (0xE2B8) and disappears (clears bit7 of +0 and 1C1823 bit1 or bit2). |
| 00E2CC | obj_lanzado | C | R | Flight with 0x3DCE (velocities 0xE374), pose 0xE37C[id] (+2 according to the thrower's +0x18 bit6). On falling (z<0x80): sound 0x27, action 2 and becomes available again (+0x5E bits 7/6). |
| 00E388 | obj_caida_desp | C | R | Dispatches +0x44&1 via table 0xE39E. |
| 00E3A6 | obj_rebote | C | R | Trajectory 0xE45A; pose 6/0xA (1 for id 0). On falling: sound 0x27, action 2 sub 3. |
| 00E462 | recoger_objeto | C | R | Searches among the 3 objects (1C0682, stride 0x10C) for one in action 2, at the same z, inside box 0xE542 and available. The CPU only picks up its target (+0x60). If found: action 0x1D, mutual link by +0x60, +0x5F=object id, +0x5E bit6 and the object to action 1. Otherwise: the CPU sets +0x5C=0. |
| 00E572 | acc_coger_obj | C | R | The CPU goes to 0x1CC36. The human: 0x9184 and 2 steps of 8 frames, base pose from table 0xE5F0[+0x5E&3]; then action 0. |
| 00E5F6 | acc_soltar_obj | C | R | The CPU goes to 0x1B326. Otherwise: 2 steps of 8 frames and then action 4 (0 without side). The object goes to action 2, at x±0x20, available; clears +0x5E bit6. |
| 00E6E0 | crear_obj_2 | C | R | Creates object 1C089A (id 2, 0x8002, action 5, available) at the position of 1C078E with z+0x20 and x±0x20; 1C1823 bit2. |
| 00E76E | soltar_obj_682 | C | R | Object 1C0682 appears where he is (z+0x20, x±0x20), action 5; 1C1823 bit2; clears +0x5E bit6. |
| 00E7E8 | obj_evitar_pared | C | R | Shifts x according to table 0xE874 (0xE880 in action 2) with the outside limits 0x21ED0; if it crashes (+0x9E&3), undoes. |
| 00E88C | zonas_todos | C | R | For the 10 objects of table 0xEA4C (except the referee) calls 0xE8A6. |
| 00E8A6 | calc_zona_18 | C | R | Except in actions 3/4/6/7 recomputes bits 0–4 of +0x18. bit0: x ≤ [0x4332]. bit1: y+0xBB < [0x4334]. bit2/bit3: corners/apron according to boxes 0xEA34 (side 1) or 0xEA40 (without bit2, clears +0xE3 bit0). bit4: +0x18&3=1 with y+0x80 ≤ 0x158. |
| 00EA74 | elegir_rival | C | R | With 1C001A≠0 and outside the states of table 0xEBCC/+0xC8: takes the two possible opponents from table 0xEBBC[slot] and dispatches by zone +0x18 (table 0xEAF0). Preference: the one holding (0x17) or doing sub 6, the uncovered one, the one in the same zone, the one on the active side. Writes +0x68 (opponent), +0xA0 (the other) and +0x6C (0/1). |
| 00EB00 | elegir_rival_z0 | C | R | Preferences of 0xEA74 for zone 0 (see there). |
| 00EB60 | elegir_rival_z1 | C | R | Chooses by matching side bit1. |
| 00EB72 | elegir_rival_z2 | C | R | Chooses the one with side bit1. |
| 00EBA0 | cmp_bando | C | R | Compares bit1 of +0x2A (side) of a0 and a2; branches of table 0xEAE6. |
| 00EBEE | acc_subtabla_b8 | C | R | Jumps by +0xB8 to table 0xEBFE. |
| 00EC12 | acc_subir_esquina | C | R | Climbs to the corner (+0x19=2) by steps from table 0xED20 (0xED40 for CPU id 2, which also extends +8 of the downed opponent to 0x40). Side/position by +0xB4 (copy of +0x18) with 0xECB8 and 0xECE2. When finished, +0xB8=2 (3 for the CPU on side bit1). |
| 00ECB8 | esquina_tablas | C | R | Selects the pose (a2) and position (a3[id]) tables according to +0xB4>>8&3; y from the table. |
| 00ECE2 | cpu_id2_sonido22 | C | R | CPU id 2: with d0=5 (or 3 if +0xB4 bit1) → +0xE2 bit0 and sound 0x22. |
| 00F018 | acc_bajar_esquina | C | R | Goes through the steps in reverse. When finished: z=0xBB, action 0, +0x5C=0, frees its bit of 1C1820 (+0x34), +0x19=+0xB5. If human without control bit0, +0x5C=7. |
| 00F098 | esquina_paso | C | R | Pose, x and z of step d0. CPU id 2 on the non-bit1 side turns from step 5. |
| 00F0DE | esquina_esperar | C | R | The CPU goes to 0x1C47E. The human dispatches by corner (+0x18&3) with table 0xF100. |
| 00F110 | esquina_q0 | C | R | Faces 0x80, pose 0x1F, position 0xF280. With control: remaps the direction (table 0xF6BA → +0x10D) and 0xF35A; otherwise, 0xF2B0. |
| 00F15E | esquina_q1 | C | R | Same facing 0 with table 0xF6C4. |
| 00F1AC | esquina_q2 | C | R | Faces 0, pose 0xF0DA[+0xBE&1]; without direction sets 4 (or 8 with +0xBF bit0); 0xF35A → 0xF2FA, 0xF2B0. |
| 00F218 | esquina_q3 | C | R | Same facing 0x80, direction 6 (or 2). |
| 00F280 | esquina_posicion | C | R | x, y, z from table 0xF6CE[corner]; +0x5C=0x7F (maximum time on the corner). |
| 00F2B0 | esquina_chk_bajar | C | R | Human: direction 5 (or 1 on side bit1) → +0xB8=1 (get down). Otherwise, decrements +0x5C; at 0 (or without control) → get down. |
| 00F2FA | esquina_elige_salto | C | R | If not in actions 3/4/6/7: according to the opponent (or +0xA0 if not the one on the side) at y≥0xDD → +0xB8=3, otherwise 4 (except poses 0x69/0x1F). |
| 00F35A | esquina_boton | C | R | Dispatches by corner with table 0xF37A. |
| 00F38A | esquina_boton_q0 | C | R | With a button in +0x114: 0xF636, 0xF684 and table 0xF3A6. |
| 00F3B6 | esquina_boton_q1 | C | R | Same with table 0xF3D2. |
| 00F3E2 | esquina_boton_q2 | C | R | Same (or with +0xBA bit7) with table 0xF406. |
| 00F416 | esquina_boton_q3 | C | R | Same with table 0xF43A. |
| 00F44A | dir_rotar_mas | C | R | +0x10C++ circular 1..8. |
| 00F466 | dir_rotar_menos | C | R | +0x10C-- circular 8..1. |
| 00F47A | salto_destino_q0 | C | R | Table 0xF6FE → 0xF498. |
| 00F482 | salto_destino_q1 | C | R | Table 0xF721. |
| 00F48A | salto_destino_q2 | C | R | Table 0xF746. |
| 00F492 | salto_destino_q3 | C | R | Table 0xF76A. Common: jump target in 1C00B4 (+0x16 x+dx, +0x18 y+dy, +0x14) according to direction +0x10C; +0xB6=1; +0x10=−1; continues at 0xF564. |
| 00F4DA | cpu_objetivo | C | R | Writes the target to 1C00B4: opponent (+0x10), x/y; if ≥0x30 away, the target is ±0x30 from him (+0x10 = −1). Opponent's z to +0xBE. Dispatches by +0x30 with list 0xF594 and table 0xF59C. |
| 00F636 | esquina_salto_sub | C | R | Sub from table 0xF6E6[id*3 + (opponent not downed)]; action 0xC; frees its bit of 1C1820. |
| 00F684 | const1 | C | R | d0=1. |
| 00F68A | b8_sub_pose68 | C | R | Pose 0x68 for 8; when finished, +0xBE^=1 and +0xB8=2. |
| 00F78E | tag_chk_relevo | C | R | Inside, on the side, with a button (+0x115), in the corner (+0x18 bit2, without +0xE3 bit0), with the partner in corner bit2, and at 0x150 (0x108 with bit4) ±0x10. If the partner is outside (+0x19=3) and in action 0: both +0x2A bit2 and action 0x1A (tag). CC. |
| 00F81A | esquina_ocupada | C | R | CC if the bit of table 0xF840[corner] is set in 1C1821. |
| 00F844 | flash_fg0 | C | R | With 1C001A≠0, manages 1C185A. bit7 → becomes bit1 with a timer of 3 (1C185B). bit1: every 2 frames toggles bit2 and draws text 0x1E/0x1F (0x23A28); with bit6 clears fg0 cells 0x80B04–0x80B18. bit0: clears 9 rows of fg0 from 0x80B04 and sets 1C185A to 0. So 1C185A=0x81 is a flashing message in fg0 (text 0x1E/0x1F), not a shake. |
| 00F94C | acc_0c_llave | C | R | Action 0xC: 0x240B6 (holds by sub); inside, if it hits the rope, 0xF9B0. Dispatches +0x30 via table 0xFB58. On leaving 0xC clears +0x33 bit3 of both. |
| 00F9B0 | llave_fuera_ring | C | R | If the opponent is not in action 0x10 → action 8 sub 1. According to sub-action +0x31: 0x1B/0x21/0x22/7 place both at x=0x280/0x390 (according to +0x9F bit0) and give them action 8; 0x29 and 0x28 are variants of that placement. |
| 00FC4C | nop | C | R | rts. |
| 00FC4E | despacho_id | C | R | Calls table 0xFC64[id]. |
| 00FC84 | sub_combo_golpes | C | R | The CPU goes to 0x15758. Three steps of table 0xFD70 (0xFD88 for id 7; 0xFD7C/0xFD94 with +0xC0 bit0). At steps 0xB/0xC accumulates the buttons in +0x22. With button 1 toggles +0xC0 bit0 and repeats (combo); otherwise, action 0. |
| 00FDA0 | sub_combo_golpes2 | C | R | Like 0xFC84, with table 0xFE88 (0xFEAC for id 2) and 10 steps. At steps 0x10/0x1C toggles +0xC1 bit0 and checks button 1 to chain; accumulates +0x114 into +0x22 except at steps 0/0xC/0x18. Without a button: action 0. |
| 00FED0 | sub_golpe_simple | C | R | Three steps of table 0xFF3A (0xFF4A with +0x2A=7); at step 0xC ends if +0xC9 bit2. Then action 0. |
| 00FF5A | sub_proyeccion_salto | C | R | If the opponent is id 7: opponent to action 0xC sub 0x1E, he to action 0x10, and 0x14CFC runs as the opponent (counterattack). Otherwise: turns, 0x14222, +0x5C=1 if +0xFC; opponent to action 0x10. Animation from table 0x10136[opponent id]+step, durations 0x1013E/0x10146. Step 2: sound 0x50, 1C183E bit7, jump (+0x22=0x40, z+0x10). Step 4: he to action 5, the opponent to action 8 sub 0x1F pose 0x1CF at x±0x40, +0x3E=0xC, 0x161C8, +0xF6+=3, 0x15B90. On falling (z≤0xBB): 1C1858=0x80 (shake) and sound 0x48. With +0x5C: 3 repetitions and 0x145F2. |
| 01014A | sub_embestida | C | R | Pose 0x1D0 and voice 3 (0x27D2); +0x18 bit7. If it connects (+0xC9 bit3 and the opponent's +0xC9 bit4 or +0x40=−2): sound 0x2F and +0x34=1 (with the opponent). Moves (0x3DCE, 0x1600C); if it hits the rope: action 8 (and the opponent too if +0x34). At the end of the steps (durations 0x10340): action 5 at x±0x30; if +0x34, the opponent to action 0xB pose 0x17. On falling (z≤0xBB, or 0x80 outside): sound 0x34 and shake; without connecting, action 8 sub 0x22 pose 0x1CF; if it connected, bounce (step 6, velocity /4, +0x28=0x200). |
| 01031C | anim_tablas_a2a4 | C | R | Pose/time from a2/a4[+0x36] (a2 = 0x10348 if +0x34 = 0). |
| 01037E | sub_salto_voz_b | C | R | Like 0x103A8 with voice 0xB. |
| 0103A8 | sub_salto_aereo | C | R | Jump with table 0x104FE and voice 1; +0x18 bit7. Advances ±8 with the limits inside (0x21E5A) or outside (0x21ED0). On hitting the rope: action 8 sub 2 (or 3 outside, if heading towards that rope). On falling (z ≤ 0xBB, or 0x80 outside): pose 0x15F, sound 0x29 (0x48 outside), step 0x10. When finished: action 5 and turns. |
| 01050E | sub_salto_hacia_rival | C | R | Same as 0x103A8, but orients like the opponent, places the trajectory with 0x156FA (table 0x1599C, ±0x20) and 0x110E4 (velocity 0x180/0x180) towards the opponent. |
| 01055A | sub_golpe_rival_8_9 | C | R | Three steps of table 0x105D0. At step 4 clears +0xC9 bit5 and, if the opponent is in action 8, matches his x. Then action 0. |
| 0105DC | llave_lanzamiento_A | C | R | If 0x14222 fails (+0xFC≠0), the opponent counterattacks (action 0xC sub 0x1E). Otherwise, 4 pose steps (table 0x106F8[opponent id]) with sound 0x2F; at the end the opponent goes to action 8 sub 1, damage +0x3E=8 (0x161DA) and +0xF6 += 3. |
| 0107CA | chk_caer_sobre_rival | C | R | If in the same plane as the opponent and the opponent is downed (0xB) or held (0x17), and z ≤ floor+0x10: pose 0x1D2, places himself on him with table 0x10920[id] (orientation). If downed: opponent to action 8 sub 0xD, +0x3E=1 and 0x161EC; otherwise, 0x108E2 with the partner. Otherwise: on reaching floor d0, action 5. |
| 0108B0 | copiar_8w | C | R | Copies 8 words from a6 to a1. |
| 0108E2 | soltar_llave | C | R | The opponent goes to action 8 sub 0x13; cancels the grabs (0xC554). |
| 010950 | sub_levantarse_rapido | C | R | Starts at step 0x10 of table 0x10A4A (continues at 0x10976). |
| 010976 | sub_rodar | C | R | Rolls with table 0x10A4A: +0x20=0x11 velocity, +0x1E direction (±0x40). From step 0x10 brakes 2/frame. With the rope: outside → action 8 sub 3; inside, if heading towards the rope → action 2 with +0xA8=2. At 0x14 ends: action 0. |
| 010A5E | sub_salto_esquina_ataque | C | R | Attack from the corner/air. Trajectory from table 0x11150[id*16 + air*8 + variant] (with sub 0x1A, according to zone x≥0x300/y<0x120) placed with 0x156FA. +0x34 = 1 from the corner (2 on side bit1); +0x5C=1 if the opponent is higher or (id 6 with sub 0x11). With +0x34, 0x110E4 (0x200/0x100). Id 1 on the floor doubles the velocity. In flight: if the opponent is downed in the same plane and z reaches +0xF4+0x10 → 0x10FCC. If it reaches the floor without an opponent: action 8 sub 5, shake 0x81, pose 0x1CF (0x14F id 7), sound 0x34, +0x3E=2 and 0x16488 (human). If it impacts (step 4): opponent to action 8 sub 0xD, +0x3E = 5/0xA/+1 id1/0xB sub 0x1A/6 sub 0xF/0xC id 7; 0x161C8, shake, sound 0x49, opponent's 0xC6CA; id 1 adds voice 8 and bounces (0x10EA8). When finished: action 5, clears 1C0AB2/1C144E. |
| 010EA8 | sprite_efecto_144e | C | R | Effect object 1C144E (0x8000) next to the wrestler: y−2, z+6, pose 0x1CC, +3=1. |
| 010F04 | ajuste_y_impacto | C | R | id 0 without +0x5D bit0: y+0xA and 0x1152A. For id 1 with +0x5C, sub 0x1A without +0x5C or id 6 with sub 0xF: y+2. |
| 010FCC | chk_impacto_aereo | C | R | Opponent's box: table 0x11084[id] (x±, with margins 0x10/0x30 according to orientation; y±8). Attacker's impact point: table 0x110A4[id*2+corner]. If inside: step 4 (impact) and sound 0x22 (0x23 for ids ≥ 6). |
| 0110E4 | cpu_ajuste_vel | C | R | Limits the velocity towards the opponent: dx<0x60 (±0x40 if downed) and dy<0x50/0x70. |
| 01143A | llave_10a5e | C | R | bsr 0x10A5E |
| 01152A | sprite_efecto_0ab2 | C | R | Effect object 1C0AB2: y−0xA, x∓4, z+0xA, pose 0x7D, inverted orientation. |
| 011598 | sub_presa_intento | C | R | If the opponent is covered: action 0. The CPU opponent rolls 0x450A against table 0x11726[difficulty 1C0028 + 0x1CE9C]; if he resists, he goes to action 5 and the opponent to 0x19. Otherwise: opponent to action 0x10, pose 0x31+id*3, 3 steps (duration 0x11724). Then both to action 0x11 (lock-up: +0xFE bit6 / bit5), +0xAA = +0x3C+0x30 (0x50 CPU), poses −1, facing each other. In mode 1C0026 bit1, with 1/4 probability, +0x2C bit4 on both. |
| 01173A | sub_pisoton | C | R | Two steps of table 0x118BC; at step 4: 0x1185A and 0x1179A. |
| 01179A | pisoton_impacto | C | R | Same plane. If the opponent is downed: action 8 sub 0xD, sound 0x49, 0xC6CA, +0x3E=1 (3 if +3=7), 0x161DA, +0xBF++ (max 4). If the opponent is holding (0x17): 1C185A=0x81, action 8 sub 0x13, clears the partner's covered state; those with +0x33 bit1 → 0xC554. |
| 01185A | pisoton_rival_levanta | C | R | In mode 1C0026 bit1 (or CPU), opponent downed and uncovered: roll 0x450A against table 0x118B6[+0xBE] → the opponent goes to action 0x19 (gets up) and clears +0xBE. |
| 0118D8 | despacho_id2 | C | R | Jumps to table 0x118EC[id]. |
| 01190C | sub_salto_cubrir | C | R | Jump towards the opponent: 1C00B4 with the height from table 0xBEF2[id][opponent id], velocity 0x380/0x50, gravity 0x4000/0x80, target +0x68, 0x15B40 → +0x14, 0x159AC. When descending: pose 0x64; if the opponent is downed inside, uncovered, and he is not outside, with z<0xC3: action 0x17 (cover), opponent +0x18 bit5 and +0x68=him; 0x11BC6 and, if not CC, 0x129A4. Otherwise: to the floor, action 8 sub 0. |
| 011A72 | sub_cubrir | C | R | Places himself over the opponent (x from table 0xBEF2[id][opponent id], −4 for id 4; z from +8), pose 0x7E (id 0/4) or table 0x11BBE. At step 8, if the opponent is downed inside, uncovered, and he is not outside: action 0x17 and cover as in 0x1190C. Otherwise, retries. At step 0xC: action 0. |
| 011BC6 | cubrir_chk_kickout_inmediato | C | R | Normal mode only (not 1C0026 bit1; with bit0, 1C0029≠0) with +0x107 bit0: roll 0x450A&0xF against table 0x11C30[difficulty*3 + 0x1CEF4]. CC/CS inverted (CS = covers). |
| 011C4E | sub_lanzar_por_encima | C | R | Grabs (0x14222), opponent in front at ±8. If the opponent is id 7: action 0xC sub 0x34 (counter). Poses 0x11E1E[opponent id]+step (step 5 pose 0x20E), 4 frames (8 with +0x5C). Step 2: sound 0x50, 1C183E bit7, +0xF6+=3. Step 5: opponent to action 8 sub 0x1E at ±0x80, pose 0x1CF. Step 6: he to action 5 (x∓0x20), +0x3E=0xC, 0x161C8, shake, 0x15B90, sound 0x34. With +0x5C: 3 repetitions and 0x145F2. |
| 011E2E | sub_golpe_cabeza | C | R | With +0xFC: counter (opponent to action 0xC sub 0x1E, 0x14CFC). Poses 0x11F52[opponent id]+step, durations 0x11F62. Step 1: sound 0x49. Step 2: he to action 0; opponent to action 8 sub 1 pose 0x15 at x−0x10; sound 0x50, 1C183E bit7, +0xF6+=3, 0x15B90, +0x3E=8, 0x161C8. |
| 011F66 | sub_suplex | C | R | With +0x30 bit7: 0x1229C (the opponent, in pose 0x1C3, gets up and returns to action 0). With +0x2C bit0 (opponent id 7, counter): 0x1214C, sequence 0x1AD–0x1B1 in which the opponent turns it around, he to action 8 sub 1 (+0x3E=6, 0x16488, sound 0x2F) and the opponent to action 0xC sub 0x8010. Otherwise: both facing each other, opponent to action 0x10; poses 0x12324[opponent id*6]+step, durations 0x12316. Step 3: voice 0x1C, jump z+0x10, sound 0x50, 1C183E, +0xF6+=3; flight 0x3DCE to the floor (step 4). Step 6: shake, sound 0x34, opponent to action 8 sub 5 pose 0x1CF, +0x3E=0xC, 0x161C8. Step 7: action 5 (x∓0x20). |
| 012354 | sub_llave_sumision | C | R | Multi-phase submission hold: 1C185A=0xC0 and dispatches +0x34 with table 0x1238E. |
| 01239E | sumision_f0 | C | R | Poses 0x125D2[opponent id]+step, 12 frames per step; after 3 steps, phase 1, sound 0x51, 1C183E bit7. |
| 012404 | sumision_f1_forcejeo | C | R | Each opponent button press adds to +0x5D; if it exceeds table 0x124D6[0x1CE9C], phase 2 (escapes). Otherwise: alternates poses every 8 frames; each cycle, +0x3E=4 and 0x161C8 (damage). After 6 cycles he escapes. With +0x3C (energy) at 0 and both on the side: phase 3 (submission). |
| 0124DA | sumision_f2_escape | C | R | Goes back through the steps; when finished, he to action 8 sub 1 pose 0x15, the opponent to action 0xD pose 0x18, 1C185A=0xC1. |
| 01255C | anim_objeto_id | C | R | Pose = table 0x125DA[opponent id] + +0x37; after 2 steps, 0x16210 and priorities 1C0BC2/1C0BDA (0x40/0x80 according to +0x18 bit4). |
| 0125F0 | sub_salto_codazo | C | R | Jump placed with 0x156FA (table 0x12A7C, +0x10 if the opponent is id 7); sub 0x35 leaves it outside (+0x19=1). On descending, if the opponent is downed in the same plane: 0x12A9C and, near the floor (+8), impact (opponent action 8 sub 0xD, +0x38+=8, +0x3E=0xC or 8 sub 0x35, 0x161C8; bounce +0x28=0x300, sound 0x48, shake, 0xC6CA). After the bounce tries to cover (inside and on the side): action 0x17 (+0x2C byte 0x20), opponent 0xB, +0x18 bit5, 0x11BC6/0x129A4. On missing on the floor: action 8 sub 5 (0x25 id 4), +0x3E=4 and 0x16488 (human), sound 0x34. Poses from tables 0x12A52 (id 4) / 0x12A60 according to height. |
| 0129A4 | cubrir_iniciar_cuenta | C | R | On covering: if +0x33 bit1 → 0xC554 with the partner. If the covered wrestler has energy 0 (+0x3C) or the partner cannot (CPU +0x106 bit1 / human +0x107 bit0, 3/16 probability) → no save. If the human partner is not CPU: 0xAF9A; if not CC, 0xC554 and the coverer's +0xC6 = 2/bit7 (save warning). CPU: the partner's 0x1B7FA and clears +0xC6. |
| 012A9C | kickout_salto_cpu | C | R | Only once (+0x2C bit0): if the opponent is CPU, sub 0x35, is below at less than 0x30 and is not covered: roll 0x450A against table 0x12B0C[0x1CE9C] → the opponent rolls (action 0x19). |
| 012B10 | sub_correr_cuerdas | C | R | Runs to the rope (direction 0x40/0xC0 according to x≥0x300, 0x1979C, poses 2+step). On reaching 0x298/0x328 bounces (+0x5C=1). If the opponent is not downed, action 0x14. Otherwise: velocity from table 0x95BC[id], runs back and at 0x288/0x378 jumps (action 0xC sub 0x35). Poses 0xA+step. |
| 012C9E | sub_voltereta_atras | C | R | Pose 0x17F+step, durations 0x12D2C, velocity 0x10 backwards; 4 steps and action 0. Ropes with 0x12DB0. |
| 012D30 | sub_voltereta_adelante | C | R | Pose 0x14B+step, durations 0x12DAC; 4 steps. 0x12DB0. |
| 012DB0 | chk_cuerda_rebote | C | R | Inside: if it hits the rope (0x21E5A) → action 2 (+0xA8=2). Outside: (0x21ED0) → action 8 sub 3. |
| 012DEE | sub_golpe_encadenable | C | R | Pose 0x15F+step (table 0x12E76), accumulates +0xC8 into +0x5C. When finished: with +0x5D bit3 and the opponent not in action 8, action 0xC sub 0 (chains); otherwise, action 0. |
| 012E7A | sub_carrera_hombro | C | R | Charge (table 0x1302E, velocity 0x10). If it connects (+0xC9 bit3 and the opponent bit4 or −2) before step 0x10: pose 0x1D2+opponent id, 8 frames, +0xC9 bit4, +0x35 bit0 (extra steps), facing each other; id 1 sounds 0x50. At step 0xC releases: opponent to action 8 sub 0x17. Rope crash: inside → action 2 (and the opponent sub 2); outside → action 8 sub 3. At the end, id 1 with impact calls 0x15B90. |
| 01304E | sub_salto_patada | C | R | Voice 5, +0x18 bit7, floor +0xF4 = 0xBB (0x80 outside), table 0x1310C. In flight (steps <8): 0x3DCE and 0x1600C; if it hits the rope, action 8 sub d0. On reaching the floor: pose 0x61, sound 0x2D. When finished: action 0. |
| 013114 | sub_dropkick | C | R | Table 0x132B8, velocity 0x20 forwards (0 if he himself is id 4, Bossman). To connect before step 4, +0xC9 bit3 is needed and the opponent must have +0xC9 bit4 or +0x40 = −2; then: pose 0x1DE+opponent id, facing each other, +0xC9 bit4. At step 8 releases: the opponent to action 8 sub 0x10, z+0x30, pose 0x9B, +0x2C bit0 (y = his own +3 if +3=4). Ropes (like 0x12E7A): inside → action 2 with +0xA8=2; outside → action 8 sub 3; the opponent receives the same. Brakes 2/frame. |
| 0132C8 | sub_bulldog_salto | C | R | Opponent to action 0x10. Pose 0x23E+opponent id*5, durations 0x134CC. Step 2: sound 0x51, 1C183E. Step 3: voice 4, jump +0x18 bit7, z+0x20. Flight (0x3DCE, 0x1600C); if it hits the rope, both to action 8 sub d0 with the same velocity. First contact with the floor: sound 0x34, shake, bounce. Second: +0x3E=0xB and 0x161EC; inside and on the side → covers (action 0x17, opponent +0x18 bit5, 0x11BC6/0x129A4); otherwise, action 5. Opponent downed (0xB) behind at ±0x20 with pose 0x17; he pose 0x65. |
| 0134D2 | sub_slam | C | R | Grabs (0x14222) and places the opponent in front (−0x10). Poses 0x13956[opponent id*0x1E], durations 0x13938. Opponent id 7: counter sequence (0x1C6–0x1C9) in which the opponent throws him (he to action 8 sub 0 pose 0xF2, +0x3E=6, 0x16488, sound 0x2F) and the opponent returns to action 0 with +3=7. With +0xFC (opponent resists): alternative poses +0x12 and 0x145F2 at step 0xC. Normal: step 2 they turn; step 0xC sound 0x50 (0x51 id 6), 1C183E, +0xF6+=3, voice 0xC, jump; step 0x10 opponent to action 8 sub 0x12 pose 0x16 (x shifted by table 0x13918), shake and sound 0x34; step 0x12: +0x3E=0xC, 0x161EC, action 5, 0x15B90. On descending (z<0xBB) step +2. |
| 0138CA | contra_llave | C | R | The opponent goes to action 0xC sub 3 (pose 0x105D0); he to action 8 sub 9; +0xC9 bit5. |
| 013A46 | llave_slam | C | R | Pose 0x1DD + 6*opponent id, voice 6. Step 3: sound 0x50, 1C183E bit7, +0xF6 += 3. Step 4: on touching the floor, damage 0xC to the opponent (0x161EC), 1C1858=0x80, sound 0x31. Step 6: he to action 5, the opponent to action 8 sub 0x21 pose 0x1CF at ±0x30. With +0xFC≠0 (counter) uses tables 0x13C64/0x13C70[opponent id*0xC]; on reaching step 0xC → 0x138CA and damage 6 to himself (+0x3E=6, 0x16488). The block at 0x13C24 (damage 7 to the opponent) is dead code: it is only evaluated with step <0xC. |
| 013CD0 | sub_golpes_repetidos | C | R | Opponent facing; poses from table 0x13E44[opponent id*10], 4 frames per step (0xD if the opponent is id 7 (André) and step +0x37 < 3, i.e. steps 0 and 2). With +0x5C bit7 (set by 0x13DF6) repeats steps 0–2 and counts in +0x5D; with +0x5D=2 at the start of step 0 → 0x145F2. Step 6: opponent to action 8 sub 0xA pose 0x9B, +0x3E=6, 0x161FE, at ±0x30 and z+0x20. Step 0xA: action 0. |
| 013DF6 | cpu_id7_tirada | C | R | If the opponent is the CPU with id 7: table 0x13E40[energy] against rng&7 → +0x5C bit7. |
| 013E94 | sub_body_slam | C | R | Grab: x−0x20 (except with +0x2C bit5, which enters at step 2 with 0x14204) and 0x14222; the opponent in front (+0x10). +0x108 bit6 without id 7 cancels the resistance +0xFC. Duration table 0x14108 and pose table 0x14124[opponent id*0x1C] (+0x10 if he resists). Step 6: sound 0x50 (0x51 id ≥6), 1C183E, +0xF6+=3. Step 8: jump and voice 0xD. On falling: step 0xC, sound 0x34, shake. Step 0x10: he to action 5, opponent to action 8 sub 0xE pose 0x1CF (−0x20), +0xAE=0, +0x3E=0xC, 0x161DA, 0x15B90. If he resists: step 0xC → 0x145F2. |
| 0140E8 | anim_a3a4 | C | R | Pose/time from a3/a4[+0x36]. |
| 014204 | agarre_reposicion | C | R | Variant of 0x14222 with table 0x14378 (0x143DC CPU) to enter from step 2; continues in the common body at 0x1423E. |
| 014222 | llave_tirada_exito | C | R | Hold success: table 0x14346 (0x143AA for the CPU) + (1C0029>>1&0xF)*0xA, +5 if DIP 0x180002 bit3=0. Index by the count +0xDC/+0xDD (max 4), depending on whether +0x31 is in list 0x14338. If rng>>1&7 < table and ≥ the streak +0xCC/+0xCD (with id 7 only subs 0x18/0x32), adds to the streak and gives +0xFC=0; otherwise, +0xFC=1 (fails and the opponent counterattacks). |
| 01440E | sub_backbreaker | C | R | Same as the body slam with tables 0x1465E (durations) / 0x14676[id*0x18] (poses), x−0x20, the opponent at +8. Step 4: sound 0x50, 1C183E, +0xF6+=3. Step 8: sound 0x31. Step 0xA: opponent to action 8 sub 0xF pose 0x15 at ±0x30, z+0x10, +0x3E=0xC, 0x161DA. Step 0xC: action 0 and 0x15B90. If he resists (+0xFC, tables +0xC): step 0xC → 0x145F2. |
| 0145D2 | anim_paso_a3a4 | C | R | Duration (a4) and pose (a3) of step +0x36. |
| 0145F2 | contra_llave_mutua | C | R | Gives the opponent the pose from table 0x1464E[id]. Both go to action 0xC sub 0x26 (+0xAE 1/0), facing each other. |
| 014736 | sub_golpe_corto | C | R | Pose 0x183+opponent id*2, 0x10 frames; step 1 sound 0x31. Step 2: he to action 0; opponent to action 8 sub 1 pose 0x15 at +0x10/+0x14, +0x3E=0xC, 0x161DA. |
| 01481C | sub_sumision_b | C | R | Submission hold: opponent to action 0x10, sound 0x51, 1C183E, 1C185A=0xC0. With the opponent's +0x114 ≠0 from step 2, each frame adds to +0x35; if it exceeds table 0x124D6[the opponent's 0x1CE9C], he escapes. Poses 0x149AA[opponent id]+step, durations 0x149A2; each cycle (steps 2–3) +0x3E=4 and 0x161C8 to the opponent, +0x5C++. If both have +0x2A bit1 and the opponent has +0x3C=0: 0x16210 (submission) and the result in 1C0BC2/1C0BDA (0x40/0x80 according to +0x18 bit4). Escape or 6 cycles end the same way (0x14950): the opponent to action 8 sub 0x15 pose 0x16 on top (z+0x40), he with sub 0x3A, 1C185A=0xC1. |
| 0149B0 | llave_B | C | R | Poses from table 0x14A82[opponent id] (stride 0x14). Step 2: sound 0x51 and 1C183E bit7. Step 4: sound 0x31. At the end, the opponent goes to action 8 sub 0x15 (z+0x10) with damage 0xB (0x161FE), and 0x15B90. |
| 014AFA | llave_C_aerea | C | R | Table 0x14C5C[opponent id*0x14] (pose+duration .l). Step 1: sound 0x51 and 1C183E. Step 3: the opponent to action 8 sub 0x10 (x±0x50, z+0x30, pose 0x9B) with damage 0xA (0x161FE). Step 4: jumps (+0x18 bit7, z+0x10, velocities to 0, +0x22=0x20) and on falling to 0xBB (0x80 outside) goes to step 5 with pose 0x17 (0x10 frames) and x+0x10. Step 6: action 5 and 0x15B90. |
| 014CFC | sub_contraataque_llave | C | R | Run by the one who counterattacks (called with a0 = the opponent from 0x152BC when 0x14222 fails): turns, pose 0x20+opponent id*2 (+1 per step), the opponent placed with table 0x14DD0. Step 4: the opponent to action 0x15 sub 0, he pose 0x30, +0x1C=0 on both. Step 6: action 0 (+0x5C=0xD if CPU). |
| 014DD6 | sub_forcejeo_presa | C | R | Grab struggle: +0x28=0x80 frames, +0xDE = table 0x150E0[id&7] (CPU time). Poses 0x150F6[opponent id*6], durations 0x150F0, alternating. If not CPU, 0x14FEE (human input); the CPU, when +0xDE runs out, 0x1E432. With +0xAF bit0 (the other's turn): 0x14F00. If 0x2786 gives CS (break): both to action 0. |
| 014F00 | presa_contra_humano | C | R | If +0x114≠0, not CPU, +0x2A bit1, inside, and the opponent is at step 2/4 of +0x37, only once (+0x108 bit7): roll 0x450A&7 in table 0x14FD8 (only if the opponent is CPU and 1C0029 < 2) or 0x14FE0 (rest). With 0xFF: sub from table 0x14FE8[id], action 0xC, opponent to 0x10 (sub 0x1E against id 7), sub 0x21 moves back 0x20, +0x2C bit5 and +0x108 bit6 (except with sub 0x1E). |
| 014FEE | presa_entrada_humano | C | R | Human with +0x28<0x70 and button 1/2: sub from table 0x15126[id*3 + button−1], action 0xC, opponent to 0x10, separation ±8/∓0x10. With +0x28=0: 0x1507C for him or for the opponent (+0xAF bit0). |
| 01507C | tag_relevo_o_llave | C | R | If 1C0026&3 = 2: action 0xD and the partner (a3) to action 0 at x±0x30. Otherwise: action 0xC sub 0x27, the opponent to 0x10. |
| 01513E | sub_presa_cabeza | C | R | Pose 0x82+id*3 alternating with tables 0xB46C[opponent id]/0xB468, 0x20 frames. When finished, 0x145F2 from the opponent and opponent +0x2C bit6. Break with 0x2786 → both to action 0. |
| 0151F8 | sub_empujon | C | R | Pose 0x150F6[opponent id*6], 7 frames; then action 0, 0x19D1A, 0x15288; the opponent to action 0xD at ±0x34, with the ring limits. |
| 015288 | cpu_tras_llave | C | R | With action 0 and 0x1D0E2 (table 0x152A4) → +0x5C=0xF (table 0x1B40C[0xF] = 0x1B486: go next to the partner who is covering, to break/protect the count; with no partner covering → 0). |
| 0152BC | llave_D_salto | C | R | 0x14222 (if it fails, counterattack 0x14CFC). Poses 0x154BC/0x154AE, sound 5. Step 1: sound 0x50, 1C183E and +0xF6+=3. In the air falls to 0xBB; the first bounce (vz 0x300) deals damage 0xC, sound 0x34 and 1C1858=0x80. At the end, the opponent to action 0xB (downed, pose 0x17) and he to 5. |
| 01552C | sub_salto_voz2 | C | R | Jump with table 0x155EA, voice 2, +0x18 bit7. Flight (0x3DCE, 0x1600C), rope → action 8 sub d0; on reaching the floor (0x155C0), step 0xC; at 0x10, action 0. |
| 0155C0 | aterrizar | C | R | If falling (+0x28<0) and z ≤ d0: z=d0, step 0xC and its pose. |
| 0155FA | sub_golpe_objeto | C | R | Hit with the object: sound 0x25 (0x26 with +0x5F). Table 0x156C8[+0x5E&3*0xC] (3 without +0x5E bit6). If it connects (+0xC9 bit3) dispatches +0x5E&3 via table 0x15692: 0 → 0xE76E (drops the object), 1 → 0xE6E0 and +0x5F=2. |
| 01569E | golpe_obj_0 | C | R | 0xE76E. |
| 0156A6 | golpe_obj_1 | C | R | 0xE6E0 and +0x5F=2. |
| 0156B4 | soltar_portado | C | R | The carried object (+0x60) goes to +0x2C=3; clears +0x5E bit6. |
| 0156FA | salto_preparar | C | R | Copies block a6 to 1C00B4 (0x108B0), target +0x68, 0x15B40 → +0x14, 0x159AC (computes velocities). Orients, pose (a2), +1=2, +0x18 bit7, +0xF4 = 0xBB/0x80. |
| 01578E | cpu_combo_id | C | R | CPU (via 0x15758, table 0x1576E by id): strikes from table 0x15860 (0x15878 if 0x1CD80 gives CC and without +0xF9 bit0), 4 bytes per step. Ends after step 0x18 (0xC for id 7 André: shorter combo). At step 0x10 continues only if the entry of the opponent's table +0x6E (+0x6C) has +9≠8, /dx/<0x40 and /dy/<8; otherwise, ends. When finished: id 7 with the opponent in action 0xA goes to action 0xC sub 8; the rest, action 0. |
| 015890 | golpe_rapido | C | R | Strike in steps of 4 (table 0x15944, or 0x15960 for the CPU that loses the 0x1CD80 roll, without +0xF9 bit0). At step 0xC (index 3): if the opponent's state has a ≠0 entry in table 0x1597C, jumps to step 0x18 (finisher); otherwise, ends. Step 0x14 and ≥0x20 end (action 0). That is: a 3-step strike, plus 2 finisher steps if the opponent is in a state from the table. |
| 0159AC | calc_trayectoria | C | R | Block 1C00B4: +0 dx, +2 dx against the downed one, +4 dy, +6 extra z, +8 vz, +0xA gravity, +0xC/+0xE vx/vy maxima, +0x10 target (−1 = fixed point +0x16/+0x18), +0x14 target z. Simulates the parabola (+0x28 −= +0x22 each frame, minimum −0x800) until it descends to the target z, counts the frames and sets +0x24/+0x26 = distance·256/frames, limited. |
| 015B40 | z_destino_salto | C | R | Table 0x15B70[own zone*8 + opponent zone*2]. |
| 015B90 | cpu_provocar | C | R | Inside and CPU: if 0x1CEF4≠0 and the roll 0x450A&0xF < table 0x15BE4[id] → action 0x12 (taunt). |
| 015BEC | llave_E_secuencia | C | R | Phased hold (+0x36/+0x37) with tables 0x15E7A/0x15EB2/0x15EE2/0x15F12, stride 8 by opponent id. In phase 2: sound 0x50, 1C183E and +0xF6+=3. In phase 8 throws the opponent (action 8 sub 0xA, damage 0xD, z+0x40). Durations with rng&7. If 0x14222 fails (or the opponent is id 7), ends in the mutual counter 0x145F2. |
| 015CC8 | warrior_33 | C(A) | A | Warrior's move 0x33 (spins, see NOTES). |
| 015F1A | sub_rival_lanzado_id | C | R | Places himself on the opponent (x, y; the z copy is a no-op: move $14(a1),$14(a1)), pose 0x209 and table 0x15FFC every 0xC frames. Step 0xC: opponent to action 8 sub 9 pose 0x9B, +0x3E=6, 0x161C8, at ±0x1E and z+0x10. Step ≥0xE: action 0, pose 0x1A, x+0x15. |
| 01600C | chk_cuerda_d0 | C | R | d0 = 0 no collision, 2 = rope inside, 3 = barrier outside. |
| 01603E | sub_esperar_tumbado | C | R | Pose 0; if the opponent is downed, action 0. |
| 016062 | sub_entrar_ring | C | R | If the opponent is inside: +0x19=0, pose 0x105, advances table 0x160CC[id], 8 frames; then action 0 with +0x19=3 (apron). |
| 0160D4 | sub_carrera_hacia_rival | C | R | With +0x2C bit4 → 0x10A5E. Otherwise, runs (0x911E, 0x9202, 0x1617C, 0x1979C, 0x924A, 0x3DCE). With the rope → action 0xC sub 0x11. At a distance of 0x50–0x5C in front of the opponent: if he is downed → +0x2C bit4 (jump); otherwise, action 0. |
| 01617C | dir_hacia_rival | C | R | +0x1E = 0x40 / (opponent's orientation inverted); inverts it if ≥0x5C in front. |
| 0161C8 | danio_a1 | C | R | 0x16488 on a1. |
| 0161DA | danio_a2 | C | R | 0x16488 on a2. |
| 0161EC | danio_a3 | C | R | 0x16488 on a3. |
| 0161FE | danio_a4 | C | R | 0x16488 on a4. |
| 016210 | rendicion | C | R | Shows fg0 banner 1 (0x2660E with d0=1). |
| 01621A | temblor_pantalla | C | R | 1C1858 bit7 activates the shake: 9 frames (3 if bit0, i.e. 0x81 = short). Adds table 0x16286[frame] to 1C002E (vertical scroll); when finished, clears 1C1858. |
| 0162A0 | procesar_impacto | C | R | Receives the hit (0x16340 filters; +0xC9 bit0 = hit). +0x40 = pending reaction: 0xFFFE → 0x16468, action 0x10 (grabbed), +0xC9 bit4. Mutual grab with action 0xC sub 0x14 → the other +0x40=−1. Otherwise: 0x16468, 0x1638E (extra damage), action = +0x40 (9 if the hit is sub 1 and he is outside), 0x16488 (applies the damage), 0x16538. +0x46 times the combo +0x48. |
| 016340 | filtro_impacto | C | R | Table 0x1636C[action]: 0 = accepts; negative = ignores the hit; positive = ignores only with sub ≠0 (+0x31). |
| 01638E | danio_extra_tumbado | C | R | If the victim is in action 1/0x15/0x16: +0x3E += table 0x1642A[attacker's sub]&0x7F. Reaction 9/0xA (except with subs 0x14/0x28/0x15) → 8; with the attacker in state 7, sub 0x23, and otherwise, +0x45=1. With the attacker's +0xF9 bit0, damage ×2. |
| 016468 | soltar_si_tumbado | C | R | Action 1/0x15/0x16 → 0x8EEA. |
| 016488 | aplicar_danio | C | R | +0x3C −= +0x3E (minimum 0; if already 0 it does not change). Sound 0x22 (0x23 if the attacker's graphics bank +2 is ≥6: DiBiase and André) except with subs 0/1. With table 0x164FA[sub] = 0xFF (or victim id 7 André with sub 0x1F) → +0xF0 bit7 (heavy hit). |
| 016538 | limpia_f0_por_estado | C | R | If table 0x1655C[state] is 0, clears +0xF0 bit7. |
| 01657E | colisiones_bucle | C | R | Collision loop: clears +0x40 of the 4 wrestlers; goes through the 6 pairs (0x165B2), 0x165FE, if they are close (0x16634): 0x16716 (boxes) and 0x1675C (impacts in both directions). |
| 0165B2 | siguiente_pareja | C | R | Pairs (i<j) from list 0xEA4C (4 wrestlers); CS when finished. |
| 0165FE | reset_mascara_golpe | C | R | If the pose changed (+6 &0x3FFF vs +0x42): +0xCE=0 (mask of whom it has already hit). |
| 016634 | pareja_cerca | C | R | CC if /dx/<0x60, /dy/<8, neither in action 0x10, nor 0x1F sub 1, without +0x2A bit2, both with +0x2C bit7 and without bit6, pose ≠ −1, 0x166FC without break, both with +0x19<2 and equal. |
| 0166FC | chk_ruptura_pareja | C | R | 0x2786 for both. |
| 016716 | cajas_pareja | C | R | a1/a4: hit boxes of both (0x1672C). |
| 01672C | caja_de_pose | C | R | Table 0x1761E[pose&0x3FFF] → the frame list [+2]; pose −1 → 0x18076. |
| 01675C | impactos_pareja | C | R | In both directions: 0x16796 (hit); CC → 0x16CF4 (sound/combo); CS → 0x172AA, which repeats while it keeps giving CS (multiple boxes, +0xCA). |
| 016796 | chk_golpe | C | R | Neither with +0xC9 bit4/5 nor +0x40 −1/−2/−4, both active, the attacker with priority (a1+0) ≥ the defence (a3+0; 0x20 with 0x1688E), 0x16D9C (has not already hit him), non-null boxes (0x18BF2/0x18AFE), overlap in x (0x16C60) and z (0x16CA8), hit ≠ 0x18C72, table 0x172FA[victim's pose] ≠ 0xFF. Then (0x168B6): reaction and sub from the hit table (+2 if they face the same side, i.e. the victim has his back turned; +0xC8 bit1 = 1 if facing each other, 0 if from behind), +0xC9 bit3 to the attacker, adjustments 0x169C2/0x16AA0/0x16BD2/0x16C04/0x16C14/0x16AD4/0x16B2A, 0x16B6A (counter). With −4: 0x17136; with −2 (grab): both linked (+0x68), 0x17228/0x17240 and the grabbed one's object to action 4. Damage = a1+1 in +0x3E (0 to the CPU with subs 0/1). +0xC0 bit0 = side, +0xC9 bit0, 0x16DD2. If it fails: 0x16E48/0x16FAA/0x16DF8 (body-to-body clash). |
| 01688E | prioridad_defensa | C | R | If the victim has sub 3 and the attacker 0/1/8: d0=0x20. (After the rts, at 0x168B6, the body of 0x16796 continues.) |
| 0169C2 | ajuste_reaccion_id7 | C | R | Victim id 7 (André) in poses 0x18/0x19, or any victim with reaction 0xF2 → 8. Reaction 0xF1 → 0xA (9 for André). Reaction 8 against André: if the attacker is downed (action 1/0x15/0x16) and does not have sub 0x20, the attacker goes to action 8 sub 1 and André to 9; with the attacker's subs 0x2A/0x16/0x20/0x17/0x12/0xD → 0xA if his +0x44=1, otherwise 9; rest unchanged. |
| 016AA0 | ajuste_sub15_cpu | C | R | Sub 0x15 against state 7 with difficulty ≥2 → reaction 0xA, +0x48=0. |
| 016AD4 | ajuste_id7_accionC0 | C | R | Id 7 in action 0xC sub 0: victim with +1=2 or an action from list 0x16B20 → 8; otherwise, 0xA. |
| 016B2A | ajuste_id7_accionC8 | C | R | Id 7, action 0xC sub 8: with +1=2 → 8; with action 0/9 → 0xA. |
| 016B6A | chk_choque_golpes | C | R | Reaction with sub 9: if the victim's action is in list 0x16BCC (or 0xC with sub 0xE/0x14), they cancel out (both 4 frames, linked, +0xC9 bit5) and returns CS. Otherwise, CC (continues). |
| 016BD2 | ajuste_F0 | C | R | Reaction 0xF0 → 8; the attacker +0x116=0, +0x22=0, +8+=0xC (id 4 advances the step +4). |
| 016C04 | ajuste_sub20 | C | R | Sub 0x20 → the victim's +0x44 0x23. |
| 016C14 | ajuste_sub31_id7 | C | R | Sub 0x31 against id 7 (not downed nor in poses 0x18/0x19): the attacker to action 8 sub 1, the victim to reaction 9. |
| 016C60 | solape_x | C | R | Box overlap in x (box: +0 offset, +1 width). |
| 016CA8 | solape_z | C | R | Overlap in z (+2 offset, +3 height). |
| 016CDE | x_caja | C | R | Box x according to orientation. |
| 016CF4 | sonido_y_combo | C | R | Action 1 → sound 0x48. Action 0xC: sound from table 0x175CE[sub] (0x30 for id 1 with sub 0); the victim's combo +0x48 += table 0x17590[sub] (+0x46=0x30); if the victim is CPU inside and the attacker has neither +0xF8 bit7 nor +0xF9 bit0, also +0xF6. |
| 016D92 | acumular_mareo | C(A) | A | Adds damage to +0xF6 (dizziness meter); see NOTES s66. |
| 016D9C | chk_ya_golpeado | C | R | CS if the victim's bit (0x8000>>index in 0xEA4C) is in +0xCE. |
| 016DD2 | marcar_golpeado | C | R | Sets that bit in +0xCE. |
| 016DF8 | chk_choque_cuerpos | C | R | Action 0/9 of both, 0x16E7E and 0x16F12 → both to action 0x11 (clash), +0xC9 bit0 is cleared, 0x170BA/0x170F0. |
| 016E48 | chk_bandos_opuestos | C | R | CC if a0 and a2 are on different teams (1C0100/1C021A versus ≥1C0334). |
| 016E7E | chk_choque_validable | C | R | CC if they are on different sides (+0x2A bit12), neither carries an object (+0x5E bit6), they are in the same zone +0x19 (if both are outside, +0x19=1, they must also have the same +0x2A bit1) and a2's action allows it according to table 0x1760C (<0x10; negative = no, 0 = yes, positive = only with a2's sub 0/1; action 0x1F is valid except with the attacker's sub 1). |
| 016F12 | chk_cuerpos_cerca | C | R | CC if /dx/<0x20 (<0x28 between two id 7s) and /dy/<0x10. |
| 016F58 | centrar_pareja | C | R | Places both at the midpoint (x, y) and in opposite orientations. |
| 016FAA | chk_agarre_carrera | C | R | The attacker in action 0 and the victim running (0xD) or bouncing (0xA) head-on: he goes to action 0xC (+0x2C bit5) with the sub from table 0x170B2[id] (0x1E against id 7), and the victim to 0x10. Outside, or CPU on alternate frames (1C0046 bit1): sub 0x1E without bit5. Id 6 with difficulty <2: sub 0x13. Links (0x170F0). |
| 0170BA | soltar_objetos | C | R | If they carry an object (+0x5E bit6), they drop it (object +0x60 to action 4). |
| 0170F0 | enlazar_pareja | C | R | Each one gets the other as opponent (+0x68) and his index +0x6C within the opposing team (list 0xEA4C; +8 with +0x2A bit4). |
| 017106 | enlazar_uno | C | R | +0x68 = a4 and +0x6C = a4's index in his team. |
| 017136 | reaccion_especial_m4 | C | R | Reaction −4 (counterattack) according to the victim's +0x44, via table 0x1715C: 0 releases the grabber (action 0), the victim to 8; 1/2 → +0x40 −1; 3 both to action 8 sub 1; 4 releases, the victim to 8 sub 1. The attacker +0x32 bit3. Damage +1 and 0x16488. CS. |
| 017168 | reac_m4_0 | C | R | See 0x17136. |
| 017198 | reac_m4_1 | C | R | See 0x17136. |
| 0171A2 | reac_m4_2 | C | R | See 0x17136. |
| 0171AA | reac_m4_3 | C | R | See 0x17136. |
| 0171D6 | reac_m4_4 | C | R | See 0x17136. |
| 017228 | ajuste_agarre_sub15 | C | R | Sub 0x15 at step ≥4 → step 0. |
| 017240 | ajuste_agarre_id7 | C | R | Only with subs 0x14/0x28 (with others it exits without doing anything). Sub 0x28 with step ≥2 → step 0 (0x14 does not restart). If the victim has state +3 = 7: roll 0x450A&7 against table 0x172A6[attacker's difficulty 0x1CE9C]; if the roll exceeds the value, the attacker goes to action 8 sub 1 and the victim to reaction 9 (the attacker's +0xC9 bit0 is cleared). |
| 0172AA | chk_pose_lista | C | R | If +0xCA=0 and the opponent's pose (+6 of a2) is in list 0x172DE: +0xCA=1 and CS. |
| 018E70 | cpu_ia_entrada | P(A) | A | Entry to the CPU AI (from action 00 and others). |
| 018ECE | ia_principal | C | R | CPU AI: decrements +0xF3; 0x1CCE8 can abort. Except with +0x5D=9/0xA/0xD, clears +0xB0 and chooses the intention (0x1D1A8). Jumps by +0x5C to table 0x18F16. |
| 018F56 | ia_sub0 | C | R | If 0x1D04C gives CS → +0x5C=0xB. Otherwise, 0x19012 and 0x1907C, and dispatches according to the opponent's action via table 0x18F92. |
| 019012 | cpu_pedir_relevo | C | R | Team CPU without 1C00F2 or +0xF9 bit0, opponent not running, partner on the apron (not in 0x13): if difficulty < +0xDA and the partner has ≥ energy → +0x5C=6 and partner +0x5C=5 (tag). |
| 01907C | cpu_rival_fuera | C | R | Opponent outside (+0x19=1): roll (0x450A>>1)&0xF; with <8 checks 0x1AE98, and if it does not give CS (or the roll ≥8) → +0x5C=3 and partner +0xC4=0x10. Otherwise: id 7 (André) → +0x5C=4 (partner +0xC4=0x7FFF); opponent in action 8 → nothing; opponent downed (0xB, already started) → table 0x19132[rng&0xF]: 0 → +0x5C=4, 1 → +0x5C=2 (opponent +0x38+=0x80, +0x34−=0x14), other → action 0xC sub 0x3B; rest → +0x5C=4. |
| 019142 | cpu_est_0 | C | R | Current pose. |
| 01914A | cpu_est_andar | C | R | 0x19248, 0x19160, 0x196F8 (walk towards the opponent), limits, 0x1BE9C. |
| 019160 | cpu_decidir_correr | C | R | CPU with +0x2A bit1 without cooldown (+0xA8 bit7), /dy/<8: according to dx (≥0xE0/≥0xA0/≥0x60/≥0x40; <0x40 never) table 0x19228[band*8+id&7] against rng&0xF; if it succeeds → action 1 (run), except against the downed opponent (0xB): only runs if they face the same side and dx ≥0xA0. Cooldown +0xA8=0x809C (0x9C frames in +0xA9). The filter on bits 8–9 (move.b + andi.w #$300) always gives 0: it has no effect. |
| 019248 | cpu_elegir_paso | C | R | If /dy/ ≥ 8: +0x34 = random 0/1/2, +0x5C=0xE. |
| 01928A | cpu_lanzar_ataque | C | R | With the attack prepared (+0x2E bit7), without break and in the same zone: if /dy/<0xC and 0x10 ≤ dx ≤ table 0x19310[id] → action 0xC with sub +0x2E (sub 4: the opponent to action 0x10). |
| 019318 | cpu_est_andar2 | C | R | = 0x1914A. |
| 01931C | cpu_est_elegir | C | R | Opponent active: 0x19422 (climb the post?) or 0x1935C (chooses the attack); if it chooses: +0x5C=0, +0x5D=+0xD9. Otherwise, walks. |
| 01935C | cpu_elegir_ataque | C | R | Opponent inside. Side against side: opponent with 0 energy → +0x2E=0x8006; otherwise, 0x19406. Off-side: subs 6/9 → 4. +0xD9 = table 0x193D6[+0x2E&0x3F] (5 by default), +0xD8 bit7. |
| 019406 | cpu_ataque_tras_golpe | C | R | If +0xE2 bit0 and the opponent's 0x1CEF4 ≠0: +0x2E=0x8004. |
| 019422 | cpu_decidir_poste | C | R | Opponent inside, not id 7, opponent without +0x104 and in the zone of table 0x19528 (0x194B8), with energy, 0x1CEF4≠2, he in the zone (0x194F8) and roll < table 0x19548[id]: +0xD9=2 (post), opponent +0x38+=0x80, +0x34−=0x14. |
| 0194B8 | chk_zona_rect_adelantado | C | R | Rectangle from table a2[(zone+0x18 bits8-9)>>5] with x advanced ±0x30; CC if inside. |
| 0194F8 | chk_zona_rect | C | R | Same without advance. |
| 019550 | cpu_est_combate | C | R | 0x1956A (dodge), 0x19160, 0x196F8, limits, 0x1928A. |
| 01956A | cpu_esquivar | C | R | Once (+0xE2 bit4): opponent attacking (0xC) nearby (dx<0x60, 0x38 with sub 2; dy<8), head-on, with a sub from list 0x19644: roll against table 0x19656[1C0028 and difficulty] (0x1966A for id 7) → +0xF1 = the response from the list and action 5 (duck/dodge); downed: +0xF0 bit0 and 0x8EEA. |
| 01966E | cpu_est_seguir | C | R | 0x196F8, limits, 0x1BE9C. |
| 01967E | cpu_est_seguir2 | C | R | = 0x1966E. |
| 01968E | cpu_est_esperar_cerca | C | R | Close (dx<0x60, dy<0x50): stops facing him; otherwise, approaches. |
| 0196C2 | cpu_est_ir_punto | C | R | Goes to the point from table 0x196F4 (0x1CF50). |
| 0196F8 | cpu_andar_hacia_rival | C | R | If /dx/<5 and /dy/<5: only moves (direction 0) if the opponent is downed (0xB) without bit6 of the entry; otherwise does nothing. Otherwise: band 0 (/dy/<4), 1 (dx<0x30), 3 (0x30–0x4F) or 2 (≥0x50); direction = table 0x1977C[band*8 + octant (bits 14–15 of the entry)*2]. Then 0x1979C, 0x924A, 0x3DCE. |
| 01979C | velocidad_por_dir | C | R | +0x21 = table 0x933E[id][direction>>5 + 1] (velocity per wrestler). |
| 0197C4 | cpu_est_ir_tabla | C | R | Goes to the point from table 0x19808[opponent's index +1] (0x1CFD8). |
| 019818 | cpu_comp_rodear | C | R | Circles the opponent (0x198B6 checks post 0x1A820) on the side according to orientation; 0x198C6 or approaches; with the opponent running continues (otherwise, +0x5C=0). |
| 0198A2 | cpu_fin_si_no_corre | C | R | Opponent ≠0xD → +0x5C=0. |
| 0198B6 | cpu_chk_poste | C | R | 0x1A7CE with table 0x1A820 and height 0xBB. |
| 0198C6 | cpu_rodear_paso | C | R | Direction from table 0x19954[side+zone], moves away if dy≥0x10; +0xEA bit7 alternates the side. |
| 019958 | cpu_ir_a_poste | C | R | With the target in actions 0xB/0xD/0xE: orients (+0xA, +0x18 bit6) and goes to the post from table 0x199FA; on arriving → action 0xF (climb), +0xB8=0. 0xF81A without CS → +0x5C=0. |
| 019A0A | cpu_ir_cuerda_rival_fuera | C | R | Opponent outside: goes to the line x=0x2D0/0x330 (or y=0x120 according to +0x18 bit4) on the opponent's side and lines up. |
| 019AD4 | cpu_perseguir_fuera | C | R | Opponent outside: 0x19B8E computes the exit point; with +0x32 bit6 waits for input 0x1A22C. On reaching the rope (+0x9F) with 0x1A25C: action 3 (exit through the ropes), +0xAC = 0/1/2 according to the rope (id 7 positions itself at x 0x2A5/0x345). +0x5C=0. |
| 019B8E | cpu_punto_salida | C | R | Exit point (+0x24/+0x26) towards the opponent, limited to x 0x280–0x380 or y 0x108–0x150 (table 0x19C20, 0x1D032); id 7 uses fixed points. 0x1CFD8 gives the direction. |
| 019C28 | cpu_rodear_tumbado | C | R | Opponent in the same zone, downed/stunned (0xB/8/5): chooses a side (+0x22 bit6) and goes to the point from table 0x19D12; if the opponent runs (0xD), 0x19D1A or 0x19D5C according to distance. Otherwise, +0x5C=0. |
| 019D1A | cpu_reaccion_carrera | C | R | Opponent inside in zone 0x19D44 (0x1D0E2): +0x5C=1; otherwise, 0xF. |
| 019D5C | cpu_reaccion_carrera2 | C | R | Opponent inside in zone 0x19D7E → action 1 (run). |
| 019D96 | cpu_ir_relevo | C | R | Goes to the corner (table 0x19E32 per team). On arriving, with the partner in action 0, +0x5D=5 and +0xE2 bit3: both to action 0x1A (tag) with +0x2A bit2; +0xDB = difficulty. The check "partner already in 0x13 → +0x5C=0" uses movea.w $A4 (reads only the high word of the pointer, a1=0x1C) and looks at ROM byte 0x49, which is 0: it is never met (bug in the original). |
| 019E3A | cpu_volver_delantal | C | R | Goes to his corner (table 0x19ED6); on arriving, 0x1A25C / 0x1A22C → action 6 (climb onto the apron), +0x2A bit7=0. 0x1B3E4: if it finishes → action 0 and, for the human in mode 1C0026 bit0=0, +0xF2 bit7. |
| 019EDE | cpu_seguir_si_rebota | C | R | Opponent inside bouncing (0xA) or running (0xD): follows him; otherwise, +0x5C=0. |
| 019F0A | cpu_ir_a_tumbado | C | R | Opponent inside downed: goes to fixed point 0x19FE8 (0x19F92 always returns that one, see 0x19F92). On arriving: if the opponent has +0x38 ≥0x10, action 0xC with sub +0x2F (sub 4 → the opponent to action 0x10); otherwise, +0x5C=0. If the opponent stops being downed or inside, +0x5C=0 (but the frame finishes). |
| 019F92 | cpu_punto_ataque | C | R | List 0x19FD6 (sub → index) — the result is overwritten: always returns 0x19FE8 (dead code: the adda is overwritten). |
| 01A008 | cpu_nada | C | R | rts. |
| 01A00A | cpu_ir_centro | C | R | 0x1D04C; goes to point 0x1A056/0x1A05A according to the opponent's y (≥0x138). |
| 01A05E | cpu_dar_vueltas | C | R | For +0x24 frames (0x20; 0x10 outside) and a number of steps from table 0x1A15E[1C0028&0xF]: moves away from the opponent (opposite direction). On colliding or when time runs out: in a team, in zone 0x1A168 and with the partner on the apron → tag (+0x5C=6/5). Id 6 uses another animation (0x1A1C8). |
| 01A170 | anim_andar | C | R | Walking animation: without object, 4-step cycle from table 0x93AE (+8 with +0x18 bit6). With object: 0x924A. |
| 01A1C8 | anim_andar_id6 | C | R | 4-step cycle from table 0x1A20C. |
| 01A22C | chk_entrada_cuerda_lado | C | R | Input 1C1894/1C1896 (according to +0x18 bit0) &3; not pressed clears +0x32 bit0, pressed → CS. |
| 01A25C | chk_puede_cruzar | C | R | CS if the side's input (1C1894/1C1896 &3) is active, except in zone 1 with +0x18 bit4. |
| 01A29A | cpu_esperar_levante | C | R | Opponent downed/getting up (1/2/0x15). Chooses the attack (0x1A33E); in the zone of table 0x1A336 and with 0xA39A → +0x22 bit7 (from the post). With +0x2E bit6: if on the post, counts +0x23 and jumps (action 0x16); otherwise, with the opponent in 0x15 with his back turned → run (action 1). |
| 01A33E | cpu_elegir_sub | C | R | Attack sub (+0x2F) from table 0x1E8FC[x position(0–2)*0xC0 + opponent's 0x1CEF4*0x40 + id*8 + roll&7]. Off-side: sub 0xB → 0x1C. Bit7 of the sub → +0x2E bit6 (from the post). +0x2E bit7 = prepared. |
| 01A3EC | cpu_ir_poste_rival | C | R | Opponent inside: goes to the post from table 0x1A48C[+0x34&3]; on arriving, with the opponent in action 0 at dx 0x20–0x40 and in zone 0x1A49C → action 0x16 (jump from the post). |
| 01A4B4 | cpu_entrar_ring | C | R | Opponent inside: goes to the point from table 0x1A512[id]; on arriving → action 1. +0x5C=0. |
| 01A532 | ia_sub_5d | C | R | Dispatches by +0x5D&0xF (<8) with table 0x1A554. |
| 01A574 | cpu_fuera_principal | C | R | Outside the ring: 0x1CDA4, 0x1A6B6 (object), 0x1AE44 (count-out). With +0x5A bit7 (high count): with +0x5B=2 → action 0x1C; otherwise, +0x5C=2 (3 in a team) to return. Otherwise: orients towards the opponent; on the same side: 0x1D04C → +0x5C=6, or attacks (0x1AF58; downed → 0x1A674), or walks. If on another side: circles the ring (0x1A742/0x1A772/0x1A79E). |
| 01A674 | cpu_atacar_fuera | C | R | Without object: 0x1AF70 chooses +0x2E; ≠0 → action 0xC with that sub (4 → the opponent to 0x10). With object: +0x5C=6. |
| 01A6B6 | cpu_buscar_objeto | C | R | Id <6, outside modes 4/9 of 1C0029, with an assigned object (+0x5E bit7, +0x60) free: if closer to the object (+0x64/+0x66) than to the opponent → +0x5C=5 (pick up the object); otherwise, +0x5C=0. |
| 01A742 | dir_rodear_x | C | R | Direction to circle the ring by x (0x3E0/0x210 according to the side). |
| 01A772 | dir_rodear_y | C | R | Direction by y (0xC0). |
| 01A79E | dir_rodear_x2 | C | R | Like 0x1A742, with the opponent's side. |
| 01A7CE | chk_rival_en_trapecio | C | R | CC if the opponent is inside the trapezoid of table a2 (and below d4, the x edges widen 1/6 per y). |
| 01A830 | cpu_volver_ring | C | R | Goes to the rope (0x1A926 or 0x1A9C2 according to team +0x2A bit4) and, on arriving facing 0x40/0xC0 on his side, with 0x1A25C → action 4 (enter), +0xAC=3/4. If the partner is outside and the opponent inside → +0x5C=0. |
| 01A926 | dir_cuerda_eq0 | C | R | Direction towards the rope (x 0x210/0x3E0, y 0x160/0xC0 according to +0x18). |
| 01A9C2 | dir_cuerda_eq1 | C | R | Same for the other team. |
| 01AA5E | cpu_entrar_por_lado | C | R | Goes to the entry line (0x1AB0C/0x1AB34) and, on arriving with input 0x1A25C, action 4 with +0xAC 0/1/2. |
| 01AB0C | dir_entrada_y | C | R | By y 0x130/0x180. |
| 01AB34 | dir_entrada_x | C | R | By x 0x280/0x380; id 7 at x 0x2A5/0x345 (adjusts to within 5). |
| 01AB92 | cpu_coger_objeto | C | R | +0xE6 state machine (table 0x1ABCA): 0 go to the table, 1 go down to y<0x30 and pick up the object, 2 return. |
| 01ABDA | obj_ir_mesa | C | R | Towards y 0xC8 and x 0x200/0x400; on arriving, +0xE6++. |
| 01AC22 | obj_bajar | C | R | Towards y<0x30; picks up the object (0x1AC42), +0xE6++. |
| 01AC42 | crear_objeto_en_mano | C | R | 1C1823 /= +0xE7. Object 0xEA60/0xEA64 (according to +0xE7 bit0): +0x5F = type, +0x5E bit6, +0x60. The object: active (0x8000), pose 0xF/8, sprite 0x17, at the wrestler's position, action 1, owner +0x60, +0x1A=0x8070. |
| 01ACE2 | obj_volver | C | R | Towards y ≥0xC8 → +0x5C=0. |
| 01AD02 | cpu_ir_a_por_objeto | C | R | Outside the ring, going for the assigned object (+0x60): 0x1A6B6 and 0x1AE44 like 0x1A574 (with high count: +0x5B=2 → action 0x1C; otherwise, +0x5C=2/3). If on the same side as the object: 0x1AF58, 0x1AE3C (0xE462, tries to pick it up) and 0x1ADD2 (approaches); otherwise, circles the ring (0x1A742/0x1A772/0x1A79E). |
| 01ADD2 | cpu_ir_al_objeto | C | R | Direction from table 0x1977C according to the distance (+0x64/+0x66) and the quadrant relative to the object. |
| 01AE3C | cpu_recoger_objeto | C | R | 0xE462 (recoger_objeto). |
| 01AE44 | cpu_chk_cuenta_fuera | C | R | Outside zone 1 → +0x5A=0. In zone 1: if neither of the two opponents (+0x6E/+0x7E) is in zone 1 → return (+0x5A=0x8001; 0x8002 with object). If one is: without +0x2A bit1, returns unless the partner (+0xA4) is also outside (+0x19=1 → +0x5A=0); with +0x2A bit1, returns if the count 1C0596 ≥ table 0x1AED4[id] (0x1AE98) and, otherwise, +0x5A=0. |
| 01AE98 | chk_cuenta_vs_id | C | R | CC/CS: the referee's count-out 1C0596 against the limit from table 0x1AED4[id]. |
| 01AEE4 | cpu_fuera_ir_tumbado | C | R | Opponent in the same zone downed/stunned/running: goes to point 0x1AF50/0x1AF54; otherwise, +0x5C=0. |
| 01AF58 | cpu_planificar | C | R | Opponent not downed → 0x1D1A8 (chooses the attack); downed → +0x2E=0. |
| 01AF70 | ia_elige_movimiento | C | R | 0x1E7DA(d1=2) → table 0x1AFA8[d0][id]; +0x2F = one of its 8 entries chosen with rng&7. |
| 01B010 | cpu_subir_poste | C | R | Action 0xF, +0xB8=2. |
| 01B01E | cpu_delantal_espera | C | R | With +0xC6 bit7 → +0x5C=0; then 0x1BC3E. |
| 01B034 | cpu_delantal_disp | C | R | Dispatches +0x5C&7 (<5) via table 0x1B04E; otherwise, 0x1B06C and the limits. |
| 01B062 | cpu_delantal_def | C | R | 0x1B06C and the limits. |
| 01B06C | cpu_delantal_seguir | C | R | Partner outside → +0x5C=4; otherwise, 0x1B120 and moves. |
| 01B084 | cpu_seguir_objetivo8e | C | R | Moves towards the target +0x8E/+0x90/+0x92 (table 0x1977C); close (+0x92<8) with +0xF2 bit7 → action 1 (inside) or 0x15 (outside). |
| 01B0FE | cpu_atacar_def | C | R | +0x2E=0x8005 and walks; 0x1BEE4 with table 0x1BEB6. |
| 01B120 | cpu_chk_objetivo_cerca | C | R | Only if the target's zone (+0x8E&3) is his own; far away does nothing. CPU: with /dx/<0x30 and /dy/<0x20 → clears +0xF2 bit7 and +0x5C. Human: with /dx/<0x60 and /dy/<0x40 (also <0x30/<0x20 if +0x97=0xB and 1C0026 bit0=0): if 1C0026 bit0=1 or +0x97=0x17 → clears +0xF2 bit7 and +0x5C; in action 0x15/2 nothing; in action 1 → action 0x14 and +0x5C=1; otherwise → action 0 and +0x5C=1, and if +0x97≠0xB also clears +0xF2 bit7 and +0x5C. |
| 01B1D6 | cpu_relevo_disp | C | R | Clears +0xE2 bit3; dispatches +0x5D&7 (<4) via table 0x1B1F8; otherwise, 0x1B208. |
| 01B208 | cpu_relevo_ir | C | R | Partner outside → +0x5C=3; otherwise, goes towards the partner going around. |
| 01B2A0 | cpu_entrar_relevo | C | R | Copies the partner's zone, action 0xC with the sub from table 0x1B2E8[id] (entry), clears the corner bit (table 0x1B2F8) of 1C1821, +0xB7 bit0. |
| 01B2FC | cpu_delantal_volver | C | R | With +0xC6 bit7 → +0x5C=0. Partner outside → 0x1BBB4; otherwise, 0x1BC3E. |
| 01B37E | cpu_bucle_principal | C | R | If nobody is covering (action 0x17) and 0x1B3E4 gives CS → +0x5C=7. Except in states 9/0xA/0xD, plans (0x1D1A8). Dispatches +0x5C&0xF via table 0x1B40C. |
| 01B3E4 | ia_compa_cubierto | C | R | CC if the partner is downed (0xB) and covered (+0x18 bit5); otherwise, CS. |
| 01B44C | cpu_ayudar_pin | C | R | Partner covering (0x17) and close (0x1B46C) → +0x5C=0xF; otherwise, 0x18F56. |
| 01B46C | chk_cerca_60_40 | C | R | CS if dx ≥0x60 or dy ≥0x40. |
| 01B486 | cpu_ir_salvar_pin | C | R | With the partner covering and close: goes to the point (0x1B4D2) next to the partner (x±0x60/0x40, the opponent's y); otherwise, +0x5C=0. |
| 01B4D2 | punto_salvar_pin | C | R | +0x24 = partner's x −0x60/+0x40 according to the team; +0x26 = the opponent's y; 0x1CFD8. |
| 01B504 | cpu_delantal_disp2 | C | R | +0xF3−− if ≠0; dispatches +0x5D&0xF (<8) via table 0x1B52A; otherwise, 0x1B54A. |
| 01B54A | cpu_delantal_pasear | C | R | On the apron: paces in y between 0x118 and 0x170 with random turns (+0xC3); with the partner close (<0x40) and without +0xE3 bit0 → +0x5C=5. 0x1B6F0 decides whether to enter. |
| 01B62E | limite_delantal | C | R | y limited to 0x118–0x170 (stops); otherwise, 0x220C4. |
| 01B656 | cpu_delantal_seguir_rival | C | R | Follows the opponent's y along the apron. |
| 01B6F0 | cpu_delantal_decidir | C | R | If 0x1BDCA gives CS (someone in action 1/2/0x15/0x16) → +0x5C=6. CPU with the partner in action 0 and +0x5D=6 → +0x5C=5. Otherwise, takes the zone of entry +0x6E (if it has bit3; otherwise, +0x7E): in zone 0 → 0x1B756 and, if it has not entered (+0x2A bit7), 0x1B942 (grab from the apron); in zone 1 → 0x1BB92. |
| 01B756 | cpu_temporizador_entrada | C | R | With +0xC6 bit7 counts +0xC7; when finished: +0x2A bit7 (enters), +0x5C=4 (0 if not on the apron), +0xF2 bit7, +0xE0 = table 0x1B7E2[id]. Otherwise, dispatches +0xC6 via table 0x1B7C2. |
| 01B7F2 | nop | C | R | Nothing. |
| 01B7FA | cpu_programar_entrada | C | R | If the partner has energy 0 and +0x106 bit1 is already set: only continues with a roll <3/16. Then: in mode 1C0026 bit0=1 during match 0, or the first time (+0x106 bit1 was 0, it gets set) → +0xC6 bit7 and +0xC7 = table 0x1B938[1C0028&0xF]. The following times → 0x1B8F4 with table 0x1B862. |
| 01B880 | cpu_entrada_ya | C | R | +0xC6 bit7. |
| 01B888 | rts_1b888 | C | R | rts. |
| 01B88A | rts_1b88a | C | R | rts. |
| 01B88C | ia_tirada_tag | C | R | In mode 1C0026 bit0=1 during match 0, or the first time (+0x106 bit0 was 0, it gets set) → +0xC6 bit7 and +0xC7 = table 0x1B938[1C0028&0xF]. The following times → 0x1B8F4 with table 0x1B8D6. |
| 01B8F4 | cpu_tirada_entrada | C | R | Roll against table a2[1C0028*3 + 0x1CEF4] → schedules the entry. |
| 01B942 | cpu_agarre_desde_delantal | C | R | With 1C001A bit7 and the opponent inside at dx ≤0x50: if right next to him (dx≤0x2C, dy≤0x10, same z), without the rope vibrating (bit14 of 1C1898/1C189A), opponent not in 0x1F, neither of them id 7, opponent bouncing/running or (0x1BB0C/+0xE2 bit5) in action 0 with his back turned, without break: he to action 0x13 and the opponent to 0x1B (grabbed from the apron), linked. Human with a button: action 0xC sub 0x3C (tag). If it does not happen: CPU → action 0 with +0x5C=1. |
| 01BB0C | chk_humano_modo1 | C | R | CS if human with control and 1C0026 bit0. |
| 01BB32 | cpu_tirada_agarre_delantal | C | R | Once (+0xE2 bit6): roll against table 0x1BB7E (0x1BB88 for the CPU)[1C0028] → +0xE2 bit5. |
| 01BB92 | cpu_delantal_a_ring | C | R | Target in zone 1 → +0x2A bit7, action 0, +0x5C=2. |
| 01BBB4 | cpu_bajar_delantal | C | R | Walks outwards (0x40/0xC0 according to the team); on colliding: action 3 (go down), +0xAC according to the side; with 1C0026 bit0 the human regains control (+0x2A bit0). |
| 01BC3E | cpu_volver_esquina | C | R | Goes towards y 0x110–0x150 and, on touching the rope with 0x1A25C, action 7 (climb onto the apron). |
| 01BCB6 | cpu_delantal_ir_esquina | C | R | Partner inside, close (<0x60) and without +0xE3 bit0: goes to the corner (y 0x108/0x150) and turns (+0xE2 bit3). |
| 01BD5C | cpu_delantal_mirar | C | R | If 0x1BDCA gives CS (someone in action 1/2/0x15/0x16, see 0x1BDCA): orients with table 0x1BDC6 while y is in 0x118–0x170; otherwise, +0x5C=0. Bug in the original: computes the team orientation in d1 but writes d0 (the index returned by 0x1BDCA) to +0xA. |
| 01BDCA | chk_alguien_accion_1_2_15_16 | C | R | CS if any of the 3 (+0x68/+0xA0/+0xA4, table 0x1BE2A) is in action 1, 2, 0x15 or 0x16 with his orientation (+0xA bit15) different from his team's (+0x2A bit4). What those actions represent here: UNCONFIRMED (it is not the downed state 0xB). |
| 01BE30 | cpu_carrera | P(A) | A | CPU run (action 01 with +0x2A bit3). |
| 01BE9C | ia_ejec_mov | C | R | Table 0x1BEB6 (0x1BECA if 0x1D136 gives CS) → 0x1BEE4. |
| 01BEE4 | ia_iniciar_llave | C | R | With +0x2E bit7, the same zone as the opponent and 0x2786 CC: looks up +0x2F in list a2 → descriptor 0x1C028+6*n with flags: bit0 = not with the same orientation as the opponent, bit1 = contact +0x6E bit6, bit2 = compares +0xA with byte +0xA of a2 (falls into the next descriptor; probable bug in the original), bit3 = side. dy<8 and dx in [+2,+4) of the descriptor; if closer and outside → +0x5C=7. If everything matches and 0x1C14E does not prevent it → action 0xC with sub +0x2F; with subs 4 and 0x1C, the opponent goes to action 0x10 and remains linked. |
| 01C14E | chk_sub_a_limite | C | R | Sub +0x2F=0xA: if x exceeds 0x330 (0x2E0 on the other side) → +0x2E=0, CS. |
| 01C180 | acc_salir_ring | C | R | Clears side bit1 and goes through table 0x1C26E (0x1C2AA for id 7) according to the side (+0x18 bit0) with steps (pose, dx, dy). When finished, +0x19=3 (outside), action 0, and clears +0x33 bit7 and +0x2A bit2. |
| 01C306 | acc_volver_ring | C | R | Same with tables 0x1C3F6/0x1C432; if +0x2A bit2, restores bit1. When finished, +0x19=0 (inside). |
| 01C4A2 | ent_esquina_2 | C | R | Entry via the corner: +0xB8 bit7, 1C1821 bit2 for 4 frames, pose 0x1F, fixed position 0xF6CE; then 0x1E8B0. |
| 01C4FA | ent_esquina_0 | C | R | Same bit0, position 0xF6D4. |
| 01C552 | ent_esquina_3 | C | R | Same bit3, pose 0x69, position 0xF6DA. |
| 01C5B0 | ent_esquina_1 | C | R | Same bit1, position 0xF6E0. |
| 01C60E | acc_caer_init | C | R | 0x1C61A and 0x8EC8. |
| 01C61A | acc_caer_inicio | C | R | First time: if 1C1828=0xFF records the id (first fallen); state 1, velocity from table 0x95BC[id], turns his back to the opponent, direction ±0x40. |
| 01C68C | acc_burla | C | R | Taunt: pose 0x1A (0 for subs 0x32/0x18/0x33/0x14) 4 frames; then dispatches by id (table 0x1C6FA). |
| 01C71A | burla_fin | C | R | Action 0, +0x5C=0. |
| 01C726 | burla_a | C | R | Sound 0x22, +0xE2 bit0; 2 poses from table 0x1C7B0 (id 5 uses id 2's) repeated twice. |
| 01C7C8 | burla_b | C | R | Sound 0x22, one of 3 random poses (table 0x1C818). |
| 01C824 | burla_c | C | R | Sound 0x22, pose 0x103 (0x20 frames). |
| 01C85C | burla_d | C | R | Sound 0x23, one of 2 random 4-pose sequences (table 0x1C8DE), twice. |
| 01C906 | acc_coger_silla | C | R | Takes/uses the object (sound 0x2C); in matches 4/9 the CPU → 0x1CB16. Outside: pose 0xEF and places the partner at ±0x33, creates the object in the hand (0x1CA6A). When finished: outside → action 7 with +0xE3 bit0 (and control if human); inside → +0xC0 bit7, waits for the partner to enter → action 6. |
| 01CA6A | crear_obj_mano | C | R | 0x1D114 gives a free object a4: active, x/y/z from the wrestler with the offsets of tables 0x1CB06/0x1CB0E[id], pose 0x7C, orientation. |
| 01CB16 | coger_silla_modo49 | C | R | In matches 4/9 (CPU): places the partner at ±0x18 and does 4 poses (tables 0x1CBF0 inside / 0x1CC10 outside, index id−6: only gives valid data for DiBiase (6) and André (7)). Outside → action 7; inside → waits for the partner to enter → action 6. |
| 01CC30 | acc_cc30 | C | R | Jumps to 0xE604. Followed by 0x1CC36: takes object +0x60 (the object goes to action 1 with owner and side), 2 poses from table 0x1CCD0[type], then action 0 with +0x5C=0. |
| 01CCE8 | chk_furia | C | R | If +0xF9 bit0=0 and (+0xF8 bit7 or the counter +0xF6 ≥ table 0x1CD48[id]): +0xFA = duration from table 0x1CD6C[1C0028], +0xF9 bit0, clears +0xF8 bit7 and +0xF6 → CS (enters special/fury mode). |
| 01CD50 | tick_furia | C | R | With +0xF9 bit0: +0xFA−−; when finished clears +0xF8/+0xF9 and +0xF6. |
| 01CD80 | chk_contador_f6 | C | R | CS if +0xF6 >= table 0x1CD48[id] (cmp.b and then eori 1 to CCR inverts the carry); CC if lower. Corrected 31-10-2026: it previously said the opposite. |
| 01CDA4 | cpu_decidir_ir_objeto | C | R | Nothing in matches 4/9, with ids ≥6 (DiBiase/André), with an object in use (1C1822) or if he already carries one. +0xE4 works as a history: each frame it shifts 8 bits and +0xE5 bit7 is set if next to the table (y<0x100 and x<0x250 or ≥0x3A8). +0xE4 == 0x80 is the arrival edge (next to the table now and not in the previous frame). At that moment, if the opponent is farther than the table (0x1CE24 ≥0) and the roll 0x1CE6C comes out lower than the table → +0xE6=1 and +0x5C=4 (go for the object). |
| 01CE24 | dist_rival_vs_mesa | C | R | d2 = dist²(opponent) − dist²(table: x 0x200/0x400 according to the side, y 0xB0). |
| 01CE6C | tirada_objeto | C | R | Roll &0xF against table 0x1CE92[1C0028]. |
| 01CE8C | tipo_objeto | C | R | d0=1. |
| 01CE9C | nivel_energia4 | C | R | Energy +0x3C divided by (maximum energy from table 0x7FEC, or, for the CPU (+0x2A bit3), 0x8190[level 1C0028*8 + slot +0x2A&7]; levels 0–3: 45/49/47/43/47/43, 60/64/62/58/60/58, 68/73/70/66/71/66, 72/76/74/70/74/70/88/96)/4 (minimum 1); the result is capped at 3. |
| 01CEF4 | nivel_energia3 | C | R | Same with /3 → 0–2. |
| 01CF50 | dir_a_rival_offset | C | R | Direction (table 0x1977C, band by distance) towards the opponent + offset (a2: dx with bit15 = side opposite to the orientation, dy). CS if it arrives (dy<5 and dx<9). |
| 01CFD8 | dir_a_punto | C | R | Same towards the absolute point (a2). |
| 01D032 | x_trapecio | C | R | x of an edge of the ring trapezoid according to y (slope 1/6, sign by side). |
| 01D04C | chk_compañero_mismo_objetivo | C | R | CS if the partner is in the same zone, with the same opponent and his action is compatible according to bit table 0x1D0A0 (bit0/bit1 by side). |
| 01D0C2 | tirada_id | C | R | Roll &0xF < a2[id] → CS. |
| 01D0E2 | tirada_por_energia_rival | C | R | Intends to roll &0xF < a2[energy_level(opponent)*8 + id] → CS. Bug in the original: adds the level offset to a1 (the opponent's pointer) instead of a2, so in practice the roll is against a2[id] without taking energy into account. |
| 01D114 | buscar_objeto_libre | C | R | First free object (bit7=0) of the 4 in table 0xBCB8. If none is free, it still returns the last one (a4) even if occupied. |
| 01D136 | chk_rival_accion_1_15_16 | C | R | CS if the opponent is in action 1, 0x15 or 0x16 (it is not the downed state 0xB; what those actions represent here: UNCONFIRMED). |
| 01D166 | ia_retardo | C | R | +0xF3 = table 0x1D18E[rng%4]. |
| 01D1A8 | ia_intencion | C | R | Chooses +0x2E/+0x2F (CPU intention). Table 0x1D33A (0x1DD7E if he himself is in action 1) indexed by the opponent's energy level 0x1CEF4, which counts as 0 until 1C1852 ≥ 0x258. Then by the opponent's action (0x1F if he is in action 0xC with the sub in list 0x1D2B0: 19 2F 24 2C 20 1A) and by his own id. rng&0xF & the mask 0x1D2FA (0x1D31A in action 1)[action]; signed byte, mask 0x807F. Unless both have +0x2A bit1 and he is not outside (+0x19≠1), it is remapped with list 0x1D2B8[id]. If he carries an object (+0x5E bit6) → +0x2F=0x30 (+0x2E=0 if the opponent is downed, 0xB). |
| 01E05C | ia_elegir_llave | C | R | Sub-action +0x30: table 0x1E392 if outside (+0x19=1, index 0x1E7DA d1=0, rng&7) or 0x1E1A6[opponent's energy level, 0 until 1C1852 ≥0x258][id][rng&0xF]. Without +0x2A bit1: +0x31 = table 0x1E14E[id][1C0046 bit1]. Adjustments 0x1E826 (list 0x1E15E) → 0x1E88A (list 0x1E170); if the sub is in list 0x1E19A, turns. Action 0xC and the opponent to 0x10. |
| 01E432 | ia_elegir_llave_b | C | R | Variant of 0x1E05C: tables 0x1E74A (outside, d1=1) and 0x1E55E[difficulty][id][rng], with ext. Sub 0x36 outside x 0x2C0–0x340 becomes 0x1E. Adjustments 0x1E510/0x1E526; turn if in list 0x1E55A. Action 0xC and the opponent to 0x10. |
| 01E7DA | chk_lado_exterior | C | R | Outside (+0x18 bit4): 1 if heading towards an edge according to x (0x2A0/0x360) and the orientation. |
| 01E826 | chk_sub_fuera_ring | C | R | Looks up sub +0x31 in list a2 (sub, dx); CS if the resulting x leaves the ring (≥0x380 / <0x280). |
| 01E88A | remap_sub_por_id | C | R | Looks up +0x31 in list a2 (9 bytes); replaces with byte [id]. |
| 01E8B0 | ia_llave_suelo | C | R | Sub +0x31 = table 0x1E8EC[id + 8 if the opponent is not downed]; action 0xC on the same side as the opponent; the opponent's +0x104 = 1. |
| 01EB40 | camara_disp | C | R | Camera: a0=1C18AC, a1=1C18B0 (both followed); dispatches 1C18A8 via table 0x1EB60. |
| 01EB68 | despacho_zonas | C | R | Jumps to 0x1EB8A[(own zone & 0xF)*0x10 + (opponent zone & 0xF)*4]. |
| 01EBCA | camara_normal | C | R | Centres x (0x1EEE0) with a maximum jump of 4; y (0x1EF2A); y does not exceed 0x15C. |
| 01EC44 | camara_seguir_uno | C | R | If a0 is CPU (+0x2A bit3): if a1 is also CPU → 0x1EE9A; otherwise follows a1. If a0 is human and 1C0026 bit1: if a0 is outside (+0x19==1) → 0x1EE9C; if a1 is → saves 1C18AC/1C18B0, swaps and 0x1EE9C. Rest: jump by +0xB8 of the followed one (table 0x1EC96). |
| 01ECAA | camara_poste | C | R | By +0x18&3 (table 0x1ECBE): each corner has its target position. |
| 01ECCE | cam_esq_0 | C | R | x → 0x302, y → 0x1FB (steps of 2). |
| 01ED18 | cam_esq_1 | C | R | x → 0x1F9, y → 0x1FB. |
| 01ED62 | cam_esq_2 | C | R | x → 0x32D, y → 0x155. |
| 01EDAC | cam_esq_3 | C | R | x → 0x1F9, y → 0x1FA. |
| 01EDF6 | camara_delantal | C | R | x as normal; y → 0x15B or 0x1CB according to +0x18 bit1. |
| 01EE9A | rts_1ee9a | C | R | rts. |
| 01EE9C | camara_x_y | C | R | 0x1EEE0 and 0x1EF2A. |
| 01EEA6 | camara_los_dos_fuera | C | R | Both outside: normal x; y goes down to 0xEF. |
| 01EEE0 | camara_x | C | R | 1C002A = x(a0) − min(/dx//2, 0x50) towards a1 − 0x80, limited to 0x1A0–0x360. |
| 01EF2A | camara_y | C | R | 1C002E follows the wrestler's y+z with a window of 0x40–0x80; minimum 0xEF. |
| 01EF78 | camara_transicion | C | R | On changing target (1C18B5 bit3): moves 1C002A 2 pixels per frame towards the target (bit1 on arriving) and the y (bit0); with both bits → 1C18A8=0 (returns to normal mode). |
| 01F0B0 | camara_elegir | C | R | With a game in progress: dispatches 1C0026&3 via table 0x1F0D0. |
| 01F0E0 | cam_elegir_1p | C | R | 1C18AC = the human (bit0), 1C18B0 = the CPU with bit1. |
| 01F11A | cam_elegir_bando | C | R | By bit1. |
| 01F154 | cam_elegir_2p | C | R | Two humans (a3/a4): rules by actions (0xF post, 0x19, 0xC, outside 0x3/0x6 with 0x1F340) to choose which one to centre; if it changes, transition (1C18B5 bit3, 1C18A8=1). |
| 01F340 | chk_fuera_o_cruzando | C | R | CS if outside or in action 3/6. |
| 01F364 | cam_saltar_delantal | C | R | If the followed one has +0xF2 bit7 (on the apron), swaps him for his partner (0x1F39C). |
| 01F39C | compañero_de | C | R | 1C0100↔1C021A, 1C0334↔1C044E. |
| 01F3CE | camara_a_hw | C | R | Scroll: 180004 = 1C002A−0x200 (bit9 → 1C2B9C bit5), 180006 = 0x200−1C002E (bit9 → bit4); 18000A = 1C2B9C. |
| 01F434 | fondo_cmd | C | R | 1C182C = d0; calls table 0x1F450[d0]. |
| 01F474 | fondo_init_ring | C | R | Copies 4 tilemap blocks (0x1F72C/0x1F868/0x1F9D4/0x1FAD0) to 0xC0000/0xC0400/0xC0800/0xC0C00 with 0x203C2 and sets the fixed cells 0xC01B0 and 0xC0A50. 1C1890=1, 1C1892=0, scroll 1C002A=0x280 and 1C002E=0x200. Ports 0x180004=0x80 and 0x180006=0. 1C2B9C &= 0xCF and copies it to 0x18000A. |
| 01F50C | marcadores_nombres | C | R | Writes the wrestler's 3×2 tiles (table 0x2197A[id]) to the text layer (c00b4/c0174/c0484/c0544); the two on the left mirrored. |
| 01F546 | nombre_derecha | C | R | 3 rows × 2 tiles, attribute 0x20. |
| 01F57E | nombre_izquierda | C | R | Same mirrored (bit7 of the attribute). |
| 01F5C8 | fondo_scroll_columnas | C | R | If 1C182D=0: according to scroll X 1C002A, looks up the column in thresholds 0x1F726 (advances 1 by 1 against 1C1890) and copies 16 tilemap rows (table 0x1F706) in two halves per frame (1C1860/62/66). According to 1C1891, adjusts the fixed cells 0xC0B80/0xC0A50/0xC01B0. |
| 0201AC | esc_dibujar_a | C | R | Scene (table 0x1F43E): draws list 0x20D9E (0x203C2) and 7 columns of table 0x20F06 on layer c0000; 0x207C6. |
| 0201F4 | esc_dibujar_b | C | R | Scene: fills c0000 (0x4FFDC), two mirrored blocks of 0x20F3E (0x20314), rows c03C0/c03CC and 10 tiles of 0x20FC8; 0x207C6. |
| 0202A0 | esc_dibujar_c | C | R | Scene: fill 0x6FF00, mirrored blocks of 0x20FDC and 32 tiles of 0x21068 in c0380. |
| 020314 | blit_bloques | C | R | Draws blocks of consecutive tiles (format: rows, columns, attribute^d7, tile, width) with step d0 and skip d6. |
| 02034A | esc_dibujar_d | C | R | Scene: list 0x210A8 and six blocks of 4×4 tiles (0x20404); c0264=0x720043. |
| 0203C2 | blit_lista_rle | C | R | Draws a list: rows; per row (attribute, tile[, 0xFF = new attribute], increment with bit7 = mirror, count). |
| 020404 | blit_4x4 | C | R | Block of 4×4 consecutive tiles. |
| 020424 | esc_dibujar_e | C | R | Scene: 6 tiles of 0x21134, rows of fixed tiles and list 0x210EC (0x2048E). |
| 02048E | blit_lista_rect | C | R | List of rectangles (destination, attribute, tile, height, width, skip); negative d6 = draws backwards (mirror). |
| 0204DC | esc_dibujar_f | C | R | Scene: list 0x2113A, fixed blocks; prepares the animation (1C1836=0x80008, 1C182E=0, 1C185E=0, 1C185C=0x10). |
| 02057A | esc_dibujar_g | C | R | Scene: list 0x218D6 and two blocks of 3 tiles × 4/3 rows. |
| 0205D6 | esc_dibujar_h | C | R | Same mirrored (list 0x21928). |
| 020632 | esc_combates_4_9 | C | R | In matches 4/9: 4 rectangles (table 0x2069E) with tiles 0x60FFE1… skipping the gaps (0x2065A). |
| 02065A | blit_rect_saltos | C | R | Rectangle with consecutive tiles that jumps from 0x60FFF4 to 0x62FF43 and is cut at 0x62FF47/0x62FF4E. |
| 0206BE | esc_anim_6 | C | R | With scene 6 (1C182D): every 8 frames alternates two versions (0x211FA/0x2121C and 0x2123E/0x21272); and a 5-step cycle (duration table 0x207F6, tiles 0x20800) in c00C0/c0100 mirrored. |
| 0207C6 | fondo_reset_scroll | C | R | Zeroes 0x180004/0x180006 and 1C002A/1C002E; 1C2B9C &= 0xCF and copies it to 0x18000A. |
| 020824 | esc_anim_7_8 | C | R | Scenes 7/8: advances the counters (0x208DA alternates every 8 frames; 0x208FE cycle of 3). |
| 0208DA | ctr_alterna8 | C | R | Alternates d1 every 8 frames (init 1C182C bit7). |
| 0208FE | ctr_ciclo3 | C | R | d1 = 0,1,2 every 8 frames (init 1C182C bit6). |
| 020928 | esc_anim_dibujar | C | R | Scenes 7/8: if the frame changes, redraws (0x209C6 / 0x20C72). |
| 0209C6 | esc_anim_a | C | R | By frame (+2 in scene 8), table 0x209E6. |
| 0209F6 | esc_anim_a0 | C | R | 4 tile blocks (0x20B1A). |
| 020A88 | esc_anim_a1 | C | R | Same, the other frame. |
| 020B1A | blit_bloque_inc | C | R | Block of increasing tiles. |
| 020B34 | esc_anim_a2 | C | R | 4 mirrored blocks (0x20C58). |
| 020BC6 | esc_anim_a3 | C | R | Same. |
| 020C58 | blit_bloque_dec | C | R | Block of decreasing tiles, backwards. |
| 020C72 | esc_anim_b | C | R | By frame (+3 in scene 8), table 0x20C92. |
| 020CAA | esc_anim_b0 | C | R | 2 blocks of 5×8 (0x20D04). |
| 020CC8 | esc_anim_b1 | C | R | Same. |
| 020CE6 | esc_anim_b2 | C | R | Same. |
| 020D04 | blit_5x8 | C | R | 5 rows × 8 tiles. |
| 020D24 | esc_anim_b3 | C | R | 2 blocks (0x20D7E). |
| 020D42 | esc_anim_b4 | C | R | Same. |
| 020D60 | esc_anim_b5 | C | R | 2 blocks with 0x20D7E: 0xC03E0 tile 0xCD006C and 0xC03C0 tile 0xCD0094. |
| 020D7E | blit_5x8_dec | C | R | 5×8 decreasing tiles, rows upwards. |
| 0212A6 | cuerdas_anim | C | R | Per side (1C1898/1C189C/1C189E/1C18A4/1C1894 and the block 1C189A…1C1896): 0x21324. |
| 021324 | cuerda_vibrar | C | R | Bit15 (requested by 0x9700) → starts: sound 0x2A and bit14 = vibrating. If the low nibble ≠0, starts at step 2 (frame 3); if 0, at step 0 (frame 1). Advances up to 8 steps with the durations of table 0x213A4 and frames 0x213AC (&3) in d4 → 1C1894/1C1896; at step 8 clears bit14. |
| 0213B4 | cuerdas_a_video | C | R | For 1C1898 with bit14 (vibrating; btst.b #6 on the high byte) and 1C1890<2, if the frame changed (1C189C≠1C189E) → 0x21412. For 1C189A with bit14 and 1C1890≠0, if 1C18A0≠1C18A2 → 0x21420. |
| 021412 | cuerda_dibujar_0 | C | R | a0=c020C, table 0x21476 → 0x2142C. |
| 021420 | cuerda_dibujar_1 | C | R | Rope on the other side: a0=0xC0620, table 0x216A6; enters the common code 0x2142C, which copies block a2[0x2146E[d0]*0x8C] (14 rows of 5 cells, with a jump of 0x400 at row 6). It is not a portrait: it is called by 0x213B4 for 1C189A. 0x21412 uses the same code with 0xC020C/0x21476. |
| 0219AA | indicador_1a92 | C | R | Edge of 1C1A92 bit7: draws (on/off) 2 rows of 4 tiles at c0C8C or c08A4 (according to bit0) with the tiles of 0x21A4A. |
| 021A00 | ind_tiles | C | R | Chooses the destination and the tiles. |
| 021A2E | ind_dibujar | C | R | 2 rows of 4. |
| 021A4E | textos_luchadores | C | R | Paints the texts 0x21BB8[id] of the 4 wrestlers (ids from 1C012A/244/35E/478). If the second of a pair has id 6 (DiBiase), swaps him with the first. It is not a portrait: 0x21BB8 points to RLE text strings (4-byte fg0 destination and then top/bottom tile pairs) painted by 0x21B4C with the two-row font. That they are the wrestlers' names is UNCONFIRMED: the letter table is not decoded. |
| 021A9A | fg0_iconos_fijos | C | R | Writes fg0 cells 0x80838–0x808C4 with tiles 0xFFE1–0xFFF8 (palette 0x10). |
| 021AEC | texto_lucha_0 | C | R | Text of wrestler d0, without extra offset (0x21B4C). |
| 021AFE | texto_lucha_1 | C | R | Text of wrestler d1, destination +0x180. |
| 021B10 | texto_lucha_2 | C | R | Text of wrestler d2, destination +0x580 (+0x100 if id 6, DiBiase). |
| 021B30 | fg0_texto_rle | C | R | Draws RLE text from (a0)[d3] in fg0 (+0x700, or +0x800 if d2=6) in two rows, with palette 0x17. Codes: 0 end, 1 skip, 2 gap, 0xEB half cell. |
| 021E06 | texto_id_1c0102 | C | R | Text 0x21BB8 of the id in 1C0102. |
| 021E1A | texto_id | C | R | Text 0x21BB8[d0] at its destination, without extra offset. It is not a portrait: 0x21BB8 points to RLE text strings (4-byte fg0 destination and then top/bottom tile pairs) painted by 0x21B4C with the two-row font. That they are the wrestlers' names is UNCONFIRMED: the letter table is not decoded. |
| 021E30 | textos_intro | C | R | Texts 0xC, 8+(1C0028&0xF) and 0xB (or 0xD if that index is 0xA, i.e. in match 2). |
| 021E5A | lim_fuera | C | R | Limits outside the ring (table 0x221AA, and 0xBB) with 0x22140; in the air (+0x18 bit7) above z 0xDB → +0x9E bit7. Applies the corrections of the bits of +0x9F (0x21EBA: x/y). |
| 021E9A | lim_aplicar | C | R | For each bit 0–3 of +0x9F applies the correction (x=d2 or y=d0). |
| 021EC4 | lim_x | C | R | x=d2. |
| 021ECA | lim_y | C | R | y=d0. |
| 021ED0 | lim_ring | C | R | Ring limits (table 0x221B2) with 0x22140; outside: edges x 0x240/0x3C0 and y 0x158; inside: side ropes ±0x30 → +0x9F bits 0/1/3. No contact → 0x21FE6; with contact in the air → 0x22040 (hit against the rope/post). |
| 021FB6 | marca_choque_on | C | R | 1C1A9A /= the wrestler's bit (index in 0xEA4C). |
| 021FE6 | marca_choque_off | C | R | Clears the wrestler's bit in 1C1A9A. |
| 022016 | chk_marca_choque | C | R | Tests the wrestler's bit in 1C1A9B. |
| 022040 | choque_poste | C | R | Once per contact (+0x9E bits 0/1; 0x22016): if action +0x2D is in list 0x220BE: sound 0x33 if (+0x18 bit0 and contact bit0) or (+0x18 bit0=0 and contact bit1), otherwise 0x47; 1C1854 bit7. Damage 5 (+0x3E=5, 0x16488) if the action ≠8 OR if it is action 8 with sub +0x45 = 0xA (corrected in audit: it previously said the opposite). Then 0x21FB6. No contact → 0x21FE6. Which side is rope or post: visually UNCONFIRMED. |
| 0220C4 | lim_delantal | C | R | Apron limits (tables 0x221C2/0x221BA) → +0x9F bit0/1; in the air above z 0xDB → +0x9E bit7. |
| 022140 | lim_trapecio | C | R | Against table a2 (yback, yfront, xleft, xright) minus d4: +0x9F bit3 (back), bit2 (front; offset 0), bits 1/0 (sides with slope 1/6 per y); d2/d0 = corrected values. |
| 0221CA | objs_extra_tick | C | R | Goes through the 5 pairs of 0x221F2 (a0, a1) and, if a1 is active, calls 0x2221A. |
| 02221A | obj_sombra_tick | C | R | Support object of wrestler a1: init (state 0xA, z 0xBB, +0x1A=0x8040); by side (+0x18&3) calls table 0x222A0 (0x222AC with 1C00F0 bit7; inside in actions 3/4 uses entry 0). Copies the orientation from the pose except with 1C00F0 bit0. |
| 0222C4 | obj_sombra_ocultar | C | R | 1C00F0 bit0. |
| 0222D6 | sombra_cuerda | C | R | Object linked to a wrestler (a1): if table 0x2535A[a1's state] = 0, it is hidden. Otherwise, +0x19=3 and y of the step of table 0x2237A. Pose from tables 0x22392[1C1894&3] (x=0x26E) or 0x223FA[1C1896&3] (x=0x38E, flipped) according to the side (a1+0x18 bit0). |
| 022462 | flash_1c183e | C | R | With a game in progress and without 1C1854 bit7: if 1C183E bit6/7, starts (1C1890/1C1892 to +4/+6, 0xA cycles of 6 frames, 0xE5) and counts it; when finished → 0x80. Otherwise, 0x23406. |
| 0224E8 | flash_dibujar | C | R | In scene 0 (1C182C=0): draws message 1C183E (3 rows from tables 0x22634/0x22640/0x230F0 according to 1C1890 and the phase); message 0x15 in phase 4 writes c0414. Otherwise, 0x230FC. |
| 0225B0 | tilemap_rle | C | R | Writes an RLE string to the tilemap: geometry from table 0x22760[d1] (x0, width, skip) and destination 0x22640[d1*0x10]. Codes 0x00: 0xFD end, 0xFC changes palette (d6), and otherwise, repetition. |
| 022848 | datos | C | R | False entry: it is data (dc.w 0xFCFD…), not code. |
| 023054 | datos_23054 | C | R | Not code: tile table (dc.w 0x0DFF, 0x00FC…) of message 0x22640, decoded by the linear seed. |
| 0230FC | fondo_anim_publico | C | R | Exits if 1C1890 == 1 or if 1C182C ≠ 0 (corrected in audit: it previously said "only if 1C1890=1"). With 1C1854 bit4 and 1C1857 == 1 draws 2 RLE strings (0x225B0) from table 0x23170 + 1C1890*0xC + 1C1856*0xC. |
| 0232DE | luces_azar | C | R | 1C184A: once, randomly chooses a position (rng%4) and repetitions (&3); cycles of 10 frames of 2 phases (bits 5/4) until exhausted. |
| 02336C | luces_dibujar | C | R | With 1C184A active (and without 1C183E bit7): tiles from table 0x233F6[position][phase] at c0B70, c0F40, c0BB0, c0F80 (4 per place). |
| 0233DC | blit_4_tiles | C | R | 4 consecutive tiles with attribute = high byte. |
| 023406 | flash_1c1854 | C | R | Starts with bit6 of 1C1854, or with bit7 if 1C1890≠1 (with bit7 and 1C1890=1 it does nothing; corrected, it previously said the opposite). Phase 0 of 4 frames and phase 1 of 0x21 frames; then 1C1854=0. Bit4 marks that it is visible. |
| 02347E | pantalla_versus_retratos | C | R | 0x23F10 and 0x207C6; chooses the pair 1C0100/21A (or 334/44E if 1C0BC2 bit6=0). Draws 4×4 tiles per id (table 0x23536) at 0xC01D4/0xC01E8 and a 4×8 block from table 0x2354E at 0xC0318. |
| 0235CE | pantalla_presentacion | C | R | Draws the presentation of match d0 on layer 0x80000: 5×5 backgrounds (0x236A2), list 0x23702[d0] (0x236BC; entry 0x237FE clears first with 0x2367A) and fixed tiles. |
| 02367A | limpiar_6x6 | C | R | Clears 6×6 tiles at 0x80B28. |
| 0236A2 | relleno_5x5 | C | R | 5×5 identical tiles. |
| 0236BC | blit_lista_presentacion | C | R | List: destination, count, tile; per element attribute (0xFF = repeat) and skip. |
| 0236F4 | fill_inc | C | R | Writes d5+1 longs incrementing d2; a2 += d6. |
| 02387C | pantalla_titulo_seq | C | R | Screen sequence with fade: scene 3, palette 0x140200=0x900, fg0 banner 0x2660E(3), draws frames 0x23CEE, texts 0x23757/0x237BD and row 0x23D2E; camera to 0; 1C0568=0; sound 0x45; 0x1D steps of table 0x23A0A (0x23A28) with wait (0x239DC); palette to 0. |
| 0239DC | espera_bucle | C | R | Busy-wait loop (d0 × 0x1B80). |
| 0239F4 | blit_texto | C | R | Initial tile of a1 and list (0x236CE). |
| 023A02 | fg0_dibujo_cont | C | R | Intermediate entry of 0x23A28 (continues with a0/a1/a2 already loaded). |
| 023A28 | fg0_dibujo | C | R | Draws graphic d1 of table 0x23AC4 in fg0 (0x80000 + offset). Runs (start, end) of tiles with palette d4. Commands after 0xFF: 0 skip n cells, 1 palette, 2 new row (+0x80), 3 repeat n, 0xFF end. |
| 023F10 | fg0_marco_versus | C | R | 0x24E2, graphics 0x18–0x1D (0x23A28) and tile borders 0xA0–0xA8 (palettes 0x38/0x39) in fg0, plus a column of table 0x23FF4. |
| 0240B6 | llave_por_sub | C | R | +0x9E=0. Looks up +0x31 in the 14-byte list 0x240F0; entry i jumps to 0x240FE+(13−i)*4 (the index goes backwards because it uses the dbra counter). |
| 024136 | llave_sub_0x24136 | C | R | 0x244EE with table 0x24146 and d0=3. |
| 024168 | llave_sub_0x24168 | C | R | 0x244EE with table 0x24178 and d0=1. |
| 02418A | hitbox_pose_a | C | R | Table 0x241AE: 0x24554 with 5 entries, dx 0x10, dz 0x10; no contact → 0x24222. |
| 0241BA | llave_sub_multi | C | R | Tries 0x24554 with 6 tables (0x24254…0x2429C) and parameters (d0, d1, d2); stops at the first that gives CC. |
| 0242AC | hitbox_pose_b | C | R | Three attempts (0x242F8/0x24306/0x24314) to shift the wrestler according to the pose. |
| 024322 | rts_24322 | C | R | rts. |
| 024324 | rts_24324 | C | R | rts. |
| 024326 | rts_24326 | C | R | rts. |
| 024328 | rts_24328 | C | R | rts. |
| 02432A | rts_2432a | C | R | rts. |
| 02432C | rts_2432c | C | R | rts. |
| 02432E | hitbox_pose_c | C | R | Six attempts (tables 0x243F8…0x243EC). |
| 024410 | hitbox_pose_d | C | R | Two attempts (0x24442, 0x24452). |
| 024460 | hitbox_pose_e | C | R | Four attempts (0x244C6…0x244EA). |
| 0244EE | ajuste_pose_lista | C | R | Looks up the current pose in the list (pose, dx, dz, flip) and applies dz to +0x14 and dx to x (with the sign according to the flip relative to +0xA). If it touches a limit (+0x9E&3≠0), restores only the z and keeps the x corrected by the limits routine. If it touches nothing, restores x and z, so it does not move (corrected: it previously said it undid x on colliding). With +0x19=0 calls 0x21E5A and with ≠0 0x21ED0. With +0x19 0=inside, this clashes with the names lim_fuera/lim_ring: UNCONFIRMED which one is backwards. C=0 if found, C=1 if not. |
| 024554 | ajuste_pose | C | R | Same with fixed dx/dz (d1/d2) and the flip in the 4 high bits of the list's pose. If it touches a limit (+0x9E&3≠0), restores only the z and keeps the x corrected by the limits routine. If it touches nothing, restores x and z, so it does not move (corrected: it previously said it undid x on colliding). With +0x19=0 calls 0x21E5A and with ≠0 0x21ED0. With +0x19 0=inside, this clashes with the names lim_fuera/lim_ring: UNCONFIRMED which one is backwards. C=0 if found. |
| 0245BE | secuencia_creditos_intro | C | R | 0x24C8/0x24E2/0x254E; 0x140200=0; sound 0x14 and 0x24B38. 4 pages with fg0 graphics 7–0xE and texts 0x29–0x31 (0x2549E), icons 0x7C00DC–DE. Transitions 0x24B54 and waits 0x453A of 0x260/0x240/0x240/0x240 frames. |
| 024B38 | pal_buffer_borrar | C | R | Clears the palette buffer 1C198A (0x78 words). |
| 024B54 | pal_fundido | C | R | 16 steps: brings closer (a3=0) or moves away (a3≠0) each RGB component of buffer 1C198A to palette 0x37D0/0x37F0/0x3810 by d2 at a time; dumps in the vblank (0x24C5C). |
| 024C5C | pal_volcar | C | R | Copies 1C198A to palette 140002 (8 rows of 15 colours). |
| 024C90 | marcador_inicio | C | R | Draws the two markers (0x80084/0x800C0) according to +0x2A bit3 of 1C0100/1C0334 (tables 0x24D86 CPU / 0x24D92 human); 1C186C=0x8000, 1C186A=1. |
| 024D36 | fg0_fila_3partes | C | R | Writes an fg0 row (palette 0x1F) of start, middle and end. |
| 024D9E | marcador_modo | C | R | For each side, if CPU (+0x2A bit3) draws nothing. Human: 0 (or 2 on side B) with bit1, 1 (or 3) without bit1; in mode 1C0026&0xF=1 uses 4, or 5 with bit5. Calls 0x24E20 (left) or 0x24E28 (right). |
| 024E20 | marcador_izq | C | R | Destination 0x80084. |
| 024E28 | fg0_bloque_2x4 | C | R | Writes 4 rows × 2 cells from table 0x24E62[d0*8] at 0x800C0 (palette 0x1F). |
| 024E92 | insert_coin_parpadeo | C | R | Per CPU side (bit3): blinking (0x24EBC). |
| 024EBC | parpadeo_texto | C | R | Alternates the text every 0x20/8 frames (table 0x24FB4 or 0x24FBC with credits) — e.g. "insert coin / press start". |
| 024F6C | blit_texto2 | C | R | Rows of tiles with attribute 0x1F. |
| 024F96 | fg0_borra_2x13 | C | R | Clears 2 rows of 13 cells (0x1FFF00). |
| 025050 | ptr_1c0890 | C | R | a0 = 1C0890 + scroll x. |
| 025064 | ocultar_cuerda_frente | C | R | 0x251D2, 0x251F0; for the wrestlers in action 4 or inside with y<0x140: 0x2509E. |
| 02509E | cuerda_frente_por_luchador | C | R | Chooses the width table by action (0x2535A → 0x25346): by action (0x252FE; the referee 1C0568 uses 0x25340), by sub +0x30 (0x25286) or by +0x44 (0x2523C). Marks the segments (16 pixels each between x 0x236 and 0x3B6) of array 1C155A that it covers; pose 0x3B/0x42 in the cases of state 7. |
| 0250C6 | cf_por_accion | C | R | Table 0x252FE[action] (the referee, 0x25340). |
| 0250E8 | cf_por_sub | C | R | Table 0x25286[+0x30&0x3F]. |
| 0250F8 | cf_por_44 | C | R | Table 0x2523C[+0x44]. |
| 0251D2 | cf_limpiar | C | R | Clears the active bit of the 23 segments of 1C155A. |
| 0251F0 | fg0_marcas_jugador | C | R | Sets tiles 0x39/0x3A (if 1C1895 bit0) and 0x40/0x41 (if 1C1897 bit0) in buffer 1C155A. |
| 02537C | cf_init | C | R | Creates the 23 segments of the front rope (1C155A, step 0x1E): x from 0x246 in steps of 16, y 0xE0, z 0xC0, pose 0x3B; the ends with poses 0x39/0x3A and 0x40/0x41 (posts). |
| 025402 | cf_extremos | C | R | Redoes the poses of the ends (0x253CE). |
| 025408 | cortinilla | C | R | Screen transition: fills layer 0x80000 with the tiles of table 0x25492 in steps (waiting 4 frames); when finished clears (0x25474) or 0x24E2 according to the direction. |
| 025474 | capa_80000_borrar | C | R | Fills 0x80000 with 0x1F0000 (empty). |
| 02549E | imprimir_texto | C | R | Prints string d0 (table 0x25600; with bit7, erases it with spaces). Format: attribute, aligned long destination and then characters; ASCII−0x20+d2 = tile. Codes <7 (table 0x2551A): 0 end, 1 new absolute destination, 2 relative destination, 3 attribute, 4 typewriter (pause of n frames per character), 5 end of pause, 6 tile offset d2. |
| 025536 | txt_fin | C | R | End. |
| 02553C | txt_destino_abs | C | R | Code 1: aligns and reads a new absolute destination (0x254C2). |
| 02553E | txt_reubicar | C | R | Destination += long. |
| 02554C | txt_atributo | C | R | New attribute. |
| 025558 | txt_pausa_on | C | R | Typewriter mode (d2 frames). |
| 025568 | txt_pausa_off | C | R | End of the mode. |
| 025570 | txt_desplaz_tile | C | R | Code 6: d2 (low) = next byte, which is added to each tile. |
| 0255A8 | capa_80000_marco | C | R | Clears rows 0 and 31 and the border columns of layer 0x80000. |
| 0255F4 | fg0_borra_n | C | R | Clears d0+1 fg0 cells. |
| 025B96 | datos_25b96 | C | R | Not code: table of 10-byte entries (0x0008, 0x08BC…), decoded by mistake. |
| 025DA2 | datos | C | R | False entry: data. |
| 026110 | frag_26110 | C | R | Data fragment decoded by mistake (no real entry). |
| 026120 | tilemap_fila_tabla | C | R | Writes a tilemap row: destination from 0x26166[d2] and source from 0x26176[d0], with the palette from 0x261B6[d1]. Format: length, initial tile (two bytes if d1=0) and consecutive tiles. |
| 0261BC | imprimir_numero | C | R | Prints the BCD number from table 0x26244[d0] (digits, destination, source) without leading zeros (0x26218). |
| 026218 | cifra_bcd | C | R | Digit → tile; leading zeros are output as a space. |
| 02626E | reloj_combate | C | R | Match clock (1C1850). On starting: draws the frame (0x265F6), the match music sound (0x6DD4), time = 0x708 adjusted by DIP 180003 bits 4–5 (0: 0x708, 1: +0x96, 2: −0x96, 3: −0x12C). Every 0x42 frames subtracts 0xA (tenths → 30:00 with the default value, shown as mm:ss with /0x3C). On reaching 0x12C (5:00): 1C1850 bit1, warning with command 0x70 (on the Z80 it does nothing: it only writes 0x821F, which nothing reads) and music 8 (hurry). With less than 0x12C colour 140036 blinks (bit2). At 0: 1C1850=1, text 0x9B ("TIME UP"), fg0 banner 0x2660E(0) and, according to the mode (1C0026&3, table 0x2653C), decides the result. |
| 026548 | tiempo_fin_1p | C | R | Time up with a human. If side A is CPU (+0x2A bit3 of 1C0100), 1C0BC2=0x4000 and 1C0BDA=0x8000; otherwise, the other way round. Sound 0x21 and wait of 0x10. What 0x4000/0x8000 mean (losing or winning): UNCONFIRMED. |
| 02657A | tiempo_fin_empate | C | R | Both with 0x8000 (draw/double loss); sound 0x21. |
| 0265A0 | celda_doble | C | R | Writes 2 cells (top/bottom) from table 0x265D2[d1] at destination 0x265E6[d2] (palette 0x10). |
| 02660E | cartel_fg0 | C | R | Large 2-row banner on the fg0 layer: clears 2×19 cells at 0x80720/0x807A0 and writes pattern 0x26696[d0] (length 0x26692[d0] = 0x12/0x10/0x10/0x1E bytes) as tile pairs 0x10xxxx (0x80D04 if d0=3). Called by: 0x1A64 (end of match), 0x16212 (submission, d0=1), 0x238A0 (title, d0=3), 0x26522 (time up, d0=0). It is not sound nor Z80. |
| 02EF54 | datos | C | R | False entry: data. |
| 02F00C | datos | C | R | False entry: data. |
| 02F068 | datos_2f068 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F070 | datos_2f070 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F106 | datos_2f106 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F14E | datos_2f14e | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F174 | datos | C | R | False entry: data. |
| 02F254 | datos_2f254 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F256 | datos_2f256 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F262 | datos_2f262 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F266 | datos_2f266 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F3C6 | datos_2f3c6 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F3EA | datos_2f3ea | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F40C | datos_2f40c | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F410 | datos_2f410 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F50A | datos_2f50a | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F51E | datos_2f51e | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F522 | datos_2f522 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F548 | datos_2f548 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F614 | datos_2f614 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F648 | datos_2f648 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F668 | datos_2f668 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F68E | datos_2f68e | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 02F6AC | datos | C | R | False entry: data. |
| 02F786 | datos_2f786 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6A8 | datos_3b6a8 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6B0 | datos_3b6b0 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6B8 | datos_3b6b8 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6C0 | datos_3b6c0 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6C8 | datos_3b6c8 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6D0 | datos_3b6d0 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6D8 | datos_3b6d8 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B6E0 | datos_3b6e0 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
| 03B7C6 | datos_3b7c6 | C | R | Not code: data (sprite/pointer tables) that the linear seed decoded as instructions (ori.b #xx,d3 = 0x0003xxxx = pointers to 0x3xxxx). Read and discarded as code. |
