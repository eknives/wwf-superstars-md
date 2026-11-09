# Padrão de golpes — receita documental do arcade → port b92

**Só estudo; sem implementação, compilação nem teste novo no MAME.** A b92 já foi entregue (PARCIAL em fidelidade visível). Isto não autoriza acrescentar personagens/golpes nem mexer no Hogan. A cadência visível do Elbow do Duggan chão/córner e do Knee do Warrior do córner fica **PRIORIDADE BAIXA, «polir no final»**.

Fontes relativas a este backup: `02_arcade_decompilado/analisis/arc_rec.dis` (instruções alinhadas), `arc.dis` só para os oito BRA.W consecutivos FC64–FC80; estudos `02_arcade_decompilado/estudios/{kneedrop,duggan_suelo,energia}/`; `03_roms/notas/NOTAS_b87.md`, `NOTAS_b88.md`, `NOTAS_b90.md`, `NOTAS_b91.md`, `NOTAS_b92.md`. Port lido: `/workspace/b92/src/`, idêntico a `01_port_sgdk/actual/src/`. As notas b89/b90 anteriores são antecedentes, não o estado da b92.

**Qualidade:** C=instrução/índice confirmado pelo código; D=valor já extraído/documentado; M=teste histórico explícito de D/W; U=conteúdo ou comportamento não confirmado aqui. Um slot calculado por um stride C NÃO implica conhecer seu ponteiro/valores nem ter testado esse lutador. O prog.bin não foi reaberto/processado nem o MAME executado.

## 1. O padrão comum: seletor → sub-rotina → tabelas → reação

1. **Identidade:** o byte `actor+2B` é o id nativo; `word+2A & FF` seleciona as tabelas. CPU é o bit3 do BYTE `+2A`, não «o rival que eu não controlo». Banco gráfico e casa do seletor são conceitos diferentes (`6CD8`, conversão da seleção `7FE2`). Identidades canônicas: 0 Warrior, 1 Hogan, 2 Macho/Savage, 3 Duggan, 4 Bossman, 5 Honky, 6 DiBiase, 7 André.
2. **Entrada/seletor:** bordas `+114`; buffer `+116` mantido por `4066–40B6`. Escolher ação/sub por estado, plano, rival e zona. Não deduzir a técnica pelo nome de um sprite.
3. **Despacho:** ação byte `+2D`, tabela `8CE2`/despacho `8C82`; a ação 0C executa `F94C`, que em `F980–F994` chama o ponteiro `FB58 + 4*sub` (`word+30 & FF`). A ação 0C por si só não significa Knee nem combo.
4. **Relógio:** ator a cada 2 refreshes (`1508–1510`), MAME 57,444852941 Hz. `+6` pose, `+8` timer e `+36` passo costumam ser compartilhados, mas cada rotina decide se decrementa ao entrar, usa > ou ≥, mantém o desenho ao sair ou acrescenta uma preparação. **Não converter um dado de tabela diretamente em frames de 60 Hz.**
5. **Física e contato:** coordenadas de mundo X/Y/Z `+0C/+10/+14` 16.16; velocidades `+24/+26/+28` 8.8. Integração `3DCE/3E20`. Broad-phase, caixa ativa e energia são três coisas diferentes.
6. **Final:** mudar as ações de atacante/vítima, ligações e camadas/objetos auxiliares; subtrair energia só no evento correto. Não substituir toda reação por uma queda genérica.

### Tradução atual (NÃO é um motor universal)

`main.c`: `FC fd[2]`, `ctxLoad/ctxSave`, `engine`, `pendBtn`, `curPose`, `p1face/dFace`, `sx/bx`, `climb/ck`, `mv/mk`, `rn`, `gs/gk`. **Slot do port 0=Duggan nativo 3; slot 1=Warrior nativo 0.** `curF`, `f^1`, `ctl` e as linhas `[2]` NÃO são ids nativos. Existem ramos `if(curF)` e `if(!curF)` e relógios privados; não basta acrescentar uma linha ou trocar o retrato. Os `gs14/15` da b92 são rótulos internos, não subs 0E/0F do arcade; o antigo `gs11` decimal também não demonstra identidade com a sub 0B.

`FC.ox/oy`+`oxf/oyf` e os privados `w81X/Y/Z`, `dugX/Y/Z92`, `kvZ90`, `fsX/Z` usam escala 256: não representam toda fração 16.16 arbitrária do arcade. A física documentada conserva as frações representáveis; não certificar precisão universal. `arcClock/arcLast/arcTick/arcDen` convertem VBlank em ticks (3125/6528 NTSC, 3125/5440 PAL, NOTAS_b87). Lógica por tick NÃO garante publicação pontual da pose por causa de CPU/DMA/SAT.

Gráficos: `Pose/Piece`, `poseTab`, `spr_tab`, `spr_tiles`, `xld/xlw`, `dLog/dPose/dLoaded`, `dFlip/dLyo`, `fLoad/drawF/buildSat`. Pose nativa, alias de sequência e pose convertida são índices diferentes. Exemplos: `duggan92_poses.h` apêndice 849..860; `native81.h` Warrior 779..791; `knee90.h` A2/17/1A para D e W. Não reutilizar números de tile como ids nativos nem mexer nas paletas do ringue/parceiros/árbitro. Os bancos de paleta por bloco citados em cl87.h (2 Warrior, 7 Duggan) NÃO são os ids dos lutadores (0 e 3).

## 2. Catálogo por id: slots que JÁ existem no arcade

Todos os endereços das tabelas a seguir são hexadecimais. São endereços de ENTRADA, não seus ponteiros de destino, salvo `→` explícito. Fontes C: `4624–463A` (banco), `FC54–FC5E` (combo), `C778–C794` (chão dentro/fora), `F63C–F648` (córner), `1500E–15020` (chave). Destinos do combo: oito BRA.W FC64–FC80 lidos no arc.dis; são instruções reais do despacho, não pseudo-op de dados.

|id|Lutador/banco|ponteiro banco 6CD8+4i|combo FC64+4i → rotina|ponteiro chão CADE+4i|ponteiro lado de fora CAFE+4i|córner F6E6+3i|chave 15126+3i|
|---|---|---|---|---|---|---|---|
|0|Warrior|6CD8|FC64→FC84|CADE|CAFE|F6E6|15126|
|1|Hogan|6CDC|FC68→FC84|CAE2|CB02|F6E9|15129|
|2|Macho/Savage|6CE0|FC6C→FDA0|CAE6|CB06|F6EC|1512C|
|3|Duggan|6CE4|FC70→FDA0|CAEA|CB0A|F6EF|1512F|
|4|Bossman|6CE8|FC74→FC84|CAEE|CB0E|F6F2|15132|
|5|Honky|6CEC|FC78→FC84|CAF2|CB12|F6F5|15135|
|6|DiBiase|6CF0|FC7C→FDA0|CAF6|CB16|F6F8|15138|
|7|André|6CF4|FC80→FC84|CAFA|CB1A|F6FB|1513B|

Conteúdo D conhecido: slot de chão CAEA→CB6C; lado de fora CB0A→CBEC. Linhas cabeça CB72=`04,11,04`, corpo CB75=`05,06,06`, colunas P/K/P+K; corpo do lado de fora CBF5=`05,05,05` (TABLAS_DUGGAN, base CBEC+9). O Warrior usa CB3C dentro e CBBC fora (estudo do Knee/main.c). **Os destinos/bytes dos demais slots de chão NÃO foram confirmados aqui: não supor CB3C+16*i.** Os grupos são escolhidos em C79E–C8A8; cabeça offset 6, corpo 9; não dar nomes às outras linhas sem ler seu ramo.

Córner: W F6E6=`2C,20,2C`; D F6EF=`2F,20,20` (estudos). `F650–F664` escolhe a coluna 0 se o rival está na ação B, 1 se não: **NÃO são colunas P/K/P+K**; o terceiro byte não é consumido nesse seletor específico. Bytes dos demais lutadores U. A chave 15126 usa sim botão−1 (1501C/15020); conteúdos para outros ids U. Ter uma linha não demonstra que todas as técnicas sejam acessadas da mesma forma.

### Tabelas do salto/impacto: distinguir atacante e vítima

C: `10A72–10AB2`: física `11150+16*idAtacante`, quatro ponteiros long: +0 chão normal, +4 chão especial, +8 ar/córner normal, +C ar especial. Especial se a vítima for id 7, ou atacante id 6/sub 11 (`10A90–10AA8`). `10AB6–10AFA` acrescenta variantes por zona para a sub 1A; não extrapolar o solver D/W sem esses ramos.

C: `10CC8–10CF6`/`10F54–10F84`: poses `112FA+40*idAtacante +20*córner +10*variante +2*passo` (bytes). Cada bloco tem 20 words: quatro listas de 5 poses. Timers 112F0 compartilhados, NÃO por lutador. Caixa da vítima `11084+4*idVitima` (duas words; 10FCC–11001A). Ponto do atacante `110A4+8*idAtacante +4*córner` (duas words; 11001E–11004E).

|id|lutador|base 4 ponteiros física|base 20 words poses|caixa vítima|ponto atacante chão / córner|
|---|---|---|---|---|---|
|0|Warrior|11150|112FA|11084|110A4 / 110A8|
|1|Hogan|11160|11322|11088|110AC / 110B0|
|2|Macho/Savage|11170|1134A|1108C|110B4 / 110B8|
|3|Duggan|11180|11372|11090|110BC / 110C0|
|4|Bossman|11190|1139A|11094|110C4 / 110C8|
|5|Honky|111A0|113C2|11098|110CC / 110D0|
|6|DiBiase|111B0|113EA|1109C|110D4 / 110D8|
|7|André|111C0|11412|110A0|110DC / 110E0|

D confirmados: física 11180/11188→111F0; especial 11184/1118C→11200; 111F0 words `(0,−64,0,0,0500,0050,2000,2000)`, especial offset −80. Poses 11372=`61,62,1CB,1CC,1CC /61,62,1CD,1CE,1CE`, repetidas para o córner. Ponto 110BC/110C0=(8,4). W poses 112FA: 61/62/7A/7B; variante 76/77; ponto 110A4=(0,4). Outros blocos **existem pelo índice C, conteúdos U**: não foi extraída uma lista inventada de poses do Hogan/Macho.

### Disputa, pin e energia: outras linhas por personagem

C: a disputa B370–B382 usa o **id do rival** em B46C+4*i (duas poses; tempos compartilhados B468). 14E0A–14E1C usa o rival em 150F6+6*i (três poses; tempos 150F0); 150E0+2*i usa o próprio id em 14DEE–14DF8 para o contador dessa rotina, não energia. O pin BDCC–BE62 usa a linha BEF2+16*idAtacante, dx byte `[idVitima]`, dz byte `[8+idVitima]`; NÃO são pares word (dx,dz). Há exceções para os ids 0/4 em BD84–BE84 e um objeto auxiliar. Valores para outros personagens U.

Humano 7FEC+2*i=48 para os oito (TABLAS.txt energia). CPU 8190+16*progressão+2*i, não valores universais de 48; `1CD48+id` é um limiar de tontura (1CD84...), NÃO energia inicial. AF66/AF6A/AF72 são faixas de energia, NÃO ids. AA00 usa `+F0&7`, também não é id.

|id|lutador|disputa B46C|poses 150F6|contador 150E0|pin BEF2|energia humano|coluna CPU linha 0|limiar de tontura|
|---|---|---|---|---|---|---|---|---|
|0|Warrior|B46C|150F6|150E0|BEF2|7FEC=48|8190|1CD48|
|1|Hogan|B470|150FC|150E2|BF02|7FEE=48|8192|1CD49|
|2|Macho/Savage|B474|15102|150E4|BF12|7FF0=48|8194|1CD4A|
|3|Duggan|B478|15108|150E6|BF22|7FF2=48|8196|1CD4B|
|4|Bossman|B47C|1510E|150E8|BF32|7FF4=48|8198|1CD4C|
|5|Honky|B480|15114|150EA|BF42|7FF6=48|819A|1CD4D|
|6|DiBiase|B484|1511A|150EC|BF52|7FF8=48|819C|1CD4E|
|7|André|B488|15120|150EE|BF62|7FFA=48|819E|1CD4F|

## 3. Receitas por família: o que reutilizar e o que NÃO clonar

### A. Socos em pé / combo
- Arcade: sub 0→FC4E→despacho FC64 por atacante; FC84 para W/Hogan/Bossman/Honky/André, FDA0 para Macho/Duggan/DiBiase. **Mesmo motor NÃO significa mesmas poses**: FDA0 escolhe FE88, exceção id 2 FEAC (FDA4–FDB2); suas sequências/durações completas não são reextraídas aqui.
- FC84: FD70/FD7C poses 150..152/153..155, 4/3/3 **ticks**=8/6/6 refreshes desses passos; preparação FCAC=3 ticks, final/ligação FD2E/FD48 timer 1. Para o **atacante id 7 (André)** são escolhidas FD88/FD94, verificação do próprio id em FCC0–FCE6; não substituir essas tabelas por FD70 automaticamente. FCFC só acumula NOVOS pressionamentos no passo C (a comparação B existe, mas o incremento 4 não chega a ela); decide-se por `&3==1`, não por manter P.
- Dano 1 humano por golpe: W cabeçalho 18810/byte 18811; D 187F5. `1761E[pose]→[id]` e cópia 1697E. Não distribuir 1/2/3 só por ser combo.
- b92: `engine` ramo `mv==1`, `mk/pAlt/pAcc/pEnd`, `move_seq`, `arcTick`; ambos os slots usam o padrão FC84. **O combo D nativo FDA0 NÃO está portado fielmente**. Para outro personagem escolher primeiro seu BRA de FC64 e converter seu banco/sequência; não copiar o combo W para todos. O `hittable`/alcances atuais não são todo o motor de caixas do arcade.

### B. Chute
- Arcade: sub 1→FED0; FF3A normal, FF4A quando atacante id 7 (FED6). Avanço em FEFc–FF38, saída especial C9.2; as durações reais dependem do decremento e da saída, não são certificadas aqui para outros ids. Pose 158: W 188AB=4, D 188C7=4. O motor de caixas determina quando está ativa.
- b92: ramo `mv` restante, `move_seq` offset 33, `MV_HIT_KIK/MV_REACH_KIK/MV_REACH_Y`; dano 4 ou 6 contra corrida/whip representado. Reação genérica `victimStep/vh`; não é um descritor nativo completo. Dar um chute a outro: tabela FF3A/FF4A + banco + caixas + reação + dano, não só copiar `mv=2`.

### C. Corrida e clothesline
- Arcade: corrida 93EE, rebote 960A/96AA; A durante a corrida CD14→ação 0C/sub 14→12E7A. Tabela compartilhada 1302E: 1D0/1D1/1DA/1DB, captura 1D2+idVitima durante 8 ticks; para o X em 12F04 e arremessa em 12FAA, não no primeiro toque. Proximidade 16634 (`|dx|<60hex,|dy|<8`, coordenadas de mundo X/Y) NÃO é a caixa final; 1672C/16796 e caixas 1761E, caso 1890C→18C2A (NOTAS_b87).
- b92: `engine` rn 1/2/3, `clStep87`, `clInit/Step/Timer/Held/Pose`, `rnW`, `rnx`; usa broad-phase+interseção em pé, danos 4/2. `clHeld` e a liberação ligados ao rival. Lacunas conhecidas: quem corre, costas/cordas e ligações; `hittable` exclui a corrida. Não declará-lo motor do arcade íntegro.
- Para outro: converter o banco do atacante incluindo **as oito capturas 1D2+vítima**, testar que caixa toca e converter a queda do banco da vítima. Não confundir `rnd` com H-flip: a liberação da b92 chama `clFallStart(o,-rnd)` por 12F16/12F1C e 9BC6/27D2. O movimento sem impacto/corrida comum não subtrai energia só por existir.

### D. Disputa / Irish Whip
- Arcade: B1D0/B48C/B670 e tabelas B46C/B468; rota 14DD6 e 150F6/150F0; entrada humana 14FEE→15126. Várias tabelas escolhem pelo **tamanho/id do rival**, não só pelo personagem atacante. Selecionar chaves por botão é diferente de decidir o vencedor da disputa.
- b92: `grTry/grStep`, `gr/grk/grCool`, `lkC*`, `trStart/trStep`, `spT`, `sp_trk`, `trO/N/Pose`, fases de rebote `rw*`; as trilhas S/W1E representam a sub 1E→14CFC (contra-chave que solta para a ação 15). Não contêm Body Slam, Headlock, Gorilla Press nem finalizações completas.
- Receita: modelar dois atores ligados e suas tabelas cruzadas, entrada/reverse/vencedor, depois a liberação e o rebote com os limites 21E5A/21ED0. Dano próprio de disputa/whip/rebote interno=0; choque especial do lado de fora 2209C=5 só com os filtros 220BE/2208C e antirrepetição. Não cobrar dano de Body Slam por reutilizar a trilha do whip.

### E. Chão: Stomp e Knee/Elbow
- Seleção comum C706/C778–C8A8: mesmo plano, |dy|<24; cabeça Xv±40 (André ±56), zonas estritas 32/48 (André 40/56), tabela de ações CB1A. O buffer/as exceções por ação são diferentes do teste final de impacto. Pin/cabeça/corpo não são escolhidos só pela distância absoluta ao centro.
- **Stomp sub 5:** 1173A/118BC `(159,8),(15A,4)`; consome ao entrar 11750→1175C: 159×14/15A×10 refreshes incluindo a saída. Golpeia ao entrar na 15A (11782/11786→1179A); só plano/estado final, sem segundo filtro XY. 117E0 dano 1; exceção 117E6 compara banco gráfico+3 com 7 e escreve 3. b92 D=`dugZone92/dugStart92/dugStep92`, gs14; W=`warriorGround*`, gs13. **O relógio do stomp W existente não é o arcTick D recém-portado** (`if(!(gk&1))`): não afirmar igualdade universal.
- **Drop comum 10A5E:** W sub 0C/2C, D 11/2F; seleciona física/poses pelas tabelas da §2, solver 156FA→159AC, integração 3DCE/3E20. D/W: 8/18/10 refreshes iniciais, não 112F0[0]=0 interpretado como 1 tick; 10F54 espera 4 ticks, depois o comparador 10D42 >8/>4. Depois disso, contato/recuperação variáveis.
- Impacto 10BF8–10C3C→10FCC: descendente, vítima B e mesmo plano, Zword≤chão+16; caixa 11084 pela vítima e ponto 110A4 pelo atacante/córner. Escreve Yword=Yv−1 e Zword=chão, conservando frações; W acrescenta o ajuste 1152A e a variante 76/77, D NÃO esse +10 nem 7D. Danos 10DC0=5/10DCC=10, reação 8/sub D→A2. Do lado de fora o offset do solver é dividido por 2 (15A52); não proibir por estar «perto da corda»; os manipuladores de D 11/2F em 24102/24106 terminam em RTS 24322/24324.
- b92 W=`warriorGroundStart/Step/End`, `w81*`, `kneePost90`, gs12; b92 D=`dugStart92/Step92/End92`, `dug*92`, gs15. Vítima compartilhada `kneeVictimStart90/Step90`. D conserva fração, ponto ±8,+4, A2 e dano 1/5/10; não usa os antigos aliases genéricos gs5/gs11.
- **Os outros personagens NÃO são cópia de D/W:** o Hogan id 1 duplica Vx/Vy no chão em 10B70–10BAE, ao descer os apaga e muda a gravidade em 10C00–10C16; dano +1 em 10DDA e final/rebote especial 10E30–10EA8. A sub 1A impõe 11, a sub 0F 6; o id 7 impõe 12 no final dessa decisão 10DFC–10E04. A ordem das exceções importa. Para o DiBiase id 6/sub 11 há um seletor especial 10A98/10B42. Não se identifica aqui o nome comercial dessas técnicas nem se dão por testadas suas animações.

### F. Ataque do córner
- Arcade: ação F, estado +B8=2, F35A recebe P **ou K**, F636 escolhe a linha F6E6 conforme o rival B. W sub 2C/D sub 2F entram na MESMA 10A5E, não num salto independente. Flags +34, alturas e solver mudam a trajetória; limites 10B5E/110E4 (distância horizontal ≥96→Vx ±200hex, vertical ≥80 dentro/112 fora→Vy ±100hex).
- b92: `climb/ck`, `cPOST/cD0`, `CK` tabelas climb*, ramos `engine` do córner, `kneePost90` W / `dugPost92` D. Rival em pé/dropkick do córner continua ausente. Não mudar o input global nem escolher outra técnica só por compartilhar botão.
- Para outro: testar a sub que sua linha realmente devolve, resolver a partir do seu canto/altura, carregar a lista de poses `+20` e o ponto `+4`, dano e final da SUA rotina; pode não ir para a 10A5E. **Cadência visível D chão/córner e W córner pendente BAIXA «polir no final»**; não se dá por resolvida ao copiar tabelas.

### G. Pin / contagens / reinício
- Arcade: cobrir ação 17→BD10, entradas 1190C/11A72/12972, flag da vítima +18.5; matriz BEF2 por dupla, poses 65 ou 7F conforme id 0/4 e 188 por flag. Árbitro D7D8: DD4E contagem de 3 (poses DED4, tempos DEDC), DEE4 contagem fora de 20; E02C/E0A8 vozes. Essas tabelas do árbitro não são por lutador.
- As faixas AF66/AF6A/AF72 e o pin humano ADEA/CPU AE7E dependem de energia/flags/tempo, não de «o primeiro pin sempre é escapado». Para o escape humano prevalece o estudo de energia §Energia baixa sobre a simplificação antiga do pin_cuenta.md: AE24–AE40 compara um acumulador com 48−E; E0 bloqueia essa saída, não é KO automático.
- b92: `pinStart/pinStepA/pinAdvance`, `pn*`, `rs*`, `digPin`, `countStep` (RO_TICK/roC), `roC/roT/roDone`, `resetReq→matchReset→fighterInit`. O modelo de kickout ainda não integra toda a energia nativa. Regra de design do port autorizada: 3/20 **reinicia a luta sem SELECT**; não confundir com a transição do arcade que seria preciso copiar para equipes completas.

### H. Energia, dano e reações (comuns, com dados por pose/id)
- Energia +3C separada do dano pendente +3E; a subtração 16488–1649A satura em 0. Sem regeneração passiva identificada, 0 não é KO; existem recargas ENTRE lutas 2060–20EC e Power Up 6F64/6FEE (não são regeneração durante a luta). b92=`energy90[2]`, `hurt90`, `fighterInit` 48, sem HUD, ambos HUMANOS. `vdmg/vlast` não são energia. Todo lutador novo deve receber energia independente, sem transformar o não controlado em CPU.
- Caixas: 1672C→1761E[pose]→[id] (cabeçalho byte+1 dano), 1697E cópia; 1698A CPU vítima contra sub 0/1 força 0. 1638E/1642A acrescenta bônus só contra as ações 1/15/16; 16418 duplica F9.0; a ligação FFFE 162BC omite ambos. D/W: soco 1, chute 4, clothesline 4/2, stomp 1, drop 5/10. Não copiar valores para Hogan/André ignorando suas exceções nem inventar contatos para chaves ausentes. Dano extra 1642A/contador 17590/som 175CE são por SUB, não por id.
- **A2**: reação ação 8/sub 0D (despacho 99BE/9A14, A554→28EC), Vz 200hex, g 40hex; alturas relativas 4/7/9/10/10/9/7/4/0 em 9 ticks; pose A2 do banco da VÍTIMA, aterrissa 17/estado B; espera B conservada conforme AB7A, levantada 5/1A (AA00). Port `kneeVictim*90`, `kvPhase/Time/Z90`, `ground90`, `kneePose90`; não acrescentar espera fixa universal.
- **Arremessado 0x17**: ação 8/sub 17→9B9A, NÃO ação 17 pin. A8BE/2964: desloca ±32, altura +24, Vx ±80hex, Vz 100hex, g 30hex; pose 15→16 ao descer abaixo de 24, rebote 9C94→A4C8 sem Vx, termina 17. Port `clFallStart/fsStep`, `koF==3`, `fs*`, `clFallPose` em `cl87.h`. A b88 corrigiu sentido/flip e paletas por bloco; a pose nativa 15/16/17 é carregada do banco da vítima, NÃO do atacante. O resto de `victimStep/fsStart` não equivale automaticamente a essas duas reações.
- **Erro do drop**: 10C4A–10CB2/10C6A, humano perde 2, CPU 0; recuo ±24 pela orientação, +ação 8/sub 5; 9FCC inverte uma vez e usa 1CF→16→17→1A, AF66/AA00 para o final. b92 D fase 6/7/8 em `dugStep92`; W ramo de erro `warriorGroundStep`. O salto 125F0/1274E é OUTRA rotina (erro 4); não universalizar o −2.

## 4. Receita passo a passo para dar uma técnica a outro lutador (trabalho futuro)

1. Identificar id/banco, papel humano/CPU e técnica a partir da sua linha do seletor; registrar slot e destino REAL. Se aparece como U acima, ler esse dado antes de escolher o comportamento. Não mexer no Hogan por usá-lo como exemplo.
2. Anotar ação/sub, eventos/flags, rival admitido, zonas/orientações/planos; verificar se a tabela indexa atacante, vítima ou dupla. Consultar as exceções id 1/4/6/7; não repetir o erro «mesmo código = mesma técnica».
3. Separar dados (poses, tempos, offsets, caixas, física, danos) do controlador. Uma futura estrutura `descriptorPorId` seria um DESIGN PROPOSTO: **não existe como motor genérico na b92**. Substituir os ramos curF exigirá um escopo autorizado específico, não só trocar assets.
4. Converter a partir de 6CD8 o banco correto com pose→peças→tiles/paleta; respeitar blocos emprestados (b88), pivôs/H-flip/camadas/auxiliares, acrescentar sem sobrescrever prefixos nem recursos do Emilio. Referências: conversores `04_herramientas/scripts/b88/tools/gen88.py`, `b92/gen92.py`; compilar não precisa regenerá-los.
5. Reproduzir init/step/hit/recover/miss/final com o relógio nativo e frações, incluindo vítima/reação/energia. Ligações de 2 atores não são uma animação isolada. Não aplicar contato duas vezes nem dano a cada refresh de caixa ativa.
6. Com autorização de implementação posterior: testes curtos MAME/MD por tick e por REFRESH visível; registrar pose nativa/convertida/carregada, mundo XYZ/frações/velocidades/energia, espelho, chão/córner/lado de fora e erro. Não comparar contagens a 57,44/60/50 sem tempo real, nem duas capturas de fases diferentes como sincronia.
7. Manter os controles C=A+B, Y troca, sem IA nova/START só persegue; energia para todo lutador novo; regressão do Hogan e recursos intocáveis, resto dos golpes. Nova pasta/ROM+MD5 só quando autorizado, nunca como consequência deste guia.

## 5. Evidência reutilizável e lacunas

- Mecânica de chão D/W: estudos do Knee/Duggan e `02_arcade_decompilado/notas_historicas/b92/shots92/{validation92.json,trajectory92_compare.csv,pose92_refreshes.csv}`. 88 estados estáveis coincidem, não igualdade visível completa. Os casos da b92 são fixtures RAM+botões, não todos os cantos/jogo natural/Everdrive.
- Combo/clothesline/queda: NOTAS_b87/b88 e capturas da b88; as lacunas de quem corre/costas/cordas continuam.
- Dano/exceções: estudo de energia, `ENERGIA_ataques.csv`, `TABLAS.txt`, `cabeceras_poses.csv`; índice por pose/id confirmado, cabeçalhos de outros lutadores não recalculados aqui.
- Hogan/Macho/Bossman/Honky/DiBiase/André: entradas/strides C listados, poucas exceções lidas; **sem testes novos nem certificação de suas técnicas completas**. Ponteiros/bytes marcados U não são completados por semelhança visual.
- Prioridades oficiais: `PENDIENTES.md`; b92 entregue conforme `03_roms/CHANGELOG.md`. Documentar pendências não reabre a ROM.

## 6. Orientação do rival deitado no Knee/Elbow (chão e córner) — estudo 9-11-2026

Só leitura do `arc_rec.dis` + capturas da b92 já existentes; sem MAME novo, sem ROM nem mudanças no port.

**Arcade (C):** o rival NUNCA muda de orientação. `10A5E` só escreve o `+A` do ATACANTE: copia o do rival (`10A6C`, de novo `10BB2–10BB6`); o id 0 Warrior ou a sub 1A o substituem pelo sinal de Vx (`10BC4–10BD8`). A partir do córner (+34≠0, salvo id 4) o flag gráfico `+4` do atacante segue o sinal de Vx na preparação/subida (`10F90–10FAC`, `10D02–10D26`). O impacto (`10D58–10E0A`: `+2C=8`, `+44=0D`, dano `+3E`, `161C8`, som `C6CA`) e a A2 (`A554`: `27D2(8)`, pose `A2`, `A56E move.b +A→+4`) desenham a vítima com o MESMO `+A`. `C6CA` só escolhe o som.
- Destino: solver `156FA` rumo a `Xv ± offset` conforme o bit7 do RIVAL (tabela de física §2); córner: `10B5E/110E4` substitui Vx/Vy por ±200/±100 hex se longe de `Xv±64`. Caixa `11084[idVítima]` também pelo bit7 do rival (ori0 `Xv−64<X≤Xv`); ponto `110A4[idAtacante]+4·córner`. Cabeça: âncora `Xv−40` se bit7=0, `Xv+40` se 1 (`C83E–C858`). O atacante se adapta ao rival, nunca o contrário.
- Acerto `10BF8–10C3C→10FCC`; erro `10C4A–10CB2` (−2 humano, ±24, ação 8/sub 5, `9FCC` inverte SÓ o atacante). Aterrissagem da vítima `A5DA–A60A`: Z=chão, ação B, `+AE=0`; orientação intacta.

**b92 (C, pelo código + PNG):** convenção dupla de `vface`.
- Todo desenho da vítima deitada usa flip `vface^1`: pose genérica 114–117/626 por `invFl` (`main.c:462`, `1485`, com `lyoOf` ±32) e quedas nativas 15/16/17 (`main.c:1468`, `dFlip=vface^1`). Ao levantar da A2, `main.c:473` põe `p1face=!vface`. Ou seja, **a orientação nativa mostrada = `vface^1`**.
- O Knee/Elbow usa `vface` como se fosse o bit7 nativo: zonas `main.c:649`, `duggan92.h:11–14`; destino `main.c:677/685`, `duggan92.h:34/39`; caixa `main.c:736`, `duggan92.h:82`; o atacante D copia `vface` (`duggan92.h:28`); e a A2/espera são desenhadas com `dFlip=vface` e `dLyo=0` (`kneeVictimStart90 main.c:483`, laço `main.c:1465`).
- Efeito: o atacante mira o lado que na tela são os pés e, no contato, a vítima se espelha (e perde o deslocamento ±32) para que a cabeça fique sob o joelho/cotovelo. Evidência: `05_referencias/capturas/b92/volteo_A2_b92_suelo.png` (refreshes 118→124 do caso elbow: botas à esquerda → à direita) e `volteo_A2_b92_poste_suelo.png`. Acontece também no chão, não só no córner.
- Os testes da b92 não detectaram isso porque fixavam `vface=0` frente ao arcade ori0, supondo `vface=bit7`; as coordenadas coincidem nesse referencial, não no visual.
- **Cadência 8/18/10:** NÃO há relação demonstrada. A inversão não mexe nos temporizadores do atacante e as amostras irregulares da pose carregada são do atacante; continua sendo pendência BAIXA de publicação visível. (U: não medido se a carga dos tiles da vítima no refresh do contato acrescenta atraso.)
- U: posição exata da 114 com `lyoOf` frente à pose nativa 17 no mesmo `ox` (possível salto de 32 px mesmo com o flip correto); fluxo natural (derrubada por golpes/clothesline → Knee/Elbow) sem fixtures, não testado.

**Proposta b93 (base b92) — IMPLEMENTADA na b93, ver o resultado abaixo:**
1. Um único helper `oriVictima(o)=vface[o]^1` (orientação nativa mostrada) usado no lugar de `vface[o]` em `warriorGroundZone`, `dugZone92`, destinos/solver/override do córner, caixa de impacto, `kneeOutsideVictim91` e cópia da orientação do Duggan (`duggan92.h:28`).
2. A2 e espera: `dFlip=oriVictima` em `main.c:483` e `1465`; manter `p1face=!vface` ao levantar (já coerente). Verificar se é preciso `dLyo` para que não salte 32 px.
3. Não mexer em `vface` nem em como é atribuído em quedas/golpes (evita quebrar a clothesline da b88 e o pin). Stomp: a zona do corpo é corrigida com o mesmo helper (hoje também invertida em relação ao que é mostrado).
4. Verificar: fixtures com arcade ori0 ↔ port `vface=1` (e espelho), mesmos contatos 88 estados; PNG por refresh sem espelho no contato; caso natural derrubada→Knee/Elbow chão e córner, ambos os lados; regressão Warrior/Duggan, clothesline e pin.

**Resultado b93 (MD5 a89af7ed95159c0899430bf0e81f6441):** pontos 1–3 implementados (`oriVictima` em main.c:464; A2/espera main.c:485 e 1467 com `dLyo=0`, que é o posicionamento do arcade da pose nativa em Xv). MAME: contatos = arcade em todos os casos do Duggan e do Warrior; flip do rival constante deitado→A2→espera; capturas `05_referencias/capturas/b93/shots93/contacto93_*.png`. Clothesline: traço da b88 idêntico b92/b93. Pin: mesmo mecanismo; o pin do Warrior (zona C798) agora cai no lado visível correto. Confirmado o que era U: há sim um salto de ~32 px entre a pose genérica deitada (com `lyoOf`) e a A2 nativa; fica pendente (não é da A2). Sem testar: derrubada natural, córner do lado oposto, PAL.

## 7. Pin (cobrir) do Warrior sobre o Duggan — verificação arcade vs b93 (9-11-2026, só verificação)

**Arcade, código (`arc_rec.dis`):** Warrior/Bossman (id 0/4) cobrem por `11A72` (sem salto): `11A8A–11A90` orientação de quem cobre `+A = +A(vítima) XOR 0x80`; pose 0x7E; `Y=Yv+1`; `X = Xv ± BEF2[0][3]` (=32; `btst #7,+A(vítima)`: bit7=1 → +32, 0 → −32 com `neg`), `Z=0xBB−16+2·18=207`. Após 8 passos (`11B2A–11B60`) ação 0x17 → `BD10`: mesmo X, `Y=Yv−1+2`, `Z=0xBB−16+16+16=203`, pose 0x7F com `+4=+A`, auxiliar `1C0AB2` pose 0x80 mesmo X/Z, Y−2. Tabela `BEF2` linha 0=[48,32,32,32,36,32,32,40 | dz 16,13,13,16,13,16,13,18]. O Duggan (id 3) usa `1190C` (salto 1C00B4): orientação = sinal de Vx (`11992–119A2`), depois a MESMA `BD10`: `X=Xv±36` (BEF2[3][0]), `Y=Yv−1`, `Z=0xBB−13`, pose 0x65. Disparo do Duggan: linha do corpo `CB75=05,06,06` (K na zona do corpo = pin, a mesma zona do Stomp, entre a cabeça e Xv).

**Resultado MAME arcade (6 casos: ori0 Xv 680/760/880, ori1 640/760/860; dentro do ringue, sem empurrão ACA4):** sempre `X−Xv=−32` (ori0) / `+32` (ori1), `Y=301`, `Z=203`, `+A/+4` de quem cobre oposto à vítima. B→sub 6 +2 f, pose 7E no X final a +4 f (Z207, sem deslocamento), 0x17 a +26 f, 7F a +28 f. Nas bordas o arcade empurra o deitado para dentro (ori0 640→675, ori1 880→861).

**b93 (código, `main.c` `pinStart`/`pinStepA`, sem mudanças desde a b77):** lado por `pnM = oriVictima?−1:+1` e `pnX = Xv − lyoOf(114)`; X final = `pnX + pnM·32 = Xv` (não `Xv∓32`). `Y=Yv+1` e `Z=203` (pose 778 = 7F+80, duas camadas) corretos. Orientação: `p1face=(pnM<0)=oriVictima`; como a 778 já foi convertida espelhada (`gen77_pin.py arc(0,ap,1)`), o sprite sai ESPELHADO em relação ao arcade.

**Resultado b93 (mesmos 6 casos):** X=Xv em todos (32 px deslocado do arcade em termos absolutos, rumo aos pés), mas em relação ao corpo VISÍVEL do deitado (desenhado com `lyoOf` ±32) a posição coincide com o arcade a ≤4 px (medido nas capturas: cabeça do Warrior↔botas do Duggan 2/−15 px vs arcade 6/−15). Y/Z exatos. Lado do corpo correto nos dois lados do ringue. **Inversão:** silhueta da 778 contra o arcade IoU 1,00 só espelhada (0,97 sem espelhar) nos 4 casos medidos; erro de cor 58 vs 117. Aproximação: a b93 desliza 24 f com as poses históricas 513/514 (Z187) a partir de Xv−35; o arcade coloca a 7E parada no X final. Assento 778 a +29 f vs 7F a +28 f. A b92 tem o mesmo código de posicionamento (só mudou a zona de disparo).

**Veredito (b93):** NÃO totalmente correto (corrigido na b94, ver §8). Bem: lado do corpo, Y, Z, relação com o corpo visível, tempo do assento. Mal: (1) Warrior cobrindo espelhado nas duas orientações; (2) aproximação diferente (deslizamento 513/514 vs 7E fixa); (3) X absoluto = Xv em vez de Xv∓32 (compensa o `lyoOf` da pose deitada genérica; mesma origem do salto de 32 px). Proposta (NÃO implementada): (1) no `pinStart`, para o Warrior `p1face=dFace=!oriVictima(v)` (= `+A(vítima)^0x80` com a convenção da 778), depois verificar o flip de 513/514; (2) opcional: substituir a aproximação pela pose 7E convertida (fixa no X final, Z207, 24 f); (3) só junto com a correção da pose deitada (lyo): `pnX=Xv`, X=`Xv+(oriVictima?32:−32)`. Duggan: mesma regra `BD10` (dx36/dz13), mesmo `pinStart`; não medido no MAME aqui; seu disparo (`bodyX±24`, lado dos pés) não é a zona `CB75` do arcade.
Evidência: `05_referencias/capturas/b93/pin_warrior/{pin93_comparativa,pin93_zoom_volteo,pin93_cmp_lados}.png`; dados `02_arcade_decompilado/notas_historicas/b93/pin_warrior/`.

## 8. b94 — deitado no X do arcade + pin ajustado (9-11-2026, MD5 b2a8ff5d4453067ad3d2bf8762239413)

**Implementado (só 2 pontos):** (1) `bodyX=ox`, `dLyo=0` no deitado 114/626/752 (main.c:487, 1491): a pose sem lyo ocupa o mesmo que a 0x17 nativa em Xv (fl0 −56..16 vs −54..10). (2) `pinStart`: `pnX=pnVX=Xv`, `pnM=oriVictima?+1:−1` (BD10/11A72), `pnKD=pnM` (B012/B0A0); Warrior `dFlip=(pnM<0)` para 514/778 (convertidas espelhadas, match69 flip1) e invertido para 513 (arc pose 2 flip0) ⇒ olha ao contrário do deitado (11A8A); flip do Duggan sem mudança; árbitro `rfX=Xv±64`, `rfM=−pnM` (mesma posição relativa ao corpo que na b77). Pin do Duggan por `dugZone92==2`+B (C706/CB75 linha do corpo, 06=cobrir); removido `bodyX±PIN_ZONE` (b69).

**Resultado MAME (Xv=760):** varredura B d −88..+88 passo 8 IGUAL ao arcade em W o0/o1 e D o0/o1 (W: K −64..−40, P −32..−16 / P +16..+40, K +48..+64; D: K −64..−40, P −32..0 / P 0..+40, K +48..+64). Quem cobre: W X−Xv ∓32, Y301, Z203; D ∓36, Y299, Z174 (arcade ∓36/+36,97, 299, 174,5); lado do ringue 680/860 OK. Silhueta: assento e 514 diretos na b94 (espelhados na b93). Contatos Knee/Elbow/Stomp = arcade 16/16, flip/dX constantes sem lyo; levantar 114→115 sem salto. Clothesline idêntica à b93. Escapar: deitado Xv∓8, quem cobre Xv∓48, Y−1, Z+4 (= fórmula B012/B0A0; não medido no arcade). Contagem de 3 OK.
**Efeito colateral:** aterrissagem depois de escapar perto da corda: ACA4 empurra ~33 px (medição no arcade pendente).
Evidência: `05_referencias/capturas/b94/`; dados `02_arcade_decompilado/notas_historicas/b94/shots94/`.

## 9. Pesquisa 9-11-2026 (só estudo, sem mudanças): corrida, lentidão perto dos córneres, choques com as cordas

**(b) Corrida — arcade (código):**
- `93EE` acc_correr → `945C` init: velocidade byte `0x95BC[id]` → `+0x21` (= [28,28,30,27,24,30,27,20]; Warrior id0 = **28**, Duggan id3 = **27**), ângulo `+0x1E = (+A&0x80)|0x40`, modo de movimento `+1 = 1`, sem aceleração.
- `3DCE`→`3DF0`: a cada tick X += velocidade·2·0x20/256 px = **vel/4 px** (Warrior 7, Duggan 6,75).
- `94CE`: poses `0x95C4[id]` = 10..15, 2 ticks cada uma.
- `953C`: `21E5A`; ao tocar a corda do lado para onde corre → ação 2 (`960A`).
- MAME arcade: 1 passo a cada 2 refreshes em 65/65 casos (também pela corda de cima perto dos córneres). W 201,1 px/s, D 193,9 px/s (57,444 Hz). Poses a cada 4 refreshes.

**(b) Port b94 (`main.c` 821–832):**
- Avança `27<<6` (8.8 = 6,75 px) quando `tick&1`. `tick` conta iterações do laço (main.c:1460), não `arcTick` (main.c:1428, que sim desconta 57,44→60/50).
- Mesmo 27 para os dois; o arcade dá 28 ao Warrior.
- Medido no MAME:
  - NTSC: Warrior 194–202 px/s, com 3 de 75 frames perdidos (vs 201,1).
  - **PAL: 167,7 px/s (−16,6 % W, −13,5 % D)**, porque continua sendo 1 passo a cada 2 refreshes, agora a 50 Hz.
  - As poses vão a cada 4 frames do MD: também 17 % mais lentas em PAL.
- Causa: corrida (e andar/animações) por frame do MD em vez de por tick do arcade, mais velocidade fixa 27.

**(a) Lentidão — port b94:**
- As perdas de frame coincidem sempre com o scroll da câmera que cruza um tile: o laço do `main.c` 1507–1510 chama `put()`/`rel()` (main.c 196–208).
  - `acq` carrega cada tile novo com `VDP_loadTileData(...,CPU)`, e `put` faz 2× `VDP_setTileMapXY`.
  - Uma coluna são 29 linhas (≈490–526 palavras de VDP por CPU) e uma linha 33 tiles.
- Frame com streaming: ocupado 0,83 frame (mediana) frente a 0,25 sem ele. Qualquer carga extra (pose nova em `fLoad`, cordas, público `caApply`) passa de 1 frame e se perde.
- Como a lógica avança por iteração (`tick`), cada frame perdido deixa o jogo mais lento.
- Perto dos córneres a câmera (`camera()` 289–332, corredor `camtab`) se move em X e Y ao mesmo tempo. `main.c:330` impede coluna e linha no mesmo frame, então elas se encadeiam.
- Medido (MAME genesis NTSC, janelas de 59 frames):
  - aproximação diagonal ao córner superior esquerdo: 8/59 frames perdidos (13,6 %);
  - córner inferior: até 12/59;
  - andar na horizontal pelo centro: 2,4 %;
  - parado: 0.
- Sprites na SAT (`nsat`): 3–20 perto dos córneres superiores e 0–39 perto dos inferiores (limite 80). Não coincide com os frames perdidos; os sprites por linha não foram medidos à parte.
- Arcade: scroll por hardware, sem streaming; a lógica não perde ticks perto dos córneres. Em hardware real (escritas da CPU no VDP com a tela ativa) pode ser pior; não medido.

**Cordas — três casos do arcade:**
1. **Rebote** (ele corre ou é arremessado):
   - `953C`→ação 2 `960A`: gira, anim 0x10, velocidade 9 que baixa 1 por tick, `9700` marca a corda.
   - Arremessado: ação 8 → `9CD0` → sub 2.
   - Port: rn==2 (trilha de 48 f, verificado na s66).
2. **Sair:**
   - `CD2C`→`CD5C/CDF8`: tocando a corda lateral (`+0x18` bit0/1 de `21E5A`), direção 7/3 rumo a ela, e y+z em [0x1E0,0x230), sem 1C1898/189A bit6.
   - Humano de equipe: 12 ticks (`+0x102`).
   - Ação 3, ou 6 se não é de equipe, está dentro e +2A bit4/bit1 estão em 0.
   - Port main.c:1023–1026: 27 frames (`SX_HOLD`) no X da corda.
3. **Choque:**
   - `9E78` a cada tick testa X∓0x10 à frente com `21E5A` (desfaz se tocar, salvo poses 9A/A1).
   - `9CD0` compara o byte alto de +0x44, então **sempre passa para a sub 2** (MAME: sub 0x1C→2 no primeiro contato, não para a sub 1).
   - `9F02`: `9700` marca a corda (1C1898/189A = 0x4001: vibra), z≥0xCB, pose 0x16, `27D2` índice 0x11 (parâmetros de voo 0x2934: Vx 0x100, Vz 0, g 0x10; não é som — corrigido na b95), **Vx negada**: rebate para dentro 2 px/tick até z=0xBB → ação 0xB.
   - Sem corda, a sub 0x1C cai com −0x20 extra (`9C5A`).
   - `ACA4` ao deitar testa ±0x30 e ∓8 **conforme o bit7 de +A**.

**Choque ao escapar (B012/B0A0) — MAME arcade vs b94** (S = X de quem cobre no momento do escape):

| Xv | S | Arcade | b94 |
|---|---|---|---|
| 760 | 712 | 642, sem corda, fica | 642 → `soilNudge` → **675** (salto 33) |
| 728 | 680 | 643, fica | 627 → 675 (salto 48) |
| 708 | 660 | bate: a corda vibra, pose 22, rebate até **677** | atravessa até 627 sem rebote → 675 |
| 693 | 645 | bate → 677 | 627 → 675 |
| 832 (dir.) | 880 | bate → **859** | 906 → 858 |

Causas no port (`main.c` 498–552, 625–632):
- `fsRope` olha o próprio X já recortado, não X∓16 à frente.
- A sub 0x1C passa para fs2 em vez de fs3.
- fs3 não move o X (falta a Vx negada).
- `soilNudge` usa `vface` como bit7, quando a convenção da b93 é `oriVictima = vface^1`; por isso empurra para o lado errado.

Evidência: `02_arcade_decompilado/notas_historicas/inv95/` (arc_run*.csv, arc_zafar*.csv, port_zafar.csv, b94_*.csv e scripts .lua).

## 10. b95 — corrida por tick do arcade, fundo por DMA, choque contra a corda (9-11-2026, MD5 7be789d70d892c1efb86af8630b296a6)

**Implementado (só os 3 pontos da §9):** (1) corrida: `rnSpd` = byte 0x95BC[id] (945C → +0x21; W 28, D 27), passo vel/4 px por `arcTick` (3DF0), pose a cada 2 `arcTick` (94CE); o resto da lógica continua por frame (pendente). (2) streaming: tiles e células BG_B/BG_A de colunas/linhas por fila DMA (`acqQ`, `stCol`, `stRow`, orçamento de 40 tiles/frame, `DMA_flushQueue` se exceder), público e cordas calculados antes; aparecem no mesmo vblank que na b94. (3) corda: 9E78 testa X±0x10 a cada tick com 21E5A/22140 (616+e / 920−e, sem recorte com z≥0xDB) → X=limite∓0x10; 9CD0 sempre sub 2 (erro do `cmpi.b` copiado); contato no tick da aterrissagem → 9C94 sem ∓0x20; 9F02 no tick seguinte: a corda vibra, z≥0xCB, pose 0x16, Vx 0x100 para dentro, g 0x10, aterrissa com z<0xBB → deitado. `soilNudge` com `oriVictima` (vface^1) como bit7 do ACA4; chamadas 875/893 revisadas (vface=atacante à direita, convenção da b93).
**Resultado MAME:** corrida W 200,5/D 194,0 px/s NTSC, 199,7–200,1/192,6–193,0 PAL (arcade 201,1/193,9), poses 14,0–14,8/s (arcade 14,36); frames perdidos rumo aos córneres sup. esq./sup. dir./inf. esq./inf. dir. 20/14/18/19 → 3/2/1/0 de 580 (máx. em 59: 10/6/12/10 → 2/1/1/0), fundo verificado lendo a VRAM: 0 erros; capturas estáticas idênticas às da b94. Escapar em Xv 760/728/708/693/832 → 642/643/677/677/859 = arcade (b94 675/675/675/675/858). Rebote da corrida, sair do ringue, clothesline (vítima igual, atacante 6–8 px mais longe pela corrida por tick) e pin continuam bem.
**Sem verificar:** sub 1 contra a corda em arremessos e derrubadas por golpes perto da corda vs arcade; PAL nos córneres; hardware real; som 0x29 inexistente no port.
Evidência: `05_referencias/capturas/b95/`; dados `02_arcade_decompilado/notas_historicas/b95/shots95/`.
