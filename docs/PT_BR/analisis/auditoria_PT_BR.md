# Auditoria da análise (31-10-2026)

Amostra: 38 entradas de R (12 da primeira metade por endereço e 26 da segunda; semente 20261031, tools/audit_sample.py). Releu-se cada uma inteira em arc_rec.dis. 6 delas são entradas de "dados" (bem descartadas).

## Resultado (32 rotinas de código)
- OK: 24.
- Erradas: 4 (12,5 %). Além disso, apareceu outro erro fora da amostra (0x1E62).
  - 0x22040 choque_poste: a condição do dano estava invertida. O código causa dano se a ação ≠ 8 OU se é a ação 8 com sub 0xA, e a anotação dizia «ação 8 salvo sub 0xA». ATENÇÃO: o comentário do port (s66 wip19 main.c, linha 124) copia a versão errada («act != 8 || a45 != 10»). Não mexi no port.
  - 0x230FC fondo_anim_publico: a condição era a contrária. Sai se 1C1890 == 1.
  - 0x945C correr_init: o ângulo é 0x40/0xC0, não 0/0x80.
  - 0x8AD8 intro_escena: 0x25408 é a cortina de transição, não a «música 1».
  - 0x1E62 (fora da amostra): 0x24B54 é o fade de paleta, não texto.
- Incompletas: 4.
  - 0x4000: faltava a condição por 1C0027.
  - 0x1EC44: faltava o ramo da CPU.
  - 0x20D60: dizia só «Idem».
  - 0xE2CC: falta a chamada a 0xE7E8 (fica assim, é menor).
- Cobertura: 0x73E8–0x7478 (escolha ao acaso com 0x450A) já tem entrada própria (tfuera_azar).

Tudo o que foi dito acima está corrigido em tools/anot2.py (cópia em anot2.py.bak_auditoria) e regenerado.

## NÃO CONFIRMADO
- 0x6BA0: passa a C. O Emilio viu no arcade que são os flashes de câmera do público.
- Continuam NÃO CONFIRMADOS 0x1F86 e 0x7E4A (falta vê-los no MAME).

## Discrepâncias com o port s66
sistemas/discrepancias.md estava desatualizado. O contraste foi feito em sistemas/discrepancias_s66.md contra s66/wip19/main.c (sha256 3d216c78…). Voltei a conferi-lo no código:
- Kick-out próprio: C. As linhas 292/396 dizem que os kick-outs são sempre o parceiro.
- Energia 0 → 13/16: C. Linhas 322 e 410: `(random()&15)>=3`.
- lieBand e/12: C (linha 366).
- Tempo no chão /2 e +0x20 de fora: C. Não existem no port.
- Relógio: C. Não há nem rastro.
- Contagem fora do ringue: C. Não há nem rastro.
- Driver de som: C. A linha 124 diz que só se guarda o id.
- random() em vez de 0x450A: C. O público já usa um rng privado com s67 (CA_RNG=0); a IA e o pin usam random().
- Continuam V (precisam do MAME): a energia inicial 55 da CPU e a regra de cobrir com energia < 16.

## Recomendação
Com 12,5 % de erros e outros 12,5 % de anotações incompletas, todos os erros são de leitura rápida: condições invertidas e nomes de sub-rotinas presumidos. Recomendo reler inteira a segunda metade (≥ 0x13000). Antes, é preciso conferir sobretudo duas coisas: os saltos condicionais e que os nomes das sub-rotinas chamadas coincidam com sua entrada em R.

## 0x7E4A (acompanhamento)
1C078E é um objeto que se pode pegar e arremessar de fora do ringue (id 1). Usam-no 0xE2CC (arremessá-lo), 0xE234 (quebrá-lo) e 0xE6E0 (passa a id 2 e cria 1C089A).
Nos combates 4/9 (os do André, segundo o Emilio) não é criado, e além disso desativa-se toda a lógica de pegar objetos (0x1A6C0, 0x1CDA8 e 0x1C90E).
A hipótese de que é retirado porque o André precisa da VRAM ou da paleta não está provada. O código o decide pelo número do combate.
Continua NÃO CONFIRMADO que objeto é visualmente. Mr. Fuji fica descartado.

## Releitura completa (índices 0–483), 31/10/2026
Método: desmontar cada rotina de novo e compará-la com sua anotação. Fixes em tools/reread/fixes1–12.py; aplicam-se com tools/reread/apply.py, que já respeita as linhas com várias entradas.
- Primeira metade: 31 correções. Segunda metade: 24 correções (fixes9–12) mais a entrada nova 0x73E8.
- Bugs do jogo original: 0x19D96 (movea.w), 0x1BD5C (escreve d0 em vez de d1), 0x1BEE4, 0x1D0E2 (a energia não é levada em conta).
- Condições que estavam invertidas nas notas: 0x1AE44, 0x1B7FA, 0x1B88C, 0x1B120, 0x23406, 0x244EE/0x24554 (restauração de pose).
- Renomeações: 0x21420 cuerda_dibujar_1 (antes era retrato); 0x21A4E… textos_luchadores/texto_*; 0x2553C txt_destino_abs; 0x25570 txt_desplaz_tile; 0x73E8 tfuera_azar.
- NÃO CONFIRMADO: nomes dos textos de 0x21BB8 (tabela de letras sem decodificar); qual de lim_fuera/lim_ring está ao contrário em 0x244EE; significado de 0x4000/0x8000 em 0x26548; laço sem fim de 0x740E se 1C0069 estiver cheio; 0x74C4/0x7552; banco 0x0F cadeira.
