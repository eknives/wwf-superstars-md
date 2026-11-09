# Estudiar — dudas, no lista de cambios autorizados

- **CPU/DMA/scroll y cadencia poste:** identificar qué trabajo cruza VBlank y separar coste CPU, transporte DMA, SAT y reloj lógico. b91 sólo observó cruces, no atribución definitiva. PRIORIDAD BAJA, pulir al final. No reciclar `experimental_post91.c.txt` como solución validada.
- **Sonido público:** medir si el corte procede de muestras PCM4, disparos repetidos, Z80/mezcla o ritmo; comparar IDs/driver OKI/Z80 del análisis con recursos WAV convertidos. Síntoma comunicado, causa pendiente.
- **Macho verde / paletas prestadas:** localizar slot/banco efectivo y correspondencia CRAM; no asumir que es un sprite roto ni modificar la paleta del ring. Referencia técnica b88, `46A0`.
- **Clothesline restantes:** investigar espalda/cuerdas/CPU/variante tardía y su enlace FFFE; no aplicar bonus/duplicación al recorrido que los evita. Ver energía162BC/1642A y colisión16634.
- **Pistas suelo Duggan:** nuevo estudio ya identifica159/15A y61/62/1CB/1CC, variante1CD/1CE y poste2F. b92 ya sustituye activaciones viejas gs5/gs11 y mide MD por refresco; falta cadencia visible Elbow y auditoría gráfica exhaustiva. Límites23/24 y falta de refiltro stomp sí probados; otras esquinas/exterior quedan sin certificar. Ver estudio Duggan.
- **Energía contra pin y levantada:** flags de B, contador restante, AF66/AF6A/AF72, CPU vs humano, rescate de compañero y E0. El informe de energía contiene fórmulas; falta cotejo completo con el modelo del port antes de integrar.
- **Calidad del decompilado:** preferir `arc_rec.dis`; `arc.dis` lineal tiene94 destinos desalineados según análisis. “100% leído” histórico no implica que cada deducción sea correcta; consultar auditoria.md/sin_confirmar.md y estudios posteriores.
- **Pruebas fuera de fixtures:** fracciones/planos, cuatro esquinas, rival/humano/CPU, PAL/NTSC y Everdrive. La frecuencia física de la placa no está medida; MAME57,444852941Hz usa totales estimados.

## Añadido b92
Perfilar publicación/carga visible Elbow Duggan antes de proponer arreglo global. SAT privado no concluyente descartado. Datos pose92_refreshes.csv en 02_arcade_decompilado/notas_historicas/b92/shots92. Faltan exterior Duggan, otras esquinas, fallo poste, partida natural y Everdrive; no autoriza cambios de Warrior/render.
