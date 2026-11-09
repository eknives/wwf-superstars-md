# b95 — corrida por tick do arcade, streaming do fundo por DMA, choque contra a corda (base b94)

ROM `wwf_b95.bin`, MD5 **7be789d70d892c1efb86af8630b296a6** (b94 b2a8ff5d4453067ad3d2bf8762239413 intacta). Só os 3 pontos autorizados (9-11-2026 9:32).

## Mudanças
1. **Corrida** (`main.c` 192, 866–871, 878):
   - Velocidade por lutador da tabela `0x95BC` (`945C` → +0x21): Warrior 28, Duggan 27. `3DF0`: vel/4 px por tick.
   - Um passo por `arcTick` (relógio arcade 28,72 Hz, NTSC e PAL), antes `tick&1`.
   - Pose a cada 2 `arcTick` (`94CE`, tabela `0x95C4`).
   - Sem mexer: andar, rebote rn 2 (trilha 48 f), freio, clothesline e arranque de 3 frames (anotado em PENDIENTES).
2. **Fundo por DMA em fila** (`main.c` 211–240, 1553–1584):
   - Tile ROM→VRAM, BG_B e BG_A de cada coluna/linha vão para a fila DMA. São descarregados no vblank (`SYS_doVBlankProcess`) antes do scroll novo, então a coluna aparece completa no mesmo frame que na b94.
   - Orçamento `ST_BUD` de 40 tiles/frame. Se for superado (salto de câmera), esvazia-se a fila sem perder a ordem.
   - O público (`caApply`, CPU) e as cordas (`ropeDraw`) são calculados antes do streaming, com o mesmo resultado.
   - Não foi preciso repartir uma coluna em vários frames: o custo estava nas escritas da CPU no VDP com a tela ativa (medido ~870 ciclos por célula BG_A e ~0,2 frame pelos tiles).
3. **Choque contra a corda** (`main.c` 530–595, 669–672):
   - **9E78**: a cada tick testa X±0x10 para onde voa, com os limites de `21E5A`/`22140` (esq. X ≤ 616+e, dir. X > 920−e). Se toca, X = limite ∓ 0x10; com z ≥ 0xDB não recorta (`21E7A`).
   - **9CD0**: o `cmpi.b #$1c,$44` compara o byte alto, então qualquer contato passa para sub 2. Erro do arcade copiado.
   - Se o contato ocorre no mesmo tick da aterrissagem: `9C94`, sub 0xC sem ∓0x20 (caso Xv728 → 643).
   - **9F02**, no tick seguinte:
     - marca a corda (vibra, `9700` d0=1);
     - z ≥ 0xCB e pose 0x16;
     - `27D2` índice 0x11 (tabela 0x2934: vx 0x100, vz 0, g 0x10), com Vx para dentro;
     - aterrissa quando z < 0xBB → deitado (ação 0xB).
   - O som 0x29 da aterrissagem (`25E6`) não existe no port e não é acrescentado. O "0x11" de 9F02 é parâmetro de movimento, não um som.
   - `9C5A` ∓0x20 sem clamp.
   - **soilNudge** usa `oriVictima` (vface^1) como bit7 de `ACA4`.
     - Chamadas 875/893 (derrube por golpes): revisadas; põem `vface = atacante à direita`, a convenção da b93, então `oriVictima` é o bit7 do arcade.
     - A chamada da aterrissagem (fs) também se encaixa na convenção.

## Verificado (MAME 0.276; genesis = NTSC, megadriv = PAL; arcade wwfsstar)
- **Corrida** px/s, ida e volta (`shots95/md/b95_{genesis,megadriv}_run.csv`):

  | | Warrior | Duggan |
  |---|---|---|
  | arcade | 201,1 | 193,9 |
  | b95 NTSC | 200,5 / 200,6 | 194,0 / 193,9 |
  | b95 PAL | 199,7 / 200,1 | 192,6 / 193,0 |
  | b94 PAL | 167,7 | 167,7 |
  | b94 NTSC | 201,5 / 202,3 | 199,7 / 196,7 |

  - Mudanças de pose: b95 14,0–14,8/s em NTSC e 14,1–14,3 em PAL (arcade 14,36; b94 PAL 12,1–12,4).
  - Rebote ao chegar à corda (906/627) e volta: OK em NTSC e PAL.
- **Frames perdidos andando em diagonal até cada poste** (580 frames; `b9x_post.csv`):

  | | sup. esq. | sup. dir. | inf. esq. | inf. dir. |
  |---|---|---|---|---|
  | b94 | 20 | 14 | 18 | 19 |
  | b95 | 3 | 2 | 1 | 0 |
  | b94, máx. em 59 frames | 10 | 6 | 12 | 10 |
  | b95, máx. em 59 frames | 2 | 1 | 1 | 0 |

  - Este script mede 10/59 e 12/59 na b94; o "8/59" da investigação era outra janela.
  - **Fundo**: a cada frame lê-se a VRAM (nametable BG_B + tile) das colunas e linhas da borda, e a janela inteira a cada 16 frames. Compara-se com W/ROM: 0 erros em cerca de 100.000 células por caso, na b94 e na b95.
  - Controle negativo (b95 sem DMA de tiles): 67.667 erros, então a verificação de fato detecta falhas.
  - A zona visível fica sempre dentro da janela carregada.
  - 6 capturas estáticas (centro e 4 postes) idênticas pixel a pixel à b94, cordas incluídas.
- **Escapar do pin perto da corda** (X final de quem cobria):

  | Xv | arcade | b94 | b95 |
  |---|---|---|---|
  | 760 | 642 | 675 | 642 |
  | 728 | 643 | 675 | 643 |
  | 708 | 677 | 675 | 677 |
  | 693 | 677 | 675 | 677 |
  | 832 | 859 | 858 | 859 |

  - b95 = arcade nos 5. Choque com a corda vibrando, pose 0x16, 17 ticks e +2 px/tick como no arcade.
  - Captura: `shots95/clave1_choque_cuerda_arcade_b94_b95.png`.
- **Regressão**:
  - **Sair do ringue**: sx 0→1→2 nos mesmos X que a b94, W e D, ambos os lados.
  - **Clothesline** DR/DL/WR/WL: contato, agarre, voo, quique e deitado, com 0 erros de tiles. A vítima termina igual à b94 (746/784); o atacante faz contato 6–8 px mais longe porque a corrida agora vai por tick.
  - **Pin**: 26 estados de cobrir iguais à b94 em 6 casos; escapar em 4 casos; a contagem de 3 funciona.
  - **Sub 1 contra a corda** (fixture do port): rebate para dentro (W 627→659, D 906→874). Na b94 saltava 48 px.

## Não verificado / limites
- Console real / Everdrive. O DMA a partir da ROM com o Z80 PCM ativo é o mesmo padrão de `fLoad`.
- Sub 1 contra a corda (arremessos, clothesline na corda) e derrube por golpes junto à corda: não medidos no MAME arcade. Só se seguiu o código de 9F02/ACA4.
- `arcTick` dá no máximo 1 tick por volta: com frames perdidos a corrida perde ~0,3–0,7 %.
- A queda da ação 8 (fs) continua avançando a cada 2 voltas (`fsTick`), não por `arcTick`: com frames perdidos dura mais (Xv708: 17 ticks em 40 frames).
- Correndo entre cordas restam 40/580 frames perdidos (b94: 55). Causa não investigada; não é o streaming.
- O limite direito de 9E78 usa 920−e (arcade); o `RING_XR` 917 global do port não muda.
