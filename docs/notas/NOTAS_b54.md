# b54 (desde b53)

ROM: wwf_b54.bin  md5 dad17974aae704c185eaf92d7e869de3

Solo dos cambios sobre b53 (b53 intacta):

1. **HUD derecha negro:** los tiles del borde derecho del marco azul (3/7/11) tenían 4 px transparentes por el bake −4 px de b53; se rellenan con color 15 (negro, PAL3). La banda negra llega al borde derecho de pantalla; no se toca el −4 px izquierdo ni el diseño de cajas.
2. **Duggan UP/DOWN invertidos:** pad UP → hacia el fondo del ring (oy++); pad DOWN → hacia cámara/delante (oy--). Antes estaban al revés en pantalla. Subida postes / salida-entrada del ring siguen la misma lógica (ABAJO poste abajo, ARRIBA poste atrás).

Sin tocar: sonido entrecortado, cuerdas, cámara, prioridad s49, IA.

Shots: shots/b54_hud.png (+ zoom), b54_down.png, b54_up.png. MAME smoke OK.
