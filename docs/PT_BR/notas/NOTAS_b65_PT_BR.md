# b65 (a partir da b64) — md5 ae934feebe83857623862ca7123f43b3
b64 intacta. Só se acrescenta o **Ultimate Warrior**:
- Aparece em pé dentro do ringue (660,262), pose idle do arcade 6.
- **START sozinho** (apertar e soltar sem A/B/C) = o Warrior te segue; START de novo = fica parado. START+A/B/C continua sendo o público como antes.
- Ao seguir **anda com a animação do arcade** (poses 69-72, move_seq 704, 8 f cada uma), velocidade ~2,5 px/f; parado = pose 6. Olha para o Duggan (H-flip do arcade).
- Distância de seguir: 40 px em X / 20 em Y. Clamp dentro do ringue (margem 8).
- Sem luta, sem IA, sem colisão (pode se sobrepor ao árbitro/Duggan).
- Ordem dos sprites pelos pés entre Duggan, árbitro e Warrior; prioridade: ALTA, dividido LOW sob a corda da frente (como o árbitro).
- Paleta: linha 2 (a do Duggan, que já é a paleta compartilhada Duggan+Warrior do port). Linha 3 (Macho/Hogan) sem mexer → Hogan igual.
- VRAM: Warrior no tile 1680 (0xD200, espaço livre da window), 44 tiles.
Sem mexer: Duggan, Macho, Hogan, árbitro, cordas, câmera, HUD, som.
Shots: shots/b65_sigue_andando1/2.png, b65_sigue_arriba.png, b65_contact.png. MAME OK.
