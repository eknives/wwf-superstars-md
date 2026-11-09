# b91 — entrega PARCIAL

**ROM:** `/workspace/b91/wwf_b91.bin` — **MD5 1f7f183b0ef6fe6367d62360697935c6**.
Base b90 copiada integralmente. **Pontos 2 e 3 corrigidos/verificados; ponto 1 NÃO resolvido. Não apresentar esta ROM como cumprimento completo.**

## 1. Knee a partir do poste — pendente, não se dá por corrigido

Novo MAME confirma `arc_corner_frames.csv`: **61×8 / 62×18 / 7A×10 refrescos**, P e K. São **4/9/5 ticks** (`10F54/10FB2`, `112F0/112FA`; relógio `1508–1510`, 57,44485 Hz). O MD precisa de conversão temporal, não forçar esses números literalmente a 60 Hz.

Ensaiaram-se relógio separado com fase compartilhada, transporte DMA limitado e SAT preparada antes do VBlank. **As repetições não mantiveram a equivalência por refresco**, embora a trajetória por tick coincidisse. Retiraram-se TODAS essas mudanças: a ROM final conserva o render, relógio, público e cadência de poste da b90. Ensaio final: registros de pose carregada K **11/19/7**, P **5/19/14**; não se afirma que sejam contadores visuais atômicos nem que coincidam com o arcade. Há PNG consecutivos `post_corner*_f*.png` e CSV por refresco.

Experimento descartado: `tools/experimental_post91.c.txt`, evidência em `shots91/experimental_post/`; **não está compilado na ROM entregue**. O perfil mostrou trabalho de scroll e construção da SAT atravessando refrescos; não há atribuição CPU/DMA definitiva para todas as pausas. Documentação SGDK consultada: [SYS/VBlank](https://stephane-d.github.io/SGDK/sys_8h.html), que adverte que perder o início pode adiar o processo um refresco. Não se ampliou o escopo nem se retirou o polling dos controles para ocultá-lo.

## 2. Exterior — corrigido e verificado

Causa: a b89 recorta a origem W510 para 512 antes de entrar e não aplica à vítima deitada o ajuste **`AB1E→ACA4`**, dois testes com deslocamentos ±48 e ±8. Seu limite exterior está em **`21ED0/22140`**, tabela **`221B2`**: chão 128, Y192..456, X488..1040, inclinação /6, margem interior 48 (`21F2A/21F54`).

**Só ao iniciar o Knee exterior** recupera-se a origem anterior ao recorte, se ainda corresponder à mesma posição, limita-se como no arcade e normaliza-se a vítima. Andar e os demais movimentos conservam seus limites originais; o solver não foi mudado.

Caso W510/R558/Y300: origem W510, vítima R546, **Vx150**; contato MD e MAME **(528,75;309;128)**, energia 48→43 e A2. Eliminou-se a diferença anterior MD540,125/Vx225.

Regressão rápida contra o MAME: chão **(727;309;187)**; variante **(727;299,375;187)**; poste P/K **(725,59375;309,8125;187,5)**, dano 10. **88 estados estáveis de trajetória coincidem**; A2 conserva alturas 4/7/9/10/10/9/7/4/0. As leituras capturadas entre instruções são descartadas ao contrastar estados; não se confundem com um contato já completado.

## 3. Seleção — corrigido e verificado visualmente

Causa: `selDraw89` escrevia os **896 tiles** de overlay por CPU com interrupções bloqueadas, atrasando as mudanças de paleta HINT. Agora prepara só as células diferentes e as publica durante o VBlank; não há escrita massiva durante a tela ativa. Navegação/confirmação e piscada nativa de confirmação permanecem sem mudanças (`749E/74F2/7552`, `1F5C/1F86`).

**74 PNG consecutivos por versão**, quatro mudanças de cursor: a b90 altera até **2799 pixels alheios ao cursor em 4 quadros**; a b91 **0 pixels, 0 quadros**. Além disso, confere-se que o cursor NÃO fica congelado: Savage→Hogan→Duggan→Honky→Savage, quatro posições visuais distintas (258 pixels verdes). Referência MAME também recapturada. Evidência: `select_b90/`, `select_b91/`, `select_arcade/`, `validation91.json`.

## Arquivos e limites

- Comparativos: `comparativa91_seleccion_secuencia.png`; `comparativa91_exterior_{vuelo,impacto,reaccion}.png`; `comparativa91_poste_K_{vuelo,impacto,reaccion}.png`; chão/variante equivalentes. São fases comparáveis, não o mesmo refresco/câmera: o MAME mantém câmera fixa nas fixtures.
- `trajectory91_compare.csv`, `pose91_refreshes.csv`, Lua e `tools/validate91.py`; NTSC e PAL executados. Fixtures de RAM + entradas, não partida completa, quatro córneres/geometrias exteriores exaustivas nem Everdrive. O MAME mantém o aviso de CRC do chip de fundo 24j6-0.112; CPU MD5 4bd7c20fe4dbaf1b7ee8225e0e5d7359.
- Auditoria completa: b90 intacta (`b90_manifest91.json`). **Só mudam `src/main.c` (normalização do Knee exterior) e `src/select89.h` (cursor)**. Todos os recursos gráficos, córneres, logo, Hogan, energia e outros movimentos são idênticos. Diffs `source91_main.diff`/`source91_select.diff`.
- **Fora do escopo na ROM: nada. Pendência principal: resolver de verdade o ponto 1.**
