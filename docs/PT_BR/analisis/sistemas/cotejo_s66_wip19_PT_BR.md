# Contraste arcade ↔ s66 wip19 (só leitura; correção na wip21)
| Caso | Arcade | s66 wip19 | Afeta hoje (Duggan vs Warrior + árbitro)? |
|---|---|---|---|
| 0x22040 dano da grade | Dano 5 salvo ação 8 com +0x45≠0xA | Invertido na ação 8 (linha 155) | Não: só é chamado com ação 0. Corrigido na wip21 (ROM idêntica) |
| 0x23406 início público-grade | bit6, ou bit7 com 1C1890≠1 | bit7 com zona==1 (invertido) | Não: CA_FENCE só a partir de w22040, nunca dispara. Corrigi-lo exige listas de zonas 0/2 (decisão) |
| 0x230FC desenho público-grade | Só com 1C1890≠1 e 1C182C=0 | Só com zona 1 (invertido) | Não (mesmo motivo) |
| Pin #1 kick-out | Próprio (martelar / CPU por energia e contagem) + sorteio 0x11BC6 + parceiro | 1.º pin sempre sai; depois sorteio | Sim. Decisão de design |
| Pin #2 energia 0 | CPU com 0 nunca sai; humano 0x30 pressionamentos | 13/16 contagem de 3 | Sim. Decisão |
| Pin #5 lieBand CPU | máx 0x8190/4 | e/12 | Sim se a máxima ≠48 (V) |
| Pin #8 CPU deitada /2 | 0xAB1E /2 e +0x20 | Não | Sim. Decisão |
| #6 energia inicial CPU 55 | Não lido | 55 | V |
| #7 / 0x1D1A8 / 0x1D0E2 / 0x1AE44 / 0x1B120 / 0x1BEE4 IA | Planejador por tabelas (com o erro de 0x1D0E2) | IA provisória própria | Sim (regra IA). Portar o planejador = decisão |
| #9 relógio / 0x26548 | 30:00, pressa 5:00, TIME UP | Falta | Sim. Decisão |
| #10 contagem fora / dupla DQ | Até 20 | Falta | Sim. Decisão |
| #11 som | Driver Z80/OKI | Falta | Sim. Fora do escopo |
| #12 RNG 0x450A | Soma de registradores | random() compartilhado | Aceito pelo Emilio (wip19) |
| 0x244EE/0x24554 ajuste de pose | Restauração x/z | Não portado (sem referências) | Não |
| 0x2549E textos / 0x21A4E | Motor de texto RLE | Textos próprios | Não (sem DiBiase) |
| 0x73E8 escolha ao acaso | mod 6 com nova tentativa | Sem seleção | Não |
| 0x19D96 / 0x1B7FA / 0x1B88C revezamento/tag | Parceiro | Sem parceiro | Não (nota) |
| André/DiBiase/Honky/Bossman (0x134D2, 0x14222, 0x13CD0, 0x169C2, 0x1578E, 0x1907C, 0x1AB34, 0x1B942, 0x1C180/0x1C306, 0x16488 som 0x23, 0x1A6B6, 0x1CDA4, 0x1CB16, 0x1C726, 0x13114) | Lógica própria | Não portados | Não: anotar ao portá-los |
