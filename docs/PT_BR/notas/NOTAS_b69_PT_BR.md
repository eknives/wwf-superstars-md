# WWF b69 (base b68, md5 b68 3a41cd79ddf5d3b669c0475ca56ca20c, sem mexer)

ROM: `wwf_b69.bin`, md5 `b3d460cb3f2bd3bc97338e499f1c2046`

## Mudanças
1. **Queda de costas**: se olha para a direita, a cabeça fica à ESQUERDA; se olha para a esquerda, à DIREITA (shots 01 e 07).
2. **Golpes no chão + reação, para os dois**: com o rival deitado, A = cotovelada (poses 521-523) e quem está no chão se sacode. B, a 16-100 px do corpo, = salto e pisão (poses 537-554), que cai sobre o corpo. Enquanto apanha, o rival continua deitado (shots 02-05 e 08-10).
3. **Warrior com o mesmo motor do Duggan**: corre (A+B), sai e entra no ringue e sobe e desce dos córneres do fundo e da frente (shots 13-17).
4. **C = trocar o controle Duggan ↔ Warrior**. Só muda quem os controles comandam; os sprites e as posições continuam iguais (shot 06).
5. **START**: o oponente (o que você não controla) te persegue; com outro START ele para (shots 11-12).

## Correções técnicas
- Os tiles do Warrior foram movidos para a VRAM 1672, porque em 1525 se corrompiam (saía lixo no público).
- O salto do pisão já não soma uma altura extra: a altura já vem nas poses.
- O perseguidor não se mete em cima de você: se está a menos de 20 px, ele se afasta.

## Aproximações e pendências
- Se o jogador anda por cima do rival, os sprites podem se sobrepor.
- O HUD continua igual ao da b68 (por exemplo, o rótulo "DUGGAN" aparece mesmo que você controle o Warrior).
- Os offsets da cotovelada e do pisão foram revisados a olho com as capturas do MAME, não comparando-os frame a frame com o arcade.
