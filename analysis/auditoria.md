# Auditoría del análisis (31-10-2026)

Muestra: 38 entradas de R (12 de la primera mitad por dirección y 26 de la segunda; semilla 20261031, tools/audit_sample.py). Se releyó cada una entera en arc_rec.dis. 6 de ellas son entradas de "datos" (bien descartadas).

## Resultado (32 rutinas de código)
- OK: 24.
- Mal: 4 (12,5 %). Además salió otro error fuera de la muestra (0x1E62).
  - 0x22040 choque_poste: la condición del daño estaba invertida. El código hace daño si la acción ≠ 8 O si es la acción 8 con sub 0xA, y la anotación decía «acción 8 salvo sub 0xA». OJO: el comentario del port (s66 wip19 main.c, línea 124) copia la versión errónea («act != 8 || a45 != 10»). No he tocado el port.
  - 0x230FC fondo_anim_publico: la condición era la contraria. Sale si 1C1890 == 1.
  - 0x945C correr_init: el ángulo es 0x40/0xC0, no 0/0x80.
  - 0x8AD8 intro_escena: 0x25408 es la cortinilla, no la «música 1».
  - 0x1E62 (fuera de la muestra): 0x24B54 es el fundido de paleta, no texto.
- Incompletas: 4.
  - 0x4000: faltaba la condición por 1C0027.
  - 0x1EC44: faltaba la rama de la CPU.
  - 0x20D60: decía solo «Ídem».
  - 0xE2CC: le falta la llamada a 0xE7E8 (se deja así, es menor).
- Cobertura: 0x73E8–0x7478 (elección al azar con 0x450A) ya tiene entrada propia (tfuera_azar).

Todo lo anterior está corregido en tools/anot2.py (copia en anot2.py.bak_auditoria) y regenerado.

## SIN CONFIRMAR
- 0x6BA0: pasa a C. Emilio ha visto en el arcade que son los flashes de cámara del público.
- Siguen SIN CONFIRMAR 0x1F86 y 0x7E4A (falta verlos en MAME).

## Discrepancias con el port s66
sistemas/discrepancias.md estaba desfasado. El cotejo se hizo en sistemas/discrepancias_s66.md contra s66/wip19/main.c (sha256 3d216c78…). Lo he vuelto a comprobar en el código:
- Kick-out propio: C. Las líneas 292/396 dicen que los kick-outs son siempre el compañero.
- Energía 0 → 13/16: C. Líneas 322 y 410: `(random()&15)>=3`.
- lieBand e/12: C (línea 366).
- Tiempo en el suelo /2 y +0x20 de fuera: C. No existen en el port.
- Reloj: C. No hay ni rastro.
- Cuenta fuera del ring: C. No hay ni rastro.
- Driver de sonido: C. La línea 124 dice que solo se guarda el id.
- random() en vez de 0x450A: C. El público ya usa un rng privado con s67 (CA_RNG=0); la IA y el pin usan random().
- Siguen V (necesitan MAME): la energía inicial 55 de la CPU y la regla de cubrir con energía < 16.

## Recomendación
Con un 12,5 % de errores y otro 12,5 % de anotaciones incompletas, todos los errores son de lectura rápida: condiciones invertidas y nombres de subrutinas supuestos. Recomiendo releer entera la segunda mitad (≥ 0x13000). Antes hay que comprobar sobre todo dos cosas: los saltos condicionales y que los nombres de las subrutinas llamadas coincidan con su entrada en R.

## 0x7E4A (seguimiento)
1C078E es un objeto cogible y arrojadizo de fuera del ring (id 1). Lo usan 0xE2CC (lanzarlo), 0xE234 (romperlo) y 0xE6E0 (pasa a id 2 y crea 1C089A).
En los combates 4/9 (los de André, según Emilio) no se crea, y además se desactiva toda la lógica de coger objetos (0x1A6C0, 0x1CDA8 y 0x1C90E).
La hipótesis de que se quita porque André necesita la VRAM o la paleta no está probada. El código lo decide por el número de combate.
Sigue SIN CONFIRMAR qué objeto es visualmente. Mr. Fuji queda descartado.

## Relectura completa (índices 0–483), 31/10/2026
Método: desensamblar cada rutina de nuevo y compararla con su anotación. Fixes en tools/reread/fixes1–12.py; se aplican con tools/reread/apply.py, que ya respeta las líneas con varias entradas.
- Primera mitad: 31 correcciones. Segunda mitad: 24 correcciones (fixes9–12) más la entrada nueva 0x73E8.
- Bugs del juego original: 0x19D96 (movea.w), 0x1BD5C (escribe d0 en vez de d1), 0x1BEE4, 0x1D0E2 (la energía no se tiene en cuenta).
- Condiciones que estaban invertidas en las notas: 0x1AE44, 0x1B7FA, 0x1B88C, 0x1B120, 0x23406, 0x244EE/0x24554 (restauración de pose).
- Renombres: 0x21420 cuerda_dibujar_1 (antes era retrato); 0x21A4E… textos_luchadores/texto_*; 0x2553C txt_destino_abs; 0x25570 txt_desplaz_tile; 0x73E8 tfuera_azar.
- SIN CONFIRMAR: nombres de los textos de 0x21BB8 (tabla de letras sin decodificar); cuál de lim_fuera/lim_ring está al revés en 0x244EE; significado de 0x4000/0x8000 en 0x26548; bucle sin fin de 0x740E si 1C0069 está lleno; 0x74C4/0x7552; banco 0x0F silla.
