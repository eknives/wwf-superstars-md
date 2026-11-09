# b73 (base b72, md5 74c37dc8839ec8780a122eabfc71a58d; b72 intacta)

ROM: `wwf_b73.bin`, md5 `684b4b738f4255cb231fa286d401fdef`

## Evidência do arcade usada
- **0x1190C / 0x11A72** (`analisis/rutinas.md`, `prog.bin`): cobrir só se o rival está na ação 0xB, **dentro** (`+0x19==0`) e o atacante não está fora. Não há margem extra «perto das cordas».
- **0xACA4** (`suelo_chk_cuerdas`): ao deitar testa ±0x30 e ±8 com o clamp **0x21E5A**; deixa o corpo dentro (não sobre a corda).
- **0xBD10 + tabela 0xBEF2** (`prog.bin`): quem cobre em `ox_rival ± dx` (Duggan→Warrior **36**, Warrior→Duggan **32**), e y = rival−1. Igual à s41 (`pinX = ox` da vítima).
- **0x21E5A** (`s66/cuerdas_casos.md`): limites inclinados do ringue (m=0).

## Mudanças (só o autorizado)
1. **Pin ao lado das cordas OK; sobre/fora NÃO.** Desfaz-se o bloqueio agressivo da b72 (`m=6/4` + veto do árbitro). `groundOK` usa a regra 0x1190C/0x21E5A (m=0): corpo ou atacante além do limite = não; dentro (mesmo junto à corda) = sim.
2. **0xACA4 ao cair** (`soilNudge`): ao passar a deitado (vh=3) empurra o corpo para dentro com a mesma lógica 0x30/8 + clamp.
3. **Centralização de quem cobre:** `pnX = ox` do rival (arcade/s41/BEF2). Durante o pin desliga-se o `lyo` do deitado para que o sprite compartilhe o ox da trilha (antes o lyo ±32 o desalinhava em relação à cobertura).

## Sem mexer
Sem IA (o outro só persegue com START). Mesmos controles. Córneres de cima, logo WWF e paletas intactos.

## Testes no MAME (`test/t73.lua`)
- **pinC**: pin no centro; `CENTER ox=720 cover=756 expect=756 err=0`.
- **pinSide**: perto da corda esquerda; pin OK.
- **pinOn**: corpo forçado fora do limite; pin bloqueado (`RESULT blocked_ok`).
Capturas em `shots/` (`hoja_b73.png`).
