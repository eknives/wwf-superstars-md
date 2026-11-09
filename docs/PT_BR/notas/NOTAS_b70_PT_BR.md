# b70 (base b69, md5 b3d460cb3f2bd3bc97338e499f1c2046; b69 intacta)

ROM: `wwf_b70.bin` — md5 `24854415d3674c5e784b99ea9f7cc8da`

## 1. Levantar mais devagar
- `wrDown`: deitado de barriga para cima (pose 114) dura 140 frames (antes 68) e a animação de levantar (115) dura 30 (antes 18).
- Medido no MAME: fica deitado do frame +14 ao +154 (uns 2,3 s, antes 1,1 s), então há mais tempo para testar os golpes no chão (cotovelo A / salto B).

## 2. Pegada do arcade (os dois lutadores)
- **Como começa:** quando os dois estão livres, a menos de 32 px em X e 16 em Y, e um deles anda, eles se agarram (lock-up). Os dois se juntam no ponto médio e usam as poses do arcade da disputa (move_seq 118 para o Duggan e 343 para o Warrior, em laço). Cada lutador usa sempre **suas próprias** poses, então os sprites não se misturam.
- **Disputa 1 (básica):** o lutador que você controla (C) aperta A ou B antes que o contador chegue a 17 → ganha e arremessa o rival contra as cordas.
- **Disputa 2 (reverter a chave):** se você não aperta nada antes de 16, a chave se inverte e ganha o outro lutador (seja ele levado pela IA ou parado sem START) quando o contador chega a 32. Nesse caso ele arremessa você.
- **Arremesso contra as cordas:** usam-se as trilhas do arcade `sp_trk` (S_1E quando o Duggan arremessa, W1E quando o Warrior arremessa). A vítima corre até a corda **real**: se a corda está mais perto salta para o frame de contato, e se está mais longe repete os passos da corrida. Rebate (com a corda flexionando), volta correndo até a corda oposta, rebate outra vez e fica em pé. Quem arremessa é liberado aos 25 frames e já pode se mover.
- Depois de cada pegada há 40 frames de espera antes de poder se agarrar de novo.
- Enquanto dura a pegada ou o arremesso não é possível dar golpes.
- C continua trocando só o controle e START só a perseguição (igual à b69).

## Pendente / limitações
- A e B fazem o mesmo (o arremesso às cordas). A chave 0x26 do arcade no A fica pendente.
- Ainda não há nada na volta das cordas (clothesline, etc.): a vítima rebate e fica em pé.
- Como a distância da pegada (32) é menor que o alcance do soco (40), se você anda até grudar no rival vocês se agarram, igual ao arcade.

## Testes (MAME, test/t70.lua e test/t70g.lua) — capturas em shots/b70
- 01-04: o Duggan agarra, aperta B e ganha; o Warrior corre, rebate na corda direita (x=912) e na esquerda (x=621).
- 05-08: nada é apertado, a chave se inverte (blk=1, c2 chega a 32), o Warrior arremessa o Duggan e o Duggan rebate na corda direita.
- 09-11: após C (você controla o Warrior) aperta A e o Warrior arremessa o Duggan.
- 12-13: o Warrior no chão (os dados do teste confirmam que continua deitado até o frame +154).
