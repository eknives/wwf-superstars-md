# b51 (a partir da b50)
ROM: wwf_b51.bin  md5 328134aa6dde7116b2ac863ecea7eb29
- Cordas laterais (esq. e dir.) do arcade (frames da b45/b46) no plano A alto, em coordenadas do fundo (arcade x+32, y+16). Sem a corda horizontal de baixo.
- A = rebote na corda esquerda, B = rebote na corda direita. Horários do arcade da b45 (84 passos, 1 por frame), como na b46.
- Fundo no plano B baixo (b50: cartaz, margens, HUD vazio).
- Câmera: direcional; C = rápido (A/B já não aceleram). START+A/B/C = público como na b49.
- Cordas: 356 tiles na VRAM 1120+, PAL2 + PAL3 (3-9); o pool do fundo baixa para 1100.
- Pendente: córneres incompletos em alguns estados (limitação da b45).
- Shots: shots/0001-0002 = dir. rebatendo, 0003-0005 = esq. rebatendo, 0006 = repouso.
