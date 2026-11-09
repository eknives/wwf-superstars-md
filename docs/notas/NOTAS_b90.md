# b90 — energía interna + Knee Drop

ROM: `/workspace/b90/wwf_b90.bin` — MD5 **24759dec91fa996dc6e7a2f227e30f45**.
Base b89 copiada; sus archivos siguen coincidiendo con `b89_manifest90.json`. Compilación SGDK local con el comando solicitado. **No presento el Knee Drop como idéntico al 100 %: hay dos diferencias verificadas pendientes abajo.**

## 1. Energía — verificado

- Dos humanos, inicial **48** (`7EE6→7F76`, tabla `7FEC`); `energy90[]` independiente de `vdmg/vlast`, sin HUD, regeneración ni KO por cero. Resta saturada (`16488–1649A`). `fighterInit` repone ambos a 48 al reiniciar combate.
- MAME Genesis, binario final: **20 fixtures RAM** con entradas reales tras preparar el estado. Ambos atacantes: puño **48→47**, patada **→44**, clothesline temprano **→44**/tardío **→46**, stomp **→47**, drop **→43**; fallo **48→46 al atacante**. Cero sigue cero sin terminar el combate; **1→0** satura. Las ramas de cuenta de pin/ring-out reinician **48/48**, conservando selección fase 4. Se forzó la fase final de cuenta, no se jugó una cuenta completa.
- Evidencia: `shots90/md90_energy_frames.csv`, `md90_energy.log`, `validation90.json`.

## 2. Restas de ataques existentes — verificado en esos contactos

Puño W/D: `18811/187F5=1`; patada `188AB/188C7=4`; clothesline `1890D=4`, `18929=2`; stomp `117E0=1`; drops suelo/poste `10DC0=5`, `10DCC=10`; fallo humano `10C6A=2`. El `gs5` de Duggan usa MD522/523 = banco 3 poses **159/15A**, cotejado con `b69/tools69/match69.pkl`: se aplica stomp 1, no un daño inventado de «codazo».

Patada incorpora +2 de `1642B` para carrera/whip cuando el contacto lo permita; el filtro de colisión b89 normalmente excluye esos estados, **no se amplió ni se verifica ese bonus en MD**. Clothesline b89 enlazado sigue la excepción FFFE (`162BC–162DA`), sin bonus ni duplicación. F9.0 no tiene equivalente completo; no se inventó. Llaves/whip/rebote interior siguen sin daño propio. No se añadieron movimientos ausentes ni el choque exterior especial de `2209C`, cuya condición/antirrepetición no existe completa en b89. Pin/kickout y levantadas ajenas al Knee no se cambiaron.

## 3. Knee Drop Warrior — verificación parcial

- Entrada `C706/C79E–C88E`; poste P **o** K `F35A/F636/F6E6`, sub2C→`10A5E`. Preparación `10F54/10FB2`: **4 ticks**; `112F0/112FA`: **9/5 ticks** de vuelo. Arcade `1508–1510`: tick=2 refrescos a 57,44485 Hz → **61×8 / 62×18 / 7A×10**. Se usa `arcTick`, no paridad del bucle. Reloj existente: NTSC 3125/6528, PAL 3125/5440.
- Solver `159AC–15B3E`: Vz500, g50, destino Xv±32 (±16 fuera), velocidades limitadas a 2000; división por coordenadas word enteras `15A6C/15AD8`. Poste conserva altura inicial y reglas `10B5E/110E4`. Impacto asimétrico `10FCC/11084/110A4`, descenso y Z≤suelo+16. Variante `10B36–10B5C`: **76/77**, Yv−1 con fracción conservada, sin 7D. Normal Yv+9 y manos auxiliares; retirada `10E9A`. Quitado el falso choque genérico: `240F0` no enumera sub0C/2C.
- Reacción `A554`, tabla `27D2[8]→28EC`: A2, Vz200/g40; alturas relativas **4,7,9,10,10,9,7,4,0**. Suelo/getup 17/1A; tabla AF66 para espera humana de esta reacción. Se añaden únicamente seis poses A2/17/1A de bancos 3/0 (`6CD8`), sin sobrescribir gráficos previos. Flip del Knee y A2 cotejado visualmente; orientación nativa `10BB2`. Fallo `9FCC`, vz300/g40 y −2.
- Contra MAME arcade: **88 estados de trayectoria por fase/timer coinciden exactamente** (X/Y/Z). Contactos: suelo izq **(727,309,187)**; derecha **(793,309,187)**; variante **(727;299,375;187)**; poste P/K **(725,59375;309,8125;187,5)**. Daño **5/10**, curva A2 de nueve ticks y variante sin 7D comprobados. Fracciones se cotejan en CSV, no por píxeles.
- PAL probado en suelo: holds visibles **7/16/9** refrescos; NTSC suelo **8–9/19/10–11**. Son conversiones de tiempo real, no se fuerzan 8/18/10 a 60 Hz.

### Pendientes encontrados, no ocultados

1. **Poste: cadencia visible irregular**, aunque trayectoria/timers lógicos coinciden. En la medición final K: **9/18/8**, P: **10/19/8** refrescos para 61/62/7A; 7A debería rondar 10–11 NTSC. Irregularidad observada durante el movimiento de cámara; **no hay perfil CPU/DMA que permita atribuir la causa definitivamente**. No se cambió el reloj ni el scroll global para no afectar otros movimientos.
2. **Exterior conecta, A2 y daño 5 funcionan, pero posición NO idéntica**. Fixture inicial W510/R558: b89 limita W a512 y conserva R558; arcade pasa R a546 (`AB1E→ACA4/21ED0`). Contacto MD **(540,125;309;128)** frente a arcade **(528,75;309;128)**; Vx225 vs150. No se alteraron los límites exteriores generales de b89. La fixture con R546/W510 del CSV general no selecciona Knee; la prueba válida MD exterior está en **`md_ext_knee_frames.csv`**, referencia arcade en **`arc_frames.csv`, caso outside**. El ensayo aislado `arc_outside_frames.csv` no ejecutó sub0C y **no se usa como validación**.
3. Las fixtures preparan RAM: no demuestran todos los casos de juego natural, cuatro esquinas, combinaciones fraccionarias, tiempo restante de suelo hasta levantarse ni Everdrive. La espera restante de víctima no se compara byte a byte: el fixture arcade mantiene inicialmente 200 ticks y MD usa AF66. El set MAME avisa CRC distinto de `24j6-0.112` (fondo); CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`.

## Capturas y preservación

`shots90/comparativa90_{suelo,variante,poste,exterior}_{vuelo,impacto,reaccion}.png` (12 PNG). Son fases comparables, **no una sincronización exacta por refresco**. Originales `arc_*.png`, `md90_*.png`, `md_ext_*.png` y PAL; números en `trajectory90_compare.csv`, `pose90_refreshes.csv`, `validation90.json`. Reproducible: `tools/validate90.py`, Lua de pruebas y `source90.diff`.

Auditoría: b89 intacto; recursos originales conservados como prefijo exacto. Solo crecen `spr_tab.bin` (+756 bytes) y `spr_tiles.bin` (+6880), con longitudes regeneradas en `res.h`. Esquineros, logo del ring, Hogan, HUD, IA y otros timings/animaciones intactos. **Ningún cambio deliberado fuera del alcance**; las diferencias pendientes se entregan expresamente, no se dan por resueltas.
