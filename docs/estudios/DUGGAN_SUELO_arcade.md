# Duggan: Stomp y Elbow Drop — SOLO ESTUDIO

6-11-2026, Europe/Madrid. Sin ROM nueva, sin b92, sin modificar b91. MAME 0.276, set `wwfsstar`; CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`. Sigue el aviso CRC del chip de fondo `24j6-0.112`, no CPU/sprites.

## Entradas y zonas

Fuente nominal: GameFAQs local, sección Duggan, líneas245–253 de `study_kneedrop/GameFAQs_text.txt` (copia en el backup). P=Button 1, K=Button 2 (A/B en port). Pulsación nueva, no dirección obligatoria. Ruta humana `8F9E/904A → C706`, buffer `+116 & 3`, acumulado por `4066–40B6` durante cuatro refrescos. Condiciones comunes `C79E–C8A8`: mismo plano `+19`, `abs(Ya−Yv)<24`; rival tendido acción B. `CB1A` contempla otras acciones/excepción 8/subD: no probadas aquí.

Ancla H=`Xv−40` con bit7 de orientación de víctima=0; H=`Xv+40` con bit7=1 (`C83E–C85C`; André usa 56). X/Y/Z son coordenadas mundo 16.16 en `+0C/+10/+14`, no pantalla. Para víctima normal:

| Técnica | Entrada/zona de suelo | Despacho |
|---|---|---|
| Stomp | P junto al cuerpo: orientación víctima 0, `H<Xa<H+48`; orientación 1, `H−48<Xa≤H`. Mismo Y ±23. | `CADE+3*4=CAEA → CB6C`; fila cuerpo `CB75=05,06,06` para P/K/P+K. `FB6C → 1173A`. |
| Elbow Drop | K junto a cabeza: orientación 0, `H−31≤Xa≤H`; orientación 1, `H<Xa≤H+31`. Mismo Y ±23. | Fila cabeza `CB72=04,11,04`; `FB9C → 10A5E`. |
| Elbow de poste | P **o K** desde acción F, estado `+B8=2`, rival B; no zona pequeña de cabeza. | `F35A → F636`, tabla Duggan `F6EF=2F,20,20`, elección por rival tendido; `FC14 → 10A5E`. |

La orientación inicial del atacante no bloquea: `10A6C/10BB2` copia la del rival. Desde poste, dibujo de preparación y fase 1 se orienta según Vx (`10F90–10FAC`, `10D02–10D26`). Las casillas de selección NO son bancos: Duggan=3, Warrior=0 (`6CD8`, `7FE2`).

Exterior por código: `CAFE+12=CB0A → CBEC`, cabeza conserva `04,11,04`, cuerpo `05,05,05` (fuera K cuerpo no pide pin). No ensayado dinámicamente en este estudio. **Cuerdas:** `240B6` borra `+9E`; la lista `240F0` sí contiene 11 y 2F, pero sus entradas `24102→24322` y `24106→24324` son RTS: no imponer cancelación genérica de cuerda a estos saltos. No se verificaron todos los límites del ring.

## 1. Stomp, no «codazo»

`1173A`: tabla **118BC = (159,8),(15A,4)**. El primer contador se decrementa ya al inicializar (`11750→1175C`): **159 dura 7 ticks/14 refrescos**, no 16. Al cambiar a paso4 (`1177A/11782/11786`) golpea; 15A tiene 4 ticks y se conserva un tick al volver a acción0: **10 refrescos visibles en RAM**, luego pose0. MAME: k25..38=159; k39..48=15A; acción0 desde k47, pose0 desde k49.

X/Y/Z constantes: caso (744,300,187). Sin salto ni velocidad. **Contacto una sola vez al entrar 15A**, `1179A`: comprueba plano y acción B, **no vuelve a medir distancia X/Y**. La zona se decidió en C706. `1185A` puede hacer levantarse a la víctima por azar en determinados modos/CPU (`118B6`), antes de ese contacto; entonces puede fallar. Esa evasión no se ensayó por separado.

Daño **1**, `117E0→117F4→161DA→16488`; el 3 de `117EE` es André, no Duggan. Víctima acción8/subD, A2; `+BF` incrementa hasta4 (`117F8–11806`). Si ya no está B, `117B8` retorna: sin penalización de energía al atacante en esta rutina. Hay rama especial para víctima acción17 (pin), `1180E`, no probada. Final atacante acción0 (`1176E`), no levantada 1A.

## 2. Elbow Drop, suelo

Comparte **10A5E** con Knee Warrior, pero **NO comparte offsets ni poses finales**. Tabla de poses Duggan **11372 = 112FA+3*40**:
- Normal: **61 → 62 → 1CB → 1CC → 1CC**.
- Variante `Ya+2<Yv`, `+5C=1` (`10B36–10B5C`): **61 → 62 → 1CD → 1CE → 1CE**.
- Duraciones: **61×8 /62×18 /1CB o1CD×10 refrescos** (`10F54/10FB2`, `112F0=0,8,4,FFFF,0`, comparador estricto `10D42`). Después 1CC/1CE variable hasta contacto +12 ticks de recuperación (`10D58–10EA6`); en suelo probado **26 refrescos** totales, luego **1A×16** (`A90E/AA00`, índice0). Tick=2 refrescos (`1508–1510`), vídeo MAME57,444852941 Hz; no son frames de60 Hz.

Física Duggan `11180/11188 →111F0`: palabras **0,−64,0,0,500,50,2000,2000** (hex salvo −64 decimal). Contra André, `11184/1118C →11200`: offset−80. Destino Xv±64 normal; fuera el solver divide el offset por2 (`15A52–15A5A`). Vz=0x500,g=0x50; velocidades8.8, coordenadas16.16. Solver común `156FA→159AC–15B3E`: divide con coordenadas word truncadas, |Vx|/|Vy|≤0x2000. Por tick de vuelo `3DCE→3E20`: ΔX=2Vx/256, ΔY=2Vy/256, ΔZ=2Vz/256, Vz−=0xA0 (límite−0x800). No integra durante la preparación.

MAME, atacante (712,300,187), víctima (760,300,187), orientación0: **Vx=−120,Vy=0**, ápice232; contacto **(697,299,187)**. Espejo (808,300): Vx=+120, contacto **(823,299,187)**. Variante Ya290: Vy75; contacto **(697;299,375;187)** y poses1CD/1CE.

Ventana `10BF8–10C3C`: descendiendo Vz<0, víctima B, mismo plano, Zword≤suelo+16. `10FCC` usa rectángulo víctima `11084[id]`: normal (−48,+8), anchos asimétricos16/48. Orientación víctima0: `Xv−64 < Xhit ≤Xv`; orientación1: `Xv < Xhit ≤Xv+64`; `Yv<Yhit≤Yv+16`. **Punto Duggan `110BC=110A4+3*8`: (Xa±8,Ya+4)**, signo X según orientación atacante; mismo punto en poste (`110C0`). Es distinto de Warrior (Xa,Ya+4). No es una caja genérica |dx|≤48.

Impacto fija paso4 y aplica el daño ese mismo tick (`11062→10D58`). `10D9E–10DB0`: Zword=suelo e Yword=Yv−1, **conserva fracciones**. Duggan no añade Y+10 ni auxiliar7D: `10F04` sólo lo hace para Warrior; **auxiliar=0 en todas estas pruebas**. Daño **5**, `10DC0`; reacción A2 descrita abajo. Tras12 ticks: acción5, retira auxiliares (`10E8A–10EA0`), levantada1A y acción0; no pin automático.

## 3. Elbow Drop desde poste

Sub **2F**, no 11 ni Knee2C. Mismas poses y **8/18/10 refrescos**, tanto P como K. Mismo registro físico Duggan111F0; `+34=1/2` según altura/lado (`10B12–10B30`). `110E4` puede limitar Vx a±0x200 si distancia horizontal al Xv±64≥96 y Vy a±0x100 si |dy|≥80 dentro/112 fuera; no un vuelo fijo.

Caso poste inferior izquierdo nativo (632,374,233), víctima (760,300,187): **Vx399,Vy−462**, ápice278; impacto **(694,34375;299,8125;187,5)**. P y K dan los mismos resultados. 1CC se ve **34 refrescos** totales (10 antes +24 desde contacto), 1A16. **Daño10**, `10DCC`, no5. Tabla F6CE proporciona la posición inicial del poste. No probadas las otras tres esquinas.

## Reacción y fallo compartidos

Víctima: `10DB4/117BA` → acción8/subD → `99BE/9A48/A554`, **pose A2**, `27D2[8]→28EC`: Vx=Vy=0, Vz0x200,g0x40. MAME: alturas relativas **4,7,9,10,10,9,7,4,0**, A2 **18 refrescos**; luego B/pose17 y levantada normal según energía/contador restante (`A5DA–A610`, `AB1E`, `AF66`, `AA00`). El literal A20004 no fija duración a4 ticks. No asignar una espera universal nueva.

Fallo de Elbow (suelo o poste), `10C4A–10CB2`: aterriza, acción8/sub5, **1CF**, Xword−24 si orientación0 /+24 si1, conserva fracción; **−2 al atacante humano**, 0 CPU (`10C62/10C6A`). Rutina `9FCC`, Vz0x300,g0x40; 1CF→16→17→1A→0. MAME ensayo miss: víctima movida durante vuelo; atacante100→98, víctima100; 1CF20/16×8/17×44/1A×16 refrescos en ese caso. Las esperas de suelo dependen del estado/energía; no convertir esa muestra en constante.

## Diferencias concretas contra b91 (inspección, sin recompilar)

- **Stomp ya usa la pista correcta**, pese al comentario «codazo»: `gs69.h` 522/523 corresponden a banco3 poses159/15A (confirmación previa `b90/NOTAS_b90.md`, cotejo `b69/tools69/match69.pkl`). Pista14/10 iteraciones, con poses de reposo antes/después; `main.c:838` avanza por iteración, **no arcTick ni refresco estable**. No se midió aquí la cadencia de la ROM MD.
- Zonas D `main.c:984–987`: usa `bodyX`, |dy|≤16, P≤40, B entre PIN_ZONE y100; no las zonas de cabeza/cuerpo C706/CB6C ni |dy|<24. P impacta `GS5_K=16`, un índice ANTES de la primera523 en índice17; arcade impacta al entrar15A. Además el port vuelve a filtrar |dx|≤48/|dy|≤16 al impactar, arcade Stomp no.
- Elbow D sigue `gs=11` (estado **decimal11 del port**, no número de subacción nativa; la rutina arcade es **sub0x11=decimal17**: aclaración de la frase ambigua del estudio de energía), **pista83 iteraciones** (`gs69.h`), X interpolada hacia `bodyX` con `gD*gs11X/7`, borrando fracción; no solver111F0, ni desplazamiento nativo hacia Xv±64, ni variantes1CD/1CE. `gs11Z` existe en header pero no se consulta en main.c; recursos viejos pueden incorporar desplazamiento visual: **no se afirma aquí una auditoría por píxeles de sus poses compuestas**.
- Contacto genérico en índice40 y caja centrada en cuerpo (`main.c:844–847`), no descendente/Z≤suelo+16 ni puntoD±8. Y no se recoloca a Yv−1 con fracción. Daño actual1/5 y fallo−2 ya correctos (`hurt90`), pero reacción `vjolt=10,vk=14,vlast=180`, **no A2 física para estos dos ataques de Duggan**. La rama A2/Knee sólo se conecta a Warrior.
- **Elbow desde poste Duggan no existe**: `main.c:906–915` autoriza el salto sólo con `curF` (Warrior); por tanto faltan sub2F, trayectoria, daño10 y su fallo para D. No basta cambiar el id de sprite del Knee.

## Verificación y archivos

**Verificado en MAME:** P cuerpo→sub5, K cabeza→sub11, espejo, variante, P y K poste→sub2F; poses y holds de RAM anteriores, posiciones/contactos, energía100→99/95/90, reacciónA2, fallo100→98. Datos cada refresco: `arc_frames.csv`; resumidos en `RESUMEN_RAM.json` y `poses_refrescos.csv`; fuentes/valores extraídos `TABLAS_DUGGAN.txt`. Script `arc_duggan.lua`, log `MAME.log`. Capturas `arc_stomp_*`, `arc_elbow_*`, `arc_cornerP_*`; resumen `RESUMEN_DUGGAN_SUELO.png`.

Arranque con monedas/start y selección; luego fixtures de posiciones, banco3 Duggan/banco0 Warrior, energía100 y rival tendido en RAM, **sin forzar subacción de ataque**. Entradas reales de botones; para poste se prepara acciónF/estado2 y se prolonga el tiempo de suelo del rival. PNG dos refrescos después del estado lógico, no sincronización perfecta de píxeles. No prueba de todas las fronteras, esquinas, rivales, evasiones ni exterior; no se ejecutó ni cambió la ROM b91. El enlace energía→espera depende de más flags: estas muestras no lo certifican exhaustivamente.
