# Pendências de implementação — por prioridade

Não autoriza mudanças. Estado na b95; sintomas relatados pelo Emilio sem teste novo são marcados como tais. A pesquisa não resolvida está separada em ESTUDIAR.md.

## ALTA — fidelidade funcional / foco no Duggan

- **Golpes ainda ausentes (excluídas as cadências de prioridade BAIXA)** do inventário `01_port_sgdk/actual/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`: Duggan High Knee, Body Slam, Headlock, Bulldog, Back Suplex, Back Body Drop, Dropkick contra quem está correndo, Pick Up e Dropkick do córner; Warrior Shoulder Tackle, Body Slam, Headlock, Gorilla Press, Atomic Drop, ataques contra quem está correndo, Pick Up e Dropkick do córner. O inventário b89 é histórico; consultar o b92: o Knee do Warrior e a energia avançaram na b90/91; o Stomp do Duggan na b92 passa nos testes; Elbow no chão/córner funcionais, com cadência pendente, exclusivamente BAIXA.
- **Energia frente a pin/kickout e levantar:** integrar as regras nativas que a b90/91 ainda não cobre fora do Knee. Zero não é KO; não estender indiscriminadamente o AF66 nem o bloqueio de escape com energia zero. Fonte: estudo de energia §§ Energia baixa / Diferenças; `NOTAS_b90.md`.

## MÉDIA — erros visuais/sonoros e cobertura de variantes

- **Público: som picotado**, relatado pelo Emilio; revisar reprodução/mixagem e comparar com o arcade antes de corrigir. Não diagnosticado de novo neste backup. Ver a análise de som/público e as notas históricas.
- **Macho verde**, relatado pelo Emilio; corrigir só depois de conferir fonte/paleta/banco. Não é apresentado como problema já medido nem como mudança autorizada em outra versão.
- **Lacunas da clothesline:** faltam variantes de costas/cordas e a cobertura completa de ligações/reações; a b88 corrigiu o sentido da queda e a paleta, não todas as variantes. Ver o inventário b89, NOTAS_b87/b88 e o estudo de energia. Não reabrir o contato já corrigido sem evidência.
- Completar a cobertura natural do Knee/seleção: outros córneres, limites, rivais, jogo sem fixtures e hardware. A normalização específica do lado de fora e o flicker da seleção ficaram corrigidos/verificados na b91 e não são listados como falhas abertas.

## Depois da b93 (orientação do rival deitado corrigida)
- **Sem verificar na b93:** derrubada natural na luta→Knee/Elbow (só fixtures equivalentes), córner pelo lado oposto (sem dados do arcade), PAL, Everdrive.

## Depois da b94 (deitado no X do arcade + pin)
- **Escapar/contagem vs MAME arcade:** só conferido com o código B012/B0A0; o fixture do arcade sem árbitro não conta.
- **Aproximação do pin:** deslizamento 513/514 histórico (arcade: 7E fixo no X final, Z207). Inversão da 513 por convenção de conversão (flip0), não medida pela silhueta. Salto do Duggan não medido.

## Depois da b95 (corrida por tick do arcade, fundo por DMA, choque contra a corda)
- **Estender o arcTick ao resto da lógica (anotado, NÃO autorizado):** andar, arranque da corrida (3 frames), rebote rn 2 (trilha de 48 f), freada, clothesline e quedas (fs avança a cada 2 voltas com `fsTick`) continuam por frame do MD; em PAL/NTSC ou com frames perdidos, o ritmo delas difere do arcade.
- **Frames perdidos correndo entre as cordas:** 40/580 na b95 (b94 55); não é o streaming (córneres já 0–3/580). Causa não investigada (suspeita não medida: `ropeDraw` por CPU / carga de sprites).
- **Sem verificar na b95:** choque contra a corda em arremessos/clothesline (sub 1, fixture do port: rebate W 627→659, D 906→874) e derrubada por golpes perto da corda (soilNudge 875/893 revisado só no código) frente ao MAME arcade; frames perdidos em PAL; hardware real/Everdrive. O som 0x29 da aterrissagem do 9F02 não existe no port (não acrescentado).
- **Limite direito do ringue:** `RING_XR` 917 do port vs 920 do arcade (21E5A); só o choque novo usa 920−e. Não alterado.

## BAIXA — polir no final

- **Cadência do Knee Drop do córner — PRIORIDADE BAIXA, «polir no final».** Arcade **8/18/10 refreshes** frente aos registros do port b91 **K11/19/7, P5/19/14**. São amostras da pose carregada, não uma certificação visual atômica. A b91 NÃO resolveu este ponto; descartou os experimentos de relógio/render. Em NTSC/PAL é preciso manter o tempo real de 57,44485 Hz, sem impor contagens idênticas a 60/50 Hz. Fonte `01_port_sgdk/actual/NOTAS_b91.md:6–12`, CSV por refresh e experimentos etiquetados. Não bloqueia as prioridades acima.

- **Cadência visível do Elbow Drop do Duggan, chão e córner — PRIORIDADE BAIXA, «polir no final».** A b92 já foi entregue. Física/contato/danos/A2 verificados; o visível ainda é desigual: NTSC chão 10/17/12, córner P 9/21/5, K 6/19/12 frente aos 8/18/10 nativos antes da conversão. Não reabrir a ROM nem mexer no Warrior por causa desta anotação. Fontes NOTAS_b92.md e pose92_refreshes.csv. Fica junto da pendência do Knee do Warrior do córner.

## CONCLUÍDO NOS TESTES DA b92
Stomp: zonas 23/24, dano 1, impacto 15A sem refiltro, conversão NTSC/PAL. Elbow: física/contato/A2/dano/erro e córner P/K, NÃO a cadência visível. Cobertura natural/lado de fora/outros córneres pendente.

## CONCLUÍDO NOS TESTES DA b93
Orientação do rival deitado: sem espelhamento deitado→A2→espera em 16 casos; contatos = arcade (Duggan stomp/elbow/espelho/em cima/córner P/K; Warrior cabeça esq./dir., em cima, córner K/P, lado de fora). Traço da clothesline idêntico ao da b92.

## CONCLUÍDO NOS TESTES DA b94
Deitado sem lyoOf: zona do pin sobre o torso visível, Knee/Elbow sobre a cabeça; varredura B = arcade (W/D, ambas as orientações); sem salto deitado→A2 nem 114→115; pin do Duggan pela zona do corpo CB75; quem cobre no X/Y/Z e na orientação do arcade.

## CONCLUÍDO NOS TESTES DA b95
Corrida = arcade em NTSC e PAL (W 200,5/199,7–200,1, D 194,0/192,6–193,0 px/s; arcade 201,1/193,9). Lentidão perto dos córneres resolvida (20/14/18/19 → 3/2/1/0 frames perdidos de 580; 0 erros de fundo). Escapar perto da corda = arcade em Xv 760/728/708/693/832 (choque 9E78→9CD0→9F02, sem salto do soilNudge).
