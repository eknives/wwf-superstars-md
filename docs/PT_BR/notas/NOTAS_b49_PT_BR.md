# b49: fundo do Emilio + câmera livre + público animado + som do público

ROM: `wwf_b49.bin` (também `out/rom.bin`), 524.288 bytes, md5 `6d1b50331b893d52879d7a11eff9f37f`
Base: b42 (`b42_camara`). Nenhuma ROM anterior foi sobrescrita.

## O que há
- Fundo do Emilio da b42, sem mudanças (`bgb_tiles.bin`, `bgb_map.bin` e `pal.bin` são os mesmos).
- A câmera livre funciona igual à da b42: direcional para mover; A, B ou C para ir rápido.
- **Público: CROWD_ARC da s67**, com as rotinas do arcade 0x22462/0x224E8/0x225B0 (ciclo de fases {0,1,2,1,2,…,0} a 30 Hz), a grade 0x23406/0x230FC e o elemento pequeno 0x232DE/0x2336C.
  - As listas da s67 tinham sido feitas sobre o fundo antigo. `tools/remap_crowd.py` as passa para o fundo do Emilio comparando pixels: acrescenta 608 tiles novos e saem 10.244 células. Nenhuma precisou ser omitida, porque as 331 células em que o fundo do Emilio muda não coincidem com células do público.
  - O mapa na RAM usa ids de 13 bits, porque 3.540 + 608 passa de 4.095.
- **Som (driver PCM4 do SGDK, amostras OKI originais 3 e 4):**
  - 0x22 = amostra 3 uma vez. 0x23 = amostra 4 uma vez.
  - 0x50 / 0x51 = ondas: as sequências Z80 0x1152 / 0x117A copiadas tal como estão. Cada entrada reinicia a amostra com sua atenuação OKI. Os tempos vão em ticks de 100 Hz (timer B 0xDD), no total uns 9,4 s.

## Como testar
- Ao iniciar toca 0x22, como no arcade (0x1010).
- **Demo automática:** a cada 8 s há uma reação do público com onda, alternando 0x50 e 0x51. É desativada compilando com `AUTO_DEMO=0`.
- **START + A** = reação + 0x50. **START + B** = reação + 0x51. **START + C** = grade + 0x22.
- O público fica em cima e embaixo: é preciso subir ou descer a câmera para vê-lo (no centro só se vê o ringue).

## Conferido (mínimo)
- Inicia. As capturas de `shots/` não mostram tiles quebrados.
- O público muda após o disparo, uns 470 frames com mudanças.
- Há saída de áudio no início e na onda.
- Os dados estão dentro da ROM: `crowd_b49.bin` em 0x4FBC8 e os tiles em 0x5EC46. `res.h` e `res.rs` foram apagados antes de compilar.

## Falta / limites
- **Flashes de câmera (0x6BA0):** não estão. São sprites (objeto 1C09A6) e vão em outro passo.
- Sem lutadores não há disparos reais. As reações saem da demo ou dos botões.
- O volume sai baixo com o PCM4. As amostras não foram normalizadas, para não mexer no original.
- Córneres: não se aplica.
- **Sem cordas:** não há bancos de rebote nem plano A. As cordas são o próximo passo.
