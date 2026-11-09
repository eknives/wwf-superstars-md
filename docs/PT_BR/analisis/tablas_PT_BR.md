# Tabelas da ROM
| Dir | Conteúdo | C/P |
|---|---|---|
| 0x1F450 | 9 modos de jogo (0x1F434) | C |
| 0x21C4 | seleção de rival por nível | C |
| 0x3DEA | modo de movimento (+1) | C |
| 0x3EC4… | 8 octantes de polar→xy | C |
| 0x6CD8 | poses de sprite | P |
| 0x7340, 0x805A, 0x828E | despachos por modo | C |
| 0x7686/0x78CA | retratos | P |
| 0x7D6A | barras de energia | P |
| 0x7FE2 | id de seleção → id de lutador | P |
| 0x7FEC/0x8190 | índices de energia humano/CPU por nível | C |
| 0x8AB0 | textos por nível | P |
| 0x8CE2 | 33 ações (+0x2D) | C |
| 0xAF66 | deitado (lieTab) | C |
| 0xBCB8 | objetos extras a desenhar | C |
| 0xEA4C | ponteiros para os 4 lutadores | C |

## Acrescentados no marco de 25 %
- 0xA74A: parâmetros por subação de "receber" (+0x44); 0x9A14: tabela de saltos das subações; 0x9E38/0x9E42: som e pose de rolar.
- 0xAF66: tempo no chão segundo a energia; 0xAF6A: pressionamentos para levantar; 0xAF72: limiar da contagem para escapar do pin; 0xAF76: subações aéreas do rival (lista que termina em 0xFF); 0xAF82/0xAF96: probabilidade de esquivar por nível/energia.
- 0xAA00: tempo para levantar; 0xAA10/0xAA20: subida ao poste da CPU (ação e probabilidade por id).
- 0xAFF4: sorteio da CPU por nível; 0xB0EA: poses para erguer; 0xB162: provocar; 0xB46C/0xB468: disputa de força.

## Acrescentados no marco de 50 %
- 0x14346 / 0x143AA: probabilidade de agarre para o humano / a CPU por nível (+5 se DIP 0x180002 bit3=0). 0xB74A: vencedor da disputa de força.
- 0xD54C/0xD646: entrada no ringue. 0x1C26E/0x1C2AA e 0x1C3F6/0x1C432: passos de saída/entrada pelas cordas (normal / id 7).
- Chaves: 0x14A82, 0x14C5C, 0x154BC/0x154AE, 0x15E7A/0x15EB2/0x15EE2/0x15F12, 0x1464E (contra mútuo), 0x15944/0x15960/0x1597C (golpe rápido).
- IA: 0x18F16 (despacho por +0x5C), 0x18F92, 0x1A554, 0x1AFA8, 0x1B938/0x1B8F4, 0x1C028 (descritores de 6 bytes), 0x1D18E (atrasos), 0x1D33A/0x1DD7E (intenções), 0x1D2FA/0x1D31A (máscaras), 0x1D2B8 (remapeamento), 0x1D2B0, 0x1E1A6/0x1E392/0x1E14E/0x1E19A, 0x1E55E/0x1E74A/0x1E55A, 0x1E8EC.
- Gráficos: 0x1F706/0x1F726 (colunas de fundo), 0x23AC4 (gráficos fg0), 0x22760/0x22640 (geometria RLE), 0x23170 (público), 0x2237A/0x22392/0x223FA (sombra/corda), 0x216A6/0x2146E (retratos), 0x23536/0x2354E (versus), 0x26166/0x26176/0x261B6, 0x265D2/0x265E6, 0x26692/0x26696, 0x2535A.

## Acrescentados no marco de 75 %

**Caixas de golpe e dano**
- 0x1761E: tabela de caixas por pose (lista por frame); 0x18076 para a pose −1.
- 0x172FA: índice de reação por pose da vítima (0xFF = não golpeável).
- 0x1636C: filtro de impacto por ação.
- 0x1642A: dano extra ao deitado por sub.
- 0x164FA: golpes fortes por sub (0xFF).
- 0x175CE: som por sub.
- 0x17590: combo por sub.

**Listas**
- 0x16B20 / 0x16BCC: listas de ações (terminadas em 0xFF).
- 0xEA4C: lista dos 4 lutadores.

**Agarre, submissão e disputa de força**
- 0x124D6: limiar de escape da submissão por dificuldade.
- 0x149A2 / 0x149AA: durações e poses da submissão.
- 0x150E0: tempo da CPU na disputa de força.
- 0x150F6 / 0x150F0: poses e durações da disputa de força.
- 0x15126: sub por id e botão.
- 0x14FD8 / 0x14FE0 / 0x14FE8: contra do humano.

**Chaves (indexadas pelo id do rival)**
- 0x1310C, 0x132B8, 0x134CC, 0x13938 / 0x13956 / 0x13918, 0x13E44, 0x14108 / 0x14124, 0x14378 / 0x143DC, 0x1465E / 0x14676, 0x14DD0, 0xB46C / 0xB468, 0x155EA, 0x156C8, 0x15692 (bra), 0x15FFC.

**Outras**
- 0x15B70: z de destino por zona própria/do rival.
- 0x15BE4: probabilidade de provocação da CPU por id.
- 0x1576E / 0x15860 / 0x15878: combos da CPU.
- 0x160CC: avanço ao entrar no ringue.
- 0x16286: deslocamentos do tremor.
