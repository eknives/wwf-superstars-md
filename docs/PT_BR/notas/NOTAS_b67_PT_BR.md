# b67 (a partir da b66) — md5 593ceefe80133aeb5b5e737fd1ec7807
b66 intacta (md5 037a4213d712fd0e7124bbe5322e1080). Novidades:

**Queda normal = de barriga para cima (pose 114)**
- O hold da derrubada usa a pose do arcade **114** (de barriga para cima), não o substituto incompleto de bruços.
- Sequência: curvado (45, 8 f) → de bruços breve (111, 6 f) → **hold de barriga para cima 114 (68 f)** → joelhos 115 → atordoado 116/117.

**De bruços com a cabeça completa**
- Na b66 as poses 111/112 (t0=4080/3832, nt=34) saíam **sem a cabeça** (falta um tile/sprite).
- Na b67 a 111 e a 112 copiam a pose **120** do mesmo banco do Warrior (t0=4414, nt=46): mesmos 5 pedaços, cabeça incluída.
- Revisadas as poses de derrubada/golpe/chão (45, 111, 112, 114, 115–117): a 114 já trazia os 5 pedaços (nt=49); 111/112 eram as incompletas.

**Orientação corrigida (inverter o flip)**
- Idle 6 olha para a **esquerda** sem flip. Antes `wrFl = (ox < wrx)` o deixava de costas para o jogador.
- Agora `wrFl = (ox > wrx)`: em pé olha **para** o Duggan / o jogador.
- Deitado / atordoado / recebendo: continua sem se virar (como na b66).

**VRAM**
- Warrior ampliado para **56 tiles** (1680–1735) porque a pose 114 pede 49.
- Banco do soco 0 movido de 1728 → **1736** para não se sobrepor.

Sem mexer: golpes A/B do Duggan, START seguir/parar, Macho, Hogan, árbitro, cordas, câmera, HUD, som. O Warrior ainda não golpeia.
Shots: `shots/b67_orientacion.png`, `b67_boca_abajo.png`, `b67_boca_arriba.png` (+ k13/hold). Teste no MAME: `test/t67.lua` / `test/run67.sh`.
