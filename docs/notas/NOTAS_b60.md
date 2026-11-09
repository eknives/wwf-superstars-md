# b60 (desde b59)

ROM: `wwf_b60.bin`  md5 `5986c9c1f2a51854b2ebda56407ce6a0`

b59 intacta (md5 `9147ee11d533442397987e165520be45`). Sin cambios de paleta.

## Cambios (solo src/main.c)

1. Macho dentro del ring: `ptX[0]=652`, `ptY[0]=300` (antes apron 602,338). Pose 449 igual.
2. Macho se dibuja como el árbitro: HIGH + zonas (morada/naranja, troceo en cuerda frontal) + piezas en HUD → LOW.
   Orden por pies de 3 actores (Duggan / árbitro / Macho, menor = delante; burbuja de 3).
   Rama del árbitro generalizada (`who==2` → pose 449, tiles `ptT[0]+toff`, sin flip).
3. Hogan igual: (939,280), LOW, pose 450, amarillo cálido de b59. El bucle de relevo solo pinta q=1.
4. Macho estático: sin colisión ni IA; el árbitro no lo rodea (refAvoid solo mira a Duggan).

## Test

Arranque OK. Shots: `shots/b60_idle.png`, `shots/b60_macho_dentro.png`, `shots/b60_hogan_dcha.png`.
