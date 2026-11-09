# Golpes do Duggan e do Ultimate Warrior — estado b92

Atualização do inventário b89 (que continha notas b83), conferida com b90/91 e NOTAS_b92.md. **Sim=utilizável, não é verificação completa com o arcade**; não=ausente; parcial=incompleto. Só foram testados de novo os três ataques autorizados do Duggan e a regressão do Knee do Warrior; os demais estados são herdados, não testes novos. P=A,K=B,C=A+B,Y=troca o controle.

## Controles do FAQ (legenda)

| Símbolo | Significado |
|--------|-------------|
| P / K | Punch / Kick (A / B no Mega Drive) |
| P+K | Correr |
| U+P | Cima + Punch |
| *R / *U | Reversível / irreversível (FAQ) |

---

## Duggan (`"HACKSAW" JIM DUGGAN`)

| Golpe | Input FAQ | Estado | Nota curta |
|------------|-----------|--------|------------|
| Punch | P (1 após 3) | sim | Combo FD70+FD7C por pressionamentos (herdado b87); o despacho nativo do Duggan é diferente, ver estudo de energia |
| Kick | K (1 após 2) | sim | B em pé (`mv=2`) |
| Run | P+K | sim | A+B ou C (b89) → `rn=1`; rebote na corda |
| Clothesline | P na corrida | sim | Colisão no contato + queda do rival 0x17 de barriga para cima (b86–b88, MAME); faltam variantes de costas/cordas |
| High Knee | K na corrida | não | B na corrida não lança ataque |
| Body Slam | U+P no grappling | não | Não há U+A na pegada |
| Headlock | P no grappling | não | Só disputa genérica (b70), sem chave Headlock |
| Bulldog | P a partir do Headlock (*U) | não | Finalização da chave ausente |
| Back Suplex | K a partir do Headlock (*R) | não | Finalização da chave ausente |
| Irish Whip | K no grappling | sim | Após a disputa: `trStart` → arremesso às cordas (ambos) |
| Back Body Drop | P vs quem corre | não | Sem ramo "Against Running" |
| Drop Kick | K vs quem corre | não | Idem |
| Pick Up | P perto da cabeça | não | Pegar o deitado não portado (`NOTAS_b82`) |
| Stomp | P perto do corpo | sim (b92 testado) | Motor nativo do Duggan, zona CB75,159/15A, dano1, arcTick; limites23/24 e sem refiltro conferidos |
| Elbow Drop | K perto da cabeça | parcial (b92) | Solver/poses/reação/dano5 e erro−2 nativos; contatos chão/espelho/variante conferidos. Cadência visível pendente |
| Pin | K perto do corpo | sim | B perto → `pinStart`; contagem do árbitro (b71+) |
| Dropkick (córner, em pé) | P/K do turnbuckle | não | Dá para **subir** no córner; não há ataque lá de cima |
| Elbow Drop (córner, deitado) | P/K do turnbuckle | parcial (b92) | Sub2F, trajetória P/K/dano10/A2 conferidos; cadência visível pendente |

**Duggan:** 7 sim / 2 parcial / 9 não (18 do FAQ; sim = utilizável, não é certificação geral idêntica ao arcade).

---

## Ultimate Warrior

| Golpe | Input FAQ | Estado | Nota curta |
|------------|-----------|--------|------------|
| Punch | P (1 após 3) | sim | Combo FD70+FD7C por pressionamentos, herdado b87; não alterado na b92 |
| Kick | K (1 após 2) | sim | B em pé |
| Run | P+K | sim | Igual ao Duggan (A+B ou C) |
| Clothesline | P na corrida | sim | Igual ao Duggan (b86–b88) |
| Shoulder Tackle | K na corrida | não | B na corrida não ataca |
| Body Slam | U+P no grappling | não | — |
| Headlock | P no grappling | não | — |
| GORILLA PRESS | P a partir do Headlock | não | Finalização ausente |
| Atomic Drop | K a partir do Headlock (*R) | não | Finalização ausente |
| Irish Whip | K no grappling | sim | `trStart` simétrico (trilhas W1E) |
| Back Body Drop | P vs quem corre | não | — |
| Dropkick | K vs quem corre | não | — |
| Pick Up | P perto da cabeça | não | Na zona de chão A → pisão, não levantar (`NOTAS_b82`) |
| Stomp | P perto do corpo | sim | Zona 2 + A → `gs=13` / sub 5 do arcade (`warriorGroundStart`) |
| Knee Drop | K perto da cabeça | sim (b90/91 herdado) | Motor/solver nativos, variante76/77 sem7D, A2 e energia; regressão b92 de contato/energia sim. Sem mudanças na b92 |
| Pin | K perto do corpo | sim | Zona 2 + B se `w82PinOK` → pin do Warrior |
| Dropkick (córner, em pé) | P/K turnbuckle | não | Sobe no córner; sem ataque aéreo |
| Knee Drop (córner, deitado) | P/K turnbuckle | parcial (b90/91) | Contato/dano10 implementados; cadência visível pendente BAIXA «polir no final». Não corrigida na b92 |

**Warrior:** 8 sim / 1 parcial / 9 não (18 do FAQ; estado herdado da b91, sem técnicas novas na b92).

---

## Compartilhados / sistema (contam para ambos)

| Sistema | Estado | Nota |
|---------|--------|------|
| Disputa / lock-up (2 lutas + reverse) | sim | b70: `grTry` / `grStep`; mash → whip |
| Irish Whip às cordas + rebote | sim | Incl. vibração curta ao bater/cair (b78–b81) |
| Queda / deitado / levantar | sim | Reações + get-up (mais lento b70) |
| Golpes no chão | parcial | Duggan motor independente b92; Warrior sem mudanças da b91. Elbow/córner ainda com cadência visível pendente |
| Pin + contagem de 3 + kickout no 1.º pin | sim | Ambos cobrem; árbitro (b71+) |
| Contagem fora 20 / contagem 3 → reinicia a luta | sim | b89: não volta à seleção |
| Tela de título + SELECT PLAYERS do arcade | sim | b89; a escolha ainda não troca os lutadores |
| Subir/descer dos córneres | sim | Finalizações contra o deitado implementadas parcialmente; contra rival em pé continuam ausentes |
| Sair/entrar no ringue (lateral / atrás) | sim | `sx` / `bx` |
| Vibração curta da corda (collide+fall / kickout perto) | sim | b78–b81 |
| IA / rival ataca sozinho | não | Rival só com START (seguir); Y troca o controle (b89) |
| Ataques "Against Running" | não | — |
| Ataques do turnbuckle | parcial | Só finalização contra o deitado; ver limites de cada lutador |
| Pick Up / pegar o deitado | não | Confirmado pendente |

---

## Evidência atual

- Duggan: `src/duggan92.h`, `duggan92_poses.h` e ramos de entrada no main.c. Substituem só suas antigas ativações gs5/gs11; pin e outros golpes continuam.
- Warrior: `src/knee90.h`, `native81.h`, funções warriorGround* sem modificar; regressão de cinco casos.
- Endereços nativos, danos, contatos, cadências medidas e limites: `NOTAS_b92.md`, `shots92/validation92.json`, `pose92_refreshes.csv`.
- Inventário histórico original: `MOVIMIENTOS_DUGGAN_WARRIOR_b89.md`. Não usar seus resumos b83 como estado atual. Energia vs pin/levantar continua pendente; sem IA nova, só START segue.

ROM `d9af08525a0f49f4bdc025ed00499135`.
