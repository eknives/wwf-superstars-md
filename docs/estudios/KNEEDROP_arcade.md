# Knee Drop de Ultimate Warrior — SOLO ESTUDIO

**No se ha cambiado b89 ni construido ninguna ROM.** Su ROM sigue con MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`.

## 1. Cómo se hace

- **Suelo: pulsar Kick, botón 2 del arcade, por la cabeza del rival tendido; no requiere dirección.** GameFAQs suministrado, líneas 167–171 de `GameFAQs_text.txt`: «Knee Drop = K (By head,2)». En b89 corresponde a **B**. Punch+Kick no es esa entrada: fila de cabeza Warrior `04,0C,04` para P/K/P+K (`0xCB3C+6`).
- Ruta humana: `0x8F9E` / exterior `0x904A` → `0xC706` → acción `0x0C`, subacción `0x0C` → tabla `0xFB58+0x30` → **`0x10A5E`**. Las entradas nuevas están en `+0x114`; `0x4066–0x40B6` las acumula en `+0x116`, borrado cada cuatro refrescos. `0xC70A` consume ese pequeño buffer, no un botón mantenido autorrepetible.
- Caso normal: rival en acción **B**, mismo plano **byte `+0x19`** (0 dentro, 1 fuera), `abs(Ya−Yv)<24`. **No se compara la altura Z para elegir la zona.** Fuentes: `0xC79E–0xC7EE`, tabla `0xCB1A`. El selector también clasifica `0x1E` como suelo y admite la excepción acción 8/sub D (`0xC82A–0xC836`); esas excepciones no se probaron con entrada en MAME. El impacto, en cambio, exige B.
- Coordenadas: **X=`+0x0C`, Y=`+0x10`, Z/altura=`+0x14`**, formato 16.16. No son coordenadas de pantalla ni centro visual del sprite. Ancla de cabeza: `Xv−40` si bit7 de `+0xA` del rival=0; `Xv+40` si=1 (`0xC83E–0xC85C`). Para un rival normal, no André:

| Orientación del rival | X del atacante que selecciona Knee Drop | Y |
|---|---|---|
| bit7=0 | `Xv−71 … Xv−40`, ambos incluidos | `Yv−23 … Yv+23` |
| bit7=1 | `Xv+41 … Xv+71`, ambos incluidos | igual |

Derivación: lado delantero del ancla y distancia **estrictamente <32**, `0xC860–0xC88E`. Detrás se selecciona otra fila: por ejemplo K en el torso → sub 6, pin, no Knee Drop. La orientación inicial del atacante no es requisito: `0x10A6C`, `0x10BB2–0x10BD8` copian/orientan; Warrior termina con bit7 según el signo de Vx.

**Cuerdas/exterior:** no hay veto genérico «cerca de las cuerdas» en esta selección. Se aplican los límites normales al andar (`0x21E5A` / `0x21ED0`). Además, `0x240B6` limpia `+0x9E` y su lista **`0x240F0` no contiene 0C ni 2C**: no debe atribuirse a esos saltos la cancelación genérica `0xF9B0`. Probados impactos con atacante X=640 y X=896, Y=300, junto a ambos laterales. **También funciona fuera**, con ambos en plano 1; la tabla exterior `0xCBBC+7` conserva sub 0C. MAME lo confirmó con suelo Z=128 y daño 5.

**Desde el esquinero:** **P o K**, con el rival tendido (GameFAQs 176–177). Acción `0x0F`/estado de poste 2 → `0xF35A`, lectura del flanco `+0x114` en `0xF38A/0xF3B6/0xF3EA/0xF41E` → `0xF636`; tabla Warrior `0xF6E6=2C,20,2C` → **sub 2C**, también `0x10A5E`. Confirmados por separado Button 1 y Button 2 desde la esquina inferior izquierda. No requiere colocarse en la pequeña zona de cabeza del ataque de suelo.

## 2. Poses y tiempo real

Un tick de luchador son **dos refrescos**, comprobado en `0x1508–0x1510`, bucle `0x155A–0x157C` y en el registro MAME. Este driver usa **57,444852941 Hz**: 17,408 ms/refresco, **34,816 ms/tick**, no 60 Hz exactos (`wwfsstar.cpp:632`; sus totales de vídeo están anotados como estimados).

Tabla de poses Warrior **`0x112FA`**:
- Normal: **61 → 62 → 7A → 7B → 7B**.
- Variante `Ya+2<Yv`, flag `+0x5C=1`: **61 → 62 → 76 → 77 → 77** (`0x10B36–0x10B5C`).
- El bloque de esquinero usa las mismas dos secuencias.

| Fase | Pose | Duración real | Fuente |
|---|---|---|---|
| Preparar | 61 | **4 ticks = 8 refrescos** | **`0x10F54`, contador hardcoded `0x10FB2–0x10FC6`** |
| Subir | 62 | **9 ticks = 18 refrescos** | `0x10D2C–0x10D4C`, `0x112F0[1]=8`; avanza cuando contador >8 |
| Descender | 7A / 76 | **5 ticks = 10 refrescos** | mismo comparador, tabla=4 |
| Buscar contacto | 7B / 77 | hasta colisión/suelo; variable | `0x10BF2–0x10CBC`, tabla=FFFF |
| Tras impacto | 7B / 77 | contador hasta **12 ticks** | `0x10D58–0x10EA6` |
| Levantarse | 1A | normalmente **8 ticks / 16 refrescos** | acción 5, `0xA90E`, `0xAA00[0]=8` |

**La primera duración NO es 1 tick aunque `0x112F0[0]=0`: esa fase salta a `0x10F54`, que espera cuatro.** La nota/comentario heredado de b83 en b89 es incorrecto.

Medido en RAM cada refresco, caso suelo normal: **61×8, 62×18, 7A×10, 7B×26, 1A×16**. Los 26 de 7B incluyen 2 antes del impacto y 24 desde él: al pasar a acción 5 conserva esa pose un tick antes de cargar 1A. El auxiliar 7D está activo **22** refrescos, no los 24 completos (`0x10E9A`). En la esquina ensayada, el vuelo prolonga 7B a **34** refrescos. No son duraciones universales para cualquier trayectoria.

## 3. Trayectoria e impacto

**Parámetros Warrior:** punteros `0x11150` → registro **`0x111D0`** (normal), ocho palabras:
`0, −32, 0, 0, 0x500, 0x50, 0x2000, 0x2000`.
`0x156FA`, `0x108B0`, `0x159AC–0x15B3E` resuelven la trayectoria. Vz inicial **0x500**, gravedad **0x50**, velocidades 8.8. Destino normal: `(Xv±32,Yv)`; fuera, el offset −32 pasa a **−16** antes del espejo (`0x15A52–0x15A5A`). Los últimos valores limitan |Vx|/|Vy|. El solver simula pasos simples y divide el desplazamiento por su número, truncando hacia cero: **34 pasos** desde suelo a suelo en estos casos.

Durante fase 0 no se integra. Por tick de vuelo, **`0x3DCE→0x3E20`**:
`X += 2*Vx/256; Y += 2*Vy/256; Z += 2*Vz/256; Vz -= 0xA0`, límite descendente −0x800. No existe un desplazamiento fijo universal en X/Y.

Ejemplo MAME: atacante `(712,300,187)`, rival `(760,300,187)`, bit7=0: **Vx=0x78, Vy=0**, subida máxima **Z=232**; contacto en el 16.º tick de movimiento, `(727,309,187)` tras ajuste. Espejo: empieza X=808, Vx=−0x78 y contacta X=793. Variante Y inicial=290: Vy=0x4B, termina Y=**299,375**, no 309.

Esquinero probado: origen nativo **`(632,374,233)`** (`0xF280`, tabla `0xF6CE`), **Vx=599, Vy=−462**, solver 41 pasos; contacto al 20.º tick de movimiento, `(725,59375;309,8125;187,5)`. `0x10B5E–0x10B6C`/`0x110E4` pueden sustituir Vx por ±0x200 si la distancia horizontal a `Xv±64` es ≥96, y Vy por ±0x100 si |dy|≥80 dentro /112 fuera. No se debe reutilizar un vuelo fijo de suelo para cualquier esquina.

**Ventana de impacto:** después de integrar, Vz<0, rival acción B, mismo `+0x19`, Z entera ≤suelo+16 (`0x10BF8–0x10C3C`). `0x10FCC` compara el punto Warrior **`(Xa,Ya+4)`**, tabla `0x110A4`, con:
- bit7 rival=0: **`Xv−64 < Xa ≤ Xv`**;
- bit7 rival=1: **`Xv < Xa ≤ Xv+64`**;
- en ambos: **`Yv < Ya+4 ≤ Yv+16`**.

Fuentes: rectángulo `0x11084` = (−48,+8), construcción/comparaciones `0x10FD6–0x11060`. Se pone fase 4 y se ejecuta su impacto ese mismo tick (`0x11062`, `0x10CBC`).

**Colocación/capas:** `0x10D9E–0x10DB0` escribe las palabras enteras Z=suelo e Y=Yv−1, **conservando fracciones**. En variante normal Warrior añade 10 a Y y crea **7D**, banco del atacante, orientación XOR80, X=atacante∓4, Y−10, Z+10 (`0x10F04–0x10F1A`, `0x1152A`). **En variante 1 no añade esos 10 ni crea 7D.**

## 4. Daño, reacción y final

- `0x10DB4–0x10DD2`: víctima **acción 8/sub D**, daño de energía **5 en suelo /10 desde poste**. `0x161C8→0x16488` lo resta con saturación. Confirmado **100→95** y **100→90**. El «2/3» de GameFAQs es la escala de su autor; no se ha demostrado su equivalencia con esos valores internos.
- Reacción real: `0x99BE→0x9A48→0xA554`, **pose A2 del banco de la víctima**, no una caída genérica. `0x27D2[8]→0x28EC`: **Vx=0,Vy=0,Vz=0x200,g=0x40**. En la prueba la altura relativa recorre **4,7,9,10,10,9,7,4,0**: nueve ticks. A2 dura **18 refrescos**. El literal `A20004` en `0xA566` NO significa que esta reacción dure cuatro ticks: la salida depende del aterrizaje (`0xA5DA–0xA610`).
- Al aterrizar: acción B con bit1 y pose 17 en su siguiente actualización; después su levantarse normal (`0xAB1E`). En humano ese bit conserva el contador de suelo restante `+0x38` (`0xAB7A–0xABBC`); no inventar una espera nueva fija. En CPU hay cálculo por energía/tabla `0xAF66`. Warrior termina en acción 5/1A y vuelve a 0; **no encadena un pin automático**. `0xAA00` contiene 8,12,16,32,20,24,28,40 ticks según `+0xF0&7`; las pruebas usaron índice 0.
- **Fallo:** `0x10C4A–0x10CB2`: acción 8/sub5, pose **1CF**, desplaza X **−24** si bit7=0 /+24 si=1, flip de dibujo opuesto; pierde **2 de energía si humano**. Sigue `0x9FCC` (`0x27D2[0x19]`: Vz=0x300,g=0x40), poses **1CF→16→17→1A→0**. Verificado desplazando el rival durante el vuelo: energía del atacante **100→98**, no del rival. Las esperas posteriores de suelo dependen del estado.

## 5. Diferencias concretas frente a b89

Fuente: `/workspace/b89/src/main.c` y `native81.h`, además de ejecutar **la ROM existente sin recompilar**.

1. **Preparación demasiado corta:** líneas 647–648 esperan 1 tick, arcade 4. Medido por refrescos: b89 normal **4/22/10/2** para 61/62/7A/7B previo al contacto; arcade **8/18/10/2**. Variante b89: **3/21/11/3**. El contacto a +38 refrescos coincide por compensación en estas fixtures, no porque el reparto sea correcto.
2. **Reloj incorrecto/no estable:** líneas 638–640 cuentan cada dos **iteraciones**, no `arcTick`. Los registros muestran iteraciones que no avanzan en todos los refrescos, de ahí poses alargadas/variables. No se ha perfilado para atribuir el coste a CPU o DMA. PAL tampoco está probado.
3. **Variante 1 mal colocada y con capa indebida:** líneas 663–685 siempre Yv+9 y pose combinada 788=77+7D; arcade Yv−1 conservando fracción, **sin 7D**. Medido: b89 Y=309 frente a MAME 299,375.
4. **Reacción/daño sin reproducir:** línea 685 solo `vjolt=10,vk=14,vlast=180` y efecto; no resta los 5 ni ejecuta A2 con física. En b89 la víctima siguió con Z=187 y pose genérica 752; en arcade hace el pequeño arco A2. `vlast=180` es un temporizador del acumulador de golpes, **no** la duración arcade de caída.
5. **Final/capas no idénticos:** la pose combinada mantiene 7D hasta cargar 1A; arcade lo borra un tick antes. Recuperación b89 observada **15 refrescos**, arcade **16**; salida inmediata al octavo contador en línea 661 frente al despacho nativo que conserva la pose.
6. **Exterior y cuerdas:** líneas 585–594/898 vetan el ataque fuera; arcade lo admite. Líneas 669–673 añaden un choque de cuerda durante el vuelo que no está justificado para sub 0C por `0x240B6` (lista sin 0C). No se probó cruzar todas las geometrías de cuerda.
7. **Selector simplificado:** `lyingNow` exige una fase concreta del derribo genérico; no representa la tabla de acciones `0xCB1A`, sus excepciones, ni el buffer de pulsación de cuatro refrescos.
8. **Esquinero no está conectado a esta técnica:** rama `climb`, líneas 843–856, descarta `pendBtn`; no implementa la entrada P/K→sub 2C ni el vuelo/daño de poste.
9. **Fallo incompleto:** líneas 689–692 no aplican los −2 de energía y borran la fracción X. La orientación normal izquierda/derecha no debe declararse incorrecta solo por `p1face=!vface`: ese es otro convenio del port; aquí no se ha hecho una auditoría de cada tile/flip.

## 6. Verificación y archivos

**Sí verificado en MAME:** entrada real Button 2 desde fixtures tendidas; ambos sentidos; variantes 0/1; límite X −71 válido/−72 no, |dy|23 válido/24 no; torso→pin; cerca de ambos laterales; exterior; reacción A2 y daño 5; fallo/−2; Button 1 y 2 desde una esquina, misma secuencia y daño 10. **Sí comparado b89** en dos fixtures con B: duraciones, colocación de variante y ausencia de física A2.

Se arrancó con monedas/start y selección normal de Warrior/Duggan. **Se prepararon posiciones/derribos/energía en RAM, no una partida completa natural**; no se forzó la subacción de Knee Drop. En la prueba de fallo se movió el rival; en las de esquina se prolongó su contador de suelo para que no se levantara antes. Los contadores de pose son de RAM cada refresco, no una certificación de cada píxel del vídeo. Las PNG se toman dos refrescos después del cambio observado para evitar capturar el bitmap anterior de la tubería de dibujo.

- **Resumen visual:** `RESUMEN_KNEEDROP.png`.
- MAME, secuencia normal: `arc_headL_01_preparacion.png`, `arc_headL_02_salto.png`, `arc_headL_03_vuelo.png`, `arc_headL_04_impacto.png`, `arc_headL_05_reaccion_apice.png`, `arc_headL_06_recuperacion.png`.
- Espejo/variante/esquina: `arc_headR_04_impacto.png`, `arc_aboveL_04_impacto.png`, `arc_cornerK_04_impacto.png`.
- b89 intacto: `md89_headL_impacto.png`, `md89_aboveL_impacto.png`.
- Datos/reproducción: `arc_frames.csv`, `arc_corner_frames.csv`, `md89_frames.csv`, sus scripts `.lua`, `AUDITORIA.txt`, `audit_knee.py`, `ROM_tables.txt` y el texto extraído del MHT.

**Límites:** no hardware/PAL, todas las esquinas/rivales/estados excepcionales ni auditoría gráfica tile a tile. MAME avisa de CRC distinto en **24j6-0.112, tiles de fondo**, no CPU/sprites; la CPU reconstruida del ZIP es idéntica a `analisis/tools/prog.bin` (MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`). Frecuencia física de la placa no medida.
