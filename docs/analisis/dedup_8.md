# Dedup sprites 8 luchadores (sin comprimir) — 31-10-2026
Fuente: tabla 0x6CD8 del arcade (prog.bin) + tiles 16x16 del arcade (port_35/sprtiles.npy). Script: /tmp/dd.py. Solo análisis, ninguna ROM tocada.
Dedup solo dentro de cada luchador. "Idéntico" = píxel a píxel, o igual con volteo H, V o H+V. 4bpp, 32 B por tile 8x8.
Nº de poses = las que lee la tabla con la heurística npose() de sheets.py (puede incluir alguna entrada no usada: SIN CONFIRMAR).

| Banco | Luchador | Poses | Antes | Poses repetidas fuera | Piezas 16x16/16x32 únicas | Tiles 8x8 únicos |
|---|---|---|---|---|---|---|
| 0 | Warrior | 509 | 1.21 MB | 0.92 MB | 0.43 MB | 0.31 MB |
| 1 | Hogan | 523 | 1.12 MB | 0.89 MB | 0.48 MB | 0.34 MB |
| 2 | Macho | 499 | 1.09 MB | 0.90 MB | 0.47 MB | 0.33 MB |
| 3 | Duggan | 532 | 1.14 MB | 0.90 MB | 0.47 MB | 0.34 MB |
| 4 | Bossman | 527 | 1.21 MB | 0.95 MB | 0.46 MB | 0.32 MB |
| 5 | Honky | 482 | 0.99 MB | 0.75 MB | 0.39 MB | 0.28 MB |
| 6 | DiBiase | 662 | 1.43 MB | 1.03 MB | 0.54 MB | 0.39 MB |
| 7 | André | 410 | 1.03 MB | 0.53 MB | 0.32 MB | 0.22 MB |
| | **Total** | | **9.22 MB** | **6.87 MB** | **3.56 MB** | **2.53 MB** |

Resto (global): árbitro 27 KB, postes 21 KB, mesa 12 KB, efectos 127 KB, textos 2 KB, silla 5 KB (nivel pieza).

Notas:
- Nivel pieza es aprovechable en Mega Drive (cada pieza = un sprite HW con volteo entero).
- Nivel tile 8x8 solo vale si se montan los tiles por DMA en cada frame (los sprites MD necesitan tiles consecutivos). Es el límite mínimo.
- Hueco b24: ~1.4 MB + ~230 KB ≈ 1.63 MB, más lo que ya ocupan Duggan+Warrior dentro de los 2.2 MB.
- **No cabe** en 4 MB ni a nivel pieza (3.56 MB) ni a nivel tile (2.53 MB). Sin compresión hace falta cartucho más grande (banking), o comprimir.
