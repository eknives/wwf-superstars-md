# b50 (a partir da b49)
ROM: wwf_b50.bin  md5 68f778ed3bbc111e38fa0ebeb78e93df
- Cartaz: o rosto de cima à direita tinha o pedaço de baixo (linhas 10-11, col 38-41) de outro rosto (id 3). Colocado o pedaço correto do Macho Man (tabela do arcade 0x2197A id 2). No arcade os 4 rostos são colocados conforme os lutadores da luta (rotina 0x1F50C); aqui ficam fixos.
- Margens azuis: preenchidas com o cenário do arcade (RLE 0x1F474 + colunas 0x1F5C8, mundo de 768 px). Fundo x = arcade x-96, y = arcade y+16. 444 células, 254 tiles novos (res/ex50_tiles.bin, ids depois do público).
- Linhas 0-3 (público duplicado pelo wrap de 512 px do arcade) em preto; o público animado já não escreve ali.
- HUD vazio no plano window (linhas 0-3, fixo): 2 caixas, moldura dupla (externa/interna), interior preto, PAL3. Cor da moldura aproximada (azul), a confirmar.
- Igual à b49: câmera livre, público e som. Sem cordas.
- Mapa novo: res/bgb_map50.bin (já no formato da RAM).
