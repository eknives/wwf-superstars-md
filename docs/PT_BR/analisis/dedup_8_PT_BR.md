# Dedup de sprites dos 8 lutadores (sem compressão) — 31-10-2026
Fonte: tabela 0x6CD8 do arcade (prog.bin) + tiles 16x16 do arcade (port_35/sprtiles.npy). Script: /tmp/dd.py. Só análise, nenhuma ROM mexida.
Dedup só dentro de cada lutador. "Idêntico" = pixel a pixel, ou igual com flip H, V ou H+V. 4bpp, 32 B por tile 8x8.
Nº de poses = as que a tabela lê com a heurística npose() de sheets.py (pode incluir alguma entrada não usada: NÃO CONFIRMADO).

| Banco | Lutador | Poses | Antes | Poses repetidas fora | Peças 16x16/16x32 únicas | Tiles 8x8 únicos |
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

Resto (global): árbitro 27 KB, postes 21 KB, mesa 12 KB, efeitos 127 KB, textos 2 KB, cadeira 5 KB (nível peça).

Notas:
- O nível peça é aproveitável no Mega Drive (cada peça = um sprite HW com flip inteiro).
- O nível tile 8x8 só vale se os tiles forem montados por DMA a cada frame (os sprites MD precisam de tiles consecutivos). É o limite mínimo.
- Espaço livre b24: ~1.4 MB + ~230 KB ≈ 1.63 MB, mais o que Duggan+Warrior já ocupam dentro dos 2.2 MB.
- **Não cabe** em 4 MB nem no nível peça (3.56 MB) nem no nível tile (2.53 MB). Sem compressão é preciso um cartucho maior (banking), ou comprimir.
