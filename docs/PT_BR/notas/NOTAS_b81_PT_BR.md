# b81 — base b80 conservada

- ROM: `/workspace/b81/wwf_b81.bin`, **1.572.864 bytes**.
- MD5: **ffa3e48e22aee99750cd82af10d6ab31**.
- Base: `/workspace/b80/wwf_b80.bin`, MD5 **d843bac410485579980872341264fda9**, verificada intacta ao terminar.
- Compilação local SGDK; sem CloudAgent, sem publicar nem mexer em repositórios remotos.

## 1. Cordas: queda curta igual à esquerda e à direita

O erro da b80 não era só quanto durava o contador: **0x2146E era interpretado como passo→mapa**. No arcade há dois níveis distintos:

1. **0x21324** inicia no passo 2 com pedido `d0=1`, fase visual `d4=3`.
2. **0x213AC** converte passo→fase: `1,2,3,2,3,2,3,0`.
3. **0x2146E** converte fase→desenho. Não pode ser indexado diretamente com o passo.

Além disso, os bancos `mp0` e `mp1` da b80 têm índices locais diferentes. Para as duas fases finais equivalentes usam-se:

| Fase arcade | Esquerda | Direita |
|---|---:|---:|
| 3 | mp0[7] | mp1[4] |
| 2 | mp0[6] | mp1[3] |
| 0, repouso | mp0[0] | mp1[0] |

A queda agora mostra **3→2→3→2→3→0**, nunca o estiramento inicial da corrida.

Durações de `0x213A4`, passos 2..7: **6,4,3,2,2,1 ticks de arcade**. Reproduz-se também o detalhe de `0x21324`: inicializa e decrementa na mesma invocação, avança antes de desenhar (`0x213B4`). O relógio curto executa uma invocação a cada duas iterações do motor, idêntico para ambos os lados. Não se acrescentam pausas nem se multiplica o tempo duas vezes.

**Corrida intacta:** o ramo do motor que corre/rebate e as sequências longas `sc0/sc1` são conservados. Há uma comparação automática contra o texto da b80 e fixtures de corrida nos dois lados.

## 2. Warrior: pisão e salto sobre rival deitado

Elimina-se a trajetória anterior do salto do Warrior baseada em deslocar/escalar `S0C`: já não mistura um deslocamento vertical gravado com uma altura de assento de pin. Para o Warrior, o movimento usa as instruções e tabelas do arcade, não uma interpolação de capturas.

### Botão e posição — 0xC706 / 0xC83E / 0xCB3C

Seja `s = +1` se o bit de orientação do rival estiver ativo, `-1` caso contrário. A âncora de seleção é **rival.x + s*0x28**. No mesmo plano e com **abs(dy)<0x18**:

- Na frente da âncora, **distância <0x20**: **B → sub 0x0C**, salto.
- Atrás, **distância <0x30**: **A → sub 5**, pisão; **B → sub 6**, cobrir/pin.
- Os limites são estritos: 31 sim / 32 não; 47 sim / 48 não; dy 23 sim / 24 não.

Assim B é o mesmo botão que cobre, mas a posição decide. Desaparece para o Warrior a faixa simétrica inventada de 28..100 px. Não se acrescenta a sub 4 nem outras chaves/entradas alheias a estes dois movimentos. O Duggan conserva seu motor anterior.

### Pisão — 0x1173A / 0x118BC

- Poses nativas **0x159 e 0x15A**, temporizadores **8 e 4 ticks**.
- Impacto ao passar para o segundo passo.
- Sem salto nem deslocamento X/Y; chão **z=0xBB**. Já não desce ao assento de um pin.

### Salto — 0x10A5E / 0x111D0 / 0x156FA / 0x159AC / 0x3E20

- Chão: **0xBB**. Impulso vertical: **0x500**; gravidade **0x50**.
- Destino X: tabela nativa `0x111D0`, **rival.x ±0x20**, conforme a orientação. Destino Y: Y do rival.
- Velocidades calculadas com o laço de `0x159AC`: divide a distância pelo número de passos de voo. Não se usa um divisor de uma trilha gravada.
- Integrador de `0x3E20`: `x+=2*vx`, `y+=2*vy`, `z+=2*vz`, `vz-=2*g`, a cada tick de arcade.
- Preparação de **4 ticks**; sequência normal **0x61/0x62/0x7A/0x7B**, variante **0x61/0x62/0x76/0x77** quando começa em `propio.y+2 < rival.y`.
- Temporizadores aéreos de `0x112F0`: **9 ticks, 5 ticks, esperar contato**.
- Contato descendente a partir de **z≤0xCB** com o ponto e retângulo exatos de `0x10FCC`, `0x11084` e `0x110A4`; não um alcance genérico de 48 px.
- Impacto: **z=0xBB**, **y=rival.y−1+10**, como `0x10D9E/0x10F04` para id 0. Objeto auxiliar **0x7D**, orientação oposta e deslocamentos de `0x1152A`; compõe-se no recurso visual, não na física do lutador.
- Apoio durante **12 ticks**, recuperação ação 5, pose **0x1A**, **8 ticks** (`0xAA00[0]`).
- Se o rival se levantar antes: não se concede um pin/impacto falso. Ramo de falha `0x10C4A` e rebote ação 8/sub 5 (`0x9FCC`, física `0x27D2[0x19]`: vz=0x300, g=0x40; poses 0x1CF/0x16), antes de voltar ao motor de deitado da b80.

### Recursos e procedência

Acrescentam-se poses nativas sem modificar os recursos anteriores: `spr_tab.bin` e `spr_tiles.bin` mantêm íntegro o prefixo da b80. A conversão confere **pixel por pixel** a pose 0x159 contra o recurso já existente na b80 e conserva sua origem/paleta, sem desenhar pixels novos. Todas cabem na janela de 64 tiles do Warrior.

**Toda a lógica/medidas procede de `/workspace/wwf_sgdk/analisis`.** Para converter os pixels utiliza-se a dependência gráfica original que `analisis/tools/render_obj.py` declara: `/workspace/wwf/port_35/sprtiles.npy`. É um array de tiles originais decodificados, não código de movimentos de outro port. Essa dependência fica explícita em `tools/native81.py`.

## Testes e capturas

- **19 fixtures** no MAME com driver **Genesis**, estados preparados e pressionamentos reais de A/B: quatro variantes/lados do salto, ambos os pisões, pin dos dois lados, colisão e corrida dos dois lados, seis limites incluídos/excluídos e falha ao levantar-se o rival.
- Além disso: **kickout natural junto à corda esquerda e direita**, a partir de golpes/pin com o controle, sem escrever o pedido de animação. Ambos terminam `RESULT ok_rope_vib`.
- Nos quatro saltos comparam-se **16 amostras X/Z** contra um integrador independente das instruções do arcade: horizonte do solver **34 passos**, máximo **z=232 (BB+45)**, aterrissagem **z=187/y=rival+9**. Os dois lados são simétricos.
- Cordas com câmera assentada: transições de fase equivalentes **exatamente nos mesmos frames** nos dois lados. Os callbacks do MAME podem observar frames VDP repetidos enquanto o motor trabalha; esses callbacks não são confundidos com ticks da máquina arcade.
- O fixture dy23 observou uma transição de carga durante um callback no meio do laço; confere-se que não persiste mais de dois VBlanks. Não se afirma que haja uma auditoria geral de cintilação/hardware nesta versão.
- `VALIDACION_b81.txt`: resultados e checksum interno **SGDK XOR**, como na b80.
- **Capturas definitivas: `/workspace/b81/shots/FINAL_b81/`**. Sequências `ropeL_secuencia.png`, `ropeR_secuencia.png`, `diveR_secuencia.png`, `diveL_secuencia.png`, variantes, pisões e falha. Inclui PNG individuais sem rótulos e folhas de contato rotuladas.
- `ARCADE_b81.txt`: instruções recuperadas, endereços, bytes de tabelas e hash da ROM de programa de referência.

**Alcance da validação:** o comportamento foi contrastado com a desmontagem; as capturas desta entrega são do port no MAME Genesis, não de uma nova execução do arcade original nem de um console físico. Conservam-se energia/IA/contagens e reações gerais da b80, salvo as rotas visuais/físicas descritas; não se apresenta como port completo desses outros sistemas.

## Reproduzir

```sh
cd /workspace/b81
python3 tools/native81.py
# make no siempre detecta cambios dentro de BIN: forzar recursos tras regenerarlos.
touch res/res.res
PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH make -f /workspace/sgdk/makefile.gen GDK=/workspace/sgdk
cp out/rom.bin wwf_b81.bin
md5sum wwf_b81.bin
python3 tools/validate81.py
```

(O comentário diz: o make nem sempre detecta mudanças dentro de BIN; forçar os recursos após regenerá-los.)

Build final: `BUILD_b81_final.log`; geração de sprites: `NATIVE_b81.log`; diff: `CAMBIO_b81.patch`.
