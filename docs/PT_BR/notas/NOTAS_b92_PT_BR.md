# b92 — entrega PARCIAL: chão do Duggan

ROM `/workspace/b92/wwf_b92.bin` — **MD5 `d9af08525a0f49f4bdc025ed00499135`**, 1703936 bytes. Base b91 intacta. **Stomp verificado nos ensaios; Elbow chão/poste funcionais e física comparada, mas a cadência visível NÃO é ainda idêntica. Não dar por encerrada toda a tarefa.**

## 1. Stomp — verificado nos casos ensaiados
- C706/C79E–C8A8 e CB6C/CB75: P=A no corpo, mesmo plano, |dy|<24, âncora cabeça Xv±40 e limites estritos originais. 1173A/118BC: 159×14 e 15A×10 refrescos arcade; dano 1 em 117E0 ao entrar em 15A (11782→1179A), sem segundo filtro XY.
- Motor Duggan independente `src/duggan92.h`, relógio arcTick existente sem modificá-lo. Mantém 7 ticks de 159 e 5 de 15A contando a saída. MAME 57,444852941 Hz, tick=2 refrescos; o MD conserva tempo real, não copia 14/10 literalmente a 60/50 Hz. Amostra NTSC 15/11, PAL 13/8; compatíveis com conversão e quantização.
- Entrada normal, |dy| 23 aceito / 24 rejeitado e rival deslocado para X900 após iniciar: mesmo dano 48→47 no MD e no MAME. Impacto normal (744;300;187). Reação A2 comparada.

## 2. Elbow na cabeça — PARCIAL
- CB72, sub11→10A5E por FB9C; tabelas 11180/11188→111F0, poses 11372: 61/62/1CB/1CC, variante 1CD/1CE. Holds nativos iniciais 8/18/10 refrescos. Solver 159AC, integração 3DCE/3E20: Vz0x500, gravidade 0x50 por refresco; limites 0x2000. Desvio interior 64, exterior 32; orientação da vítima, não a regra Vx do Warrior.
- 11084/110BC/110C0: descendo e altura≤chão+16, ponto Xa±8,Ya+4 contra o retângulo nativo. O impacto conserva frações: Yword=Yv−1, Zword=chão; sem 7D nem choque de corda artificial (24102→24322, 24106→24324 são RTS). Dano 5 (10DC0), A2 (A554/28EC).
- Contatos exatos MD/MAME: normal (697;299;187), espelho (823;299;187), variante (697;299,375;187), energia 48→43. A2: 4/7/9/10/10/9/7/4/0, comparação de RAM de ambos. Falha 10C6A: −2, recuo 24 conforme a orientação, 1CF→16→17→1A (9FCC/AF66/AA00); contato de falha (672,0625;300), 48→46.
- **Pendente a cadência visível:** NTSC 61/62/1CB=10/17/12 frente à conversão esperada 8–9/18–19/10–11. Espelho 10/18/10; variante 9/18/10. PAL também tem discrepâncias. A lógica usa arcTick, mas não certifica a duração visível; ver `pose92_refreshes.csv` e PNG consecutivos.

## 3. Elbow do poste P/K — PARCIAL
- F6EF=`2F,20,20`, despacho FC14→10A5E. Mesma física/poses do Duggan, ajustes 10B5E/110E4. Dano 10 (10DCC); falha nativa compartilhada, não um novo salto genérico.
- P e K conectam no MD/MAME (694,34375;299,8125;187,5), Vx399, Vy−462, energia 48→38 e A2. **88 estados estáveis de trajetória** chão/espelho/variante/poste coincidem; 0 sem amostra.
- **NÃO resolvida a cadência visível:** NTSC P 9/21/5 e K 6/19/12; arcade 8/18/10 antes de converter a frequência. PAL P 4/18/7, K 8/18/5. Não se corrigiu o render global nem o poste do Warrior. Ensaio de SAT privada descartado: `tools/experimental_sat92*`, NÃO compilado. Causa precisa CPU/DMA/publicação ainda não isolada; não se atribui gratuitamente a nenhuma delas.

## Evidência e limites
- MAME 0.276: arcade `wwfsstar`, MD `genesis` e PAL `megadriv`, dez casos breves por região, fixtures de RAM + botões reais. `shots92/validation92.json`, `arc_frames.csv`, `md92_knee_frames.csv`, `pal_md92_knee_frames.csv`, `trajectory92_compare.csv`, `pose92_refreshes.csv`. Scripts em `tools/`.
- PNG: `comparativa92_stomp_impacto.png`, `comparativa92_elbow_{vuelo,impacto,reaccion}.png`, `comparativa92_elbow_mirror_impacto.png`, `comparativa92_elbow_above_impacto.png`, `comparativa92_corner{P,K}_{vuelo,impacto,reaccion}.png`, `comparativa92_miss.png`. Fases comparáveis, câmeras/refrescos NÃO sincronizados; não são certificação pixel a pixel de paletas. Sequências `refresh_{stomp,elbow,cornerP}_f*.png`.
- Regressão do Warrior: mesmas funções/headers e render original, mesmos contatos/energia que a b91 em chão, variante, poste P/K, exterior. A cadência de poste já irregular permanece: amostras em `warrior92_refreshes.csv`, NÃO se afirma igualdade visível. Não se testou Everdrive, partida completa, todos os córneres, exterior do Duggan nem falha a partir do poste.
- Só muda main.c para entrada/motor do Duggan, novos `duggan92.h`/`duggan92_poses.h`, e apêndices de tabelas/tiles com 12 poses do banco 3 (6CD8/7FE2; conversor `tools/gen92.py`). Prefixo gráfico anterior idêntico. Resto de res intacto, Hogan/córneres/logo/seleção/energia alheia/Warrior sem editar. `source92_main.diff`, `b91_manifest92.json`.
- Arcade CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; o MAME conserva o aviso de CRC do fundo 24j6-0.112. Não se empacota a ROM arcade no backup.
- **Fora do escopo na ROM: nada intencional. Pendência principal b92: cadência visível do Elbow; não substituir esta limitação pela coincidência lógica.**
