# b92 — entrega PARCIAL: suelo Duggan

ROM `/workspace/b92/wwf_b92.bin` — **MD5 `d9af08525a0f49f4bdc025ed00499135`**, 1703936 bytes. Base b91 intacta. **Stomp verificado en los ensayos; Elbow suelo/poste funcionales y física cotejada, pero la cadencia visible NO es todavía idéntica. No dar por cerrado todo el encargo.**

## 1. Stomp — verificado en los casos ensayados
- C706/C79E–C8A8 y CB6C/CB75: P=A en cuerpo, mismo plano, |dy|<24, ancla cabeza Xv±40 y límites estrictos originales. 1173A/118BC: 159×14 y 15A×10 refrescos arcade; daño1 en 117E0 al entrar15A (11782→1179A), sin segundo filtro XY.
- Motor Duggan independiente `src/duggan92.h`, reloj arcTick existente sin modificarlo. Mantiene 7ticks de159 y 5 de15A contando salida. MAME57,444852941Hz, tick=2refrescos; MD conserva tiempo real, no copia14/10 literalmente a60/50Hz. Muestra NTSC15/11, PAL13/8; compatibles con conversión y cuantización.
- Entrada normal, |dy|23 aceptado /24 rechazado y rival desplazado aX900 después de iniciar: mismo daño48→47 en MD y MAME. Impacto normal(744;300;187). Reacción A2 cotejada.

## 2. Elbow de cabeza — PARCIAL
- CB72, sub11→10A5E por FB9C; tablas11180/11188→111F0, poses11372:61/62/1CB/1CC, variante1CD/1CE. Holds nativos iniciales8/18/10 refrescos. Solver159AC, integración3DCE/3E20: Vz0x500, gravedad0x50 por refresco; límites0x2000. Desvío interior64, exterior32; orientación de víctima, no regla Vx de Warrior.
- 11084/110BC/110C0: descendiendo y altura≤suelo+16, punto Xa±8,Ya+4 contra rectángulo nativo. Impacto conserva fracciones: Yword=Yv−1, Zword=suelo; sin7D ni choque de cuerda artificial (24102→24322,24106→24324 son RTS). Daño5(10DC0), A2(A554/28EC).
- Contactos exactos MD/MAME: normal(697;299;187), espejo(823;299;187), variante(697;299,375;187), energía48→43. A2:4/7/9/10/10/9/7/4/0, cotejo RAM de ambos. Fallo10C6A:−2, retroceso24 según orientación,1CF→16→17→1A(9FCC/AF66/AA00); contacto de fallo(672,0625;300),48→46.
- **Pendiente cadencia visible:** NTSC61/62/1CB=10/17/12 frente a conversión esperada8–9/18–19/10–11. Espejo10/18/10; variante9/18/10. PAL también tiene discrepancias. La lógica usa arcTick, pero no certifica duración visible; ver `pose92_refreshes.csv` y PNG consecutivos.

## 3. Elbow poste P/K — PARCIAL
- F6EF=`2F,20,20`, despachoFC14→10A5E. Misma física/poses Duggan, ajustes10B5E/110E4. Daño10(10DCC); fallo nativo compartido, no un nuevo salto genérico.
- P y K conectan en MD/MAME(694,34375;299,8125;187,5), Vx399,Vy−462, energía48→38 y A2. **88 estados estables de trayectoria** suelo/espejo/variante/poste coinciden;0sin muestra.
- **NO resuelta la cadencia visible:** NTSC P9/21/5 y K6/19/12; arcade8/18/10 antes de convertir frecuencia. PAL P4/18/7,K8/18/5. No se corrigió el render global ni el poste Warrior. Ensayo SAT privado descartado: `tools/experimental_sat92*`, NO compilado. Causa precisa CPU/DMA/publicación aún no aislada; no se atribuye gratuitamente a una de ellas.

## Evidencia y límites
- MAME0.276: arcade `wwfsstar`, MD `genesis` y PAL `megadriv`, diez casos breves por región, fixtures RAM + botones reales. `shots92/validation92.json`, `arc_frames.csv`, `md92_knee_frames.csv`, `pal_md92_knee_frames.csv`, `trajectory92_compare.csv`, `pose92_refreshes.csv`. Scripts en `tools/`.
- PNG: `comparativa92_stomp_impacto.png`, `comparativa92_elbow_{vuelo,impacto,reaccion}.png`, `comparativa92_elbow_mirror_impacto.png`, `comparativa92_elbow_above_impacto.png`, `comparativa92_corner{P,K}_{vuelo,impacto,reaccion}.png`, `comparativa92_miss.png`. Fases comparables, cámaras/refrescos NO sincronizados; no son certificación píxel a píxel de paletas. Secuencias `refresh_{stomp,elbow,cornerP}_f*.png`.
- Regresión Warrior: mismas funciones/headers y render original, mismos contactos/energía que b91 en suelo,variante,posteP/K,exterior. Cadencia de poste ya irregular permanece: muestras en `warrior92_refreshes.csv`, NO se afirma igualdad visible. No se probó Everdrive, partida completa, todas las esquinas, exterior Duggan ni fallo desde poste.
- Sólo cambia main.c para entrada/motor Duggan, nuevos `duggan92.h`/`duggan92_poses.h`, y apéndices de tablas/tiles con12poses de banco3(6CD8/7FE2; conversor `tools/gen92.py`). Prefijo gráfico anterior idéntico. Resto res intacto, Hogan/esquineros/logo/selección/energía ajena/Warrior sin editar. `source92_main.diff`, `b91_manifest92.json`.
- Arcade CPU MD5 `4bd7c20fe4dbaf1b7ee8225e0e5d7359`; MAME conserva aviso CRC fondo24j6-0.112. No se empaqueta ROM arcade en backup.
- **Fuera de alcance en la ROM: nada intencionado. Pendiente principal b92: cadencia visible de Elbow, no suplantar esta limitación con la coincidencia lógica.**
