# b83 (base b82, md5 b6c57f8cb194c7c7805b5a75b3775dc8; b82 intacta)

ROM: `wwf_b83.bin`, md5 `028b1ee1de56104bb26ab5fc56810c80`. Compilación SGDK local.
Solo remate Warrior sobre rival tumbado (zona + animación + capas 7D). Sin inventar: `/workspace/wwf_sgdk/analisis` + ROM arcade MAME.

## Fallo de b82 (lo que Emilio vio)
1. **Zona inventada:** b82 usaba `X = ox±48` y `b7 = !vface`. Desde el **torso** (mismo X que el rival) lanzaba el salto; en arcade **no**.
2. **Destino mal:** `ox±16` en vez de `±0x20` (tabla 0x111D0 / 0x159AC).
3. **Orientación mal:** `p1face = vface` en vez de copiar bit7 y mapear `p1face = !bit7` (0x10A6C).
4. **7D mal horneado:** `native82` hacía un segundo mirror y `+4` en el bitmap → pierna/puño **duplicados** a un lado.
5. **Fase 0:** 4 ticks inventados; arcade `0x112F0[0]=0` → 1 tick de pose 0x61.

## Arcade (citas)
| Addr | Qué |
|------|-----|
| 0xC706 / 0xC798–0xC8A8 | Selección: ancla = rival.x ±0x28 según bit7; frente `<0x20` → sub 0x0C; detrás `<0x30` → A sub5 / B sub6 |
| 0xC928–0xC95A | Pin solo si d4==0 y d\<0x20; si no B → sub1 |
| 0xCB3C | Warrior: tabla de subacciones por zona (B delante = 0x0C); volcado de bytes omitido en la versión pública |
| 0xCB1A[0xB] | 0xFF → rama tumbado |
| 0x10A5E / 0x10A6C | Salto; copia orientación del rival |
| 0x111D0 / 0x159AC | Trayectoria dx=0xFFE0 (−32), espejo si bit7; vz=0x500 g=0x50 |
| 0x112F0 | Timers `0, 8, 4, FFFF` |
| 0x112FA | Poses `61 62 7A 7B 7B` (+ variante `61 62 76 77 77`) |
| 0x10D9E / 0x10F04 | Impacto: z=suelo, y=rival−1+0xA |
| 0x1152A | Objeto 1C0AB2 pose **0x7D**: y−0xA, x∓4, z+0xA, **ori opuesta** |

## Arreglo b83
- `warriorGroundZone`: `X = fd[o].ox`, `b7 = vface` (fsStart ya copia bit7 → vface). **Sin ±48.**
- Destino: `ox ± 0x20`; `p1face = !vface`.
- Fase 0: 1 tick.
- 7D: tiles sin mirror/+4; en `drawF` la capa aux usa **flip opuesto** y **dx = fl ? −4 : +4** (1152A). Sort y−10.

## Pruebas MAME Genesis + arcade
| Caso | Resultado |
|------|-----------|
| diveL / headL | 712→727 impact y=309 pose787 — **igual log arcade** |
| diveR / headR | 808→793 |
| feetL/R, **torsoR** | **no salta** (gs=0) |
| front31 / front32 | 12 / 0 |
| behind47 / behind48 | 13 / 0 |
| stompR, pinL/R | OK |
| Arcade MAME `shots/arcade/k063` | aux 7D en x=723 (=727−4), y=299 (=309−10) |

## Capturas
- `shots/arcade/` — MAME wwfsstar suelo (no esquina).
- `shots/FINAL_b83/compare_arcade_vs_b83.png` — arcade vs port.
- `shots/FINAL_b83/port_diveL_pose_*.png`

## Reproducir
```sh
cd /workspace/b83
python3 tools/native82.py
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b83.bin && md5sum wwf_b83.bin
./test/run83.sh diveL
```
