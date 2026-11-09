# b87 — candidata; NO afirmar igualdad arcade completa
ROM: `wwf_b87.bin` — MD5 `f956cfbcbf5012f63d66c8b0ac457a0d`. Base b86 intacta (MD5 `0cbe0756ba9ff3dff97b4acfaa8a76b8`).

## 1. Puñetazos — verificado en emulador
- FC84/FD04: el temporizador se consume en ticks de dos refrescos. FD70/FD7C = 4/3/3 **ticks**, no frames MD. FCAC: arranque 3 ticks. FD2E/FD48: decisión/recuperación y enlace con temporizador 1. FCFC: sólo flancos nuevos con +36=0xC (0xB no se alcanza con incrementos de 4).
- MAME mide 17,408 ms/refresco arcade (57,44485 Hz): tick=34,816 ms. Reloj por VBlank real: 3125/6528 ticks/frame NTSC; 3125/5440 PAL. No se ralentizan otros movimientos.
- NTSC, ambos: 150/151/152 = 9/6/8 frames visibles en la fase probada; los últimos 8 incluyen 6 de animación + 2 de recuperación. Otro medio combo: 9/6/8. PAL: 7/5/7. Mantener A NO encadena; nueva pulsación SÍ. La cuantización puede variar un frame según fase del reloj.

## 2. Clothesline — contacto verificado; cobertura arcade incompleta
- 12E7A/1302E: 1D0/1D1/1DA/1DB, y contacto 1D2+id rival durante 8 ticks; salida E/F. 12F04 detiene X durante captura; 12FAA lanza al rival después, no al tocarlo.
- 16634 usa coordenadas +C/+10 en píxeles: |dx|<96, |dy|<8; NO es una caja de impacto. 1672C/16C60/16CA8: cajas 18C2A (-20,12,48,16) y 18B82 (-16,28,0,72); defensa de pie 18B02 (-8,16,0,80). Activas 1D1 y 1DA. Velocidad heredada: 6,75 px/tick; luego 4 px/tick (12F76).
- b86 SÍ disparó el hit en MAME, pero a 64 px y antes del contacto visual: apartaba al rival con el zafado del pin. No era un condicional muerto. Se eliminó ese impacto prematuro.
- PASS: Duggan/Warrior, izquierda/derecha; contacto 1D1; contacto tardío 1DA; separación Y=20 NO golpea.
- **Pendiente para igualdad completa:** cajas de víctima en otras poses/corriendo (hittable todavía excluye carrera), variantes por la espalda y contra cuerdas. La caja de defensa actual es la de pie: no presentarlo como motor completo 16796.

## 3. Reacción 0x17 — vuelo/rebote/pose final verificados
- 9B9A/9BBE/A8BE/2964: desplazamiento inicial +/-32 px, altura +24, vx=+/-0x80, vz=0x100, gravedad=0x30. 3E20: posición +=2*v, luego vz-=2*g. 9E4C: pose 15 hasta altura 24 al descender; luego 16. 9C94 -> A4C8: rebote sin velocidad X; ABBC: pose final 17.
- Se conserva la fracción vertical cuando 9C44/A530 escriben sólo la palabra entera. Alturas por tick medidas: 213,214,214,214,213,211,209,206,202,197,191,187 / 189,190,191,191,190,188,187: iguales a MAME arcade.
- Gráficos arcade nuevos sólo por añadido: poses 799..820, motores 627..637. Los datos y mapas gráficos anteriores permanecen como prefijos idénticos; logo WWF y esquineros no se tocaron.
- **Límite:** reposo posterior usa 22 ticks (AF66, banda sana); no reproduce todas las bandas de energía del arcade. La transición contra cuerda conserva la caída anterior del port.

## Ritmo/ralentización y evidencia
- b86: 40 avances Clothesline ocuparon 42 refrescos MD (2 sin avance). b87 sin impacto: 43 refrescos, de los que 42 son poses (11/8/8/15): ~700 ms frente a 40 refrescos arcade=696,32 ms. No se observó pérdida de bucle en ese caso.
- En impacto b87: derecha Duggan 0 pérdidas; Warrior 1; izquierda 4. Existe lag de render/bucle residual; no se aisló CPU frente a DMA. El reloj de estos movimientos usa VBlank transcurrido para no acumular ralentización por esas pérdidas. **No afirmar que se eliminaron todos los frames perdidos.**
- Ocho ensayos cortos MAME Genesis/PAL, entrada A+B -> carrera -> nueva A; RAM sólo coloca luchadores/control para repetir el caso. CSV, scripts y aserciones: `verify/`; resumen `verify/RESULTADO_b87.txt`. Arcade real emulado: `verify/arcnatural.log`, contacto sin forzar flags; `arc87.log` para punch/temporizador. Capturas: `shots87/DR_contact.png`, `DR_catch.png`, `DR_flight.png`, `DR_bounce.png`, `DR_land.png`, equivalentes WR/DL/WL.
- El driver MAME dice HTOTAL/VTOTAL estimados: no hay medición de placa arcade física ni prueba de esta candidata en Everdrive.

**Resultado: candidata probada en los casos descritos, NO entrega final de «idéntico al arcade» por los límites anteriores.**
