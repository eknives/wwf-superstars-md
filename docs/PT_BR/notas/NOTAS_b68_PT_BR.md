# b68 (a partir da b67) — md5 3a41cd79ddf5d3b669c0475ca56ca20c
b67 intacta (md5 593ceefe80133aeb5b5e737fd1ec7807).

**Erro da b67 (reconhecido):** as poses 111/112 foram copiadas da 120, que é o **Duggan** deitado (calção azul, malha branca, barba castanha). A captura «de bruços» mostrava o Duggan duas vezes e o rótulo era falso.

**Correção:**
- Nova pose MD **626** = Ultimate Warrior **de bruços DE VERDADE**, tirada do banco do arcade **0 (Warrior)**, pose 157. Cabeça completa (cabelo loiro), costas, calção, botas roxas; 4 peças, 39 tiles, paleta linha 2.
- Cores: o mesmo mapa arcade→MD que a pose 114 já usa (Warrior de barriga para cima, verificado pixel a pixel contra a pose 23 do arcade, coincidência de 100 %).
- Sequência de derrubada: curvado 45 (8 f) → **de bruços 626 (6 f)** → **hold de barriga para cima 114 (68 f, Warrior)** → joelhos 115 → atordoado 116/117.
- `wrDown` passa a u16 (626 não cabe em u8). O Warrior já não usa 111/112/120 (Duggan) em nenhum momento.

**Verificado a olho no MAME:**
- `shots/b68_boca_abajo_WARRIOR.png` (+ _x3): deitado de bruços = **Warrior** (cabelo loiro, botas roxas); em pé = **Duggan** (barba, calção azul) finalizando o chute.
- `shots/b68_boca_arriba_WARRIOR.png` (+ _x3): deitado de barriga para cima = **Warrior** (pintura facial, cabelo loiro); em pé = Duggan.
- `shots/b68_pose626_vs_114.png`: as duas poses isoladas.
(No teste o Warrior é colocado mais acima no ringue para que a corda da frente não o cubra.)

Sem mexer: golpes A/B, START seguir/parar, orientação, Macho, Hogan, árbitro, cordas, câmera, HUD, som. O Warrior ainda não golpeia.
Teste no MAME: `test/t68.lua`. Ferramenta: `tools68/addfd.py`.
