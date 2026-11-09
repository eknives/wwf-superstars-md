# b66 (a partir da b65) — md5 037a4213d712fd0e7124bbe5322e1080
b65 intacta. Novidades:

**Golpes básicos do Duggan (arcade, sequências move_seq do port s05-s07)**
- **A = soco** (33 f, poses 40-41), **B = chute** (31 f, poses 42-43). A+B continua sendo correr (como antes).
- Impacto no frame do arcade: soco f24, chute f18. Alcance 40 / 42 px em X e 7 px em Y, só se o Warrior estiver na frente.
- Ao golpear, se o Warrior está perto (±64 X, ±24 Y), o Duggan se vira para ele. Olhando para a esquerda os golpes usam H-flip.
- Só a partir do chão normal (não nos córneres, fora do ringue, correndo nem no rebote).

**O Warrior recebe golpes (ainda não golpeia)**
- Soco → reação do arcade (pose 44, 13 f). Chute → curvado (pose 45, 41 f).
- Dano acumulado: soco 1, chute 4; ao chegar a 8 → **derrubada**: curvado → deitado (111/112, ~74 f) → de joelhos (115) → **atordoado** (116/117, ~96 f) → em pé.
- O dano acumulado se perde após 3 s sem receber golpes. Deitado não recebe golpes.

**Orientação do Warrior**
- Em pé: sempre olha para o Duggan (como na b65).
- Recebendo golpe / deitado / de joelhos / atordoado: **não se vira** (fica como caiu) e não se move nem segue.
- Córneres: o Warrior ainda não sobe nos córneres, então a regra dos córneres ainda não se aplica (fica pronta para quando ele subir).

**START**: igual à b65 (segue / para, andando com animação). Durante golpe/derrubada não se move; ao levantar volta a seguir se estava no modo seguir.

VRAM do Warrior ampliada para 48 tiles (1680-1727; antes 44) para a pose 44.
Sem mexer: Macho, Hogan, árbitro, cordas, câmera, HUD, som.
Shots: shots/b66_punetazo_reaccion.png, b66_patada_derribo.png, b66_tumbado.png, b66_atontado.png, b66_contact.png. Teste no MAME: test/t66.lua.
