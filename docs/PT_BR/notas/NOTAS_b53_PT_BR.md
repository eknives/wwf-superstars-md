# b53 (a partir da b52)

ROM: wwf_b53.bin  md5 61a87b67e3fbb6df3b64dd7362789db2

- Base b52 intacta no visual: mapa 88×68, fundo no B baixo, cordas (laterais + horizontais da frente) no A alto, público, rebote A/B. Som picotado: sem mexer.
- Duggan controlável (walk / run A+B / rebote na corda / exit-enter pelas laterais e por baixo / subir nos córneres). O controle move o Duggan; a câmera o segue (arcade→scroll b52: cx≈camx+96, cy≈camy+32). Sem luta nem IA (stub dormente).
- Caixas vazias do HUD: bake −4 px para a esquerda (tile-bake; o CRT RGB come a borda esquerda). Mesma janela.
- Prioridade dos sprites (esquema de cores s49 do Emilio; HIGH quase sempre):
  - VERDE: HIGH por padrão dentro do ringue / avental da frente.
  - ROXO: LOW dentro, na altura das cordas horizontais de baixo (divide a peça se cruzar rl=ROPE_FRONT_R0).
  - LARANJA: HIGH se dentro; LOW se fora perto das laterais (corda na frente).
  - Córneres: muro; subir = HIGH. Cruzando sx: dentro conforme x vs corda.
  - Fundo no B baixo; plano A baixo vazio. Ordem futura da SAT: jogador, oponente, parceiro J, parceiro O, árbitro.
- Paletas: PAL2 = spr_pal (Duggan); PAL3 = palR3 (cordas remapeadas + HUD). VRAM: pool de tiles 16..1015, sprites em 1016 (72 slots), cordas 1120+.
- Controles: direcional andar; A+B correr; manter contra a lateral = sair/entrar; BAIXO no córner de baixo = subir; CIMA no córner de trás = subir; A/B+START disparo do público (b52).
- Shots: shots/b53_walk.png, b53_side.png, b53_run.png, b53_mat.png (+ série 0000–0009). Smoke no MAME OK; não testado em hardware.
