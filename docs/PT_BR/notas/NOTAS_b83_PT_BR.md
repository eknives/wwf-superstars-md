# b83 (base b82, md5 b6c57f8cb194c7c7805b5a75b3775dc8; b82 intacta)

ROM: `wwf_b83.bin`, md5 `028b1ee1de56104bb26ab5fc56810c80`. Compilação SGDK local.
Só o golpe final do Warrior sobre o rival deitado (zona + animação + camadas 7D). Sem inventar: `/workspace/wwf_sgdk/analisis` + ROM arcade no MAME.

## Erro da b82 (o que o Emilio viu)
1. **Zona inventada:** a b82 usava `X = ox±48` e `b7 = !vface`. A partir do **torso** (mesmo X do rival) lançava o salto; no arcade **não**.
2. **Destino errado:** `ox±16` em vez de `±0x20` (tabela 0x111D0 / 0x159AC).
3. **Orientação errada:** `p1face = vface` em vez de copiar o bit7 e mapear `p1face = !bit7` (0x10A6C).
4. **7D mal embutido:** `native82` fazia um segundo espelhamento e `+4` no bitmap → perna/punho **duplicados** para um lado.
5. **Fase 0:** 4 ticks inventados; arcade `0x112F0[0]=0` → 1 tick da pose 0x61.

## Arcade (citações)
| Addr | O quê |
|------|-----|
| 0xC706 / 0xC798–0xC8A8 | Seleção: âncora = rival.x ±0x28 conforme o bit7; frente `<0x20` → sub 0x0C; atrás `<0x30` → A sub5 / B sub6 |
| 0xC928–0xC95A | Pin só se d4==0 e d\<0x20; se não B → sub1 |
| 0xCB3C | Warrior: tabela de subações por zona (B na frente = 0x0C); dump de bytes omitido na versão pública |
| 0xCB1A[0xB] | 0xFF → ramo deitado |
| 0x10A5E / 0x10A6C | Salto; copia a orientação do rival |
| 0x111D0 / 0x159AC | Trajetória dx=0xFFE0 (−32), espelho se bit7; vz=0x500 g=0x50 |
| 0x112F0 | Timers `0, 8, 4, FFFF` |
| 0x112FA | Poses `61 62 7A 7B 7B` (+ variante `61 62 76 77 77`) |
| 0x10D9E / 0x10F04 | Impacto: z=chão, y=rival−1+0xA |
| 0x1152A | Objeto 1C0AB2 pose **0x7D**: y−0xA, x∓4, z+0xA, **orientação oposta** |

## Correção b83
- `warriorGroundZone`: `X = fd[o].ox`, `b7 = vface` (fsStart já copia bit7 → vface). **Sem ±48.**
- Destino: `ox ± 0x20`; `p1face = !vface`.
- Fase 0: 1 tick.
- 7D: tiles sem espelho/+4; em `drawF` a camada aux usa **flip oposto** e **dx = fl ? −4 : +4** (1152A). Sort y−10.

## Testes MAME Genesis + arcade
| Caso | Resultado |
|------|-----------|
| diveL / headL | 712→727 impact y=309 pose787 — **igual ao log do arcade** |
| diveR / headR | 808→793 |
| feetL/R, **torsoR** | **não salta** (gs=0) |
| front31 / front32 | 12 / 0 |
| behind47 / behind48 | 13 / 0 |
| stompR, pinL/R | OK |
| Arcade MAME `shots/arcade/k063` | aux 7D em x=723 (=727−4), y=299 (=309−10) |

## Capturas
- `shots/arcade/` — MAME wwfsstar chão (não córner).
- `shots/FINAL_b83/compare_arcade_vs_b83.png` — arcade vs port.
- `shots/FINAL_b83/port_diveL_pose_*.png`

## Reproduzir
```sh
cd /workspace/b83
python3 tools/native82.py
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b83.bin && md5sum wwf_b83.bin
./test/run83.sh diveL
```
