# ROMs entregadas — changelog documental

48 binarios identificados por nombre propio en b48–b95 (las ROMs no se publican: contienen gráficos y sonido convertidos del arcade; sólo se indican sus MD5). Para versiones anteriores no se identificó un binario entregado con nombre inequívoco.

Versión condensada: la nota completa de cada versión está en `docs/notas/NOTAS_bNN.md`. Una limitación histórica puede estar corregida por una versión posterior.

## b95 — ENTREGADA
ROM wwf_b95.bin; MD5 7be789d70d892c1efb86af8630b296a6. Base b94.
Pedido: exactamente 3 puntos (PATRON_MOVIMIENTOS.md §9/§10): (1) carrera con velocidad 0x95BC (W28/D27), paso por arcTick, pose cada 2 ticks; (2) columnas/filas del fondo por DMA en cola con presupuesto; (3) choque contra cuerda 9E78/9CD0/9F02 y soilNudge con bit7 = vface^1. MAME: carrera W 200,5/D 194,0 px/s NTSC y 199,7–200,1/192,6–193,0 PAL (arcade 201,1/193,9; b94 PAL 167,7); frames perdidos hacia postes 20/14/18/19 → 3/2/1/0 de 580 sin corrupción de fondo; zafar pin Xv 760/728/708/693/832 → 642/643/677/677/859 = arcade; rebote carrera, salir del ring, clothesline y pin siguen bien. Sin verificar: hardware real, choque sub 1 por lanzamiento vs arcade, derribos por golpes junto a cuerda vs arcade, sonido 0x29 (no existe en el port).

## b94 — ENTREGADA
ROM wwf_b94.bin; MD5 b2a8ff5d4453067ad3d2bf8762239413. Base b93.
Pedido: sólo 2 puntos (PATRON_MOVIMIENTOS.md §8): (1) tumbado 114/752 sin lyoOf ±32; (2) pin: cubre en Xv∓32 (W) / Xv∓36 (D), Warrior mira al revés que el tumbado (513/514/778 con su volteo), entrada pin Duggan = zona cuerpo CB75. Barrido B = arcade en W y D, ambas orientaciones; quien cubre X/Y/Z = arcade; sin salto tumbado→A2 ni al levantarse; clothesline idéntico b93; zafar y cuenta de 3 funcionan. Pendiente: salto al aterrizar tras zafar cerca de cuerda (ACA4); zafar/cuenta no medidos en MAME arcade.

## b93 — ENTREGADA
ROM wwf_b93.bin; MD5 a89af7ed95159c0899430bf0e81f6441. Base b92.
Pedido: sólo los 3 puntos de orientación del rival tumbado (PATRON_MOVIMIENTOS.md §6). Hecho: `oriVictima=vface^1` en zonas/destino/poste/caja/exterior/copia Duggan (Stomp incluido) y A2/espera sin espejo. Contactos = arcade en 16 casos; clothesline idéntico a b92; pin sin cambios de mecanismo. Pendiente: salto ~32 px de pose genérica tumbada→A2, poste lado opuesto sin datos arcade, cadencia BAJA.

## b92 — ENTREGADA (PARCIAL en fidelidad visible)
ROM wwf_b92.bin; MD5 d9af08525a0f49f4bdc025ed00499135.
Pedido: sólo Stomp/Elbow cabeza/Elbow poste Duggan. Hecho: zonas/motor/poses nativos, física/contacto/daños1/5/10/A2/fallo−2 contrastados. Stomp sí en ensayos; Elbow PARCIAL por cadencia visible. Warrior y render sin modificar; b91 intacta.

**Actualización posterior autorizada:** b92 ya está entregada; cadencia visible del Elbow Drop Duggan suelo/poste pasa a **PRIORIDAD BAJA, «pulir al final»**, junto al Knee Warrior poste. No se modifica el binario ni se abre otra versión. La nota original siguiente conserva el estado y límites medidos al entregar.

## b91
ROM `wwf_b91.bin`, 1703936 bytes; MD5 `1f7f183b0ef6fe6367d62360697935c6`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b91.md`.

## b90
ROM `wwf_b90.bin`, 1703936 bytes; MD5 `24759dec91fa996dc6e7a2f227e30f45`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b90.md`.

## b89
ROM `wwf_b89.bin`, 1703936 bytes; MD5 `7c1c5202f5fb27f115278eecd9b9ffb9`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b89.md`.

## b88
ROM `wwf_b88.bin`, 1703936 bytes; MD5 `96371335c6b9cb43b08d158ba73ec488`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b88.md`.

## b87
ROM `wwf_b87.bin`, 1572864 bytes; MD5 `f956cfbcbf5012f63d66c8b0ac457a0d`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b87.md`.

## b86
ROM `wwf_b86.bin`, 1572864 bytes; MD5 `0cbe0756ba9ff3dff97b4acfaa8a76b8`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b86.md`.

## b85
ROM `wwf_b85.bin`, 1572864 bytes; MD5 `0477ea3fbf29e81b98a79ca1d574abf0`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b85.md`.

## b84
ROM `wwf_b84.bin`, 1572864 bytes; MD5 `426988a7344009ffd63ad6e8f34e609b`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b84.md`.

## b83
ROM `wwf_b83.bin`, 1572864 bytes; MD5 `028b1ee1de56104bb26ab5fc56810c80`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b83.md`.

## b82
ROM `wwf_b82.bin`, 1572864 bytes; MD5 `b6c57f8cb194c7c7805b5a75b3775dc8`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b82.md`.

## b81
ROM `wwf_b81.bin`, 1572864 bytes; MD5 `ffa3e48e22aee99750cd82af10d6ab31`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b81.md`.

## b80
ROM `wwf_b80.bin`, 1572864 bytes; MD5 `d843bac410485579980872341264fda9`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b80.md`.

## b79
ROM `wwf_b79.bin`, 1572864 bytes; MD5 `80c22913744ca241ac6a4673d64b7a09`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b79.md`.

## b78
ROM `wwf_b78.bin`, 1572864 bytes; MD5 `baa09bf2c1316b25c6881ca0ec0a4019`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b78.md`.

## b77
ROM `wwf_b77.bin`, 1572864 bytes; MD5 `947bdf6ccc66d33c7d9ecc526e3e8e97`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b77.md`.

## b76
ROM `wwf_b76.bin`, 1572864 bytes; MD5 `49075e62b6b23d071da6035564adcea8`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b76.md`.

## b75
ROM `wwf_b75.bin`, 1572864 bytes; MD5 `b2f37978b626d9bd1a072b1e655e7218`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b75.md`.

## b74
ROM `wwf_b74.bin`, 1572864 bytes; MD5 `715494ea2b1a1f41ac0b4013ae7b7a0b`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b74.md`.

## b73
ROM `wwf_b73.bin`, 1572864 bytes; MD5 `684b4b738f4255cb231fa286d401fdef`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b73.md`.

## b72
ROM `wwf_b72.bin`, 1572864 bytes; MD5 `74c37dc8839ec8780a122eabfc71a58d`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b72.md`.

## b71
ROM `wwf_b71.bin`, 1441792 bytes; MD5 `dbfe401359b8f726186dd01e82cd5b2c`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b71.md`.

## b70
ROM `wwf_b70.bin`, 1441792 bytes; MD5 `24854415d3674c5e784b99ea9f7cc8da`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b70.md`.

## b69
ROM `wwf_b69.bin`, 1441792 bytes; MD5 `b3d460cb3f2bd3bc97338e499f1c2046`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b69.md`.

## b68
ROM `wwf_b68.bin`, 1310720 bytes; MD5 `3a41cd79ddf5d3b669c0475ca56ca20c`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b68.md`.

## b67
ROM `wwf_b67.bin`, 1310720 bytes; MD5 `593ceefe80133aeb5b5e737fd1ec7807`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b67.md`.

## b66
ROM `wwf_b66.bin`, 1310720 bytes; MD5 `037a4213d712fd0e7124bbe5322e1080`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b66.md`.

## b65
ROM `wwf_b65.bin`, 1310720 bytes; MD5 `ae934feebe83857623862ca7123f43b3`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b65.md`.

## b64
ROM `wwf_b64.bin`, 1310720 bytes; MD5 `9b3cffff1bd585fc241f684f09ab77a4`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b64.md`.

## b63
ROM `wwf_b63.bin`, 1310720 bytes; MD5 `c4e24dd1024eced745681c0bd9c0ef7d`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b63.md`.

## b62
ROM `wwf_b62.bin`, 1310720 bytes; MD5 `6c4316bb90496df914dd0e75e6b536d8`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b62.md`.

## b61
ROM `wwf_b61.bin`, 1179648 bytes; MD5 `080a39c45570498fe8dab0dec0c8b4b8`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b61.md`.

## b60
ROM `wwf_b60.bin`, 1179648 bytes; MD5 `5986c9c1f2a51854b2ebda56407ce6a0`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b60.md`.

## b59
ROM `wwf_b59.bin`, 1179648 bytes; MD5 `9147ee11d533442397987e165520be45`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b59.md`.

## b58
ROM `wwf_b58.bin`, 1179648 bytes; MD5 `cbe3a2b0976a142ceb25068edc660869`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b58.md`.

## b57
ROM `wwf_b57.bin`, 1179648 bytes; MD5 `8651e4ef71af09be6260350b1489e20d`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b57.md`.

## b56
ROM `wwf_b56.bin`, 1179648 bytes; MD5 `69171a59c5c65f55f93bfeb09de3d094`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b56.md`.

## b55
ROM `wwf_b55.bin`, 1179648 bytes; MD5 `e00cc84cccd7180ed7822ff219e3c978`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b55.md`.

## b54
ROM `wwf_b54.bin`, 1179648 bytes; MD5 `dad17974aae704c185eaf92d7e869de3`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b54.md`.

## b53
ROM `wwf_b53.bin`, 1179648 bytes; MD5 `61a87b67e3fbb6df3b64dd7362789db2`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b53.md`.

## b52
ROM `wwf_b52.bin`, 524288 bytes; MD5 `7c3254185b41c1494120155d126850e7`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b52.md`.

## b51
ROM `wwf_b51.bin`, 524288 bytes; MD5 `328134aa6dde7116b2ac863ecea7eb29`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b51.md`.

## b50
ROM `wwf_b50.bin`, 524288 bytes; MD5 `68f778ed3bbc111e38fa0ebeb78e93df`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b50.md`.

## b49
ROM `wwf_b49.bin`, 524288 bytes; MD5 `6d1b50331b893d52879d7a11eff9f37f`.

**Qué se pidió / qué se hizo / pendiente:** declaración de esa versión a continuación; si la nota no separa la petición original o no declara pendientes, no se reconstruyen ni se dan por cerrados. Fuente: `notas/NOTAS_b49.md`.

## b48
ROM `wwf_b48.bin`, 2752512 bytes; MD5 `8721a90f5a03b5ddfd21987096ca0f4b`.

**Pedido:** no consta en una NOTAS propia localizada. **Hecho:** sólo se acredita existencia del binario y MD5. **Pendiente:** no documentado; no inferido.
