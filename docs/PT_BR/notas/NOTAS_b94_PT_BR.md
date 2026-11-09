# b94 — deitado no X do arcade + pin ajustado (base b93)

ROM `wwf_b94.bin`, MD5 **b2a8ff5d4453067ad3d2bf8762239413** (b93 a89af7ed95159c0899430bf0e81f6441 intacta).

## Mudanças (só os 2 pontos autorizados)
1. **Deitado sem `lyoOf` ±32** (main.c:487 `bodyX=ox`; desenho main.c:1491 `dLyo=0`). A pose 114/626 sem lyo ocupa o mesmo que a nativa do arcade 0x17 em Xv (±6 px). Zonas C798/C706 sem mexer.
2. **Pin**:
   - `pinStart`: `pnX=pnVX=Xv`, `pnM = oriVictima?+1:−1` (BD10/11A72, `neg` se bit7=0), `pnKD=pnM`. As trilhas já levam BEF2: Warrior Xv∓32, Y+1, Z203; Duggan Xv∓36, Y−1, Z174.
   - O Warrior olha ao contrário do deitado (11A8A `+A = rival^0x80`): `dFlip=(pnM<0)` para 514/778, que foram convertidas espelhadas (match69 flip1), e invertido para 513, que é a arc pose 2 sem espelhar.
   - Duggan: o flip continua igual (já coincide com o arcade).
   - Árbitro: `rfX/rfM` o deixam no mesmo lugar em relação ao corpo visível que na b77, sem mudança de coreografia.
   - Entrada do pin do Duggan = zona do corpo C706/CB75 (`dugZone==2`, B, como o Stomp). Retira-se o bloco `bodyX±PIN_ZONE` da b69.
   - Escapar (B012/B0A0) fica em absoluto do arcade: deitado Xv∓8, quem cobre Xv∓48, Y−1, Z+4.
   - Cadência e deslizamento sem mudanças.

## Verificado (MAME 0.276, genesis NTSC vs arcade wwfsstar, fixtures de RAM, Xv=760)
- **Varredura B** d=−88..+88, passo 8, W e D, ambas as orientações. As 4 linhas são IGUAIS ao arcade (`shots94/md/sweep_cmp94.txt`):
  - W o0: K −64..−40, P −32..−16. W o1: P +16..+40, K +48..+64.
  - D o0: K −64..−40, P −32..0. D o1: P 0..+40, K +48..+64.
  - Na b93 o Duggan não coincidia.
  - Com o deitado em Xv, a faixa P cai sobre o torso visível e a K sobre a cabeça (`shots94/clave1_zonas_b93_b94_arcade.png`).
- **Quem cobre** (W 778 / D 499):
  - W X−Xv = −32/+32, Y301, Z203 (arcade −32/+32, 301, 203). D −36/+36, Y299, Z174 (arcade −36/+36,97, 299, 174,5).
  - Lado do ringue 680/860: também ∓32.
  - Orientação por silhueta contra captura do arcade: assento W e aproximação 514 coincidem diretos na b94 (0,79/0,72, contra 0,69/0,55 espelhado); na b93 saíam espelhados. Duggan cobrindo: rosto/braços do mesmo lado que o arcade (visual).
  - Captura: `shots94/clave2_cubriendo_arcade_b93_b94.png`.
- **Sem salto deitado→reação:**
  - 16 casos md94/reg94 (`shots94/validation94.json`): contatos = arcade (16/16); dX e flip constantes com lyo 0 em 114/752→A2→espera. A b93 passava de lyo 32 a 0.
  - Levantar 114→115: também já não salta (a b93 saltava 32).
- **Clothesline** DL/DR/WL/WR: traço e 144 capturas idênticas pixel a pixel b93 vs b94; 0 erros de tiles.
- **Escapar** (1.º pin, W e D, ambas as orientações): funciona, posições segundo a fórmula B012/B0A0.
- **Contagem de 3** (2.º pin): chega a "3" (pnS 3, winK 117).
- **Queda nativa de quem cobre ao escapar:** ao terminar a queda, 114 fica no mesmo dX sem lyo (a b93 saltava −32).

## Efeitos colaterais / NÃO verificado
- **Escapar perto da corda:**
  - Quem cobre sai agora de Xv∓48 (arcade), 32 px mais para fora que na b93. Seu voo de queda (sem mudanças, 70 px) pode passar do limite.
  - Com Xv=760 o0 aterrissa em 642 e o empurrão ACA4 o põe em 675: um salto de 33 px. Na b93 isso só acontecia perto da corda.
  - No arcade não foi medido: a fixture arcade não conta, porque não há árbitro. Fica em PENDIENTES.
- **Escapar/contagem vs arcade:** só contrastado com o código (B012/B0A0), não com o MAME arcade.
- **Pose 513:** a virada sai da convenção de conversão (flip0), não de silhueta medida. São 4 frames.
- **Aproximação:** continua o deslizamento 513/514 (o arcade coloca 7E fixo). O salto do Duggan não foi medido.
- Um frame de atraso pontual do contador durante o pin (lag de emulação; também ocorre na b93).
- Derrube natural em partida, PAL e Everdrive: sem testar.
