# b77 — base b76 conservada

ROM: `wwf_b77.bin` (1.572.864 bytes). MD5: `947bdf6ccc66d33c7d9ecc526e3e8e97`.
Base intacta: `/workspace/b76/wwf_b76.bin`, MD5 `49075e62b6b23d071da6035564adcea8`.

Só três mudanças: árbitro na contagem, assento/camadas do pin do Warrior, saída do pin de ambos. Sem mudanças de IA, HOME, córneres, logo, público, som nem outros golpes. Os recursos antigos de sprites são prefixos idênticos; só se acrescenta a pose 778.

## 1. Árbitro: corrupção de peças, não um suposto limite por linha

No Mega Drive o árbitro ocupa dois blocos **não contíguos**: tiles 1088–1115 e 1512–1524. O desenho antigo traduzia só o primeiro tile de cada peça e depois somava offsets como se o bloco fosse contínuo. Algumas peças das poses 503, 506 e 507 cruzam o tile lógico 28; então eram lidos tiles alheios (inclusive de cordas), independentemente de onde estivessem os lutadores.

`rfColumn` corta as colunas exatamente nesse salto da VRAM. Também traduz os offsets antes —não depois— da divisão de prioridade das cordas. Mantêm-se as paletas, o bit de prioridade, os números na frente e as posições do árbitro da b76.

A verificação exaustiva de todos os tiles das poses 500–509 encontra **36 endereços errados no cálculo antigo e 0 no novo**. Os sintomas não foram tapados escondendo o árbitro ou mudando-o de lugar.

Fonte da ordem de desenho do arcade: `analisis/arc_rec.dis`, 0x43D4–0x4508 (entrada com X, Y e Z separados), 0x45AE–0x45FA (ordem pelo Y do chão; comparação na entrada+8), 0x45FC–0x4614 (Z é somado só para projetar). Números: 0xE02C e 0x2549E; o fundo transparente de `pin_glyph.bin` não muda.

## 2. Warrior cobrindo: Z e duas camadas do arcade

A tabela real **0xBEF2**, linha Warrior 0 / coluna Duggan 3, dá **dx=32 e dz=16**, não dz=13. Em 0xBDCC–0xBE84:

- Warrior (id 0): Y = Y do coberto +1.
- Z inicial = 0xBB−16 e depois soma-se 16 duas vezes: **Z=203**.
- Pose principal 0x7F: 0xBD96.
- Objeto auxiliar 0x1C0AB2, pose 0x80: 0xBE84–0xBEC0, mesmo X/Z e Y do corpo−2.

A trilha histórica WPIN já tinha o Z embutido nos seus pixels. A b75/b76 lhe aplicavam ainda o fallback 174: baixavam-no mais 13 pixels. Esse fallback não foi mudado para o Duggan nem para as chaves.

No assento do Warrior usa-se agora a pose **778**, convertida diretamente das poses do arcade 0x7F e 0x80. Seus 48 tiles são carregados juntos, mas desenhados em duas passadas: corpo atrás do coberto e mãos na frente, pelos seus respectivos Y do chão. Durante a aproximação histórica WPIN não se duplica o Z embutido. Conserva-se a centralização X do pin existente.

O conversor é `tools/gen77_pin.py`; confere que o programa usado pelo decodificador coincide exatamente com `analisis/tools/prog.bin`. A união das máscaras 0x7F/0x80, com o deslocamento e o Z originais, coincide com a máscara histórica da pose 515. Não há pixels desenhados nem gerados por IA.

Capturas: `shots/b77_01_warrior_pin.png`, `b77_02_warrior_cuenta2.png`, `b77_06_antes_despues_pin.png` (mesmo fixture na b76 e na b77). A captura do Emilio no MAME é a referência visual; câmera, escala e paleta do port não foram mudadas.

## 3. Escapar e sair arremessado: ticks, posicionamento e velocidade

Fonte primária: `analisis/arc_rec.dis` e `analisis/tools/prog.bin`:

- **0xB012–0xB04C**: o coberto se desloca ±8 uma vez.
- **0xB0EA**: pose 0x9F durante 8 ticks e 0xA0 durante 4 ticks. São **16+8 frames**, não os 8+4 frames da b76.
- Durante a primeira pose, quem cobre ainda mantém o pin. **0xB0A0–0xB0E4** só o posiciona na segunda pose: 0x9B, X do coberto±0x28, Y−1, Z+4. A b76 o mudava desde o início.
- **0xB068–0xB084**: coberto → ação 5; quem cobre → ação 8 sub 0x1C, virado.
- **0x9B66 / 0x9BBE / 0x9C14**: deslocamento inicial ±0x10 e Z+0x18.
- Tabela **0xA74A[0x1C] → 0xA8E6**, parâmetro físico 0x21; **0x2814[0x21] → 0x29B4**: vx=0x100, vy=0, vz=0x100, g=0x40. São valores fixados pelo arcade, não a gravidade/vz supostas das notas da b76.
- **0x27D2–0x280E** carrega esses valores; **0x3E20–0x3E8C** aplica X/Z e gravidade uma vez por tick (dois frames). A b76 não deslocava X em voo e começava com vz=0.
- **0x9E4C**: 0x9B/0x9C conforme a altura ao cair. **0x9C5A–0x9C92**: deslocamento ±0x20 ao tocar o chão, sub 0xC. **0xA4C8–0xA53E**: rebote pequeno com vz=0x100/g=0x30.
- **0xA90E–0xA954**, tabela 0xAA00, índice 0: levantar 8 ticks = 16 frames, só para estas saídas. Não se acrescentam atordoamentos.

A saída usa a origem visível do coberto, sem transferi-lo subitamente para a origem corrigida do pin (a correção `lyo` era só de desenho). Os sinais são convertidos para o eixo X do port separadamente do flip de desenho. A atualização do pin é feita uma vez antes dos dois atores: não depende de quem cobre ser o Duggan ou o Warrior nem da ordem do laço.

Capturas/folhas: `shots/b77_04_warrior_lanzado.png`, `b77_05_duggan_lanzado.png`, `b77_07_kickout_warrior.png`, `b77_07_kickout_duggan.png`.

## Compilação e verificações

- SGDK local, `PATH=/tmp/marsdev/mars/m68k-elf/bin:$PATH`.
- É necessário reconstruir `out/res/res.o`: a cópia da b76 trazia um `.d` com caminhos absolutos da b76. Já está reconstruído com dependências exclusivas da b77. Não se entrega uma ROM com recursos antigos.
- Compilação final sem instrumentação de diagnóstico: `BUILD_b77.log`, sem erros. Avisos herdados de indentação/variáveis sem uso.
- `python3 tools/verify77.py`: verifica a base, os prefixos de sprites, recursos fora do escopo e o endereçamento do árbitro. Resultado: `VALIDACION_b77.txt`.
- Fixtures do MAME para Genesis: `test/fixture77.lua`, `test/fixture77.sh`. Exemplos: `test/fixture77.sh Wvalidated 1 1 1` (contagem de três), `test/fixture77.sh Dvalidated 0 0 1`, `test/fixture77.sh WKvalidated 1 1 0` e `test/fixture77.sh DKvalidated 0 0 0` (saídas). Chegam aos seus finais sem timeout. As capturas são do emulador, não recriações.
- Os fixtures colocam a dupla e preparam seu estado para repetir o caso; a ROM de entrega não contém esses atalhos. Os CSV leem a RAM durante o frame e podem mostrar uma lista SAT ainda em construção: não são usados como prova de ausência de sprites. A tentativa de ler o espaço `videoram` do VDP devolveu zeros e **não constitui uma validação de hardware**. A verificação exaustiva de endereços é sim independente dessa tentativa, e as capturas foram revisadas.
- A execução auxiliar de diagnóstico no arcade avisou de checksum de `24j6-0.112`; não é usada para importar arte nem fixar constantes. As constantes acima saem do binário/desmontagem de `analisis`, e a arte do seu mesmo decodificador.

## Limites desta entrega

Não é uma validação de todos os casos do jogo nem uma promessa de equivalência global com o arcade. Foram verificados os casos repetíveis de contagem e saída descritos. Conservam-se as decisões anteriores de quando escapar (primeira contagem automática), a duração do deitado e os limites/quedas de corda do port; sua máquina de colisões não foi ampliada. O GameFAQs não foi necessário para estas três correções.
