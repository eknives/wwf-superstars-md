# b76 (base b75, md5 b2f37978b626d9bd1a072b1e655e7218; b75 intacta)

ROM: `wwf_b76.bin`, md5 `49075e62b6b23d071da6035564adcea8`
Só as 5 correções pedidas. Não foram mexidos a IA, os ataques novos, HOME, os córneres, o logo nem o som do público.
Toda a evidência sai de `/workspace/wwf_sgdk/analisis` (arc_rec.dis, rutinas.md, tools/prog.bin e os bancos de sprites do arcade).

## 1. Soco do Warrior completo
- **Arcade:** o soco é o mov 0x00, em 0xFC84. Usa a tabela 0xFD70 com as poses 0x150 (4 f), 0x151 (3 f) e 0x152 (3 f); 0xFD7C é a alternativa do combo (0x153 a 0x155).
- **Banco 0 (Warrior):** 0x152 é a pose com o braço estendido. Coincide com a referência do MAME 01M6PKH6….
- **Causa da falha:** no port, `xl_w[41]` apontava para a pose 658, que é a 0x150 do banco 0 (preparação, sem braço). Por isso o Warrior nunca esticava o braço.
- **Correção:** acrescenta-se a pose nova 765, convertida a partir da 0x152 do banco 0 com `tools/gen76_punch.py` (mesmo método do gen69). Agora `xl_w[41]` = 765. O Duggan não muda.
- Captura: `shots/b76_01_punetazo_warrior.png`.

## 2. Contagem e árbitro
- **Arcade, números:** o fg0 é desenhado por cima dos sprites (wwfsstar.cpp: bg0 → sprites → fg0) e o texto da contagem vai por 0xE02C/0x2549E. Os números do port já têm o fundo transparente (índice 0, conferido em pin_glyph.bin), então isso fica como está.
- **Causa real de o árbitro «desaparecer»:** `refSideY` (inventado na b73) o mandava para a FRENTE (−73) quando não cabia atrás. Ficava em y < RING_Y0, fora do ringue e coberto pela corda da frente.
- **Arcade:** o estado 2 do árbitro (0xDD4E) vai rumo à dupla (0xDFE0) e a cada frame faz `jsr 0x21E5A` (0xDECC), que é o limite do ringue. Nunca sai.
- **Correção:** o árbitro sempre vai para o lado da trilha (+73) e é limitado ao ringue com `rfClamp`, tanto na contagem quanto ao levantar.
- Capturas: `shots/b75_antes_cuenta_arbitro_fuera.png` (antes) e `shots/b76_02_cuenta_arbitro_dentro.png` (depois).

## 3. Pegada desalinhada (um mais alto que o outro)
- **Causa:** quando o Warrior cobre, a trilha WPIN/WKO não traz Z, então se usa `pinZof` = 174. Ao terminar o kickout, `z0` ficava em 174 e o Warrior aparecia 13 px mais alto na pegada seguinte.
- Reproduz-se na b75 com o teste koW: dZ do Warrior = 174 depois do pin. Na b76 volta a 187.
- **Correção, sem mexer no assento z0=174 do pin:**
  - z no chão nas reações e no chão (0xAB1E e 0xA90E, «z no chão»).
  - z = 0xBB para os dois ao começar a disputa (0xB1D0 + 0x16F58 centrar_pareja).
  - A saída do pin passa agora pela ação 8, que termina no chão.
- A regressão pinC continua igual: `SETTLE z0=174`, `CENTER err=0`.

## 4. Queda contra a corda numa chave (a famosa)
- **Arcade 0xF94C (ação 0xC):** se está dentro do ringue e toca a corda (+0x9E&3, limite 0x21E5A/0x22140), chama 0xF9B0.
- **0xF9B0:**
  - Marca a corda (0x9700, d0=1).
  - Se o rival JÁ NÃO está em 0x10, quem faz a chave passa para a ação 8 sub 1.
  - Se o rival continua em 0x10, só atuam as subs 0x1B/0x21/0x22/07/0x29/0x28. O whip é a sub 0x1E, então ali não acontece nada.
- **Ação 8 (0x99BE, tabela 0x9A14 / parâmetros 0xA74A):**
  - Sub 1 (0x9B7E): impulso 0x10 para trás (0x9BBE), z+0x10 e pose 0x15/0x16 conforme a altura (0x9E4C).
  - Com a corda (0x9CD0) passa para a sub 2 (0x9F02): z ≥ 0xCB, pose 0x16, vx negada. Ao chegar a 0xBB passa para a ação 0xB (deitado).
- **Port:** durante o whip, a partir do momento em que a vítima deixa a ação 16 (0x10) na trilha, se quem arremessa está na borda do trapézio do ringue cai contra a corda e fica deitado. A corda vibra e depois ele se levanta.
- Captura: `shots/b76_04_caida_cuerda_llave.png` (teste MAME `rope`).
- **Limite importante:** a disputa coloca os dois no ponto médio (igual ao arcade, 0x16F58). Por isso quem arremessa só toca a corda se a pegada começa colada nela. No teste força-se x=627 (a corda esquerda em y=300). O arcade também pode chegar empurrando na disputa (+0xAF modo 2/3), mas esse movimento não está portado e não o inventei.

## 5. Escapar do pin, para os dois
- **Arcade ação 0x1E (0xB012), a do coberto:**
  - x ±8, pose 0x9F durante 8 f e 0xA0 durante 4 f (tabela 0xB0EA).
  - Quem cobre fica com a pose 0x9B em x ±0x28, y−1, z+4.
  - Ao terminar, o coberto passa para a ação 5 (levantar) e quem cobre para a ação 8 sub 0x1C, virado (0xB068–0xB084).
  - Sub 0x1C (0x9B66): impulso 0x10, z+0x18, poses 0x9B/0x9C pela altura.
  - Ao tocar o chão com +0x45=0x1C (0x9C5A): x ±0x20 e sub 0xC (0xA4C8: pose 0x16, vz 0x100, g 0x30). Depois a ação 0xB.
- **Poses novas** (tools/gen76_poses.py, bancos 0 e 3):
  - Warrior: 766 9F, 767 A0, 768 9B, 769 15, 770 16, 776 9C.
  - Duggan: 771, 772, 773, 774, 775, 777.
- O deitado de quem cobria dura 44 f, como medido no inventário: "08 34 + 0B 44 + 05 16". Depois se levanta, sem atordoamento. O coberto se levanta (0x5) sem atordoamento.
- Capturas: `shots/b76_05a_zafar_warrior_cubierto.png` e `shots/b76_05b_zafar_duggan_cubierto.png`.

## O que não foi possível tirar do arcade (aproximações declaradas)
- **Gravidade da ação 8:** a sub 1 e a 0x1C não fixam vz nem g. Usa-se a física de 0x3E20 com g=0x30 (o valor que 0xA4C8 põe) e vz inicial 0.
- **Sons da queda** (0x11, 0x29, 0x21): não foram acrescentados.
- **Duração do levantar:** usa-se a pose 115 do port (30 f) em vez dos 16 f da ação 5.

## Testes no MAME (test/t76.lua, run76.sh)
- `pun`/`punD`: o Warrior estica o braço e golpeia.
- `ko`/`koW`: escape completo nos dois sentidos; z0 = 187 no final (na b75, koW deixa dZ = 174).
- `rope`: queda contra a corda.
- `cnt`: árbitro dentro do ringue durante a contagem.
- Regressão t75 `pinC`/`pinSide`: pin_ok, SETTLE z0=174, CENTER err=0.
