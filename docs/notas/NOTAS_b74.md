# b74 (base b73, md5 684b4b738f4255cb231fa286d401fdef; b71/b72/b73 intactas)

ROM: `wwf_b74.bin`, md5 `715494ea2b1a1f41ac0b4013ae7b7a0b`

## Evidencia arcade (leída ANTES de tocar código)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc_rec.dis`, `rutinas.md`): y = rival.y−1 (+2 si id 0/4); x = rival.x ± BEF2[id][rival]; z = 0xBB − BEF2[id][rival+8]. Signo de dx: `btst #7,+0xA(rival)` → si claro, `neg.w d1`.
- **Tabla 0xBEF2** (`prog.bin`): por atacante `id*0x10`, byte dx en `[rival]`, dz en `[rival+8]`.
  - Duggan(0)→Warrior(1): dx=**32**, dz=13
  - Warrior(1)→Duggan(0): dx=**36**, dz=13
- **0x1190C / 0x11A72**: cubrir solo si rival acción 0xB, **dentro** (`+0x19==0`) y atacante no fuera. No hay veto «cerca de cuerda».
- **0xACA4**: al tumbarse prueba ±0x30/±8 + clamp 0x21E5A (empuja el cuerpo dentro).
- **Pista s41** (`sp_trk` PT_PIN@2731): en el settle (frame 28) dx=**36**, dy=0 (la pista ya lleva el offset visual del arcade). Origen de la pista = x arcade del rival (= centro del cuerpo).
- **Ref. visual Emilio (MAME arcade)**: cubridor tendido torso-sobre-torso; árbitro debajo del pin contando.

## Por qué b73 quedó peor
- Pose tumbada **114/626**: el torso del sprite está ~28 px a un lado del origen.
- `lyo` (±32) corrige eso al dibujar (`bodyX = ox+lyo`).
- b73 **apagó el lyo** durante el pin y puso `pnX=ox`. El métrico `err=0` comparaba cover con `ox+36` (la propia fórmula), no con el torso visible → gap visual ~60 px (Emilio: «está peor»).
- Con lyo ON y `pnX=ox` el gap era ~28 px; con **`pnX = ox − lyo`** los centroides cover/torso quedan a ~4 px.

## Cambios (solo lo autorizado)
1. **Centrado:** `pnX = fd[v].ox - lyoOf(114, fl)` y **lyo ON** mientras le cubren. Misma pista s41 (`ox = pnX + pnM * q[1]`). Árbitro/RPIN usan el mismo `pnX`.
2. **Pin al lado de cuerdas OK; sobre/fuera NO.** `groundOK` = regla 0x1190C: atacante `ropeIn(m=0)`, rival no fuera (`sx/bx!=2`), `ox` del rival dentro. Se quita el veto por extents del sprite (lyo) que bloqueaba el pin junto a la cuerda. Se mantiene `soilNudge` 0xACA4.

## Sin tocar
Sin IA (el otro solo persigue con START). Mismos controles. Esquineros de arriba, logo WWF y paletas intactos. Cifras/gestos ring-out de b72 intactos.

## Pruebas MAME (`test/t73.lua`)
- **pinC** (centro 780/720): `CENTER ox=720 lyo=32 pnX=688 cover=724 expect=724 err=0`
- **pinSide** (junto a cuerda izq.): pin OK, `err=0`
- **pinOn** (ox forzado fuera del límite): `RESULT blocked_ok`
Capturas en `shots/` (`hoja_b74.png`).

## Límites conocidos
- El centrado usa el sesgo de la pose 114 del port (±lyo); si se cambian esas poses hay que recalibrar.
- La cifra grande del pin sigue anclada a pantalla fija (no pedida en b74).
- Warrior WPIN (pista dx=32) usa la misma fórmula `ox-lyo`; no se regrabó la pista.
