# b55 (desde b54)

ROM: wwf_b55.bin  md5 e00cc84cccd7180ed7822ff219e3c978

Solo un cambio sobre b54 (b54 intacta):

1. **Tope derecho del ring:** `RING_XR` 920 → 917. Sacado del state/screenshot de Emilio (Duggan ox=917, oy=232): no puede acercarse más al esquinero derecho (si lo hace, se pisa con la cuerda). Tope izquierdo (`RING_XL` 616) sin tocar. Luego este límite no se retoca.

Comprobado MAME: en esquina trasera-derecha, b55 ox=917 / b54 ox=920 (oy=234, sin climb). Shot: shots/b55_right_clamp.png.

Sin tocar: HUD, UP/DOWN, cuerdas art, cámara, prioridad, sonido, esquineros tiles.
