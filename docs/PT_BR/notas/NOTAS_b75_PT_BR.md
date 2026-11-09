# b75 (base b74, md5 715494ea2b1a1f41ac0b4013ae7b7a0b; b74 intacta)

ROM: `wwf_b75.bin`, md5 `b2f37978b626d9bd1a072b1e655e7218`

## Evidência do arcade (lida ANTES de mexer no código)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc.dis` / `rutinas.md`): y = rival.y−1 (+2 se id 0/4); z parte de **0xBB**, subtrai BEF2[id][rival+8] (dz). Duggan↔Warrior dz=**13** → assento z=**174** (rota genérica) ou 200 (id 0/4 com +dz×2).
- **Tabela 0xBEF2**: D→W dx=32 dz=13; W→D dx=36 dz=13.
- **Trilha s41 PT_PIN@2731** (gravada do arcade): q[3] = Z absoluto. Início 187 → arco ~210 → **assento 174**. s41/s42 fazem `z0 = q[3]`.
- **s62 `wcStep` (Warrior 0x0C)**: `oy = wcY0 + q[2]` — a altura vai no dy; não usa GH_SIGN sobre dY.
- **A b74** fixava `z0 = 187` no pin (ignorava a trilha) e o S0C aplicava `dY += GH_SIGN * q[2]` (sinal oposto ao s-port) → quem se lança ficava **alto demais**.

## Mudanças (só o eixo Y do salto/pin — autorizado)
1. **Pin / kickout:** `z0 = pinZof(q[3])` — se q[3]≥128 usa o Z da trilha (Duggan); se não (flags WPIN/WKO), fallback `0xBB − 13` (BEF2).
2. **Salto do Warrior 0x0C:** `oy = gY0 + q[2]` como na s62; deixa-se de usar o GH_SIGN. Após o impacto, z de assento BEF2.
3. **Golpe no chão 0x05/0x11:** após o frame de impacto, z = `0xBB − 13` (mesmo assento BD10/BEF2).

Sem mexer no X do pin (b74 `pnX=ox−lyo` intacto), nem na IA, nem nos controles, nem nos córneres/logo.

## Pendente (NÃO na b75 — o Emilio anota para depois)
- O **soco do Warrior está incompleto**. Referência MAME: anexo `01M6PKH6KN28S4JX7VQTBV1KMX.jpg`. Não foi mexido na b75.

## Testes no MAME (`test/t75.lua`, pinC)
- `RESULT pin_ok`; `CENTER … err=0` (centralização X da b74 OK).
- `SETTLE z0=174 dZ=174` (antes, na b74, ficava em 187) → **13 px mais abaixo** na tela (`by −=(z−187)`).
- Capturas: `shots/b75_03_pin_settle_z174.png` (depois), `shots/b74_before_pin_cubre.png` (antes).

## Limites
- O WPIN não traz Z em q[3]; o assento usa o dz BEF2 D↔W (=13). Outros pareamentos não estão neste port.
- O arco visual do 0x11 do Duggan continua nas poses (como na b69); só se baixa o z no impacto.
- O FC do teste no MAME passa de 94→96 por causa do campo `gY0`.
