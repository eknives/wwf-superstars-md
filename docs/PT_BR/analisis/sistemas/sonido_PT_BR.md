# Som: driver Z80, OKI e sino

Fonte: ROM 24ab-0.12 (Z80, 32 KB) e ROMs OKI 24a9-0.46 + 24j8-0.45.
Ferramentas: tools/z80rec.py (listagem em /tmp/z80.lst) e tools/oki.py (gera oki/sXX.wav).
Leu-se todo o código Z80 alcançado: 1.200 instruções e 2.523 bytes, mais os manipuladores de opcodes do sequenciador 0x468–0x6C0.

## Hardware e fluxo
- O 68K escreve no latch 0x180009. Isso provoca uma NMI no Z80, que põe o byte na fila 0x8400.
- O YM2151 gera a IRQ de 0x38 com seu temporizador. O laço principal está em 0x100 e o despachante em 0x18F.

## Comandos
- 0 = reset.
- Bit7 ativo = parar.
- 0xF0, 0xF1 e 0xF2 mudam o manipulador (0x821A).
- 0xFE e 0xFF = reset.
- Tabela 0x1000: 0x67 entradas de 4 bytes.

| Faixa | Significado |
|---|---|
| 0x01–0x17 | Música FM. 8 canais em 0x8000 com passo 0x40; tabela de opcodes do sequenciador 0x8CF (C0–EA). O 0x16 é um duplicado do 0x0A. |
| 0x18–0x1F | Entradas de preenchimento (tocam a amostra 1). |
| 0x20–0x49 | Amostra OKI = comando − 0x1F. Driver em 0xC4B, 4 vozes em 0x8310. |
| 0x50 / 0x51 / 0x52 | Sequências de amostras (0xD79/0xDAA) com dados em 0x1152/0x117A/0x11A2. 0x50 e 0x51 são ondas de público (amostras 3 e 4); 0x52 é um ritmo com a amostra 5 e o 68K nunca o envia. |
| 0x55–0x67 | As «entradas» se sobrepõem aos dados de sequência: não são comandos reais. |
| > 0x67 | Vai para 0x345, que só escreve 0x821F, e nada o lê: é um NO-OP. Por isso o aviso 0x70 do relógio não soa. |

As amostras válidas são 1–0x2A.

## Sino (resolvido)
- **0x20 = sino de início.** Amostra 1: 1,5 s, pico espectral em 2.360 Hz e decaimento exponencial. Só inicio_combate (0x84A2) o envia.
- **0x21 = sino repetido.** Amostra 2: mesmo pico (2.350 Hz), sustentado 2,3 s. Enviam-no musica_combate (0x179A) e o fim de tempo (0x26548 / 0x2657A / 0x2658E).
- O 0x3B (amostra 0x1C), que antes se supunha ser o sino, **não é**.
- Isso se deduz do espectro e do contexto de chamada; ninguém o ouviu.

## Outros IDs identificados

| ID | Amostra | Uso |
|---|---|---|
| 0x22 / 0x23 | 3 / 4 | Público |
| 0x24 | 5 | Passos |
| 0x29 | 0xA | Golpe surdo |
| 0x32 | — | Rolar para fora do ringue |
| 0x33 | 0x14 | Corda |
| 0x47 | 0x28 | Poste |
| 0x3D / 0x3E / 0x3F | — | Vozes da contagem do árbitro: 1, 2, 3 |

A lista completa de que rotina envia cada ID está em sonido_ids_llamadas.txt.
