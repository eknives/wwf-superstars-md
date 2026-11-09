# b89 — seleção e controles

ROM: `/workspace/b89/wwf_b89.bin`  
MD5: `7c1c5202f5fb27f115278eecd9b9ffb9`  
Base b88 intacta: `96371335c6b9cb43b08d158ba73ec488`. Compilação local SGDK com o PATH/make solicitados, `BUILD_b89.log`.

## 1. SELECT PLAYERS — verificado, com os limites indicados abaixo

- Tela isolada antes do combate, depois do título/START. Retratos, nomes, trama, logo central e cursores decodificados dos dados do arcade, não redesenhados. Cena: `0x704E`, `0x1F434 → 0x2034A`; mapa `0x210A8`; seis blocos 4×4 de `0x20404` (tiles `383–392`, `393–3A2`, `3A3–3B2`, `3D3–3E2`, `3C3–3D2`, `3B3–3C2`). Paleta 4: `0x706C/0x29F6`, tabela BG `0x2FAE`.
- Mesma distribuição 2×3 e posições. Conversão de 4 para 3 bits por canal própria do MD; não se reduzem as cores dos retratos. Reutilizam-se bancos CRAM nos espaços verticais: mudanças ao terminar as linhas MD 95/119/143. A seleção conserva as primeiras 224 linhas do arcade: só se omitem as 16 inferiores de margem, sem escalar.
- Cursores verde 1P / amarelo 2P: tabelas nativas `0x7686/0x782A`, desenho `0x75B6`. Movimento por bordas e sem dar a volta: tabela `0x74F2`. **A confirma**, que já era soco/Button 1; B não confirma, igual ao despacho `0x749E/0x7552`. Não permite escolher repetidos.
- Temporizador invisível `0x180` = **384 refrescos arcade**, `0x7098/0x72A4`. Relógio convertido a tempo real: 6250/6528 por VBlank NTSC, 6250/5440 PAL; teste: chega a zero após **401** VBlanks NTSC e **334** PAL, aproximadamente 6,68 s nominais. Sorteio: módulo 6 e filtro de escolhidos `0x740E–0x742A`; movimento `0x747A`; novos candidatos a cada 16 e confirmação na fase 63/64 (`0x73E8`). A semente MD não reproduz os registradores aleatórios da CPU de `0x450A`.
- Piscada: cores/pens de `0x2048/0x2054/0x205A`, passos de 2 refrescos e duração `0x40`, motor `0x1F5C/0x1F86`. **81 ticks de registradores de piscada comparados com o MAME: zero diferenças** (`flash89_result.txt`). Fechamento de 64 refrescos, ou 112 em versus: `0x7134–0x717A`, verificados.
- Adaptação dos inícios MD: START do controle 1 = solo, você escolhe dois; START do controle 2 = cooperativo, um para cada jogador; ambos START = versus, dois para cada jogador. Os modos correspondem ao fechamento `0x72DA–0x73DC`. **O resultado é guardado mas não modifica o combate: continua Duggan contra Warrior da b88.**
- Evidência gráfica: 12 capturas comparadas com o MAME, **0/57.344 pixels diferentes** após conversão de cor. Outras três só diferem na fase visível da piscada, não nos desenhos; são identificadas assim nos pares. A inicial também verificada em PAL e controle de três botões. Resultados: `verify89/RESULTADO_b89.txt`.

## 2. Contagem terminada → reiniciar combate — verificado

A seleção só é chamada uma vez antes do laço de luta. Conserva-se `countStep/pinAdvance → matchReset` da b88; nenhum reinício volta ao menu. Testes curtos com fixtures de RAM logo antes do terceiro golpe de contagem e da contagem de 20 fora: aparece 3/20, termina a espera existente de 120 frames e ambos os lutadores voltam a X=736/660, contagens a zero, fase de combate=4 durante todo o percurso. Não se simulou uma luta completa para chegar naturalmente a essas posições.

## 3. C=A+B; troca para Y — verificado

Normaliza-se C para A+B **antes de calcular as bordas**; não se acrescenta outra lógica de corrida. Em duas execuções independentes, C e A+B geram **32 instantâneos idênticos dos 100 bytes do lutador**; C corre sem mudar `ctl`. Mesmo resultado com controle de 3 e 6 botões. Y do controle de 6 botões muda `ctl` 0→1→0, uma vez por pressionamento. O atalho antigo START+C passa igualmente a START+Y para que C seja realmente equivalente a A+B.

## Capturas e limites

Em `shots89/`: `pareja_C_initial.png`, `pareja_C_partner.png`, `pareja_C_confirmed2.png`, `pareja_COOP_initial.png`; `md_C_C_run.png`, `md_C_Y_swap.png`, `md_C_pin3.png`, `md_C_pin_restarted.png`, `md_C_ringout20.png`, `md_C_ringout_restarted.png`.

A b88 não tinha título/início: acrescenta-se uma porta START com o título do arcade **estático e reduzido a 16 cores**; não se porta o attract, a apresentação posterior nem a música 0x0A. Após selecionar há restauração/carga do combate; não se afirma que essa transição seja idêntica ao arcade. Também não se afirma sincronia de captura frame a frame nas três imagens com fase de piscada diferente. O MAME avisa de checksum diferente em `24j6-0.112` do set local existente; as comparações são contra esse set. Sem teste no Everdrive/placa física.

Todos os recursos preexistentes de `res/` continuam idênticos à b88 (exceto a lista/declarações de recursos novos). **Córneres superiores e logo WWF do ringue intactos; nenhum outro movimento, IA ou timing de combate retocado.**
