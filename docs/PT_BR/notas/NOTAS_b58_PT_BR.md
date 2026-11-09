# b58 (a partir da b57)

ROM: `wwf_b58.bin`  md5 `cbe3a2b0976a142ceb25068edc660869`

b57 intacta (md5 `8651e4ef71af09be6260350b1489e20d`). Só o árbitro passa de estático a vivo.

## Regras do árbitro (confirmadas pelo Emilio)

1. **Como os demais:** prioridade HIGH + zonas de cor (verde / roxa / laranja / amarela) + ordem de desenho pelos pés vs Duggan; **continua contornando** (`refAvoid`).
2. **HUD:** qualquer peça do árbitro cujo `y` de tela toque o HUD (`y < HUD_H`, 34) é forçada a **LOW**; o resto não.
3. **Laterais:** mantém-se o limite — ele não pisa nas cordas laterais (`RF_MARGIN 16` dentro de `RING_XL`/`RING_XR` com o `e` de perspectiva).
4. **Anda pelo ringue:** segue o Duggan quando este se afasta mais de `RF_KEEP` (56 px), 1 px/frame (lógica s41 / estado 0 do arcade).

## Clamp (origem)

`rfClamp` em `src/main.c`:

- Y: `RING_Y0+8` … `RING_Y1-4`, e além disso `ylim` (teto do HUD / câmera).
- X: `lo = RING_XL + e + RF_MARGIN`, `hi = RING_XR - e - RF_MARGIN` com `e = (rfy-RING_Y0)/6`.
- `RF_MARGIN = 16` (folga s51). É chamado antes e depois de `refAvoid`.

`RING_XL=616`, `RING_XR=917` (limite direito da b55).

## Walk (origem)

- **Follow:** `rfStep` — se `|ox-rfx|` ou `|oy-rfy|` > `RF_KEEP`, avança 1 px rumo ao Duggan (eixo dominante; diagonal se ambos forem grandes). Fonte: série s / s41 volta para casa / follow do arcade estado 0.
- **Contornar:** `refAvoid` portado da **s51** (1 ator = Duggan): se se sobrepõe em X com os pés mais abaixo na tela, procura um espaço abaixo / ±X sem violar a margem lateral.
- **Anim:** as poses **510–512** do `spr_tab` (`PT_RWK`) vêm **sem cabeça** (primeira peça em dy=16). Na b58:
  - idle / movimento lateral ou rumo à câmera → pose **8** + H-flip se vai para a direita;
  - só se afastando (`hy>0`, sem `hx`) → alterna **508/509** (de costas, com cabeça).

## Paletas

Sem mudança em relação à b57:

| Linha | Uso |
|---|---|
| 0/1 | fundo + público + cordas + HUD + **árbitro** |
| 2 | Duggan |
| 3 | parceiros (Macho/Hogan) |

VRAM do árbitro: `RF_T0=1088` (28 t), `RF_T1=1512` (resto). Cordas em 1120 sem mexer.

## O que não foi mexido

Parceiros, Duggan, cordas, córneres, logo WWF (continua pendente, manual), controles, som, `RING_XR`.

## Shots

- `shots/b58_idle.png` — idle com cabeça
- `shots/b58_walk1.png` … `b58_walk4.png` — follow pelo ringue (rfx 768→887 na execução do MAME)
- MAME: `test/t58.lua` + `test/o_b58/`

Pendente manual (sem mudança): córneres superiores + logo WWF com remendos.
