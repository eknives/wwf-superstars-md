# b82 (base b81, md5 ffa3e48e22aee99750cd82af10d6ab31; b81 intacta)

ROM: `wwf_b82.bin`, md5 `b6c57f8cb194c7c7805b5a75b3775dc8`. Compilação SGDK local.
Só se mexe no golpe final do Warrior no chão (salto sobre o rival deitado). As cordas não foram mexidas.

## 1. De onde é lançado (arcade 0xC706 / 0xC798–0xC8A8 / 0xC928–0xC95A)
- Em CB1A[ação 0xB] = 0xFF o rival está deitado, então usa-se o ramo da âncora. Âncora = rival.x ± 0x28 (+ com bit7).
- Linha do Warrior em 0xCB3C: na frente da âncora (<0x20) → A = sub 4, **B = sub 0x0C (salto)**. Em direção ao corpo (<0x30) → A = sub 5 (pisão), B = sub 6 (pin). Em 0xC928 o pin só vale se a distância for <0x20 e propio.y ≥ rival.y; se não, B dá um golpe normal (sub 1).
- **Verificado no MAME arcade** (`test/probe.lua`, `test/warrior_probe.txt`) com Warrior id 0 e rival deitado em x=760:
  - sem bit7 (cabeça à esquerda): salto em dx −64..−40; pisão em −32..0; pin em −32..−16.
  - com bit7: salto em +48..+64; pisão em 0..+40; pin em +16..+40.
  - **Pelo lado dos pés nunca salta.**
- A pose 0x17 do arcade ocupa x−48..x+16, com a cabeça em x−48. Ou seja, **o salto só sai de além da cabeça**.
- **Erro da b81:** confundia a orientação do port com o bit7 do arcade e tomava ox como se fosse o x do arcade. Por isso saltava a partir dos pés, como na sua captura.
- **Correção:** bit7 = !vface e X = ox ± 48. Com isso a seleção é exatamente a de 0xC798, incluída a restrição do pin de 0xC928.

## 2. Trajetória
- 0x10A6C: o Warrior toma a orientação do rival. Destino segundo 0x111D0: rival.x − 0x20, espelhado com bit7.
- No arcade (MAME) vai de x 712 a 727 com o rival em 760. Antes ia em direção ao centro do corpo e olhava ao contrário.

## 3. Perna e punho duplicados
- 0x1152A: o objeto 7D (1C0AB2) é **outro sprite** colocado em y−10, z+10, com a orientação oposta e x±4.
- O Warrior fica em y = rival+9, **atrás** do rival, e o 7D (joelho e punho) em y−10, **na frente**.
- A b81 colocava tudo num só sprite por cima de tudo, e por isso se viam dois joelhos e dois punhos.
- Agora as poses 787/788 levam o corpo e o 7D em peças separadas (`tools/native82.py`) e cada uma é ordenada com sua profundidade. É o mesmo mecanismo de duas camadas do pin 778.
- Resultado: as pernas do rival tapam o corpo do Warrior, como em `shots/arcade_MAME_impacto_7D.png`.

## Testes (MAME Genesis, `test/b82.lua`)
- headL/headR (a partir da cabeça, B): salta (gs=12). feetL/feetR (a partir dos pés, B): **não salta**.
- stompL/stompR: pisão. pinL/pinR: pin.

## Capturas (`shots/`)
- Arcade: `arcade_MAME_salto_desde_cabeza.png`, `arcade_MAME_impacto_7D.png`.
- b82: `b82_salto_cabeza_R.png`, `b82_salto_cabeza_L.png`, `b82_impacto_capas.png`, `b82_pies_B_no_salta.png`.

## Fora do escopo / pendente
- A na frente da âncora = sub 4 no arcade (agarrar o deitado). Não implementado; o port dá um soco.
