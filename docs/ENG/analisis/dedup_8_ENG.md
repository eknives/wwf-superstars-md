# Sprite dedup of the 8 wrestlers (uncompressed) — 31-10-2026
Source: arcade table 0x6CD8 (prog.bin) + arcade 16x16 tiles (port_35/sprtiles.npy). Script: /tmp/dd.py. Analysis only, no ROM touched.
Dedup only within each wrestler. "Identical" = pixel for pixel, or equal with H, V or H+V flip. 4bpp, 32 B per 8x8 tile.
No. of poses = those read from the table with the npose() heuristic of sheets.py (may include some unused entry: UNCONFIRMED).

| Bank | Wrestler | Poses | Before | Repeated poses removed | Unique 16x16/16x32 pieces | Unique 8x8 tiles |
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

Rest (global): referee 27 KB, posts 21 KB, table 12 KB, effects 127 KB, texts 2 KB, chair 5 KB (piece level).

Notes:
- Piece level is usable on Mega Drive (each piece = one HW sprite with whole flip).
- 8x8 tile level only works if the tiles are assembled via DMA every frame (MD sprites need consecutive tiles). It is the lower bound.
- b24 free space: ~1.4 MB + ~230 KB ≈ 1.63 MB, plus what Duggan+Warrior already occupy within the 2.2 MB.
- **It does not fit** in 4 MB either at piece level (3.56 MB) or at tile level (2.53 MB). Without compression a bigger cartridge (banking) is needed, or compression.
