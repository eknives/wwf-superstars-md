# b75 (base b74, md5 715494ea2b1a1f41ac0b4013ae7b7a0b; b74 intacta)

ROM: `wwf_b75.bin`, md5 `b2f37978b626d9bd1a072b1e655e7218`

## Evidencia arcade (leída ANTES de tocar código)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc.dis` / `rutinas.md`): y = rival.y−1 (+2 si id 0/4); z parte de **0xBB**, resta BEF2[id][rival+8] (dz). Duggan↔Warrior dz=**13** → asiento z=**174** (ruta genérica) o 200 (id 0/4 con +dz×2).
- **Tabla 0xBEF2**: D→W dx=32 dz=13; W→D dx=36 dz=13.
- **Pista s41 PT_PIN@2731** (grabada del arcade): q[3] = Z absoluto. Arranque 187 → arco ~210 → **asiento 174**. s41/s42 hacen `z0 = q[3]`.
- **s62 `wcStep` (Warrior 0x0C)**: `oy = wcY0 + q[2]` — la altura va en dy; no usa GH_SIGN sobre dY.
- **b74** fijaba `z0 = 187` en el pin (ignoraba la pista) y el S0C aplicaba `dY += GH_SIGN * q[2]` (signo opuesto al s-port) → el que se lanza quedaba **demasiado arriba**.

## Cambios (solo eje Y del lanzamiento/pin — autorizado)
1. **Pin / kick-out:** `z0 = pinZof(q[3])` — si q[3]≥128 usa la Z de la pista (Duggan); si no (WPIN/WKO flags), fallback `0xBB − 13` (BEF2).
2. **Salto Warrior 0x0C:** `oy = gY0 + q[2]` como s62; se deja de usar GH_SIGN. Tras el impacto, z asiento BEF2.
3. **Golpe a suelo 0x05/0x11:** tras el frame de impacto, z = `0xBB − 13` (mismo asiento BD10/BEF2).

Sin tocar X del pin (b74 `pnX=ox−lyo` intacto), ni IA, ni controles, ni esquineros/logo.

## Pendiente (NO en b75 — Emilio lo anota para después)
- El **puñetazo de Warrior está incompleto**. Referencia MAME: adjunto `01M6PKH6KN28S4JX7VQTBV1KMX.jpg`. No se ha tocado en b75.

## Pruebas MAME (`test/t75.lua`, pinC)
- `RESULT pin_ok`; `CENTER … err=0` (centrado X de b74 OK).
- `SETTLE z0=174 dZ=174` (antes b74 quedaba en 187) → **13 px más abajo** en pantalla (`by −=(z−187)`).
- Capturas: `shots/b75_03_pin_settle_z174.png` (después), `shots/b74_before_pin_cubre.png` (antes).

## Límites
- WPIN no trae Z en q[3]; el asiento usa el dz BEF2 D↔W (=13). Otros emparejamientos no están en este port.
- El arco visual del 0x11 de Duggan sigue en las poses (como b69); solo se baja el z al impactar.
- FC del test MAME pasa de 94→96 por el campo `gY0`.
