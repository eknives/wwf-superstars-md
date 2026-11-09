# b81 — base b80 conservada

- ROM: `/workspace/b81/wwf_b81.bin`, **1.572.864 bytes**.
- MD5: **ffa3e48e22aee99750cd82af10d6ab31**.
- Base: `/workspace/b80/wwf_b80.bin`, MD5 **d843bac410485579980872341264fda9**, comprobada intacta al terminar.
- Compilación local SGDK; no CloudAgent, sin publicar ni tocar repositorios remotos.

## 1. Cuerdas: caída corta igual a izquierda y derecha

El fallo de b80 no era solamente cuánto duraba el contador: se interpretaba **0x2146E como paso→mapa**. En el arcade hay dos niveles distintos:

1. **0x21324** inicia en paso 2 con petición `d0=1`, fase visual `d4=3`.
2. **0x213AC** convierte paso→fase: `1,2,3,2,3,2,3,0`.
3. **0x2146E** convierte fase→dibujo. No se puede indexar directamente con el paso.

Además, los bancos `mp0` y `mp1` de b80 tienen índices locales diferentes. Para las dos fases finales equivalentes se usan:

| Fase arcade | Izquierda | Derecha |
|---|---:|---:|
| 3 | mp0[7] | mp1[4] |
| 2 | mp0[6] | mp1[3] |
| 0, reposo | mp0[0] | mp1[0] |

La caída ahora muestra **3→2→3→2→3→0**, nunca el estiramiento inicial de carrera.

Duraciones de `0x213A4`, pasos 2..7: **6,4,3,2,2,1 ticks arcade**. Se reproduce también el detalle de `0x21324`: inicializa y decrementa en la misma invocación, avanza antes de dibujar (`0x213B4`). El reloj corto ejecuta una invocación cada dos iteraciones del motor, idéntico para ambos laterales. No se añaden pausas ni se multiplica dos veces el tiempo.

**Carrera intacta:** la rama del motor que corre/rebota y las secuencias largas `sc0/sc1` se conservan. Hay una comparación automática contra el texto de b80 y fixtures de carrera en ambos lados.

## 2. Warrior: pisotón y salto sobre rival tumbado

Se elimina la trayectoria anterior del salto Warrior basada en desplazar/escalar `S0C`: ya no mezcla un desplazamiento vertical grabado con una altura de asiento de pin. Para Warrior, el movimiento usa las instrucciones y tablas del arcade, no una interpolación de capturas.

### Botón y posición — 0xC706 / 0xC83E / 0xCB3C

Sea `s = +1` si el bit de orientación del rival está activo, `-1` en otro caso. El ancla de selección es **rival.x + s*0x28**. En el mismo plano y con **abs(dy)<0x18**:

- Delante del ancla, **distancia <0x20**: **B → sub 0x0C**, salto.
- Detrás, **distancia <0x30**: **A → sub 5**, pisotón; **B → sub 6**, cubrir/pin.
- Los límites son estrictos: 31 sí / 32 no; 47 sí / 48 no; dy 23 sí / 24 no.

Así B es el mismo botón que cubre, pero la posición decide. Desaparece para Warrior la banda simétrica inventada de 28..100 px. No se añade la sub 4 ni otras llaves/entradas ajenas a estos dos movimientos. Duggan conserva su motor anterior.

### Pisotón — 0x1173A / 0x118BC

- Poses nativas **0x159 y 0x15A**, temporizadores **8 y 4 ticks**.
- Impacto al pasar al segundo paso.
- Sin salto ni desplazamiento X/Y; suelo **z=0xBB**. Ya no baja al asiento de un pin.

### Salto — 0x10A5E / 0x111D0 / 0x156FA / 0x159AC / 0x3E20

- Suelo: **0xBB**. Impulso vertical: **0x500**; gravedad **0x50**.
- Destino X: tabla nativa `0x111D0`, **rival.x ±0x20**, según orientación. Destino Y: Y del rival.
- Velocidades calculadas con el bucle de `0x159AC`: divide la distancia por el número de pasos de vuelo. No se usa un divisor de una pista grabada.
- Integrador de `0x3E20`: `x+=2*vx`, `y+=2*vy`, `z+=2*vz`, `vz-=2*g`, cada tick arcade.
- Preparación de **4 ticks**; secuencia normal **0x61/0x62/0x7A/0x7B**, variante **0x61/0x62/0x76/0x77** cuando empieza en `propio.y+2 < rival.y`.
- Temporizadores aéreos de `0x112F0`: **9 ticks, 5 ticks, esperar contacto**.
- Contacto descendente desde **z≤0xCB** con el punto y rectángulo exactos de `0x10FCC`, `0x11084` y `0x110A4`; no un alcance genérico de 48 px.
- Impacto: **z=0xBB**, **y=rival.y−1+10**, como `0x10D9E/0x10F04` para id 0. Objeto auxiliar **0x7D**, orientación opuesta y desplazamientos de `0x1152A`; se compone en el recurso visual, no en la física del luchador.
- Apoyo durante **12 ticks**, recuperación acción 5, pose **0x1A**, **8 ticks** (`0xAA00[0]`).
- Si el rival se levanta antes: no se concede un pin/impacto falso. Rama de fallo `0x10C4A` y rebote acción 8/sub 5 (`0x9FCC`, física `0x27D2[0x19]`: vz=0x300, g=0x40; poses 0x1CF/0x16), antes de volver al motor de tumbado de b80.

### Recursos y procedencia

Se añaden poses nativas sin modificar los recursos anteriores: `spr_tab.bin` y `spr_tiles.bin` mantienen íntegro el prefijo de b80. La conversión comprueba **píxel por píxel** la pose 0x159 contra el recurso ya existente en b80 y conserva su origen/paleta, sin dibujar píxeles nuevos. Todas caben en la ventana de 64 tiles de Warrior.

**Toda la lógica/medidas procede de `/workspace/wwf_sgdk/analisis`.** Para convertir los píxeles se utiliza la dependencia gráfica original que declara `analisis/tools/render_obj.py`: `/workspace/wwf/port_35/sprtiles.npy`. Es un array de tiles original decodificado, no código de movimientos de otro port. Queda explícita esta dependencia en `tools/native81.py`.

## Pruebas y capturas

- **19 fixtures** en MAME con driver **Genesis**, estados preparados y pulsaciones reales de A/B: cuatro variantes/lados del salto, ambos pisotones, pin ambos lados, colisión y carrera ambos lados, seis límites incluidos/excluidos y fallo al levantarse el rival.
- Además: **kickout natural junto a cuerda izquierda y derecha**, desde golpes/pin con mando, sin escribir la petición de animación. Ambos terminan `RESULT ok_rope_vib`.
- En los cuatro saltos se contrastan **16 muestras X/Z** contra un integrador independiente de las instrucciones del arcade: horizonte del solver **34 pasos**, máximo **z=232 (BB+45)**, aterrizaje **z=187/y=rival+9**. Los dos lados son simétricos.
- Cuerdas con cámara asentada: transiciones de fase equivalentes en **exactamente los mismos fotogramas** en los dos lados. Los callbacks MAME pueden observar fotogramas VDP repetidos mientras el motor trabaja; no se confunden esos callbacks con ticks de la máquina arcade.
- El fixture dy23 observó una transición de carga durante un callback a mitad del bucle; se comprueba que no persiste más de dos VBlanks. No se afirma que haya una auditoría general de parpadeo/hardware en esta versión.
- `VALIDACION_b81.txt`: resultados y checksum interno **SGDK XOR**, como b80.
- **Capturas definitivas: `/workspace/b81/shots/FINAL_b81/`**. Secuencias `ropeL_secuencia.png`, `ropeR_secuencia.png`, `diveR_secuencia.png`, `diveL_secuencia.png`, variantes, pisotones y fallo. Incluye PNG individuales sin etiquetas y hojas de contacto etiquetadas.
- `ARCADE_b81.txt`: instrucciones recuperadas, direcciones, bytes de tablas y hash de la ROM de programa de referencia.

**Alcance de la validación:** el comportamiento se contrastó con el desensamblado; las capturas de esta entrega son del port en MAME Genesis, no de una nueva ejecución del arcade original ni de una consola física. Se conservan energía/IA/cuentas y reacciones generales de b80 salvo las rutas visuales/físicas descritas; no se presenta como port completo de esos otros sistemas.

## Reproducir

```sh
cd /workspace/b81
python3 tools/native81.py
# make no siempre detecta cambios dentro de BIN: forzar recursos tras regenerarlos.
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b81.bin
md5sum wwf_b81.bin
python3 tools/validate81.py
```

Build final: `BUILD_b81_final.log`; generación de sprites: `NATIVE_b81.log`; diff: `CAMBIO_b81.patch`.
