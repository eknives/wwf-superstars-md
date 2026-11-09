# b75 (base b74, md5 715494ea2b1a1f41ac0b4013ae7b7a0b; b74 intact)

ROM: `wwf_b75.bin`, md5 `b2f37978b626d9bd1a072b1e655e7218`

## Arcade evidence (read BEFORE touching code)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc.dis` / `rutinas.md`): y = opponent.y−1 (+2 if id 0/4); z starts from **0xBB**, subtracts BEF2[id][opponent+8] (dz). Duggan↔Warrior dz=**13** → sitting z=**174** (generic route) or 200 (id 0/4 with +dz×2).
- **Table 0xBEF2**: D→W dx=32 dz=13; W→D dx=36 dz=13.
- **s41 track PT_PIN@2731** (recorded from the arcade): q[3] = absolute Z. Start 187 → arc ~210 → **sitting 174**. s41/s42 do `z0 = q[3]`.
- **s62 `wcStep` (Warrior 0x0C)**: `oy = wcY0 + q[2]` — the height goes in dy; it does not use GH_SIGN on dY.
- **b74** fixed `z0 = 187` in the pin (ignoring the track) and S0C applied `dY += GH_SIGN * q[2]` (opposite sign to the s-port) → the jumping wrestler ended up **too high**.

## Changes (only the Y axis of the jump/pin — authorised)
1. **Pin / kick-out:** `z0 = pinZof(q[3])` — if q[3]≥128 it uses the track's Z (Duggan); otherwise (WPIN/WKO flags), fallback `0xBB − 13` (BEF2).
2. **Warrior's jump 0x0C:** `oy = gY0 + q[2]` as in s62; GH_SIGN is no longer used. After the impact, BEF2 sitting z.
3. **Floor hit 0x05/0x11:** after the impact frame, z = `0xBB − 13` (same sitting as BD10/BEF2).

The pin's X not touched (b74 `pnX=ox−lyo` intact), nor AI, controls, corner posts/logo.

## Pending (NOT in b75 — Emilio notes it for later)
- **Warrior's punch is incomplete**. MAME reference: attachment `01M6PKH6KN28S4JX7VQTBV1KMX.jpg`. Not touched in b75.

## MAME tests (`test/t75.lua`, pinC)
- `RESULT pin_ok`; `CENTER … err=0` (b74 X centring OK).
- `SETTLE z0=174 dZ=174` (b74 stayed at 187) → **13 px lower** on screen (`by −=(z−187)`).
- Captures: `shots/b75_03_pin_settle_z174.png` (after), `shots/b74_before_pin_cubre.png` (before).

## Limits
- WPIN does not carry Z in q[3]; the sitting uses the BEF2 dz D↔W (=13). Other pairings are not in this port.
- The visual arc of Duggan's 0x11 is still in the poses (as in b69); only the z is lowered on impact.
- The FC of the MAME test goes from 94→96 because of the `gY0` field.
