# b93 — orientación del rival tumbado (base b92)

ROM `wwf_b93.bin`, MD5 **a89af7ed95159c0899430bf0e81f6441** (b92 d9af08525a0f49f4bdc025ed00499135 intacta; su fuente recompila al mismo MD5).

## Cambios (sólo los 3 puntos autorizados)
1. `oriVictima(o) = vface[o]^1` (main.c:464): el bit7 de +A arcade de un rival tumbado = el flip con que el port lo dibuja. El arcade (10A5E/A554) nunca lo cambia. Se usa en: zona Warrior C798 (`warriorGroundZone`), `kneeOutsideVictim91`, destino del salto y ajuste de poste (15A6C / ±64), caja de impacto 10FCC (`warriorGroundStep`), zona Duggan C706 (Stomp/Elbow), copia de orientación Duggan 10A6C/10BB2, solver y poste Duggan, caja Duggan.
2. Reacción A2 y espera en suelo (`kneeVictimStart90` main.c:485 y bucle main.c:1467): `dFlip = oriVictima`, `dLyo = 0` (la pose nativa A2 se coloca en Xv igual que el arcade: cabeza en Xv∓40).
3. Sin tocar asignaciones de `vface` en caídas/golpes, clothesline b88, pin, `bodyX`, `lyoOf`, cadencia 8/18/10.

## Verificado (MAME 0.276, genesis NTSC, fixtures RAM: rival tumbado vh=3 con las dos orientaciones que producen los derribos)
- Contactos = arcade exactos (x,y,z,energía): Duggan stomp/elbow/elbow espejo/elbow arriba/poste P/poste K/stomp lejos/y23 (+y24 y fallo −2 iguales); Warrior Knee cabeza izq./der., arriba, poste K/P, exterior. Ver `shots93/validation93.json`.
- Sin espejo: el flip del rival no cambia de tumbado → A2 (846/847/848, 843/844/845) → espera, en los 16 casos (`flip` en validation93.json). Capturas: el codo/rodilla cae sobre la cabeza visible; botas siguen al mismo lado.
- Clothesline: traza b88 (DL/DR/WL/WR, 147 refrescos, incl. flip/poses) idéntica byte a byte b92 vs b93; 0 errores de tiles.
- Pin: `pinStart`/contador/poses sin cambios. Pin de Duggan (bodyX) en las mismas X. Pin de Warrior (zona 2 C798) conserva la geometría arcade (torso_pin 744/760 ori0 → pin) y ahora cae en el lado visible correcto; por eso en b93 sus X respecto a `vface` son las simétricas de b92 (`shots93/pin93_b92.csv` vs `pin93_b93.csv`).

## NO verificado / pendiente
- Derribo natural en partida (sólo fixtures equivalentes), PAL, Everdrive.
- Poste por el lado opuesto (sin datos arcade de ese lado).
- Salto visual ~32 px al pasar de la pose genérica tumbada 114/752 (con `lyoOf` b74 del pin) a la A2 nativa: la A2 está donde el arcade; el desfase es de la pose genérica previa (fuera de alcance, no tocado).
- Pin de Duggan usa `bodyX` (invento b71, lado pies) mientras el del Warrior sigue el arcade: incoherencia previa, no tocada.
- Cadencia 8/18/10 (BAJA, sin cambios).
