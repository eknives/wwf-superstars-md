# b88 — só sentido da queda e revisão gráfica do Clothesline
ROM: `wwf_b88.bin` — MD5 `96371335c6b9cb43b08d158ba73ec488`. Base b87 intacta.

## 1. Queda — SIM, verificada no MAME
**Erro:** a b87 chamava `clFallStart(o,rnd)`: arremessava o rival no mesmo sentido e escolhia o espelho contrário. Agora usa `-rnd`.
Arcade: 12F16/12F1C copia a orientação do atacante para o rival e muda o bit7; 9B9A/9BC6 aplica ±32 px; 27D2/2964 aplica vx=±0x80. Resultado: atacante →, rival ← (e vice-versa), 32 px iniciais + 1 px/tick. 9E4C/A8BE e ABBC: 15→16→17, queda **de barriga para cima**, cabeça em direção ao atacante. Não se muda para uma pose de bruços.
Testados Duggan e Warrior como atacante/vítima, esquerda/direita. Os CSV registram deslocamento e H-flip: rival Hflip=1 ao atacar para a direita, 0 ao atacar para a esquerda.

## 2. Animações — SIM, verificadas nos casos testados
**Segundo erro:** a conversão da b87 perdia o banco de paleta de cada bloco e coloria as extremidades emprestadas do rival com as cores do atacante. Corrigido por bloco: fonte 2=Warrior, 7=Duggan; o arcade seleciona a paleta efetiva por ator em 46A0. Sem mudar `spr_pal.bin`.
Tabelas 6CD8: bancos 0/3. 1302E/12EF6: 1D0,1D1, captura 1D2/1D5,1DB,E,F; 1DA se não captura. Vítima: 15,16, rebote 16, chão 17. Ordem e flip contrastados; seus tempos não foram alterados.
**38 comparações exatas de pixels**, após a correspondência de cores MD existente, contra os sprites realmente emitidos pelo MAME (RAM 100000). Além disso, **20 poses carregadas** comparadas palavra por palavra com a VRAM real do VDP e a paleta CRAM: 0 diferenças. Levaram-se em conta os dois refrescos de atraso entre estado lógico e desenho.

## Evidência e limites
`verify88/RESULTADO_b88.txt`, CSV, scripts e dumps SAT. PNG emparelhados contato/voo/chão: `shots88/Duggan_R_comparacion.png`, `Duggan_L_comparacion.png`, `Warrior_R_comparacion.png`, `Warrior_L_comparacion.png`; também `par_*` e `pixels_*`.
Só muda o sinal do arremesso e a conversão/carga gráfica destas poses. Prefixos de gráficos anteriores, logo WWF, córneres, socos e demais recursos intactos. Não se corrigem nem se ampliam as colisões/cordas/energia pendentes da b87. Testes NTSC MAME; **b88 ainda não testada no Everdrive**. A igualdade de pixels indicada é após a conversão para a paleta MD, não igualdade RGB de ambas as plataformas.
