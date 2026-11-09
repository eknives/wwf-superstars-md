# b73 (base b72, md5 74c37dc8839ec8780a122eabfc71a58d; b72 intacta)

ROM: `wwf_b73.bin`, md5 `684b4b738f4255cb231fa286d401fdef`

## Evidencia arcade usada
- **0x1190C / 0x11A72** (`analisis/rutinas.md`, `prog.bin`): cubrir solo si el rival está en acción 0xB, **dentro** (`+0x19==0`) y el atacante no está fuera. No hay margen extra «cerca de cuerdas».
- **0xACA4** (`suelo_chk_cuerdas`): al tumbarse prueba ±0x30 y ±8 con clamp **0x21E5A**; deja el cuerpo dentro (no sobre la cuerda).
- **0xBD10 + tabla 0xBEF2** (`prog.bin`): el que cubre en `ox_rival ± dx` (Duggan→Warrior **36**, Warrior→Duggan **32**), y = rival−1. Igual que s41 (`pinX = ox` víctima).
- **0x21E5A** (`s66/cuerdas_casos.md`): límites inclinados del ring (m=0).

## Cambios (solo lo autorizado)
1. **Pin al lado de las cuerdas OK; sobre/fuera NO.** Se deshace el bloqueo agresivo de b72 (`m=6/4` + veto del árbitro). `groundOK` usa la regla 0x1190C/0x21E5A (m=0): cuerpo o atacante pasado el límite = no; dentro (aunque junto a la cuerda) = sí.
2. **0xACA4 al caer** (`soilNudge`): al pasar a tumbado (vh=3) empuja el cuerpo dentro con la misma lógica 0x30/8 + clamp.
3. **Centrado del que cubre:** `pnX = ox` del rival (arcade/s41/BEF2). Durante el pin se apaga el `lyo` del tumbado para que el sprite comparta el ox de la pista (antes el lyo ±32 lo desalineaba respecto a la cover).

## Sin tocar
Sin IA (el otro solo persigue con START). Mismos controles. Esquineros de arriba, logo WWF y paletas intactos.

## Pruebas MAME (`test/t73.lua`)
- **pinC**: pin en centro; `CENTER ox=720 cover=756 expect=756 err=0`.
- **pinSide**: junto a cuerda izquierda; pin OK.
- **pinOn**: cuerpo forzado fuera del límite; pin bloqueado (`RESULT blocked_ok`).
Capturas en `shots/` (`hoja_b73.png`).
