# b52 (a partir da b51)
ROM: wwf_b52.bin  md5 7c3254185b41c1494120155d126850e7
- Câmera equilibrada: mapa 80x68 -> 88x68 (+8 colunas = 64 px à esquerda, tiradas do fundo do arcade, mesmo método do preenchimento da b50; 242 tiles novos em ex52_tiles). Limites cx 0..448. Margem do córner até a borda: esq. 162 px, dir. 165 px.
- Público (crowd_b52.bin) e cordas deslocados +8 colunas; zonas do público ajustadas (camx -64).
- Cordas horizontais da frente (vermelha/branca/azul + córneres) de ring_edit/ring_cuerdas_planoA.png, no plano A alto, fixas. Nas células das laterais elas se misturam com cada frame do rebote.
- As horizontais de trás já estavam no fundo (plano B); não são alteradas.
- A = rebote esq., B = rebote dir. (igual à b51). C = rápido.
- Cordas: 391 tiles na VRAM 1120+. Cores das horizontais ajustadas à paleta das cordas (5 tons aproximados).
- Conferido: assets na ROM (byte a byte), o MAME inicia, shots/b52_test.png (esq. no limite, rebote A, dir. no limite, rebote B).
- Som picotado: sem mexer.
