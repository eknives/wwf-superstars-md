# b74 (base b73, md5 684b4b738f4255cb231fa286d401fdef; b71/b72/b73 intactas)

ROM: `wwf_b74.bin`, md5 `715494ea2b1a1f41ac0b4013ae7b7a0b`

## Evidência do arcade (lida ANTES de mexer no código)
- **0xBD10 `acc_cubrir_pin`** (`analisis/arc_rec.dis`, `rutinas.md`): y = rival.y−1 (+2 se id 0/4); x = rival.x ± BEF2[id][rival]; z = 0xBB − BEF2[id][rival+8]. Sinal de dx: `btst #7,+0xA(rival)` → se zerado, `neg.w d1`.
- **Tabela 0xBEF2** (`prog.bin`): por atacante `id*0x10`, byte dx em `[rival]`, dz em `[rival+8]`.
  - Duggan(0)→Warrior(1): dx=**32**, dz=13
  - Warrior(1)→Duggan(0): dx=**36**, dz=13
- **0x1190C / 0x11A72**: cobrir só se o rival está na ação 0xB, **dentro** (`+0x19==0`) e o atacante não está fora. Não há veto «perto da corda».
- **0xACA4**: ao deitar testa ±0x30/±8 + clamp 0x21E5A (empurra o corpo para dentro).
- **Trilha s41** (`sp_trk` PT_PIN@2731): no assentamento (frame 28) dx=**36**, dy=0 (a trilha já traz o offset visual do arcade). Origem da trilha = x do arcade do rival (= centro do corpo).
- **Ref. visual do Emilio (MAME arcade)**: quem cobre deitado torso sobre torso; árbitro embaixo do pin contando.

## Por que a b73 ficou pior
- Pose deitada **114/626**: o torso do sprite fica ~28 px para um lado da origem.
- `lyo` (±32) corrige isso ao desenhar (`bodyX = ox+lyo`).
- A b73 **desligou o lyo** durante o pin e pôs `pnX=ox`. A métrica `err=0` comparava a cobertura com `ox+36` (a própria fórmula), não com o torso visível → diferença visual de ~60 px (Emilio: «está pior»).
- Com lyo ON e `pnX=ox` a diferença era de ~28 px; com **`pnX = ox − lyo`** os centroides cobertura/torso ficam a ~4 px.

## Mudanças (só o autorizado)
1. **Centralização:** `pnX = fd[v].ox - lyoOf(114, fl)` e **lyo ON** enquanto é coberto. Mesma trilha s41 (`ox = pnX + pnM * q[1]`). Árbitro/RPIN usam o mesmo `pnX`.
2. **Pin ao lado das cordas OK; sobre/fora NÃO.** `groundOK` = regra 0x1190C: atacante `ropeIn(m=0)`, rival não fora (`sx/bx!=2`), `ox` do rival dentro. Retira-se o veto pelos extents do sprite (lyo) que bloqueava o pin junto à corda. Mantém-se o `soilNudge` 0xACA4.

## Sem mexer
Sem IA (o outro só persegue com START). Mesmos controles. Córneres de cima, logo WWF e paletas intactos. Números/gestos de ring-out da b72 intactos.

## Testes no MAME (`test/t73.lua`)
- **pinC** (centro 780/720): `CENTER ox=720 lyo=32 pnX=688 cover=724 expect=724 err=0`
- **pinSide** (perto da corda esq.): pin OK, `err=0`
- **pinOn** (ox forçado fora do limite): `RESULT blocked_ok`
Capturas em `shots/` (`hoja_b74.png`).

## Limites conhecidos
- A centralização usa o viés da pose 114 do port (±lyo); se essas poses forem mudadas, é preciso recalibrar.
- O número grande do pin continua ancorado a uma posição fixa da tela (não pedido na b74).
- O Warrior WPIN (trilha dx=32) usa a mesma fórmula `ox-lyo`; a trilha não foi regravada.
