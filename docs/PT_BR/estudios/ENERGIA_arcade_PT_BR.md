# Energia do WWF Superstars: viabilidade para a b89

Só estudo, 6-11-2026 (Europe/Madrid). **A b89 não foi modificada, nem construída ROM, nem criada a b90.**

## Conclusão antes de implementar

**Sim: é possível acrescentar energia independente para o Duggan e o Warrior e subtraí-la nos contatos já existentes.** Não basta desenhar uma barra nem reutilizar `vdmg`: este último é um acumulador temporário de derrubada que a b89 apaga quando `vlast` expira (`main.c:1357`), não a energia do arcade. A fidelidade completa tem partes pendentes: identidade/zonas das trilhas de chão do Duggan, modo humano/CPU, variantes da clothesline e pin/levantar dependentes da energia.

O rival sem controle da b89 **não tem IA** (inventário, linha 96). Não deve ser considerado CPU simplesmente por não ser `ctl`: o arcade diferencia expressamente esse papel e muda o dano de soco/chute. Essa distinção de dados pode ser implementada sem mudar a IA, mas é preciso definir o modo.

## Fontes, unidades e método

- ROM da CPU big-endian `analisis/tools/prog.bin`, MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; conferida com os dois chips de CPU do ZIP local. Endereços deste documento: **endereços 68000 do arcade**, salvo as RAM e as linhas do port expressamente indicadas.
- Desmontagem `analisis/arc.dis`, tabelas lidas diretamente do binário e desmontagem alinhada das rotinas. O inventário b89 conserva referências antigas à b83: conferido com o `b89/src/main.c` atual. O FAQ serve para nomes/inputs, **não converte seus «1 após 3 / após 2» em pontos exatos de RAM**.
- MAME `wwfsstar`, ROM local `/workspace/wwf/mame/roms/wwfsstar.zip`. Fichas/START/seleção reais; depois fixtures de RAM para isolar ações, energia inicial, posições e, quando cabe, impedir evasão/IA até o contato. Executa-se a rotina nativa: não foi aplicado patch no código da CPU. **Não são todas partidas jogadas do início ao fim nem verificações dos inputs de cada chave.** Scripts `arc_energy*.lua`, CSV por refresh e logs conservados.
- CPU/vídeo do arcade: 57,444852941 refreshes/s; lógica de atores a cada **2 refreshes**, `0x1508–0x1510`. Tick = 34,816 ms. Os pontos de energia não são escalados por PAL/NTSC.
- O MAME avisa CRC diferente de `24j6-0.112`: chip de **fundo**, não código de CPU/sprites. Aviso conservado; o set não foi corrigido nem substituído.

## Representação e regras comuns

Ator: energia **word `+0x3C`**, dano pendente **word `+0x3E`**; `+0x2A` byte bit 3 = CPU; `+0x2B` id (Warrior 0, Duggan 3). Atores principais na RAM `0x1C0100` e `0x1C0334`.

Subtração em **`0x16488`**: `0x16492` subtrai `+3E`, `0x16496–0x16498` satura em **0** diante de empréstimo; `0x1649A` escreve `+3C`. Não contém um máximo universal de 48. Wrappers para outras referências de vítima: `0x161C8/161DA/161EC/161FE`.

Golpes com caixa: `0x1672C` consulta `0x1761E[pose]` e depois `[id]`; o byte de cabeçalho **+1** é o dano. `0x1697E–0x16984` o copia para `+3E`.

1. **Vítima CPU e atacante sub 0/1 (soco/chute): o dano base é forçado a 0**, `0x1698A–0x169A2`. Não confundir «não perde energia» com «não recebe golpe»: há sim contato, reação e acumulador de combo/tontura.
2. No percurso comum `0x16304–0x16328`, se a vítima estava na ação **1, 0x15 ou 0x16** (corrida/percursos automáticos, **não atordoamento**), `0x1638E–0x163C6` acrescenta `0x1642A[sub] & 0x7F`: soco +0, chute +2, clothesline +1.
3. Nesse mesmo percurso, o flag do atacante **`+F9.0`** duplica o resultado, `0x16418–0x16420`. Ativação `0x1CCE8–0x1CD28`, limiar de tontura `+F6` em `0x1CD48`; duração `0x1CD6C`, desligamento `0x1CD50`. Não há equivalente completo na b89.
4. **Exceção importante**: vítima com reação pendente `+40=0xFFFE` (ligação/pegada da clothesline) passa por `0x162BC–0x162DA` diretamente para a subtração `0x16328`; **omite bônus e duplicação**. Não aplicar indiscriminadamente as regras 2–3 a todos os golpes. As subtrações diretas de stomp/drop também não passam por `0x1638E`.
5. `+48` combo / `+46` janela e `+F6` tontura são diferentes da energia: `0x16D4C–0x16D92`, tabela `0x17590`. Não somar esse contador à barra.

## Danos por golpe e possibilidade de ligá-los agora

H/C = **vítima humana/CPU**, salvo a coluna de erro, que distingue o atacante. Valores em pontos internos, não segmentos do HUD. W=Warrior, D=Duggan.

| Ataque existente ou parcial | Dano do arcade confirmado e endereço | Acrescentar subtração na b89? |
|---|---|---|
| Soco W | **1 H / 0 C por golpe**, não 1/2/3 conforme o número do combo. Poses ativas 0x152/0x155: cabeçalho 0x18810, byte **0x18811=1**; FD70/FD7C. | **Sim**, contato `main.c:799`; uma subtração por golpe, separada da derrubada. |
| Soco D | **1 H / 0 C por golpe**; poses ativas 0x150/0x153, byte **0x187F5=1**. | **Sim para a energia** no mesmo contato; animação não idêntica, ver abaixo. |
| Chute W/D | **4 H / 0 C**. Pose 0x158; bytes **0x188AB=4 (W)** / **0x188C7=4 (D)**; sequência FF3A. Contra vítima na ação 1/15/16: **6 H / 2 C**, bônus **0x1642B=2**. | **Sim**, `main.c:816`; identificar corrida/whip, não somar 2 só por estar ferido. |
| Clothesline W/D | Contato pose **0x1D1: 4**, byte **0x1890D**; contato **0x1DA: 2**, byte **0x18929**. Ambas as vítimas H/C. Sequência 12E7A/1302E. Rota comum: +1 contra quem corre e ×2 com F9.0; **rota ligada FFFE: sem ambos**. | **Sim** para 4/2: `clStep87`, linha 729, já distingue esses valores para `vdmg`. Igualdade completa das variantes **parcial**: nem todas as ligações/reações estão representadas. |
| Stomp W | **1 H/C**, escrita **0x117E0**, chamada `0x117F4→161DA`; rotina 1173A/1179A. O 3 de 117EE é para o id 7, não W/D. | **Sim**, `warriorGroundStep`, `gs=13`, contato em 638–698. |
| «Stomp/cotovelada» D `gs=5` | O stomp nativo sub 5 é **1 H/C** (117E0). **Não fica demonstrada aqui a equivalência gráfica da trilha MD `gs5P` com esse stomp**: o inventário e o comentário a chamam de cotovelada. | **Parcial**: há contato em 782–784, mas não rotular como stomp exato do arcade nem escolher o dano de outra cotovelada pelo alias. |
| Knee Drop W `gs=12`, sub 0x0C | **5 H/C do chão**, **10 H/C do córner**: **0x10DC0=5**, se +34 ativo **0x10DCC=10**; sub 0x0C/0x2C em FB58 → 10A5E. | **Sim para a subtração** em `warriorGroundStep`; movimento/zona/animação ainda parcial segundo o estudo do Knee Drop. |
| Elbow/salto D `gs=11`, sub 0x11 | A sub **0x11 de FB58 também aponta para 0x10A5E**: **5 chão / 10 córner H/C**, mesmas escritas. | **Parcial** para equivalência completa: o contato em 782–784 permite subtrair 5, mas trilha/input/zona do port são genéricos, não um elbow do arcade plenamente verificado. |
| Erro do drop W 0x0C / D 0x11 | **2 ao atacante humano; 0 ao atacante CPU**, **0x10C6A** e verificação de CPU anterior. Só se esse salto errar, não por qualquer queda. | **Parcial**: é preciso distinguir impacto/erro e aplicar no evento de aterrissagem nativo; atualmente sem energia nem penalização real. |
| Disputa / reverse W/D | **Sem subtração própria** em B1D0/B48C/B670. | **Sim: 0**. Não cobrar energia por cada pressionamento ou por decidir o vencedor. |
| `trStart` chamado Irish Whip W/D | Trilhas S_1E/W1E: sub **0x1E → 0x14CFC**, contra-chave que libera a vítima na ação 0x15; **sem subtração própria**. | **Sim: 0** ao soltar, correr e rebote normal. Não atribuir os 8 do Body Slam a esta trilha. |
| Corrida, corda interna / queda do atacante no retorno do whip | **Sem dano de energia por si só**. Limite interno **0x21E5A**, rebote 960A/96AA, choque de chave F94C/F9B0; ação 8 sub 1 não recebe os 5 de 2209C. | **Sim: 0**, incluídos `trStep:1021–1023` e `fsStart`. |
| Bater no córner/limite do ringue pelo lado de fora W/D | **5 a quem bate H/C**, **0x2209C→220A2**. Limite **externo 21ED0→21FA8→22040**, primeiro contato por bitmask 22016; lista **220BE = 08,01,14,15,16,FF**. Na ação 8 só subtrai se a sub de reação for **0x0A** (2208C–2209A). | **Parcial**: o port tem limites/saídas/reações, mas é preciso reproduzir a condição do lado de fora e a antirrepetição. **Não subtrair 5 em todo rebote interno.** |
| Pin/kickout, subir/descer do córner, entrar/sair W/D | Sem subtração própria de ataque nas rotas estudadas B012/AB1E/AD12/ADEA/AE7E e EC12. O pin usa a energia que já restava. | **Sim: 0** de dano; adaptar pin/getup à energia é outra integração, atualmente não arcade. |

**Diferenças importantes do inventário:**
- O Duggan humano não despacha o combo nativo pelo FC84: **FC4E→FC70→FDA0**, sequência **FE88** (golpes 150/150/153 se encadeados). O W usa FC84/FD70/FD7C. A b89 usa FD70/FD7C para ambos: o dano unitário pode ser acrescentado sem mexer nisso, mas não permite afirmar que toda a sequência do D seja exata. Nada foi alterado.
- O alias `gs=11` é decimal 17 = **sub 0x11**, não sub 0x0B. Esta última é 132C8 (bulldog), **não** a trilha D tratada aqui.
- **Gorilla Press, Body Slam, Headlock, Bulldog, Back Suplex, Atomic Drop e ataques do córner não estão implementados** (inventário e código); ainda não há contatos correspondentes aos quais acrescentar dano. «Finalização do Warrior» aqui pode se referir ao Knee Drop parcial; **não há Gorilla Press escondido no `trStart`**.
- Outro elbow/finalização aérea **125F0** tem dano **12** em 126B8, **8** se sub 0x35 em 126C6 e erro humano **4** em 1274E. **Não confundir com gs11/10A5E**. Valores só pelo código; essa variante não foi testada nem é um ataque disponível na b89.
- Choque mútuo especial `+40=FFFC` pode subtrair **1** por meio de **17202→1720A** (seletor 17136/1715C). Não é «dano de disputa» automático; não há ramo equivalente identificado em `grStep`. **Parcial/não acrescentar a todas as chaves.**

## Energia inicial, máximo, recarga

- **Humano W e D: 48**. Tabela **7FEC**, oito words 48; inicialização **7EE6→7F76**. O HUD **7CF2–7D14** mostra `min(12, ceil(E/4))`. Um ponto interno não equivale a uma célula visível.
- CPU: tabela **8190**, linha `1C0028 & 0xFF`, coluna `(word +2A)&7`; inicialização **7FFC/8066/8110**, bônus de dificuldade **80A6–80B4**: **8×(1C004A & 3)**. Primeira linha W=45, D=43; dificuldade interna 1 → **53/51**. Nem todos os rivais começam com 48.
- Bases da CPU por índice de progressão 0..9, W/D: **45/43, 60/58, 68/66, 72/70, 40/40, 76/74, 76/74, 76/74, 86/86, 64/68**. Máximo inicial W/D nessas dez linhas e quatro dificuldades: **110**, não um teto global do subtrator. Dados completos em `energia_inicial.csv`.
- **Não foi encontrada regeneração passiva durante a luta** entre as escritas de +3C revisadas. Amostra idle curta sem mudança; não é apresentada como prova dinâmica de todos os estados possíveis.
- Entre lutas, **2060→20C2**: com contador +40 não negativo, consome 4 do contador; se o DIP **180002 bit7=0**, soma 4 à energia (20D6); **20DC–20E4** limita a 48 mesmo quando não soma. **20EC** repõe 48 aos membros da equipe eliminada para o fluxo posterior. Não é regeneração durante um salto/queda.
- Power Up com crédito/START nos modos admitidos: **6F64**, **6FEE/701E**, escritas **7000/7014/7030/7044**: **restaura à tabela 7FEC (48), não soma 48 por cima**. Recarga e Power Up: conferidos pelo código, não executados como teste de compra de energia.

## Energia baixa ou zero: não é KO automático

- Índice por quartos **1CE9C**: divide por `max(1, referencia_inicial >> 2)`, limita 0..3. Humano: faixas **0–11 / 12–23 / 24–35 / 36+**. A CPU usa a base 8190 sem somar o bônus de dificuldade neste cálculo. `1CEF4` calcula terços 0..2 para outros usos.
- Tempo deitado **AB1E→AB82–ABAA**, tabela **AF66 bytes**: **112/82/54/22 ticks** da menor para a maior energia = **224/164/108/44 refreshes** de lógica completa. A CPU pode dividir pela metade com F9.0 ou se **1CD80** devolver CS. O flag +33.0 acrescenta 32 ticks (ABB6). Não converter esses tempos em «frames de 60 Hz» sem conservar o tempo real.
- Antecipar a saída do chão do humano **AD12**: entradas novas `+116 != 0` incrementam +34; limiares **AF6A bytes = 24/10/6/3**, saída para a ação 0x19. Com E=0 ainda pode se levantar; demora mais. Não ler essa tabela como words.
- Pin humano **ADEA**: AF72=6/6/6/6 controla a janela em relação ao árbitro; **AE24–AE40** soma a +34 a cada tick com `+114 != 0` e compara com **48−E**. **AE36 com E=0 impede esta saída por entrada**. Também há condições de fase do árbitro que levam a AE42: não é simplesmente um único contador de pressionamentos.
- Pin da CPU **AE7E/AF26**: índices **0/1/2/3/4/5/6** para **E≥54 / ≥48 / ≥36 / ≥25 / ≥14 / >0 / =0**. Cada nível muda a fase/tempo de escape; o índice 6 não sai por essa rotina (**AE8E–AE92**). **129A4** também não pede o resgate do parceiro quando a energia=0.
- **0 não termina a luta sozinho**: exige pin/contagem ou a condição de vitória correspondente. MAME: vítima com E=0 continua em pé e, deitada, volta à ação 0 conservando **E=0**. Na b89 o pin/kickout do «primeiro pin» é determinístico, não lê a energia (`pinAdvance` 1040+); acrescentar a barra não corrige isso automaticamente.

## Verificação no MAME — resultados válidos e limites

Evidência primária: `mame_energy2..5_frames.csv` (RAM por refresh), logs de mesmo nome; resumo `mame_resumen.csv`. São leituras internas antes/depois, não estimativas da barra por pixels. As letras W/D nos nomes dos casos indicam o atacante; ambos foram testados salvo onde se especifica.

| Teste | Resultado observado |
|---|---|
| Início VS, W e D humanos | **48/48**, linha NATURAL_START_ENERGY nos logs. |
| Início 1P natural antes dos golpes | `natural_cpu_final.log`: W humano **48**, CPU ids 4 e 2 **55/55** = 47+8, progressão 0/dificuldade 1. Fórmula da CPU confirmada com essas colunas; todas as linhas W/D só pela tabela. |
| Soco W/D em humano / CPU | **48→47 / 48→48**, com golpe pendente/reação mesmo na CPU (energy2). FD7C W pose 155 também **48→47**. Não foi medido um combo inteiro de três contra cada tipo. |
| Chute W/D em humano / CPU | **48→44 / 48→48**, contatos registrados (energy2). |
| Chute em quem corre ação 15 | **48→42 humano / 48→46 CPU**, ambos os atacantes (energy2). |
| Clothesline pose 1D1 | **48→44 humano e CPU**, ambos os atacantes (energy4). |
| Clothesline pose 1DA | **48→46**, humano ligado (energy2/3) e CPU em contato tardio (energy3), ambos os atacantes. A ligação da CPU não é dada por verificada com esse fixture. Não confundir o nome early de um teste com a pose real: o CSV mostra qual tocou. |
| Clothesline ativa 1D1 contra quem corre | **48→43**, ambos (energy5; o fixture começa na fase ativa para isolar este caso). |
| F9.0, soco / clothesline cedo / ligada tardia | Soco **48→46** (energy3), 1D1 **48→40** (energy4), 1DA ligada **48→46**, **não duplica** (energy5). Ambos os atacantes. |
| Stomp nativo sub 5, W/D, H/C | **48→47**, energy2. D nativo verificado, não a identidade da trilha MD gs5. |
| Drop W 0C / D 11, chão, H/C | **48→43**, energy2; vítima CPU imobilizada para impedir que desvie antes do contato. |
| Drop do córner W/D sub 2C | **48→38**, energy2; fixture na posição/altura do córner, não teste do input completo de subir. Ataque não disponível hoje no port. |
| Erro do drop, atacante humano / CPU | Atacante **48→46 / 48→48**, vítima sem dano, energy2; os casos `miss_attackerCPU` são CPU atacante. Os `drop_miss_cpu` antigos foram congelados errado e NÃO verificam o erro. |
| Saturação | Drop com vítima E=3: **3→0**, não negativo (energy2, W_saturate3). |
| Contra-chave S/W1E, corrida, corda interna e choque no retorno | **48→48** para ambos os atores, embora haja rebote e queda (energy2, counter_whip). |
| Corrida do lado de fora, impacto no limite/córner | Atacante **48→43**, ambos, energy3 `post_outside`. Não se afirma comparação visual exata de qual córner físico foi. |
| Idle e zero | Idle **48→48**; em pé **0→0** sem fim de luta (energy2). Amostra curta, não todos os estados. |
| Levantar conforme a energia | `levantarse_mame.csv`: valores iniciais da tabela menos o tick já consumido: E48=21, E24=53, E12=81, E0=111; até a ação 5 a partir de k21: **42/106/162/222 refreshes**; E0 volta à ação 0 em k259 com E0. Concorda com **22/54/82/112 ticks** no total. |

**Não verificado dinamicamente**: matrizes completas de progressão/dificuldade W/D, recarga entre lutas, Power Up, toda a lógica de pin/parceiro/kickout, combo triplo completo, todas as variantes de costas/cordas/ligações. Seus valores acima são distinguidos como dedução direta do código. A comparação da arte de chão do D e a equivalência completa de cada ramo com a b89 ficam pendentes; o port não foi alterado para facilitar os testes.

Os primeiros testes também ficam guardados (`arc_energy.lua`, log/CSV sem número), mas alguns fixtures permitiam evasão ou não moviam a clothesline. **A ausência de dano neles não é usada como prova de dano zero**. Em `mame_resumen.csv` são assinalados os testes sem contato e os erros mal isolados.

## Arquivos e preservação

- `ENERGIA_ataques.csv`: decisão por lutador/golpe, valores e endereços.
- `energia_inicial.csv`, `cabeceras_poses.csv`, `TABLAS.txt`: extração de tabelas/cabeçalhos; caixa vazia expressamente distinguida de dano ativo.
- `mame_resumen.csv`, `levantarse_mame.csv` e CSV/log/Lua de cada teste: reprodução e auditoria.
- PNG opcionais do MAME: `W_drop_antes.png`, `W_drop_despues.png`, `W_clothes_antes.png`, `W_clothes_despues.png`. A leitura da RAM é a evidência numérica; a barra arredonda de quatro em quatro.
- ROM b89 continua **MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`**. Nada escrito dentro da b89; todo o trabalho novo fica neste diretório.
