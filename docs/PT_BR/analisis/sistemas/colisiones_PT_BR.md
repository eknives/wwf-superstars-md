# Sistema de colisões (0x1657E)

Lido inteiro no marco de 75 %. Tudo nesta página está confirmado (C) salvo indicação.

1. **Laço** (0x1657E): é chamado a cada frame. Põe +0x40 a 0 nos 4 lutadores e percorre os 6 pares da lista 0xEA4C (0x165B2).
2. **Reinício de vítimas** (0x165FE): quando muda a pose, +0xCE volta a 0. Assim um mesmo frame ativo não golpeia duas vezes a mesma vítima.
3. **Filtro de proximidade** (0x16634): |dx| < 0x60 e |dy| < 8, o mesmo +0x19 (< 2), nenhum agarrado (ação 0x10), etc.
4. **Caixas de golpe** (0x1672C): a tabela 0x1761E[pose] dá uma lista por frame. Cada caixa: prioridade (+0), dano (+1), caixa de ataque (+2), caixa de defesa (+6), caixa alternativa (+0xE) e tabela de reações (+0xA).
5. **Impacto** (0x16796): requer prioridade do atacante ≥ defesa, sobreposição em x (0x16C60) e em z (0x16CA8), e que a pose da vítima seja golpeável (0x172FA). Então:
   - escreve a reação em +0x40 (com +2 se o golpe é pelas costas) e a sub em +0x44;
   - o dano vai para +0x3E (0 contra a CPU com as subs 0/1);
   - há ajustes especiais para o id 7 (0x169C2, 0x16AD4, 0x16B2A, 0x16C14);
   - golpe contra golpe (0x16B6A): anulam-se;
   - agarre (+0x40 = −2): os dois ficam ligados.
6. **Choque de corpos** sem golpe (0x16DF8): os dois vão para a ação 0x11.
7. **Som e combo** (0x16CF4): as tabelas 0x175CE e 0x17590 enchem o acumulador +0x48. Seu temporizador +0x46 vale 0x30 frames.
8. **Aplicação** (0x162A0, no laço do lutador): ação = +0x40; dano extra se está deitado (0x1638E), ×2 com +0xF9 bit0; 0x16488 subtrai a energia e soa 0x22/0x23.
