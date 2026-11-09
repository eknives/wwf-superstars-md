# b93 — orientação do rival deitado (base b92)

ROM `wwf_b93.bin`, MD5 **a89af7ed95159c0899430bf0e81f6441** (b92 d9af08525a0f49f4bdc025ed00499135 intacta; sua fonte recompila para o mesmo MD5).

## Mudanças (só os 3 pontos autorizados)
1. `oriVictima(o) = vface[o]^1` (main.c:464): o bit7 de +A do arcade de um rival deitado = o flip com que o port o desenha. O arcade (10A5E/A554) nunca o muda. Usa-se em: zona Warrior C798 (`warriorGroundZone`), `kneeOutsideVictim91`, destino do salto e ajuste de poste (15A6C / ±64), caixa de impacto 10FCC (`warriorGroundStep`), zona Duggan C706 (Stomp/Elbow), cópia de orientação Duggan 10A6C/10BB2, solver e poste Duggan, caixa Duggan.
2. Reação A2 e espera no chão (`kneeVictimStart90` main.c:485 e laço main.c:1467): `dFlip = oriVictima`, `dLyo = 0` (a pose nativa A2 é colocada em Xv igual ao arcade: cabeça em Xv∓40).
3. Sem mexer nas atribuições de `vface` em quedas/golpes, clothesline b88, pin, `bodyX`, `lyoOf`, cadência 8/18/10.

## Verificado (MAME 0.276, genesis NTSC, fixtures de RAM: rival deitado vh=3 com as duas orientações que os derrubes produzem)
- Contatos = arcade exatos (x,y,z,energia): Duggan stomp/elbow/elbow espelho/elbow acima/poste P/poste K/stomp longe/y23 (+y24 e falha −2 iguais); Warrior Knee cabeça esq./dir., acima, poste K/P, exterior. Ver `shots93/validation93.json`.
- Sem espelhamento: o flip do rival não muda de deitado → A2 (846/847/848, 843/844/845) → espera, nos 16 casos (`flip` em validation93.json). Capturas: o cotovelo/joelho cai sobre a cabeça visível; as botas continuam do mesmo lado.
- Clothesline: traço b88 (DL/DR/WL/WR, 147 refrescos, incl. flip/poses) idêntico byte a byte b92 vs b93; 0 erros de tiles.
- Pin: `pinStart`/contador/poses sem mudanças. Pin do Duggan (bodyX) nos mesmos X. O pin do Warrior (zona 2 C798) conserva a geometria arcade (torso_pin 744/760 ori0 → pin) e agora cai no lado visível correto; por isso na b93 seus X em relação a `vface` são os simétricos da b92 (`shots93/pin93_b92.csv` vs `pin93_b93.csv`).

## NÃO verificado / pendente
- Derrube natural em partida (só fixtures equivalentes), PAL, Everdrive.
- Poste pelo lado oposto (sem dados do arcade desse lado).
- Salto visual de ~32 px ao passar da pose genérica deitada 114/752 (com `lyoOf` b74 do pin) para a A2 nativa: a A2 está onde o arcade a põe; o desfasamento é da pose genérica anterior (fora do escopo, não mexido).
- O pin do Duggan usa `bodyX` (invenção da b71, lado dos pés) enquanto o do Warrior segue o arcade: incoerência anterior, não mexida.
- Cadência 8/18/10 (BAIXA, sem mudanças).
