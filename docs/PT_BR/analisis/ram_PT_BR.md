# Mapa de RAM / hardware
Hardware (C, MAME wwfsstar.cpp): ROM 0-3FFFF; fg0 080000; bg0 0C0000; sprites 100000; paleta 140000; DSW 180000/2; P1 180004; P2 180006; SYSTEM 180008 (bit0 vblank); latch de som escrevendo em 180008 (byte 180009); scroll 180004/6 (escrita); flip 18000A. RAM 1C0000-1C3FFF. As notas antigas que dizem "FFxxxx" referem-se a 1Cxxxx.
| Dir | Uso | C/P |
|---|---|---|
| 1C0000/1C0002 | deslocamento de sprites x/y | P |
| 1C001A | modo demo/attract | P |
| 1C0016 | créditos | P |
| 1C0026 | modo de jogo (bits 0-1: jogadores/equipes) | P |
| 1C0027 | atribuição de controles (bit0) | P |
| 1C0028 | nível de dificuldade / índice da tabela 0x8190 | C |
| 1C0029 | nº do combate (4 e 9 são especiais; 9 = final) | P |
| 1C002A/1C002E | câmera x/y | P |
| 1C003A | semente do RNG 0x450A | C |
| 1C0042 | máscara de recarga de paletas | C |
| 1C006A-1C0095 | estado da tela de seleção | P |
| 1C00A2 | tabela de 6 rivais (bit15 = usado) | P |
| 1C0100, 1C021A, 1C0334, 1C044E | 4 lutadores (passo 0x11A; os ponteiros estão na ROM 0xEA4C) | C |
| 1C0568, 1C0682, 1C078E, 1C089A | objetos extras | P |
| 1C0AB2 | árbitro | P |
| 1C0BC2/1C0BDA | flags de energia | P |
| 1C1814 | tabela de tradução de entrada | P |
| 1C1854 | efeito de grade do público | C (segundo as notas) |
| 1C18C4 | fila de escritas adiadas (32) | C |
| 1C1A7A | 6 flags de placar | P |
| 1C1AB0 | buffer de sprites (10 B cada, contador 1C208C, máx 0x4B) | C |
| 1C2094 | lista de desenho | C |
Os campos de objeto (+0 … +0xFA) estão em sistemas/luchadores.md.

## Acrescentados no marco de 25 % (lido inteiro)
- Lutador +0x19: 1 = fora do ringue (chão z 0x80; dentro, 0xBB). +0x38: tempo no chão. +0x34: pressionamentos ao levantar. +0x114/+0x116: pressionamentos/direção do humano. +0xFF: contador de disputas de força. +0xD6 bit7: o rival está deitado e pode ser coberto. +0x18 bit5: está coberto (pin).
- Objeto 1C0568 (contagem do pin): +0x2D=1C0595 (modo; 2 = contagem final), +0x2F=1C0597 (número da contagem), 1C059E, 1C059F, 1C05A5 bit2 (contagem em andamento), 1C0570 (subcontador). Que seja o árbitro está NÃO CONFIRMADO, porque ainda não se leu sua rotina.
- 1C0AB2: um objeto que se desativa (bit7) nas ações 0x99BE e 0xB012. NÃO se confirma que seja o árbitro.
- 1C1858 / 1C185A: são postos a 0x81 (0x80 com o id 7) nas quedas e arremessos. Efeito NÃO CONFIRMADO.

## Acrescentados no marco de 50 %
- 1C185A: mensagem piscante fg0 (textos 0x1E/0x1F com 0x23A28; apaga-se em 0x80B04). Ativa-o 0xB012 com 0x81. CONFIRMADO.
- 1C00B4: alvo escolhido pela CPU (0xF4DA).
- 1C1852: contador de combate; a dificuldade da IA (0x1CEF4) vale 0 até ≥0x258 (0x1D1A8).
- 1C1890/1C1891/1C1892: coluna de fundo atual e estado das células fixas (0x1F5C8). 1C1860/62/66: cópia de tilemap dividida em dois frames.
- 1C182C: último comando de fundo (0x1F434). 1C182D≠0: congela o scroll de colunas.
- 1C1854 bit4 / 1C1856 / 1C1857: animação do público (0x230FC).
- 1C1894/1C1896: seletor das poses de sombra/corda por lado (0x222D6). 1C1895/1C1897 bit0: marcas de jogador (0x251F0).
- 1C183E bit7: ativado pelas chaves (0x105DC, 0x13A46, 0x149B0…). Significado NÃO CONFIRMADO (não se leu quem o consome).
- Lutador: +0xCC/+0xCD/+0xDC/+0xDD sequências de agarre; +0xFC=1 força uma falha; +0x5C/+0x5D estado da IA; +0x2E/+0x2F intenção; +0x30/+0x31 sub da chave; +0xF3 atraso da IA; +0xC6/+0xC7 sorteio tag; +0xCA pose vista; +0x104 marca de chave no chão; +0x106 primeira vez em tag; +0xF6 contador +3 por chave.

## Acrescentados no marco de 75 %
- 1C0568: árbitro; estados em 0xD7D8 (0 seguir, 1 vigiar, 2 contagem de pin até 3, 3 contagem fora em BCD até 20).
- 1C05D0: bloco auxiliar do árbitro.
- 1C0BBE / 1C0BD6: estruturas de resultado por lado. Em +4 (1C0BC2 / 1C0BDA): 0x40 / 0x80 (bits 6/7 = quem ganha ou perde). São escritas na rendição (0x1481C) e no pin.
- 1C0682 / 1C078E / 1C089A: objetos (stride 0x10C).
- 1C1820 / 1C1821 / 1C1823: estado dos objetos.
- 1C00B4: bloco de trajetória do salto (calculado por 0x159AC). +0/+2 dx, +4 dy, +8 vz, +0xA gravidade, +0xC/+0xE máximos de vx/vy, +0x10 alvo (−1 = ponto fixo +0x16/+0x18), +0x14 z de destino.
- 1C0AB2 / 1C144E: efeitos.
- 1C183E: flag de impacto de chave (posta nos passos de força).
- 1C185A: estado da chave de submissão (0xC0 ativa, 0xC1 escapada).
- 1C1858 / 1C1859: tremor de tela. Bit7 = pedir; 0x81 = curto (3 frames), se não 9. Bit6 = em curso; 1C1859 conta os frames. Soma a tabela 0x16286 a 1C002E (scroll).
- Campos do lutador confirmados:
  - +0x3C energia; +0x3E dano (0x16488 subtrai).
  - +0x40 reação pendente do golpe (−1 nenhuma, −2 agarre, −4 especial).
  - +0x46/+0x48 temporizador/acumulador do combo.
  - +0xC9 bit0 golpeado, bit3 conectou, bit4 agarrado, bit5 golpes anulados.
  - +0xCE máscara de vítimas já golpeadas com a pose atual; +0x42 pose anterior.
  - +0xF0 bit7 golpe forte; +0xF6 acumulador da CPU.
  - +0x28/+0xDE tempos da disputa de força.
