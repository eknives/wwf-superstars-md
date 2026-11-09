# b86 (base b85, md5 0477ea3fbf29e81b98a79ca1d574abf0; b85 intacta)

ROM: `wwf_b86.bin`. Compilación SGDK local (`PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`).
Solo: (1) timing arcade de puñetazos, (2) combo por **pulsaciones** (no hold), (3) Clothesline con hit + reacción del rival. Sin IA, sin otros movimientos.

## Qué pedía Emilio
b85 encadenaba FD70↔FD7C con **hold** (`joyHeld`) y se veía demasiado rápido. En arcade no se mantiene A: son varias pulsaciones. Además los Clothesline de ambos no tenían colisión ni reacción.

## Arcade (citas)

### Puñetazos — `sub_combo_golpes` 0xFC84
| Addr | Qué |
|------|-----|
| 0xFC84 | Tres pasos; en pasos `+0x36==0xB/0xC` hace `OR +0x114 → +0x22` (**recién pulsados**, no hold) |
| 0xFD2E | Al acabar: si `+0x22 & 3 == 1` (solo botón 1) → `eori #$1,+0xC0` y repite; si no → acción 0 |
| 0xFD70 | Punch sano: `0x150`×4, `0x151`×3, `0x152`×3 |
| 0xFD7C | Alternativa: `0x153`×4, `0x154`×3, `0x155`×3 |
| 0xFD48 | Al encadenar: `$8=1` (carga la 1ª pose del otro half al frame siguiente) |

Contenido (versión pública, sin volcado de bytes): FD70 = poses 0x150, 0x151, 0x152 con esperas 4, 3, 3; FD7C = poses 0x153, 0x154, 0x155 con esperas 4, 3, 3.

GameFAQs: `Punch = P (1 after 3 Punches)` → tras las 3 poses de un half, otra pulsación P continúa.

### Clothesline — carrera A → sub 0x14
| Addr | Qué |
|------|-----|
| 0x93EE | `acc_correr`: 0xCC26 puede lanzar golpe corriendo |
| 0xCD14 | A en carrera: Warrior/Duggan → sub **0x14** |
| 0xFB58+0x14*4 | → `0x12E7A` `sub_carrera_hombro` |
| 0x1302E | Poses embestida: `0x1D0`×6, `0x1D1`×4, `0x1DA`×4, `0x1DB`×6, … |
| 0x12E7A | Conecta antes de paso 0x10 (+0xC9 bit3); al paso 0xC rival → acción **8** sub **0x17** |
| 0x9B9A | `rec_lanzado_20` (impulso 0x20) |
| 0x16634 | Filtro proximidad colisión: \|dx\|<0x60, \|dy\|<8 |

GameFAQs: `Clothesline = P (2)` en carrera.

## Arreglo b86
1. **Combo por pulsaciones:** `pAcc` (= +0x22). Durante la última pose (mk 10..12 = 0x152/0x155) se acumula el flanco de A (`pendBtn`, ya es +0x114). Al terminar el half: solo si `(pAcc & (A|B)) == A` → `pAlt^=1; mk=2` (equiv. `$8=1`). Hold ya **no** encadena.
2. **Timing:** se mantienen las duraciones FD70/FD7C (4+3+3) en `move_seq`; no se inventan multiplicadores. El ritmo percibido baja porque hay que volver a pulsar entre halves.
3. **Clothesline hit:** en `rn==3`, si `rnk∈[1,20]` y rival a ≤0x60/≤8: `vdmg+=2`, `fsStart(o,1,…)` = caída lanzada (acción 8 / `rec_lanzado_20`). `rnW` evita multi-hit. Ambos luchadores (mismo motor).

## Caveats
- No se porta el camino CPU 0x15878 ni André (FD88/FD94).
- La animación del Clothesline atacante sigue siendo la pista MD `atkR/atkL` (ya en b83+); no se regeneran poses 0x1D0–0x1DB arcade.
- `fsStart(...,1,...)` usa el impulso del port (lanzado); arcade sub 0x17 es 0x20 exacto en parámetros A74A — aproximación del sistema de caídas ya portado.
- Un frame de solape al encadenar (como `$8=1` del arcade).

## Reproducir
```sh
cd /workspace/b86
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b86.bin && md5sum wwf_b86.bin
```

Prueba manual: un tap A = solo FD70 (0x150–152). Segundo tap A durante la última pose → FD7C. Hold sin soltar no debe encadenar. A+B en carrera → run; solo A en carrera → Clothesline; al conectar el rival sale volando/cae.
