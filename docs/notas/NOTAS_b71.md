# b71 (base b70, md5 24854415d3674c5e784b99ea9f7cc8da; b70 intacta)

ROM: `wwf_b71.bin`, md5 `dbfe401359b8f726186dd01e82cd5b2c`

## Cambios (solo los 4 pedidos)
1. **Cuenta de 3 (pin) para los dos.** Con el rival tumbado, **B pegado al cuerpo (a menos de 24 px)** = cubrir, como el B2 del arcade (acción 0x06/0x17). Duggan cubre con sus poses (494-499) y Warrior con las suyas (513-515). El árbitro se tira al suelo y palmea con las pistas arcade (500-506). La cifra grande 1/2/3 sale en +94/+194/+294, como en el arcade. Si llega a 3, el combate se reinicia 2 s después.
2. **Se libra solo en la 1.ª cuenta.** En el primer pin de cada luchador, después del "1" (arcade +128 Duggan / +136 Warrior), el que cubre se quita y se aparta 40 px, y el tumbado se levanta (pose 115). El árbitro se levanta (507-509) y vuelve a seguir. A partir del 2.º pin, la cuenta llega a 3.
3. **Cuenta de 20 fuera del ring.** Mientras alguno está fuera (lateral o detrás), el árbitro cuenta 1…20, sumando 1 cada 64 frames (arcade 0xDEE4/0xDA38: 4 pasos × 8 ticks de 2 f). Si vuelven los dos dentro, la cuenta se borra. Si llega a 20, el combate se reinicia 2 s después.
4. **Salto de Warrior sobre el rival completo.** Antes usaba las poses de Duggan traducidas, y del 547 al 554 salía Warrior de pie. Ahora usa su movimiento real del arcade, 0x0C (pista S0C del s62, poses propias 569-573 y luego 277/483/72): sube, cae de rodillas sobre el cuerpo (impacto en f40) y se levanta. Se activa con B a 24-100 px del cuerpo, igual que antes. El salto de Duggan (0x11) no se ha tocado.

**Reset combate:** los dos vuelven a la posición de salida y sin daño, y el árbitro a su sitio. No se reinicia la consola. Se mantienen C (a quién controlas) y START (persecución). La cámara vuelve con su paso normal.

## Sin tocar
No hay IA de ataque: el que no controlas solo persigue con START. Los controles son los mismos: B junto al cuerpo cubre, B más lejos salta y A da el codazo. Tampoco se han tocado los gráficos de los esquineros de arriba, el logo WWF ni las paletas. Las cifras usan la PAL0 del fondo.

## VRAM
- Cifra grande: tiles 1525-1534.
- Cifras de la cuenta fuera: tiles 1779-1788. Las dos zonas estaban libres.

## Límites
- Durante la cuenta fuera, el árbitro no hace el gesto de contar del arcade: sigue andando como antes. Solo se ve la cifra pequeña (8×8), y no hay voces 1-2-3.
- El arcade decide el kick-out por energía/machaque. Aquí, por petición de Emilio, el 1.er pin siempre se libra y los siguientes siempre llegan a 3.
- El kick-out es la cubierta al revés más un desplazamiento de 40 px (aproximación del s41). En el arcade, el compañero entra.
- El rival tumbado tiene que estar en la fase boca arriba (pose 114) para cubrirlo o saltar sobre él.

## Pruebas (MAME, test/t71.lua, modos pin / jump / ro con T71=…)
Capturas en shots/: 01-04 pin 1 (cubre, "1", se quita, se levanta), 05-08 pin 2 (1, 2, 3 y reset), 10-16 salto de Warrior, 20-24 cuenta fuera (1, 2, 10, 20 y reset). Las hojas son hoja_*.png.
