# b60 (a partir da b59)

ROM: `wwf_b60.bin`  md5 `5986c9c1f2a51854b2ebda56407ce6a0`

b59 intacta (md5 `9147ee11d533442397987e165520be45`). Sem mudanças de paleta.

## Mudanças (só src/main.c)

1. Macho dentro do ringue: `ptX[0]=652`, `ptY[0]=300` (antes avental 602,338). Pose 449 igual.
2. O Macho é desenhado como o árbitro: HIGH + zonas (roxa/laranja, divisão na corda da frente) + peças no HUD → LOW.
   Ordem pelos pés de 3 atores (Duggan / árbitro / Macho, menor = na frente; bolha de 3).
   Ramo do árbitro generalizado (`who==2` → pose 449, tiles `ptT[0]+toff`, sem flip).
3. Hogan igual: (939,280), LOW, pose 450, amarelo quente da b59. O laço de parceiros só pinta q=1.
4. Macho estático: sem colisão nem IA; o árbitro não o contorna (refAvoid só olha o Duggan).

## Teste

Início OK. Shots: `shots/b60_idle.png`, `shots/b60_macho_dentro.png`, `shots/b60_hogan_dcha.png`.
