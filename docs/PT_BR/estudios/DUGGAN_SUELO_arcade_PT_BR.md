# Duggan: Stomp e Elbow Drop — SÓ ESTUDO

6-11-2026, Europe/Madrid. Sem ROM nova, sem b92, sem modificar a b91. MAME 0.276, set `wwfsstar`; CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`. Continua o aviso de CRC do chip de fundo `24j6-0.112`, não CPU/sprites.

## Entradas e zonas

Fonte nominal: GameFAQs local, seção do Duggan, linhas 245–253 de `study_kneedrop/GameFAQs_text.txt` (cópia no backup). P=Button 1, K=Button 2 (A/B no port). Pressionamento novo, sem direção obrigatória. Rota humana `8F9E/904A → C706`, buffer `+116 & 3`, acumulado por `4066–40B6` durante quatro refreshes. Condições comuns `C79E–C8A8`: mesmo plano `+19`, `abs(Ya−Yv)<24`; rival deitado na ação B. `CB1A` contempla outras ações/exceção 8/subD: não testadas aqui.

Âncora H=`Xv−40` com o bit7 de orientação da vítima=0; H=`Xv+40` com bit7=1 (`C83E–C85C`; o André usa 56). X/Y/Z são coordenadas de mundo 16.16 em `+0C/+10/+14`, não de tela. Para vítima normal:

| Técnica | Entrada/zona de chão | Despacho |
|---|---|---|
| Stomp | P perto do corpo: orientação da vítima 0, `H<Xa<H+48`; orientação 1, `H−48<Xa≤H`. Mesmo Y ±23. | `CADE+3*4=CAEA → CB6C`; linha do corpo `CB75=05,06,06` para P/K/P+K. `FB6C → 1173A`. |
| Elbow Drop | K perto da cabeça: orientação 0, `H−31≤Xa≤H`; orientação 1, `H<Xa≤H+31`. Mesmo Y ±23. | Linha da cabeça `CB72=04,11,04`; `FB9C → 10A5E`. |
| Elbow do córner | P **ou K** a partir da ação F, estado `+B8=2`, rival B; sem zona pequena de cabeça. | `F35A → F636`, tabela do Duggan `F6EF=2F,20,20`, escolha pelo rival deitado; `FC14 → 10A5E`. |

A orientação inicial do atacante não bloqueia: `10A6C/10BB2` copia a do rival. A partir do córner, o desenho da preparação e a fase 1 se orientam pela Vx (`10F90–10FAC`, `10D02–10D26`). As casas da seleção NÃO são bancos: Duggan=3, Warrior=0 (`6CD8`, `7FE2`).

Lado de fora, pelo código: `CAFE+12=CB0A → CBEC`, a cabeça conserva `04,11,04`, o corpo `05,05,05` (fora, K no corpo não pede pin). Não testado dinamicamente neste estudo. **Cordas:** `240B6` apaga `+9E`; a lista `240F0` contém sim 11 e 2F, mas suas entradas `24102→24322` e `24106→24324` são RTS: não impor cancelamento genérico de corda a esses saltos. Não foram verificados todos os limites do ringue.

## 1. Stomp, não «cotovelada»

`1173A`: tabela **118BC = (159,8),(15A,4)**. O primeiro contador já é decrementado ao inicializar (`11750→1175C`): **159 dura 7 ticks/14 refreshes**, não 16. Ao mudar para o passo 4 (`1177A/11782/11786`) golpeia; 15A tem 4 ticks e um tick é mantido ao voltar à ação 0: **10 refreshes visíveis na RAM**, depois pose 0. MAME: k25..38=159; k39..48=15A; ação 0 desde k47, pose 0 desde k49.

X/Y/Z constantes: caso (744,300,187). Sem salto nem velocidade. **Contato uma única vez ao entrar na 15A**, `1179A`: verifica plano e ação B, **não volta a medir a distância X/Y**. A zona foi decidida em C706. `1185A` pode fazer a vítima se levantar ao acaso em certos modos/CPU (`118B6`), antes desse contato; então pode errar. Essa evasão não foi testada separadamente.

Dano **1**, `117E0→117F4→161DA→16488`; o 3 de `117EE` é do André, não do Duggan. Vítima ação 8/subD, A2; `+BF` incrementa até 4 (`117F8–11806`). Se já não está em B, `117B8` retorna: sem penalização de energia ao atacante nesta rotina. Há um ramo especial para vítima na ação 17 (pin), `1180E`, não testado. Final do atacante ação 0 (`1176E`), não a levantada 1A.

## 2. Elbow Drop, chão

Compartilha a **10A5E** com o Knee do Warrior, mas **NÃO compartilha offsets nem poses finais**. Tabela de poses do Duggan **11372 = 112FA+3*40**:
- Normal: **61 → 62 → 1CB → 1CC → 1CC**.
- Variante `Ya+2<Yv`, `+5C=1` (`10B36–10B5C`): **61 → 62 → 1CD → 1CE → 1CE**.
- Durações: **61×8 /62×18 /1CB ou 1CD×10 refreshes** (`10F54/10FB2`, `112F0=0,8,4,FFFF,0`, comparador estrito `10D42`). Depois 1CC/1CE variável até o contato +12 ticks de recuperação (`10D58–10EA6`); no chão testado **26 refreshes** no total, depois **1A×16** (`A90E/AA00`, índice 0). Tick=2 refreshes (`1508–1510`), vídeo do MAME 57,444852941 Hz; não são frames de 60 Hz.

Física do Duggan `11180/11188 →111F0`: palavras **0,−64,0,0,500,50,2000,2000** (hex salvo −64 decimal). Contra o André, `11184/1118C →11200`: offset −80. Destino Xv±64 normal; fora, o solver divide o offset por 2 (`15A52–15A5A`). Vz=0x500, g=0x50; velocidades 8.8, coordenadas 16.16. Solver comum `156FA→159AC–15B3E`: divide com coordenadas word truncadas, |Vx|/|Vy|≤0x2000. Por tick de voo `3DCE→3E20`: ΔX=2Vx/256, ΔY=2Vy/256, ΔZ=2Vz/256, Vz−=0xA0 (limite −0x800). Não integra durante a preparação.

MAME, atacante (712,300,187), vítima (760,300,187), orientação 0: **Vx=−120, Vy=0**, ápice 232; contato **(697,299,187)**. Espelho (808,300): Vx=+120, contato **(823,299,187)**. Variante Ya 290: Vy 75; contato **(697;299,375;187)** e poses 1CD/1CE.

Janela `10BF8–10C3C`: descendo Vz<0, vítima B, mesmo plano, Zword≤chão+16. `10FCC` usa o retângulo da vítima `11084[id]`: normal (−48,+8), larguras assimétricas 16/48. Orientação da vítima 0: `Xv−64 < Xhit ≤Xv`; orientação 1: `Xv < Xhit ≤Xv+64`; `Yv<Yhit≤Yv+16`. **Ponto do Duggan `110BC=110A4+3*8`: (Xa±8,Ya+4)**, sinal de X conforme a orientação do atacante; mesmo ponto no córner (`110C0`). É diferente do Warrior (Xa,Ya+4). Não é uma caixa genérica |dx|≤48.

O impacto fixa o passo 4 e aplica o dano nesse mesmo tick (`11062→10D58`). `10D9E–10DB0`: Zword=chão e Yword=Yv−1, **conserva frações**. O Duggan não acrescenta Y+10 nem o auxiliar 7D: `10F04` só faz isso para o Warrior; **auxiliar=0 em todos estes testes**. Dano **5**, `10DC0`; reação A2 descrita abaixo. Após 12 ticks: ação 5, retira os auxiliares (`10E8A–10EA0`), levantada 1A e ação 0; sem pin automático.

## 3. Elbow Drop do córner

Sub **2F**, não 11 nem o Knee 2C. Mesmas poses e **8/18/10 refreshes**, tanto P quanto K. Mesmo registro físico do Duggan 111F0; `+34=1/2` conforme altura/lado (`10B12–10B30`). `110E4` pode limitar Vx a ±0x200 se a distância horizontal até Xv±64 ≥96 e Vy a ±0x100 se |dy|≥80 dentro/112 fora; não é um voo fixo.

Caso do córner inferior esquerdo nativo (632,374,233), vítima (760,300,187): **Vx 399, Vy −462**, ápice 278; impacto **(694,34375;299,8125;187,5)**. P e K dão os mesmos resultados. A 1CC é vista por **34 refreshes** no total (10 antes +24 desde o contato), 1A 16. **Dano 10**, `10DCC`, não 5. A tabela F6CE fornece a posição inicial do córner. Os outros três cantos não foram testados.

## Reação e erro compartilhados

Vítima: `10DB4/117BA` → ação 8/subD → `99BE/9A48/A554`, **pose A2**, `27D2[8]→28EC`: Vx=Vy=0, Vz 0x200, g 0x40. MAME: alturas relativas **4,7,9,10,10,9,7,4,0**, A2 **18 refreshes**; depois B/pose 17 e levantada normal conforme energia/contador restante (`A5DA–A610`, `AB1E`, `AF66`, `AA00`). O literal A20004 não fixa a duração em 4 ticks. Não atribuir uma espera universal nova.

Erro do Elbow (chão ou córner), `10C4A–10CB2`: aterrissa, ação 8/sub 5, **1CF**, Xword−24 se orientação 0 /+24 se 1, conserva a fração; **−2 ao atacante humano**, 0 CPU (`10C62/10C6A`). Rotina `9FCC`, Vz 0x300, g 0x40; 1CF→16→17→1A→0. Teste de erro no MAME: vítima movida durante o voo; atacante 100→98, vítima 100; 1CF 20/16×8/17×44/1A×16 refreshes nesse caso. As esperas no chão dependem do estado/energia; não transformar essa amostra em constante.

## Diferenças concretas frente à b91 (inspeção, sem recompilar)

- **O Stomp já usa a trilha correta**, apesar do comentário «cotovelada»: `gs69.h` 522/523 correspondem ao banco 3 poses 159/15A (confirmação anterior `b90/NOTAS_b90.md`, conferência `b69/tools69/match69.pkl`). Trilha de 14/10 iterações, com poses de repouso antes/depois; `main.c:838` avança por iteração, **não por arcTick nem refresh estável**. A cadência da ROM do MD não foi medida aqui.
- Zonas D `main.c:984–987`: usa `bodyX`, |dy|≤16, P≤40, B entre PIN_ZONE e 100; não as zonas de cabeça/corpo C706/CB6C nem |dy|<24. P impacta em `GS5_K=16`, um índice ANTES da primeira 523 no índice 17; o arcade impacta ao entrar na 15A. Além disso o port volta a filtrar |dx|≤48/|dy|≤16 no impacto; o Stomp do arcade não.
- O Elbow D continua com `gs=11` (estado **decimal 11 do port**, não número de subação nativa; a rotina do arcade é **sub 0x11=decimal 17**: esclarecimento da frase ambígua do estudo de energia), **trilha de 83 iterações** (`gs69.h`), X interpolado rumo a `bodyX` com `gD*gs11X/7`, apagando a fração; sem o solver 111F0, sem o deslocamento nativo rumo a Xv±64, sem as variantes 1CD/1CE. `gs11Z` existe no header mas não é consultado no main.c; recursos antigos podem incorporar deslocamento visual: **não se afirma aqui uma auditoria por pixels de suas poses compostas**.
- Contato genérico no índice 40 e caixa centrada no corpo (`main.c:844–847`), não descendente/Z≤chão+16 nem ponto D ±8. O Y não é reposicionado em Yv−1 com fração. Dano atual 1/5 e erro −2 já corretos (`hurt90`), mas reação `vjolt=10,vk=14,vlast=180`, **sem A2 física para estes dois ataques do Duggan**. O ramo A2/Knee só está ligado ao Warrior.
- **O Elbow do córner do Duggan não existe**: `main.c:906–915` autoriza o salto só com `curF` (Warrior); portanto faltam a sub 2F, a trajetória, o dano 10 e seu erro para o D. Não basta trocar o id do sprite do Knee.

## Verificação e arquivos

**Verificado no MAME:** P corpo→sub 5, K cabeça→sub 11, espelho, variante, P e K córner→sub 2F; poses e holds da RAM acima, posições/contatos, energia 100→99/95/90, reação A2, erro 100→98. Dados por refresh: `arc_frames.csv`; resumidos em `RESUMEN_RAM.json` e `poses_refrescos.csv`; fontes/valores extraídos `TABLAS_DUGGAN.txt`. Script `arc_duggan.lua`, log `MAME.log`. Capturas `arc_stomp_*`, `arc_elbow_*`, `arc_cornerP_*`; resumo `RESUMEN_DUGGAN_SUELO.png`.

Início com fichas/start e seleção; depois fixtures de posições, banco 3 Duggan/banco 0 Warrior, energia 100 e rival deitado na RAM, **sem forçar a subação de ataque**. Entradas reais de botões; para o córner prepara-se a ação F/estado 2 e prolonga-se o tempo no chão do rival. PNG dois refreshes depois do estado lógico, não sincronização perfeita de pixels. Não é teste de todas as fronteiras, cantos, rivais, evasões nem do lado de fora; a ROM b91 não foi executada nem alterada. A ligação energia→espera depende de mais flags: estas amostras não a certificam exaustivamente.
