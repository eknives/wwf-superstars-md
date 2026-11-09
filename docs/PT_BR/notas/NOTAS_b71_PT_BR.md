# b71 (base b70, md5 24854415d3674c5e784b99ea9f7cc8da; b70 intacta)

ROM: `wwf_b71.bin`, md5 `dbfe401359b8f726186dd01e82cd5b2c`

## Mudanças (só as 4 pedidas)
1. **Contagem de 3 (pin) para os dois.** Com o rival deitado, **B colado ao corpo (a menos de 24 px)** = cobrir, como o B2 do arcade (ação 0x06/0x17). O Duggan cobre com suas poses (494-499) e o Warrior com as dele (513-515). O árbitro se joga no chão e bate com as trilhas do arcade (500-506). O número grande 1/2/3 aparece em +94/+194/+294, como no arcade. Se chega a 3, a luta é reiniciada 2 s depois.
2. **Escapa sozinho só na 1.ª contagem.** No primeiro pin de cada lutador, depois do "1" (arcade +128 Duggan / +136 Warrior), quem cobre sai e se afasta 40 px, e o deitado se levanta (pose 115). O árbitro se levanta (507-509) e volta a seguir. A partir do 2.º pin, a contagem chega a 3.
3. **Contagem de 20 fora do ringue.** Enquanto algum está fora (lateral ou atrás), o árbitro conta 1…20, somando 1 a cada 64 frames (arcade 0xDEE4/0xDA38: 4 passos × 8 ticks de 2 f). Se os dois voltam para dentro, a contagem é apagada. Se chega a 20, a luta é reiniciada 2 s depois.
4. **Salto do Warrior sobre o rival completo.** Antes usava as poses do Duggan traduzidas, e da 547 à 554 aparecia o Warrior em pé. Agora usa seu golpe real do arcade, 0x0C (trilha S0C da s62, poses próprias 569-573 e depois 277/483/72): sobe, cai de joelhos sobre o corpo (impacto em f40) e se levanta. É ativado com B a 24-100 px do corpo, igual a antes. O salto do Duggan (0x11) não foi mexido.

**Reset da luta:** os dois voltam à posição de saída e sem dano, e o árbitro ao seu lugar. O console não é reiniciado. Mantêm-se C (quem você controla) e START (perseguição). A câmera volta com seu passo normal.

## Sem mexer
Não há IA de ataque: o que você não controla só persegue com START. Os controles são os mesmos: B perto do corpo cobre, B mais longe salta e A dá a cotovelada. Também não foram mexidos os gráficos dos córneres de cima, o logo WWF nem as paletas. Os números usam a PAL0 do fundo.

## VRAM
- Número grande: tiles 1525-1534.
- Números da contagem fora: tiles 1779-1788. As duas zonas estavam livres.

## Limites
- Durante a contagem fora, o árbitro não faz o gesto de contar do arcade: continua andando como antes. Só se vê o número pequeno (8×8), e não há vozes 1-2-3.
- O arcade decide o kickout por energia/apertar botões. Aqui, a pedido do Emilio, sempre se escapa do 1.º pin e os seguintes sempre chegam a 3.
- O kickout é a cobertura ao contrário mais um deslocamento de 40 px (aproximação da s41). No arcade, o parceiro entra.
- O rival deitado tem que estar na fase de barriga para cima (pose 114) para cobri-lo ou saltar sobre ele.

## Testes (MAME, test/t71.lua, modos pin / jump / ro com T71=…)
Capturas em shots/: 01-04 pin 1 (cobre, "1", sai, levanta), 05-08 pin 2 (1, 2, 3 e reset), 10-16 salto do Warrior, 20-24 contagem fora (1, 2, 10, 20 e reset). As folhas são hoja_*.png.
