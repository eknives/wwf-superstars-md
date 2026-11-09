# Energía de WWF Superstars: viabilidad para b89

Estudio solamente, 6-11-2026 (Europe/Madrid). **No se ha modificado b89, construido ROM ni creado b90.**

## Conclusión antes de implementar

**Sí: se puede añadir energía independiente para Duggan y Warrior y restarla en los contactos ya existentes.** No basta con dibujar una barra ni reutilizar `vdmg`: este último es un acumulador temporal de derribo que b89 borra al caducar `vlast` (`main.c:1357`), no la energía del arcade. La fidelidad completa tiene partes pendientes: identidad/zonas de las pistas de suelo de Duggan, modo humano/CPU, variantes del clothesline y pin/levantarse dependientes de energía.

El rival sin control de b89 **no tiene IA** (inventario, línea 96). No debe considerarse CPU simplemente por no ser `ctl`: el arcade diferencia expresamente ese papel y cambia el daño de puño/patada. Se puede implementar esa distinción de datos sin cambiar IA, pero hay que definir el modo.

## Fuentes, unidades y método

- ROM CPU big-endian `analisis/tools/prog.bin`, MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; cotejada con los dos chips CPU del ZIP local. Direcciones de este documento: **direcciones 68000 del arcade**, salvo las RAM y líneas del port expresamente indicadas.
- Desensamblado `analisis/arc.dis`, tablas leídas directamente del binario y desensamblado alineado de las rutinas. El inventario b89 conserva referencias antiguas a b83: contrastado con `b89/src/main.c` actual. El FAQ sirve para nombres/inputs, **no convierte sus “1 tras 3 / tras 2” en puntos exactos de RAM**.
- MAME `wwfsstar`, ROM local `/workspace/wwf/mame/roms/wwfsstar.zip`. Monedas/START/selección reales; después fixtures RAM para aislar acciones, energía inicial, posiciones y, cuando procede, impedir evasión/IA hasta el contacto. Se ejecuta la rutina nativa: no se parcheó código CPU. **No son todas partidas jugadas de principio a fin ni verificaciones de inputs de cada llave.** Scripts `arc_energy*.lua`, CSV por refresco y logs conservados.
- CPU/vídeo arcade: 57,444852941 refrescos/s; lógica de actores cada **2 refrescos**, `0x1508–0x1510`. Tick = 34,816 ms. Los puntos de energía no se escalan por PAL/NTSC.
- MAME avisa CRC distinto de `24j6-0.112`: chip de **fondo**, no código CPU/sprites. Advertencia conservada; no se ha arreglado ni sustituido el set.

## Representación y reglas comunes

Actor: energía **word `+0x3C`**, daño pendiente **word `+0x3E`**; `+0x2A` byte bit 3 = CPU; `+0x2B` id (Warrior 0, Duggan 3). Actores principales RAM `0x1C0100` y `0x1C0334`.

Resta en **`0x16488`**: `0x16492` resta `+3E`, `0x16496–0x16498` satura a **0** ante préstamo; `0x1649A` escribe `+3C`. No contiene un máximo universal de 48. Wrappers para otras referencias de víctima: `0x161C8/161DA/161EC/161FE`.

Golpes con caja: `0x1672C` consulta `0x1761E[pose]` y luego `[id]`; cabecera byte **+1** es daño. `0x1697E–0x16984` lo copia a `+3E`.

1. **Víctima CPU y atacante sub 0/1 (puño/patada): daño base se fuerza a 0**, `0x1698A–0x169A2`. No confundir “no pierde energía” con “no recibe golpe”: sí hay contacto, reacción y acumulador de combo/mareo.
2. En el recorrido común `0x16304–0x16328`, si la víctima estaba en acción **1, 0x15 o 0x16** (carrera/recorridos automáticos, **no aturdimiento**), `0x1638E–0x163C6` añade `0x1642A[sub] & 0x7F`: puño +0, patada +2, clothesline +1.
3. En ese mismo recorrido, bandera del atacante **`+F9.0`** duplica el resultado, `0x16418–0x16420`. Activación `0x1CCE8–0x1CD28`, umbral de mareo `+F6` en `0x1CD48`; duración `0x1CD6C`, apagado `0x1CD50`. No hay equivalente completo en b89.
4. **Excepción importante**: víctima con reacción pendiente `+40=0xFFFE` (enlace/agarre del clothesline) pasa por `0x162BC–0x162DA` directamente a la resta `0x16328`; **omite bonus y duplicación**. No aplicar indiscriminadamente las reglas 2–3 a todos los golpes. Las restas directas de stomp/drop tampoco pasan por `0x1638E`.
5. `+48` combo / `+46` ventana y `+F6` mareo son distintos de energía: `0x16D4C–0x16D92`, tabla `0x17590`. No sumar ese contador a la barra.

## Daños por movimiento y posibilidad de engancharlos ahora

H/C = **víctima humana/CPU**, salvo columna de fallo, que distingue al atacante. Valores en puntos internos, no segmentos del HUD. W=Warrior, D=Duggan.

| Ataque existente o parcial | Daño arcade confirmado y dirección | ¿Añadir resta en b89? |
|---|---|---|
| Puño W | **1 H / 0 C por impacto**, no 1/2/3 según número de combo. Poses activas 0x152/0x155: cabecera 0x18810, byte **0x18811=1**; FD70/FD7C. | **Sí**, contacto `main.c:799`; una resta por golpe, separada del derribo. |
| Puño D | **1 H / 0 C por impacto**; poses activas 0x150/0x153, byte **0x187F5=1**. | **Sí para energía** en el mismo contacto; animación no idéntica, véase abajo. |
| Patada W/D | **4 H / 0 C**. Pose 0x158; bytes **0x188AB=4 (W)** / **0x188C7=4 (D)**; secuencia FF3A. Contra víctima en acción 1/15/16: **6 H / 2 C**, bonus **0x1642B=2**. | **Sí**, `main.c:816`; identificar carrera/whip, no sumar 2 por estar simplemente herido. |
| Clothesline W/D | Contacto pose **0x1D1: 4**, byte **0x1890D**; contacto **0x1DA: 2**, byte **0x18929**. Ambas víctimas H/C. Secuencia 12E7A/1302E. Ruta común: +1 contra corredor y ×2 con F9.0; **ruta enlazada FFFE: sin ambos**. | **Sí** para 4/2: `clStep87`, línea 729, ya distingue esos valores para `vdmg`. Igualdad completa de variantes **parcial**: no todos los enlaces/reacciones están representados. |
| Stomp W | **1 H/C**, escritura **0x117E0**, llamada `0x117F4→161DA`; rutina 1173A/1179A. El 3 de 117EE es para id 7, no W/D. | **Sí**, `warriorGroundStep`, `gs=13`, contacto en 638–698. |
| “Stomp/codazo” D `gs=5` | Stomp nativo sub 5 es **1 H/C** (117E0). **No queda demostrada aquí la equivalencia gráfica de la pista MD `gs5P` con ese stomp**: inventario y comentario la llaman codazo. | **Parcial**: hay contacto en 782–784, pero no etiquetar como stomp arcade exacto ni elegir daño de otro codazo por el alias. |
| Knee Drop W `gs=12`, sub 0x0C | **5 H/C desde suelo**, **10 H/C desde poste**: **0x10DC0=5**, si +34 activo **0x10DCC=10**; sub 0x0C/0x2C en FB58 → 10A5E. | **Sí para la resta** en `warriorGroundStep`; movimiento/zona/animación aún parcial según estudio Knee Drop. |
| Elbow/salto D `gs=11`, sub 0x11 | La sub **0x11 de FB58 también apunta a 0x10A5E**: **5 suelo / 10 poste H/C**, mismas escrituras. | **Parcial** para equivalencia completa: contacto en 782–784 permite restar 5, pero pista/input/zona del port son genéricos, no elbow arcade plenamente verificado. |
| Fallo de drop W 0x0C / D 0x11 | **2 al atacante humano; 0 al atacante CPU**, **0x10C6A** y comprobación CPU anterior. Solo si falla ese salto, no por cualquier caída. | **Parcial**: hay que distinguir impacto/fallo y aplicar en el evento de aterrizaje nativo; actualmente sin energía ni penalización real. |
| Forcejeo / reverse W/D | **Sin resta propia** en B1D0/B48C/B670. | **Sí: 0**. No cobrar energía por cada pulsación o por decidir ganador. |
| `trStart` llamado Irish Whip W/D | Pistas S_1E/W1E: sub **0x1E → 0x14CFC**, contra-llave que libera víctima en acción 0x15; **sin resta propia**. | **Sí: 0** en soltar, correr y rebote normal. No asignar 8 de Body Slam a esta pista. |
| Carrera, cuerda interior / caída del atacante en retorno del whip | **Sin daño de energía por sí mismo**. Límite interior **0x21E5A**, rebote 960A/96AA, choque de llave F94C/F9B0; acción 8 sub 1 no recibe el 5 de 2209C. | **Sí: 0**, incluidos `trStep:1021–1023` y `fsStart`. |
| Chocar con el poste/límite del ring desde fuera W/D | **5 al que choca H/C**, **0x2209C→220A2**. Límite **exterior 21ED0→21FA8→22040**, primer contacto por bitmask 22016; lista **220BE = 08,01,14,15,16,FF**. En acción 8 solo resta si sub de reacción **0x0A** (2208C–2209A). | **Parcial**: port tiene límites/salidas/reacciones, pero hay que reproducir condición exterior y antirrepetición. **No restar 5 en todo rebote interior.** |
| Pin/kickout, subir/bajar poste, entrar/salir W/D | Sin resta propia de ataque en las rutas estudiadas B012/AB1E/AD12/ADEA/AE7E y EC12. El pin usa la energía que ya quedaba. | **Sí: 0** de daño; adaptar pin/getup según energía es otra integración, actualmente no arcade. |

**Diferencias importantes del inventario:**
- Duggan humano no despacha el combo nativo por FC84: **FC4E→FC70→FDA0**, secuencia **FE88** (impactos 150/150/153 si se encadenan). W usa FC84/FD70/FD7C. b89 usa FD70/FD7C para ambos: el daño unitario se puede añadir sin tocar eso, pero no permite afirmar que toda la secuencia de D sea exacta. No se cambió nada.
- El alias `gs=11` es decimal 17 = **sub 0x11**, no sub 0x0B. Esta última es 132C8 (bulldog), **no** la pista D aquí tratada.
- **Gorilla Press, Body Slam, Headlock, Bulldog, Back Suplex, Atomic Drop y ataques desde poste no están implementados** (inventario y código); no hay contactos correspondientes a los que añadir daño todavía. “Remate Warrior” aquí puede referirse al Knee Drop parcial; **no hay Gorilla Press escondido en `trStart`**.
- Otro elbow/remate aéreo **125F0** tiene daño **12** en 126B8, **8** si sub 0x35 en 126C6 y fallo humano **4** en 1274E. **No confundirlo con gs11/10A5E**. Valores solo por código; esa variante no se probó ni es un ataque disponible en b89.
- Choque mutuo especial `+40=FFFC` puede restar **1** mediante **17202→1720A** (selector 17136/1715C). No es “daño de forcejeo” automático; no hay rama equivalente identificada en `grStep`. **Parcial/no añadir a todas las llaves.**

## Energía inicial, máximo, recarga

- **Humano W y D: 48**. Tabla **7FEC**, ocho words 48; inicialización **7EE6→7F76**. HUD **7CF2–7D14** muestra `min(12, ceil(E/4))`. Un punto interno no equivale a una celda visible.
- CPU: tabla **8190**, fila `1C0028 & 0xFF`, columna `(word +2A)&7`; inicialización **7FFC/8066/8110**, bonus de dificultad **80A6–80B4**: **8×(1C004A & 3)**. Primera fila W=45, D=43; dificultad interna 1 → **53/51**. No todos los rivales empiezan en 48.
- Bases CPU por índice de progresión 0..9, W/D: **45/43, 60/58, 68/66, 72/70, 40/40, 76/74, 76/74, 76/74, 86/86, 64/68**. Máximo inicial W/D en estas diez filas y cuatro dificultades: **110**, no un tope global del restador. Datos completos en `energia_inicial.csv`.
- **No se encontró regeneración pasiva durante el combate** entre las escrituras de +3C revisadas. Muestra idle corta sin cambio; no se presenta como prueba dinámica de todos los estados posibles.
- Entre combates, **2060→20C2**: con contador +40 no negativo, consume 4 del contador; si DIP **180002 bit7=0**, suma 4 a energía (20D6); **20DC–20E4** limita a 48 incluso cuando no suma. **20EC** repone 48 a miembros del equipo eliminado para el flujo posterior. No es regeneración durante un salto/caída.
- Power Up con crédito/START en modos admitidos: **6F64**, **6FEE/701E**, escrituras **7000/7014/7030/7044**: **restaura a tabla 7FEC (48), no añade 48 encima**. Recarga y Power Up: comprobados por código, no ejecutados como ensayo de compra de energía.

## Energía baja o cero: no es KO automático

- Índice por cuartos **1CE9C**: divide por `max(1, referencia_inicial >> 2)`, limita 0..3. Humano: franjas **0–11 / 12–23 / 24–35 / 36+**. CPU usa la base 8190 sin sumar el bonus de dificultad en este cálculo. `1CEF4` calcula tercios 0..2 para otros usos.
- Tiempo tumbado **AB1E→AB82–ABAA**, tabla **AF66 bytes**: **112/82/54/22 ticks** de menor a mayor energía = **224/164/108/44 refrescos** de lógica completa. CPU puede dividir a la mitad con F9.0 o si **1CD80** devuelve CS. Flag +33.0 añade 32 ticks (ABB6). No convertir estos tiempos a “frames de 60 Hz” sin conservar tiempo real.
- Adelantar salida del suelo humano **AD12**: entradas nuevas `+116 != 0` incrementan +34; umbrales **AF6A bytes = 24/10/6/3**, salida a acción 0x19. A E=0 aún puede levantarse; tarda más. No leer esa tabla como words.
- Pin humano **ADEA**: AF72=6/6/6/6 controla ventana respecto del árbitro; **AE24–AE40** suma a +34 cada tick con `+114 != 0` y compara contra **48−E**. **AE36 con E=0 impide esta salida por entrada**. También hay condiciones de fase del árbitro que llevan a AE42: no es simplemente un único contador de pulsaciones.
- Pin CPU **AE7E/AF26**: índices **0/1/2/3/4/5/6** para **E≥54 / ≥48 / ≥36 / ≥25 / ≥14 / >0 / =0**. Cada nivel cambia fase/tiempo de escape; índice 6 no sale por esa rutina (**AE8E–AE92**). **129A4** tampoco pide rescate del compañero cuando energía=0.
- **0 no termina solo el combate**: exige pin/cuenta o la condición de victoria correspondiente. MAME: víctima E=0 permanece de pie y, tumbada, vuelve a acción 0 conservando **E=0**. En b89 el pin/kickout de “primer pin” es determinista, no lee energía (`pinAdvance` 1040+); añadir la barra no arregla esto automáticamente.

## Verificación MAME — resultados válidos y límites

Evidencia primaria: `mame_energy2..5_frames.csv` (RAM por refresco), logs del mismo nombre; resumen `mame_resumen.csv`. Son lecturas internas antes/después, no estimaciones de barra por píxeles. Letras W/D en nombres de casos indican atacante; se probaron ambos salvo donde se especifica.

| Prueba | Resultado observado |
|---|---|
| Inicio VS, W y D humanos | **48/48**, línea NATURAL_START_ENERGY en logs. |
| Inicio 1P natural antes de golpes | `natural_cpu_final.log`: W humano **48**, CPU ids 4 y 2 **55/55** = 47+8, progresión 0/dificultad 1. Fórmula de CPU confirmada con esas columnas; todas las filas W/D solo por tabla. |
| Puño W/D a humano / CPU | **48→47 / 48→48**, con hit pendiente/reacción incluso en CPU (energy2). FD7C W pose155 también **48→47**. No se midió un combo entero de tres contra cada tipo. |
| Patada W/D a humano / CPU | **48→44 / 48→48**, contactos registrados (energy2). |
| Patada a corredor acción15 | **48→42 humano / 48→46 CPU**, ambos atacantes (energy2). |
| Clothesline pose1D1 | **48→44 humano y CPU**, ambos atacantes (energy4). |
| Clothesline pose1DA | **48→46**, humano enlazado (energy2/3) y CPU en contacto tardío (energy3), ambos atacantes. El enlace CPU no se da por verificado con ese fixture. No confundir nombre early de un ensayo con pose real: el CSV muestra cuál tocó. |
| Clothesline activo 1D1 contra corredor | **48→43**, ambos (energy5; fixture comienza en fase activa para aislar este caso). |
| F9.0, puño / clothesline temprano / enlazado tardío | Puño **48→46** (energy3), 1D1 **48→40** (energy4), 1DA enlazado **48→46**, **no duplica** (energy5). Ambos atacantes. |
| Stomp nativo sub5, W/D, H/C | **48→47**, energy2. D nativo verificado, no identidad de pista MD gs5. |
| Drop W0C / D11, suelo, H/C | **48→43**, energy2; víctima CPU inmovilizada para impedir que esquive antes del contacto. |
| Drop desde poste W/D sub2C | **48→38**, energy2; fixture en posición/altura de poste, no prueba del input completo de subir. Ataque no disponible hoy en port. |
| Fallo de drop, atacante humano / CPU | Atacante **48→46 / 48→48**, víctima sin daño, energy2; casos `miss_attackerCPU` son CPU atacante. Los `drop_miss_cpu` antiguos se congelaron mal y NO verifican fallo. |
| Saturación | Drop con víctima E=3: **3→0**, no negativo (energy2, W_saturate3). |
| Contra-llave S/W1E, carrera, cuerda interior y choque al retorno | **48→48** para ambos actores, aunque hay rebote y caída (energy2, counter_whip). |
| Carrera exterior, impacto límite/poste | Atacante **48→43**, ambos, energy3 `post_outside`. No se afirma comparación visual exacta de qué poste físico fue. |
| Idle y cero | Idle **48→48**; de pie **0→0** sin fin de combate (energy2). Muestra corta, no todos los estados. |
| Levantarse según energía | `levantarse_mame.csv`: valores iniciales de tabla menos el tick ya consumido: E48=21, E24=53, E12=81, E0=111; hasta acción5 desde k21: **42/106/162/222 refrescos**; E0 vuelve a acción0 en k259 con E0. Concuerda con **22/54/82/112 ticks** totales. |

**No verificado dinámicamente**: matrices completas de progreso/dificultad W/D, recarga entre combates, Power Up, toda la lógica de pin/teammate/kickout, triple combo completo, todas las variantes de espalda/cuerdas/enlaces. Sus valores anteriores se distinguen como deducción directa del código. La comparación del arte de suelo D y la equivalencia completa de cada rama con b89 quedan pendientes; no se cambió el port para facilitar los ensayos.

Los primeros ensayos también quedan guardados (`arc_energy.lua`, log/CSV sin número), pero algunas fixtures permitían evasión o no movían el clothesline. **No se usan sus ausencias de daño como prueba de daño cero**. En `mame_resumen.csv` se señalan ensayos sin contacto y los fallos mal aislados.

## Archivos y preservación

- `ENERGIA_ataques.csv`: decisión por luchador/movimiento, valores y direcciones.
- `energia_inicial.csv`, `cabeceras_poses.csv`, `TABLAS.txt`: extracción de tablas/cabeceras; caja vacía expresamente distinguida de daño activo.
- `mame_resumen.csv`, `levantarse_mame.csv` y CSV/log/Lua de cada ensayo: reproducción y auditoría.
- PNG opcionales de MAME: `W_drop_antes.png`, `W_drop_despues.png`, `W_clothes_antes.png`, `W_clothes_despues.png`. La lectura RAM es la evidencia numérica; la barra redondea de cuatro en cuatro.
- b89 ROM sigue **MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`**. Nada escrito dentro de b89; todo el trabajo nuevo queda en este directorio.
