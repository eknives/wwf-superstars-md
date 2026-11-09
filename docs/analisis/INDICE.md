# Análisis WWF Superstars (arcade) — ÍNDICE
Estado (31-10-2026): 100 % leído, AUDITADO por muestra (auditoria.md). Muestra de 32 rutinas: 12,5 % mal y 12,5 % incompletas, corregidas. Se recomienda releer la segunda mitad. SIN CONFIRMAR: 2 (0x1F86, 0x7E4A; 0x6BA0 confirmado por Emilio). Discrepancias con s66: sistemas/discrepancias_s66.md (cotejado y reverificado); discrepancias.md está obsoleto.
- arc_rec.dis: desensamblado recursivo con cabeceras de rutina (el bueno). arc.dis: el lineal (desalineado en 94 destinos).
- rutinas.md: tabla de rutinas anotadas. ram.md: mapa de RAM y de hardware. tablas.md: tablas de ROM.
- sistemas/: bucle principal, luchadores, cuerdas, público, mareo, RNG y discrepancias. Los apartados IA, árbitro, sonido y pin/cuenta están solo esbozados.
- Herramientas: tools/rdis.py, rd.py, dump.py, sig.py, anot.py, cg.py.

## Añadido (100 %)
- sistemas/sonido.md: driver Z80, OKI, campana 0x20/0x21 e IDs (con sonido_ids_llamadas.txt).
- sistemas/arbitro.md, sistemas/pin_cuenta.md y sistemas/reloj.md.
- sistemas/discrepancias_s66.md: cotejo con wip19, solo lectura.
- Cobertura: 100 % de bytes; 50.062/50.062 instrucciones 68K en rutinas leídas (sin contar los bloques de datos); Z80 con 1.200 instrucciones y 2.523 bytes alcanzados, todo leído.


## Nombres de banco (+0x2B / índice de 0x6CD8)
Verificado en MAME 31-10-2026 (demo de atracción, /workspace/idp): +0x2B = banco (+3, copiado en 0x7F44); el rótulo de cada exhibición coincide con el id del objeto 1 (Hogan 1, Warrior 0, Macho 2, Duggan 3, Bossman 4, Honky 5). La casilla de selección NO es el id: 0x7FE2 convierte casilla→banco (0→2,1→1,2→0,3→5,4→3,5→4,6→6,7→7).
| Banco | Contenido |
|---|---|
| 0 | Ultimate Warrior |
| 1 | Hulk Hogan |
| 2 | Macho Man |
| 3 | Jim Duggan |
| 4 | Big Bossman |
| 5 | Honky Tonk Man |
| 6 | Ted DiBiase |
| 7 | André the Giant |
| 8 | mesa |
| 9 | árbitro |
| 0x0A | postes |
| 0x0F | silla (SIN CONFIRMAR) |
| 0x10 | efectos |
| 0x11 | textos |

Ojo: 0x4D4C y 0x5F54 ponen "banco 0x10" en objetos de luchador; ahí el valor puede ser otro campo y no el banco gráfico (SIN CONFIRMAR).
