# Pin e contagem

## Início
- Cobrir = ação 0x17 (0xBD10). É posta por 0x1190C, 0x11A72 e 0x12972.
- Ao mesmo tempo marcam o rival com +0x18 bit5, e isso passa o árbitro ao estado 2.
- Ao terminar a contagem, o coberto passa para a ação 0x19 (rolar, 0x12B00).

## Tempo no chão: ação 0xB (0xAB1E)
- +0x38 = tabela 0xAF66[faixa] = 112 / 82 / 54 / 22 ticks. Cada tick são 2 frames, então dura 224 / 164 / 108 / 44 frames.
- Faixa (0x1CE9C) = energia / (máxima/4), limitada a 3:
  - Humano: máxima 48 (0x7FEC).
  - CPU: máxima da tabela 0x8190[nível*8 + vaga].
- CPU: o tempo é dividido por 2 se 0x1CD80 dá CS (+0xF6 >= 0x1CD48[id], medidor alto) ou se +0xF9 bit0.
- +0x20 se vinha de fora do ringue.
- Martelar botões (0xAD12, limiar 0xAF6A = 24 / 10 / 6 / 3) → ação 0x19.

## Saída do pin: kick-out próprio, ação 0x1E
- **Humano (0xADEA):** o limiar é AF72[energia]/2; os pressionamentos durante a contagem o libertam.
- **CPU (0xAE7E):** nível d1 de 0xAF26:

  | Energia | d1 |
  |---|---|
  | ≥ 0x36 | 0 |
  | ≥ 0x30 | 1 |
  | ≥ 0x24 | 2 |
  | ≥ 0x19 | 3 |
  | ≥ 0xE | 4 |
  | > 0 | 5 |
  | 0 | 6: nunca sai |

  Sai quando contagem*2 + paridade ≥ d1 (mais condições dos frames do árbitro).
- **Kick-out imediato (0x11BC6):** sorteio contra a tabela 0x11C30[dificuldade*3 + 0x1CEF4].

## Salvamento do parceiro (0x129A4)
- Não há salvamento se o coberto tem energia 0, ou se o parceiro não pode (3/16 de probabilidade).
- A CPU acode com o estado 0xF (0x1B486).
