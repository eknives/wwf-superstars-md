# b90 — energia interna + Knee Drop

ROM: `/workspace/b90/wwf_b90.bin` — MD5 **24759dec91fa996dc6e7a2f227e30f45**.
Base b89 copiada; seus arquivos continuam coincidindo com `b89_manifest90.json`. Compilação SGDK local com o comando solicitado. **Não apresento o Knee Drop como idêntico a 100 %: há duas diferenças verificadas pendentes abaixo.**

## 1. Energia — verificado

- Dois humanos, inicial **48** (`7EE6→7F76`, tabela `7FEC`); `energy90[]` independente de `vdmg/vlast`, sem HUD, regeneração nem KO por zero. Subtração saturada (`16488–1649A`). `fighterInit` repõe ambos a 48 ao reiniciar o combate.
- MAME Genesis, binário final: **20 fixtures de RAM** com entradas reais após preparar o estado. Ambos os atacantes: soco **48→47**, chute **→44**, clothesline cedo **→44**/tardio **→46**, stomp **→47**, drop **→43**; falha **48→46 para o atacante**. Zero continua zero sem terminar o combate; **1→0** satura. Os ramos de contagem de pin/ring-out reiniciam **48/48**, conservando a fase de seleção 4. Forçou-se a fase final da contagem; não se jogou uma contagem completa.
- Evidência: `shots90/md90_energy_frames.csv`, `md90_energy.log`, `validation90.json`.

## 2. Danos dos ataques existentes — verificado nesses contatos

Soco W/D: `18811/187F5=1`; chute `188AB/188C7=4`; clothesline `1890D=4`, `18929=2`; stomp `117E0=1`; drops chão/poste `10DC0=5`, `10DCC=10`; falha humana `10C6A=2`. O `gs5` do Duggan usa MD522/523 = banco 3 poses **159/15A**, comparado com `b69/tools69/match69.pkl`: aplica-se stomp 1, não um dano inventado de «cotovelada».

O chute incorpora +2 de `1642B` para corrida/whip quando o contato permite; o filtro de colisão da b89 normalmente exclui esses estados, **não foi ampliado nem se verifica esse bônus no MD**. O Clothesline encadeado da b89 segue a exceção FFFE (`162BC–162DA`), sem bônus nem duplicação. F9.0 não tem equivalente completo; não foi inventado. Chaves/whip/rebote interior continuam sem dano próprio. Não se acrescentaram movimentos ausentes nem o choque exterior especial de `2209C`, cuja condição/antirrepetição não existe completa na b89. Pin/kickout e levantadas alheias ao Knee não foram mudados.

## 3. Knee Drop do Warrior — verificação parcial

- Entrada `C706/C79E–C88E`; poste P **ou** K `F35A/F636/F6E6`, sub2C→`10A5E`. Preparação `10F54/10FB2`: **4 ticks**; `112F0/112FA`: **9/5 ticks** de voo. Arcade `1508–1510`: tick=2 refrescos a 57,44485 Hz → **61×8 / 62×18 / 7A×10**. Usa-se `arcTick`, não a paridade do laço. Relógio existente: NTSC 3125/6528, PAL 3125/5440.
- Solver `159AC–15B3E`: Vz500, g50, destino Xv±32 (±16 fora), velocidades limitadas a 2000; divisão por coordenadas word inteiras `15A6C/15AD8`. O poste conserva a altura inicial e as regras `10B5E/110E4`. Impacto assimétrico `10FCC/11084/110A4`, descida e Z≤chão+16. Variante `10B36–10B5C`: **76/77**, Yv−1 com fração conservada, sem 7D. Normal Yv+9 e mãos auxiliares; retirada `10E9A`. Removido o falso choque genérico: `240F0` não enumera sub0C/2C.
- Reação `A554`, tabela `27D2[8]→28EC`: A2, Vz200/g40; alturas relativas **4,7,9,10,10,9,7,4,0**. Chão/getup 17/1A; tabela AF66 para a espera humana desta reação. Acrescentam-se unicamente seis poses A2/17/1A dos bancos 3/0 (`6CD8`), sem sobrescrever gráficos anteriores. Flip do Knee e A2 comparado visualmente; orientação nativa `10BB2`. Falha `9FCC`, vz300/g40 e −2.
- Contra o MAME arcade: **88 estados de trajetória por fase/timer coincidem exatamente** (X/Y/Z). Contatos: chão esq. **(727,309,187)**; direita **(793,309,187)**; variante **(727;299,375;187)**; poste P/K **(725,59375;309,8125;187,5)**. Dano **5/10**, curva A2 de nove ticks e variante sem 7D verificados. As frações são comparadas em CSV, não por pixels.
- PAL testado no chão: holds visíveis **7/16/9** refrescos; NTSC chão **8–9/19/10–11**. São conversões de tempo real; não se forçam 8/18/10 a 60 Hz.

### Pendências encontradas, não ocultadas

1. **Poste: cadência visível irregular**, embora trajetória/timers lógicos coincidam. Na medição final K: **9/18/8**, P: **10/19/8** refrescos para 61/62/7A; 7A deveria rondar 10–11 NTSC. Irregularidade observada durante o movimento da câmera; **não há perfil CPU/DMA que permita atribuir a causa definitivamente**. Não se mudou o relógio nem o scroll global para não afetar outros movimentos.
2. **Exterior conecta, A2 e dano 5 funcionam, mas posição NÃO idêntica**. Fixture inicial W510/R558: a b89 limita W a 512 e conserva R558; o arcade passa R a 546 (`AB1E→ACA4/21ED0`). Contato MD **(540,125;309;128)** frente ao arcade **(528,75;309;128)**; Vx225 vs 150. Não se alteraram os limites exteriores gerais da b89. A fixture com R546/W510 do CSV geral não seleciona o Knee; o teste válido MD exterior está em **`md_ext_knee_frames.csv`**, referência arcade em **`arc_frames.csv`, caso outside**. O ensaio isolado `arc_outside_frames.csv` não executou sub0C e **não é usado como validação**.
3. As fixtures preparam a RAM: não demonstram todos os casos de jogo natural, quatro córneres, combinações fracionárias, tempo restante no chão até levantar nem Everdrive. A espera restante da vítima não é comparada byte a byte: a fixture arcade mantém inicialmente 200 ticks e o MD usa AF66. O set do MAME avisa CRC diferente de `24j6-0.112` (fundo); CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`.

## Capturas e preservação

`shots90/comparativa90_{suelo,variante,poste,exterior}_{vuelo,impacto,reaccion}.png` (12 PNG). São fases comparáveis, **não uma sincronização exata por refresco**. Originais `arc_*.png`, `md90_*.png`, `md_ext_*.png` e PAL; números em `trajectory90_compare.csv`, `pose90_refreshes.csv`, `validation90.json`. Reproduzível: `tools/validate90.py`, Lua de testes e `source90.diff`.

Auditoria: b89 intacta; recursos originais conservados como prefixo exato. Só crescem `spr_tab.bin` (+756 bytes) e `spr_tiles.bin` (+6880), com comprimentos regenerados em `res.h`. Córneres, logo do ringue, Hogan, HUD, IA e outros timings/animações intactos. **Nenhuma mudança deliberada fora do escopo**; as diferenças pendentes são entregues expressamente, não dadas por resolvidas.
