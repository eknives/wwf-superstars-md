# b87 — candidata; NÃO afirmar igualdade completa com o arcade
ROM: `wwf_b87.bin` — MD5 `f956cfbcbf5012f63d66c8b0ac457a0d`. Base b86 intacta (MD5 `0cbe0756ba9ff3dff97b4acfaa8a76b8`).

## 1. Socos — verificado no emulador
- FC84/FD04: o temporizador é consumido em ticks de dois refrescos. FD70/FD7C = 4/3/3 **ticks**, não frames MD. FCAC: início 3 ticks. FD2E/FD48: decisão/recuperação e ligação com temporizador 1. FCFC: só bordas novas com +36=0xC (0xB não é alcançado com incrementos de 4).
- O MAME mede 17,408 ms/refresco arcade (57,44485 Hz): tick=34,816 ms. Relógio por VBlank real: 3125/6528 ticks/frame NTSC; 3125/5440 PAL. Não se tornam mais lentos outros movimentos.
- NTSC, ambos: 150/151/152 = 9/6/8 frames visíveis na fase testada; os últimos 8 incluem 6 de animação + 2 de recuperação. Outro meio combo: 9/6/8. PAL: 7/5/7. Manter A NÃO encadeia; novo pressionamento SIM. A quantização pode variar um frame conforme a fase do relógio.

## 2. Clothesline — contato verificado; cobertura do arcade incompleta
- 12E7A/1302E: 1D0/1D1/1DA/1DB, e contato 1D2+id do rival durante 8 ticks; saída E/F. 12F04 detém o X durante a captura; 12FAA arremessa o rival depois, não ao tocá-lo.
- 16634 usa coordenadas +C/+10 em pixels: |dx|<96, |dy|<8; NÃO é uma caixa de impacto. 1672C/16C60/16CA8: caixas 18C2A (-20,12,48,16) e 18B82 (-16,28,0,72); defesa em pé 18B02 (-8,16,0,80). Ativas 1D1 e 1DA. Velocidade herdada: 6,75 px/tick; depois 4 px/tick (12F76).
- A b86 DISPAROU sim o hit no MAME, mas a 64 px e antes do contato visual: afastava o rival com o escape do pin. Não era um condicional morto. Esse impacto prematuro foi eliminado.
- PASS: Duggan/Warrior, esquerda/direita; contato 1D1; contato tardio 1DA; separação Y=20 NÃO golpeia.
- **Pendente para igualdade completa:** caixas da vítima em outras poses/correndo (hittable ainda exclui a corrida), variantes pelas costas e contra as cordas. A caixa de defesa atual é a de pé: não apresentá-la como motor completo 16796.

## 3. Reação 0x17 — voo/rebote/pose final verificados
- 9B9A/9BBE/A8BE/2964: deslocamento inicial +/-32 px, altura +24, vx=+/-0x80, vz=0x100, gravidade=0x30. 3E20: posição +=2*v, depois vz-=2*g. 9E4C: pose 15 até altura 24 ao descer; depois 16. 9C94 -> A4C8: rebote sem velocidade X; ABBC: pose final 17.
- Conserva-se a fração vertical quando 9C44/A530 escrevem só a palavra inteira. Alturas por tick medidas: 213,214,214,214,213,211,209,206,202,197,191,187 / 189,190,191,191,190,188,187: iguais ao MAME arcade.
- Gráficos novos do arcade só por acréscimo: poses 799..820, motores 627..637. Os dados e mapas gráficos anteriores permanecem como prefixos idênticos; logo WWF e córneres não foram mexidos.
- **Limite:** o deitado posterior usa 22 ticks (AF66, faixa sã); não reproduz todas as faixas de energia do arcade. A transição contra a corda conserva a queda anterior do port.

## Ritmo/lentidão e evidência
- b86: 40 avanços do Clothesline ocuparam 42 refrescos MD (2 sem avanço). b87 sem impacto: 43 refrescos, dos quais 42 são poses (11/8/8/15): ~700 ms frente a 40 refrescos arcade=696,32 ms. Não se observou perda de laço nesse caso.
- No impacto b87: direita Duggan 0 perdas; Warrior 1; esquerda 4. Existe lag residual de render/laço; não se isolou CPU frente a DMA. O relógio destes movimentos usa o VBlank decorrido para não acumular lentidão por essas perdas. **Não afirmar que todos os frames perdidos foram eliminados.**
- Oito ensaios curtos MAME Genesis/PAL, entrada A+B -> corrida -> novo A; a RAM só coloca lutadores/controle para repetir o caso. CSV, scripts e asserções: `verify/`; resumo `verify/RESULTADO_b87.txt`. Arcade real emulado: `verify/arcnatural.log`, contato sem forçar flags; `arc87.log` para soco/temporizador. Capturas: `shots87/DR_contact.png`, `DR_catch.png`, `DR_flight.png`, `DR_bounce.png`, `DR_land.png`, equivalentes WR/DL/WL.
- O driver do MAME diz HTOTAL/VTOTAL estimados: não há medição de placa arcade física nem teste desta candidata no Everdrive.

**Resultado: candidata testada nos casos descritos, NÃO é entrega final de «idêntico ao arcade» pelos limites anteriores.**
