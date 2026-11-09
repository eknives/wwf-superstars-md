# Contraste com o port s66 (wip19/main.c, só leitura)

Arquivo contrastado: s66/wip19/main.c, sha256 3d216c78…, sem modificar.

Estados:
- **C** = discrepância confirmada pelo código do arcade.
- **=** = coincide.
- **V** = é preciso o MAME para decidir.

## Pin e chão

| # | Port (linha) | Arcade | Estado |
|---|---|---|---|
| 1 | 292 e 396: «os kick-outs são SEMPRE o parceiro entrando»; o primeiro pin sempre termina em kick-out. | Kick-out próprio, ação 0x1E: o humano martelando (0xADEA, limiar AF72/2) e a CPU segundo a energia e a contagem (0xAE7E/0xAF26). Além disso há um kick-out imediato com sorteio (0x11BC6). O salvamento do parceiro (0x129A4) é mais uma via, não a única. | C |
| 2 | 294 e 397: com energia 0, 13/16 → contagem de 3. | A CPU com energia 0 (d1=6) nunca sai e o parceiro não pode salvá-la (0x129A4) → a contagem de 3 é certa (16/16). Um humano com energia 0 precisa de 0x30 pressionamentos. O 3/16 do arcade é a probabilidade de o parceiro não poder salvar, não a da contagem. | C |
| 3 | 365: lieTab {180,120,64,0} + 44 de base. | 2×AF66 = 224/164/108/44 frames. | = (exato) |
| 4 | 365: mashTab {24,10,6,3}. | AF6A = 24/10/6/3. | = |
| 5 | 366: lieBand = e/12 também para a CPU. | A CPU usa a máxima de 0x8190[nível*8 + vaga]/4, não 12. | C. O efeito depende dessa máxima: com 48 coincide. |
| 6 | 76: a CPU começa com 55 (demo MAME). | 55 não aparece na tabela 0x8190. Não se leu onde se inicializa a energia da CPU no modo demo. | V |
| 7 | 396: a CPU só cobre com a energia de P1 < 16. | A decisão de cobrir da CPU (planejador 0x1D1A8 → subs 0x1190C/0x11A72) não foi contrastada regra por regra. | V |
| 8 | A CPU deitada não reduz seu tempo à metade. | 0xAB1E: a CPU usa /2 se 0x1CD80 dá CS, e +0x20 se vinha de fora. | C |

## Sistemas que faltam no port

| # | Sistema | Estado |
|---|---|---|
| 9 | Relógio 30:00, pressa em 5:00 (música 8) e TIME UP (0x2626E). | C (falta) |
| 10 | Contagem fora do ringue até 20 e dupla desqualificação (0xDEE4). | C (falta) |
| 11 | Som: não há driver; faltam as vozes da contagem 0x3D–0x3F e o sino 0x20/0x21. | C (falta) |
| 12 | RNG: o port usa random(); o arcade usa 0x450A. | C |

## Corrigido em relação a discrepancias.md
- A grade/público 1C1854 (antiga discrepância #1) já está implementada na wip19, linhas 788–811. A condição coincide com 0x22462; não foi contrastada linha por linha.
- A antiga #4 («lieTab é uma aproximação») é retirada: os valores são exatamente 2×AF66.
