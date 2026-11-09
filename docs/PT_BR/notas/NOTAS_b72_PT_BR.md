# b72 (base b71, md5 dbfe401359b8f726186dd01e82cd5b2c; b71 intacta)

ROM: `wwf_b72.bin`, md5 `74c37dc8839ec8780a122eabfc71a58d`

## O que olhei no arcade
- 0xBD10 / tabela 0xBEF2: quem cobre se coloca no x do rival ± d (Duggan sobre Warrior 36, Warrior sobre Duggan 32), com o y do rival −1. As trilhas da b71 já terminavam em 36 e 32, então o posicionamento no centro do ringue era o do arcade. O erro da captura era **a corda**.
- 0xACA4 + 0x21E5A: ao cair, o arcade confere o corpo deitado (de x−8 a x+48) contra os limites do ringue. 0x1190C e 0x11A72 só cobrem se o rival está deitado **dentro** e quem cobre não está fora.
- 0xDEE4 + 0xDA38 + tabela 0xDB04: na contagem fora, o árbitro olha para quem está fora e usa as poses de contar 0xA-0x11, 4 poses de 8 ticks. Soma 1 a cada volta (64 f).

## Mudanças
1. **Cordas: nem pin nem salto.** Só é possível cobrir (B colado) ou saltar (B mais longe) se três coisas se cumprem: o atacante não está contra as cordas; o corpo deitado, com seus pixels reais (pose 114 com lyo), está inteiro dentro; e o lugar onde se coloca quem cobre também está dentro. Se não se cumprem, B é o chute normal.
2. **O árbitro não conta atravessando as cordas.** O pin só começa se as posições do árbitro na trilha (ao se jogar e ao bater) caem dentro do ringue com sua margem. Se não cabe atrás, ele se coloca na frente do corpo.
3. **Contagem fora como no arcade.** O árbitro faz o gesto de contar: poses do arcade 0xA-0x11 importadas como 757-764 (757-760 de frente, 761-764 de costas), uma pose a cada 16 f e olhando para quem está fora. Os números são **grandes e vermelhos**, de 16×40, no estilo da contagem de 3. 1, 2 e 3 são os originais; o resto foi composto com seus segmentos (`tools_dig72.py` → `res/big_dig.bin`). Com dois algarismos, as dezenas vão nos tiles 1779 e as unidades nos 1525.

## Sem mexer
Não há IA: o outro só persegue com START. Os controles são os mesmos (C troca, START persegue, A/B como na b71). Também não foram mexidos os córneres de cima, o logo WWF nem as paletas.

## Limites
- A forma dos números 0 e 4-9 é uma reconstrução com os segmentos do 2 e do 3, não uma captura do arcade.
- À pose 764 do árbitro faltam 2 linhas da mão: o árbitro tem um limite de 41 tiles.
- Não faço o empurrão do arcade que afasta o corpo das cordas ao cair (0xACA4). Aqui, perto das cordas, simplesmente não se pode cobrir.
- Continua sem haver vozes na contagem (no arcade, a contagem fora é muda).

## Testes (MAME, test/t72.lua; T72X=780 coloca a luta no centro)
pinC: pin no centro (contagem 1, 2, 3 e reset). pinR: perto da corda esquerda não cobre. ro: gestos e 1/2/10/20 grandes, e reset. jumpC/jumpR: salto do Warrior. Capturas em shots/ (hoja_b72.png).
