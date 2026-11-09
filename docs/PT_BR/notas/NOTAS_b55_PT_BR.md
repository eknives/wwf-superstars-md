# b55 (a partir da b54)

ROM: wwf_b55.bin  md5 e00cc84cccd7180ed7822ff219e3c978

Só uma mudança sobre a b54 (b54 intacta):

1. **Limite direito do ringue:** `RING_XR` 920 → 917. Tirado do state/screenshot do Emilio (Duggan ox=917, oy=232): ele não pode se aproximar mais do córner direito (se o fizer, se sobrepõe à corda). Limite esquerdo (`RING_XL` 616) sem mexer. Daqui em diante este limite não é mais retocado.

Conferido no MAME: no canto de trás à direita, b55 ox=917 / b54 ox=920 (oy=234, sem climb). Shot: shots/b55_right_clamp.png.

Sem mexer: HUD, CIMA/BAIXO, arte das cordas, câmera, prioridade, som, tiles dos córneres.
