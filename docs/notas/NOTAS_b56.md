# b56 (desde b55)

ROM: wwf_b56.bin  md5 69171a59c5c65f55f93bfeb09de3d094

Solo compañeros en el relevo, para ver las cuerdas (b55 intacta):

- **Macho Man** relevo IZQUIERDO (602,338); **Hogan** relevo DERECHO (939,280). Posiciones del arcade (s35).
- Estáticos (pose fija 449 / 450, las mismas de s35–s46). Sin IA, sin colisión, sin relevo.
- Sprites con prioridad **BAJA** siempre (cuerdas plano A alta por delante). En el SAT van detrás de Duggan.
- Assets: spr_tab/spr_tiles de b55 (idénticos a wwf_sgdk). Tiles remapeados a PAL2 (PAL3 la usan cuerdas+HUD) → res/part_tiles.bin. Nota: esas poses traen cuerda pintada dentro (de s35); queda debajo de la cuerda del plano A.
- VRAM: Macho en tile 1728 (0xD800), Hogan en 1941 (0xF2A0), zonas libres; no se toca pool, cuerdas ni Duggan.

Sin tocar: cuerdas, fondo, HUD, RING_XL/XR, controles, sonido, esquineros, logo.
Shots: shots/b56_macho_izq.png, shots/b56_hogan_dcha.png. MAME arranca OK.
