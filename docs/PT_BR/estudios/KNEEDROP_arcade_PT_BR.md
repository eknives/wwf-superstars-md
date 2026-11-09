# Knee Drop do Ultimate Warrior — SÓ ESTUDO

**A b89 não foi alterada nem foi construída nenhuma ROM.** Sua ROM continua com MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`.

## 1. Como se faz

- **Chão: apertar Kick, botão 2 do arcade, pela cabeça do rival deitado; não exige direção.** GameFAQs fornecido, linhas 167–171 de `GameFAQs_text.txt`: «Knee Drop = K (By head,2)». Na b89 corresponde ao **B**. Punch+Kick não é essa entrada: linha da cabeça do Warrior `04,0C,04` para P/K/P+K (`0xCB3C+6`).
- Rota humana: `0x8F9E` / lado de fora `0x904A` → `0xC706` → ação `0x0C`, subação `0x0C` → tabela `0xFB58+0x30` → **`0x10A5E`**. As entradas novas ficam em `+0x114`; `0x4066–0x40B6` as acumula em `+0x116`, apagado a cada quatro refreshes. `0xC70A` consome esse pequeno buffer, não um botão mantido com autorrepetição.
- Caso normal: rival na ação **B**, mesmo plano **byte `+0x19`** (0 dentro, 1 fora), `abs(Ya−Yv)<24`. **A altura Z não é comparada para escolher a zona.** Fontes: `0xC79E–0xC7EE`, tabela `0xCB1A`. O seletor também classifica `0x1E` como chão e admite a exceção ação 8/sub D (`0xC82A–0xC836`); essas exceções não foram testadas com entrada no MAME. O impacto, por outro lado, exige B.
- Coordenadas: **X=`+0x0C`, Y=`+0x10`, Z/altura=`+0x14`**, formato 16.16. Não são coordenadas de tela nem o centro visual do sprite. Âncora da cabeça: `Xv−40` se o bit7 de `+0xA` do rival=0; `Xv+40` se =1 (`0xC83E–0xC85C`). Para um rival normal, não o André:

| Orientação do rival | X do atacante que seleciona o Knee Drop | Y |
|---|---|---|
| bit7=0 | `Xv−71 … Xv−40`, ambos incluídos | `Yv−23 … Yv+23` |
| bit7=1 | `Xv+41 … Xv+71`, ambos incluídos | igual |

Derivação: lado da frente da âncora e distância **estritamente <32**, `0xC860–0xC88E`. Atrás é selecionada outra linha: por exemplo K no torso → sub 6, pin, não Knee Drop. A orientação inicial do atacante não é requisito: `0x10A6C`, `0x10BB2–0x10BD8` copiam/orientam; o Warrior termina com o bit7 conforme o sinal de Vx.

**Cordas/lado de fora:** não há veto genérico «perto das cordas» nesta seleção. Aplicam-se os limites normais ao andar (`0x21E5A` / `0x21ED0`). Além disso, `0x240B6` limpa `+0x9E` e sua lista **`0x240F0` não contém 0C nem 2C**: não se deve atribuir a esses saltos o cancelamento genérico `0xF9B0`. Testados impactos com atacante X=640 e X=896, Y=300, perto de ambas as laterais. **Também funciona do lado de fora**, com ambos no plano 1; a tabela do lado de fora `0xCBBC+7` conserva a sub 0C. O MAME confirmou com chão Z=128 e dano 5.

**Do córner:** **P ou K**, com o rival deitado (GameFAQs 176–177). Ação `0x0F`/estado de córner 2 → `0xF35A`, leitura da borda `+0x114` em `0xF38A/0xF3B6/0xF3EA/0xF41E` → `0xF636`; tabela do Warrior `0xF6E6=2C,20,2C` → **sub 2C**, também `0x10A5E`. Confirmados separadamente Button 1 e Button 2 a partir do canto inferior esquerdo. Não exige se colocar na pequena zona da cabeça do ataque no chão.

## 2. Poses e tempo real

Um tick de lutador são **dois refreshes**, conferido em `0x1508–0x1510`, laço `0x155A–0x157C` e no registro do MAME. Este driver usa **57,444852941 Hz**: 17,408 ms/refresh, **34,816 ms/tick**, não 60 Hz exatos (`wwfsstar.cpp:632`; seus totais de vídeo estão anotados como estimados).

Tabela de poses do Warrior **`0x112FA`**:
- Normal: **61 → 62 → 7A → 7B → 7B**.
- Variante `Ya+2<Yv`, flag `+0x5C=1`: **61 → 62 → 76 → 77 → 77** (`0x10B36–0x10B5C`).
- O bloco do córner usa as mesmas duas sequências.

| Fase | Pose | Duração real | Fonte |
|---|---|---|---|
| Preparar | 61 | **4 ticks = 8 refreshes** | **`0x10F54`, contador hardcoded `0x10FB2–0x10FC6`** |
| Subir | 62 | **9 ticks = 18 refreshes** | `0x10D2C–0x10D4C`, `0x112F0[1]=8`; avança quando o contador >8 |
| Descer | 7A / 76 | **5 ticks = 10 refreshes** | mesmo comparador, tabela=4 |
| Buscar contato | 7B / 77 | até colisão/chão; variável | `0x10BF2–0x10CBC`, tabela=FFFF |
| Após o impacto | 7B / 77 | contador até **12 ticks** | `0x10D58–0x10EA6` |
| Levantar | 1A | normalmente **8 ticks / 16 refreshes** | ação 5, `0xA90E`, `0xAA00[0]=8` |

**A primeira duração NÃO é 1 tick embora `0x112F0[0]=0`: essa fase salta para `0x10F54`, que espera quatro.** A nota/comentário herdado da b83 na b89 está incorreto.

Medido na RAM a cada refresh, caso de chão normal: **61×8, 62×18, 7A×10, 7B×26, 1A×16**. Os 26 da 7B incluem 2 antes do impacto e 24 a partir dele: ao passar para a ação 5 mantém essa pose um tick antes de carregar a 1A. O auxiliar 7D fica ativo **22** refreshes, não os 24 completos (`0x10E9A`). No canto testado, o voo prolonga a 7B para **34** refreshes. Não são durações universais para qualquer trajetória.

## 3. Trajetória e impacto

**Parâmetros do Warrior:** ponteiros `0x11150` → registro **`0x111D0`** (normal), oito palavras:
`0, −32, 0, 0, 0x500, 0x50, 0x2000, 0x2000`.
`0x156FA`, `0x108B0`, `0x159AC–0x15B3E` resolvem a trajetória. Vz inicial **0x500**, gravidade **0x50**, velocidades 8.8. Destino normal: `(Xv±32,Yv)`; fora, o offset −32 passa a **−16** antes do espelho (`0x15A52–0x15A5A`). Os últimos valores limitam |Vx|/|Vy|. O solver simula passos simples e divide o deslocamento pelo seu número, truncando rumo a zero: **34 passos** de chão a chão nestes casos.

Durante a fase 0 não há integração. Por tick de voo, **`0x3DCE→0x3E20`**:
`X += 2*Vx/256; Y += 2*Vy/256; Z += 2*Vz/256; Vz -= 0xA0`, limite descendente −0x800. Não existe um deslocamento fixo universal em X/Y.

Exemplo no MAME: atacante `(712,300,187)`, rival `(760,300,187)`, bit7=0: **Vx=0x78, Vy=0**, subida máxima **Z=232**; contato no 16.º tick de movimento, `(727,309,187)` após o ajuste. Espelho: começa em X=808, Vx=−0x78 e contata em X=793. Variante Y inicial=290: Vy=0x4B, termina em Y=**299,375**, não 309.

Córner testado: origem nativa **`(632,374,233)`** (`0xF280`, tabela `0xF6CE`), **Vx=599, Vy=−462**, solver 41 passos; contato no 20.º tick de movimento, `(725,59375;309,8125;187,5)`. `0x10B5E–0x10B6C`/`0x110E4` podem substituir Vx por ±0x200 se a distância horizontal até `Xv±64` for ≥96, e Vy por ±0x100 se |dy|≥80 dentro /112 fora. Não se deve reutilizar um voo fixo de chão para qualquer canto.

**Janela de impacto:** depois de integrar, Vz<0, rival na ação B, mesmo `+0x19`, Z inteiro ≤chão+16 (`0x10BF8–0x10C3C`). `0x10FCC` compara o ponto do Warrior **`(Xa,Ya+4)`**, tabela `0x110A4`, com:
- bit7 do rival=0: **`Xv−64 < Xa ≤ Xv`**;
- bit7 do rival=1: **`Xv < Xa ≤ Xv+64`**;
- em ambos: **`Yv < Ya+4 ≤ Yv+16`**.

Fontes: retângulo `0x11084` = (−48,+8), construção/comparações `0x10FD6–0x11060`. Coloca-se a fase 4 e seu impacto é executado nesse mesmo tick (`0x11062`, `0x10CBC`).

**Posicionamento/camadas:** `0x10D9E–0x10DB0` escreve as palavras inteiras Z=chão e Y=Yv−1, **conservando as frações**. Na variante normal o Warrior soma 10 ao Y e cria a **7D**, banco do atacante, orientação XOR80, X=atacante∓4, Y−10, Z+10 (`0x10F04–0x10F1A`, `0x1152A`). **Na variante 1 não soma esses 10 nem cria a 7D.**

## 4. Dano, reação e final

- `0x10DB4–0x10DD2`: vítima **ação 8/sub D**, dano de energia **5 no chão /10 do córner**. `0x161C8→0x16488` o subtrai com saturação. Confirmado **100→95** e **100→90**. O «2/3» do GameFAQs é a escala do seu autor; não foi demonstrada sua equivalência com esses valores internos.
- Reação real: `0x99BE→0x9A48→0xA554`, **pose A2 do banco da vítima**, não uma queda genérica. `0x27D2[8]→0x28EC`: **Vx=0,Vy=0,Vz=0x200,g=0x40**. No teste a altura relativa percorre **4,7,9,10,10,9,7,4,0**: nove ticks. A A2 dura **18 refreshes**. O literal `A20004` em `0xA566` NÃO significa que esta reação dure quatro ticks: a saída depende da aterrissagem (`0xA5DA–0xA610`).
- Ao aterrissar: ação B com bit1 e pose 17 na sua atualização seguinte; depois seu levantar normal (`0xAB1E`). Para humano esse bit conserva o contador de chão restante `+0x38` (`0xAB7A–0xABBC`); não inventar uma espera fixa nova. Para a CPU há um cálculo por energia/tabela `0xAF66`. O Warrior termina na ação 5/1A e volta a 0; **não encadeia um pin automático**. `0xAA00` contém 8,12,16,32,20,24,28,40 ticks conforme `+0xF0&7`; os testes usaram o índice 0.
- **Erro:** `0x10C4A–0x10CB2`: ação 8/sub 5, pose **1CF**, desloca X **−24** se bit7=0 /+24 se =1, flip de desenho oposto; perde **2 de energia se humano**. Segue `0x9FCC` (`0x27D2[0x19]`: Vz=0x300,g=0x40), poses **1CF→16→17→1A→0**. Verificado deslocando o rival durante o voo: energia do atacante **100→98**, não do rival. As esperas posteriores no chão dependem do estado.

## 5. Diferenças concretas frente à b89

Fonte: `/workspace/b89/src/main.c` e `native81.h`, além de executar **a ROM existente sem recompilar**.

1. **Preparação curta demais:** as linhas 647–648 esperam 1 tick, o arcade 4. Medido por refreshes: b89 normal **4/22/10/2** para 61/62/7A/7B antes do contato; arcade **8/18/10/2**. Variante b89: **3/21/11/3**. O contato a +38 refreshes coincide por compensação nestes fixtures, não porque a distribuição esteja correta.
2. **Relógio incorreto/instável:** as linhas 638–640 contam a cada duas **iterações**, não `arcTick`. Os registros mostram iterações que não avançam em todos os refreshes, daí poses alongadas/variáveis. Não foi feito perfil para atribuir o custo a CPU ou DMA. PAL também não foi testado.
3. **Variante 1 mal posicionada e com camada indevida:** as linhas 663–685 sempre Yv+9 e pose combinada 788=77+7D; arcade Yv−1 conservando a fração, **sem 7D**. Medido: b89 Y=309 frente a MAME 299,375.
4. **Reação/dano não reproduzidos:** a linha 685 só `vjolt=10,vk=14,vlast=180` e efeito; não subtrai os 5 nem executa a A2 com física. Na b89 a vítima continuou com Z=187 e pose genérica 752; no arcade faz o pequeno arco A2. `vlast=180` é um temporizador do acumulador de golpes, **não** a duração da queda no arcade.
5. **Final/camadas não idênticos:** a pose combinada mantém a 7D até carregar a 1A; o arcade a apaga um tick antes. Recuperação na b89 observada **15 refreshes**, arcade **16**; saída imediata no oitavo contador na linha 661 frente ao despacho nativo que mantém a pose.
6. **Lado de fora e cordas:** as linhas 585–594/898 vetam o ataque do lado de fora; o arcade o admite. As linhas 669–673 acrescentam um choque com a corda durante o voo que não se justifica para a sub 0C pelo `0x240B6` (lista sem 0C). Não foi testado cruzar todas as geometrias de corda.
7. **Seletor simplificado:** `lyingNow` exige uma fase concreta da derrubada genérica; não representa a tabela de ações `0xCB1A`, suas exceções, nem o buffer de pressionamento de quatro refreshes.
8. **O córner não está ligado a esta técnica:** o ramo `climb`, linhas 843–856, descarta `pendBtn`; não implementa a entrada P/K→sub 2C nem o voo/dano do córner.
9. **Erro incompleto:** as linhas 689–692 não aplicam os −2 de energia e apagam a fração de X. A orientação normal esquerda/direita não deve ser declarada incorreta só por `p1face=!vface`: essa é outra convenção do port; aqui não foi feita uma auditoria de cada tile/flip.

## 6. Verificação e arquivos

**Verificado no MAME:** entrada real Button 2 a partir de fixtures deitados; ambos os sentidos; variantes 0/1; limite X −71 válido/−72 não, |dy| 23 válido/24 não; torso→pin; perto de ambas as laterais; lado de fora; reação A2 e dano 5; erro/−2; Button 1 e 2 a partir de um canto, mesma sequência e dano 10. **Comparada a b89** em dois fixtures com B: durações, posicionamento da variante e ausência da física A2.

Iniciou-se com fichas/start e seleção normal de Warrior/Duggan. **Posições/derrubadas/energia foram preparadas na RAM, não uma partida natural completa**; não se forçou a subação do Knee Drop. No teste de erro o rival foi deslocado; nos de canto prolongou-se seu contador de chão para que não se levantasse antes. Os contadores de pose são da RAM a cada refresh, não uma certificação de cada pixel do vídeo. Os PNG são tirados dois refreshes depois da mudança observada para evitar capturar o bitmap anterior do pipeline de desenho.

- **Resumo visual:** `RESUMEN_KNEEDROP.png`.
- MAME, sequência normal: `arc_headL_01_preparacion.png`, `arc_headL_02_salto.png`, `arc_headL_03_vuelo.png`, `arc_headL_04_impacto.png`, `arc_headL_05_reaccion_apice.png`, `arc_headL_06_recuperacion.png`.
- Espelho/variante/canto: `arc_headR_04_impacto.png`, `arc_aboveL_04_impacto.png`, `arc_cornerK_04_impacto.png`.
- b89 intacta: `md89_headL_impacto.png`, `md89_aboveL_impacto.png`.
- Dados/reprodução: `arc_frames.csv`, `arc_corner_frames.csv`, `md89_frames.csv`, seus scripts `.lua`, `AUDITORIA.txt`, `audit_knee.py`, `ROM_tables.txt` e o texto extraído do MHT.

**Limites:** sem hardware/PAL, nem todos os cantos/rivais/estados excepcionais, nem auditoria gráfica tile a tile. O MAME avisa de CRC diferente em **24j6-0.112, tiles de fundo**, não CPU/sprites; a CPU reconstruída do ZIP é idêntica a `analisis/tools/prog.bin` (MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`). Frequência física da placa não medida.
