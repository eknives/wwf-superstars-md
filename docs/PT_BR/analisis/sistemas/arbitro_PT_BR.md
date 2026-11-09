# Árbitro (objeto 1C0568)

## Escolha de estado: 0xD7D8
Toma o lutador ativo de cada equipe e escolhe o estado. Se o estado muda, escreve-o em +0x2D e apaga +0x2C.

| Estado | Quando |
|---|---|
| 2 | Algum está coberto (+0x18 bit5) |
| 3 | Algum está fora do ringue (+0x19=1) ou na ação 4 |
| 1 | Sub 0x13/0x2E da ação 0xC, ou ação 0x1B |
| 0 | Nos demais casos: seguir o combate |

## Estado 2: contagem do pin (0xDD4E)
- Aproxima-se do ponto médio entre os dois lutadores.
- Batidas: poses da tabela 0xDED4 e durações de 0xDEDC.
- Em cada batida: +0x2E++ e 0xE02C.
- Ao chegar a 3: o resultado vai para 1C0BBE+4 / 1C0BD6+4.

## Estado 3: contagem fora do ringue (0xDEE4)
- Conta em BCD até 20.
- Ao chegar a 20: bit7 ou bit6 conforme cada lutador continue fora. Pode haver dupla desqualificação.

## Som da contagem: 0xE02C
- Tabela 0xE0A8 = ff,3d,3e,3f: vozes «1, 2, 3».
- No estado 3 com +0x2E<4 não soa nada: a contagem fora é muda.
- Também mostra o texto 0x9B e o texto de 0xE086[+0x2E].
