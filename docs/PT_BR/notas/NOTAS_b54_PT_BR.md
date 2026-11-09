# b54 (a partir da b53)

ROM: wwf_b54.bin  md5 dad17974aae704c185eaf92d7e869de3

Só duas mudanças sobre a b53 (b53 intacta):

1. **HUD direito preto:** os tiles da borda direita da moldura azul (3/7/11) tinham 4 px transparentes por causa do bake −4 px da b53; são preenchidos com a cor 15 (preto, PAL3). A faixa preta chega à borda direita da tela; não se mexe no −4 px esquerdo nem no design das caixas.
2. **CIMA/BAIXO do Duggan invertidos:** controle CIMA → rumo ao fundo do ringue (oy++); controle BAIXO → rumo à câmera/frente (oy--). Antes estavam ao contrário na tela. A subida nos córneres / saída-entrada do ringue seguem a mesma lógica (BAIXO no córner de baixo, CIMA no córner de trás).

Sem mexer: som picotado, cordas, câmera, prioridade s49, IA.

Shots: shots/b54_hud.png (+ zoom), b54_down.png, b54_up.png. Smoke no MAME OK.
