# b72 (base b71, md5 dbfe401359b8f726186dd01e82cd5b2c; b71 intacta)

ROM: `wwf_b72.bin`, md5 `74c37dc8839ec8780a122eabfc71a58d`

## Lo que he mirado del arcade
- 0xBD10 / tabla 0xBEF2: el que cubre se pone en x del rival ± d (Duggan sobre Warrior 36, Warrior sobre Duggan 32), con y del rival −1. Las pistas de b71 ya terminaban en 36 y 32, así que la colocación en el centro del ring era la del arcade. El fallo de la captura era **la cuerda**.
- 0xACA4 + 0x21E5A: al caer, el arcade comprueba el cuerpo tumbado (de x−8 a x+48) contra los límites del ring. 0x1190C y 0x11A72 solo cubren si el rival está tumbado **dentro** y el que cubre no está fuera.
- 0xDEE4 + 0xDA38 + tabla 0xDB04: en la cuenta fuera, el árbitro mira al que está fuera y usa las poses de contar 0xA-0x11, 4 poses de 8 ticks. Suma 1 en cada vuelta (64 f).

## Cambios
1. **Cuerdas: ni pin ni salto.** Solo se puede cubrir (B pegado) o saltar (B más lejos) si se cumplen tres cosas: el atacante no está contra las cuerdas; el cuerpo tumbado, con sus píxeles reales (pose 114 con lyo), está entero dentro; y el sitio donde se coloca el que cubre también está dentro. Si no se cumplen, B es la patada normal.
2. **El árbitro no cuenta atravesando las cuerdas.** El pin solo empieza si las posiciones del árbitro de la pista (al tirarse y al palmear) caen dentro del ring con su margen. Si detrás no cabe, se pone delante del cuerpo.
3. **Cuenta fuera como en el arcade.** El árbitro hace el gesto de contar: poses arcade 0xA-0x11 importadas como 757-764 (757-760 de frente, 761-764 de espaldas), una pose cada 16 f y mirando al que está fuera. Las cifras son **grandes y rojas**, de 16×40, con el estilo de la cuenta de 3. 1, 2 y 3 son las originales; el resto se ha compuesto con sus segmentos (`tools_dig72.py` → `res/big_dig.bin`). Con dos cifras, las decenas van en los tiles 1779 y las unidades en los 1525.

## Sin tocar
No hay IA: el otro solo persigue con START. Los controles son los mismos (C cambia, START persigue, A/B como en b71). Tampoco se han tocado los esquineros de arriba, el logo WWF ni las paletas.

## Límites
- La forma de las cifras 0 y 4-9 es una reconstrucción con los segmentos del 2 y el 3, no una captura del arcade.
- A la pose 764 del árbitro le faltan 2 líneas de la mano: el árbitro tiene un límite de 41 tiles.
- No hago el empuje del arcade que aparta el cuerpo de las cuerdas al caer (0xACA4). Aquí, cerca de las cuerdas, simplemente no se puede cubrir.
- Sigue sin haber voces en la cuenta (en el arcade, la cuenta fuera es muda).

## Pruebas (MAME, test/t72.lua; T72X=780 coloca el combate en el centro)
pinC: pin en el centro (cuenta 1, 2, 3 y reset). pinR: junto a la cuerda izquierda no cubre. ro: gestos y 1/2/10/20 grandes, y reset. jumpC/jumpR: salto de Warrior. Capturas en shots/ (hoja_b72.png).
