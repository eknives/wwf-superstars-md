# WWF Superstars (arcade) → Sega Mega Drive — port feito por fãs

Port do arcade *WWF Superstars* (Technōs, 1989) para Mega Drive / Genesis, escrito do zero em C com SGDK. O objetivo é que o port seja notavelmente igual ao arcade: mesmos tempos, física, colisões, reações e poses, conferidos com o MAME e com o código do arcade.

Idiomas: [Español (original)](README.md) · **Português (Brasil)** · [English](README_ENG.md). Nas notas vale o original em espanhol; as traduções levam o sufixo `_PT_BR` ou `_ENG`.

## Aviso legal

- Projeto de fãs, **gratuito e sem fins lucrativos**. Port feito com ajuda de IA. Não pode ser vendido nem distribuído com fins comerciais.
- **Sem afiliação**: não é afiliado nem endossado pelos titulares de *WWF Superstars*.
- **As marcas, personagens, nomes, gráficos, música e som pertencem aos seus donos.**
- O repositório **não contém nenhuma ROM nem material protegido por direitos autorais**: nem gráficos, nem som, nem paletas, nem mapas, nem tabelas de dados extraídas, nem o desassemblado. Apenas nosso código, nossas notas e nossas ferramentas.
- **Para compilar é preciso ter uma ROM própria, obtida legalmente** (set MAME `wwfsstar`), da qual os recursos serão extraídos.
- Nosso código e notas: licença MIT ([LICENSE](LICENSE)). Os arquivos de inicialização `src/boot/` vêm do SGDK (MIT, © Stephane Dallongeville).

## Estado atual: b95 (09/11/2026)

- Joga-se com 2 lutadores humanos: **Duggan** e **Warrior** (controle de 6 botões: A = soco, B = chute, C = A+B, Y = troca o lutador controlado; START = o rival te segue ou para). Há tela de título e de seleção (SELECT PLAYERS); a seleção ainda termina sempre em Duggan contra Warrior.
- Feito e conferido com o MAME, com os limites de cada versão anotados nas suas notas:
  - andar, corrida com rebote nas cordas (b95: velocidade e ritmo do arcade, iguais em PAL e NTSC);
  - sair e entrar no ringue, subir no córner;
  - combo de socos, chute, clothesline;
  - Knee Drop do Warrior (chão, córner e lado de fora), Stomp e Elbow Drop do Duggan (chão e córner);
  - arremesso contra as cordas, energia interna com os danos do arcade;
  - pin com contagem de 3, contagem de 20 fora do ringue, árbitro, público, HUD;
  - choque contra a corda ao escapar do pin (b95 = arcade).
- Desde a b95 o fundo é carregado por DMA em fila e já não se perdem frames perto dos córneres.
- O que falta está em [docs/PT_BR/PENDIENTES_PT_BR.md](docs/PT_BR/PENDIENTES_PT_BR.md) (resumo mais abaixo).
- A última ROM (b95) tem MD5 `7be789d70d892c1efb86af8630b296a6`. As ROMs não são publicadas.

## Importante: hoje o código não compila sem os recursos

O código está completo, mas **precisa de recursos que vêm da ROM do arcade**. Eles não são publicados e serão gerados por um **extrator que ainda está PENDENTE** ([tools/extractor/README_PT_BR.md](tools/extractor/README_PT_BR.md)). São necessárias duas coisas:

- 32 arquivos em `res/` (30 `.bin` e 2 `.wav`): sprites, tiles, mapas, paletas, trilhas de animação, público, seleção, título e som;
- 4 cabeçalhos em `src/gen/`: `ropes.h`, `gs69.h`, `hud.h`, `select89_data.h`.

Enquanto o extrator não existir:

- **Com os recursos reais** (backup privado do projeto) a ROM dá exatamente o MD5 da b95. Comprovado ao preparar este repositório, já com `src/gen/` e os `#include` alterados.
- **Com recursos zerados** (mesmo tamanho) e os 4 cabeçalhos declarados com zeros, **compila sem erros** e sai uma ROM do mesmo tamanho, preta e sem conteúdo jogável. Serve só para comprovar que o código compila.

**As edições do Emilio não são publicadas**: os córneres superiores e o logo WWF do fundo do ringue. O extrator vai gerar o fundo original do arcade; por isso, com ele o MD5 não vai coincidir com a b95 nessa parte.

## Compilar (resumo; passo a passo em [docs/PT_BR/COMPILAR_PT_BR.md](docs/PT_BR/COMPILAR_PT_BR.md))

1. Instalar **SGDK 2.11**, **m68k-elf-gcc 13.1.0** (com binutils), **Java 17** (para o `rescomp`) e `make`.
2. Gerar `res/**` e `src/gen/*.h` a partir do seu set `wwfsstar` (extrator PENDENTE).
3. `make GDK=/caminho/para/SGDK` → `out/rom.bin`. **Não use `make -B`**: o template do SGDK pode sobrescrever o `main.c`.
4. Testar no MAME 0.276 (`genesis` = NTSC, `megadriv` = PAL) ou em hardware real.

## Método de trabalho

Resumo; as regras completas estão em [docs/PT_BR/REGLAS_PT_BR.md](docs/PT_BR/REGLAS_PT_BR.md).

1. **Primeiro o código descompilado.** Localizar a rotina e as tabelas do arcade, com seu endereço (`docs/analisis/rutinas.md`, `tablas.md`, `ram.md`). Não inventar números: cada valor é rastreado até um endereço ou uma medição.
2. **Depois o MAME.** Medir o arcade (`wwfsstar`) e o port (`genesis`/`megadriv`) com scripts Lua: posições, ticks, poses, RAM. O arcade avança a lógica dos atores a cada 2 refreshes (57,44 Hz → tick de 28,72 Hz); no MD usa-se `arcTick`. Não se deve confundir ticks com frames de 60/50 Hz.
3. **Igualdade notável.** Ao fechar uma técnica, ela deve coincidir com o arcade em entrada, ritmo real, colisão, física, reação, poses e paleta. Nada que não tenha sido medido é dado como verificado.
4. **Os bugs do arcade são reproduzidos** (p. ex. a comparação do byte alto em `9CD0`); **não se inventam bugs novos**.
5. **Só o que foi pedido.** Cada versão vai numa pasta nova, a base fica intacta e se anotam a ROM nova e seu MD5. Os estudos não autorizam mudanças.
6. **Respeitar o que existe:** o motor SGDK (ringue, cordas nos planos, prioridades), Hogan como referência, paletas, córneres e logo. Não acrescentar IA nova.

## Onde estão as descobertas

- [docs/PT_BR/INDICE_PT_BR.md](docs/PT_BR/INDICE_PT_BR.md): índice mestre por tema e endereço. É o ponto de entrada.
- [docs/PT_BR/PATRON_MOVIMIENTOS_PT_BR.md](docs/PT_BR/PATRON_MOVIMIENTOS_PT_BR.md): receita comum dos golpes (seletor → rotina → tabelas → física/contato → reação). Inclui os estudos b93–b95: orientação do lutador deitado, pin, corrida, córneres e cordas.
- [docs/PT_BR/ARQUITECTURA_PT_BR.md](docs/PT_BR/ARQUITECTURA_PT_BR.md): como o `src/main.c` está organizado.
- [docs/PT_BR/analisis/](docs/PT_BR/analisis/): mapa do programa do arcade (rotinas, RAM, tabelas, sistemas).
- [docs/PT_BR/estudios/](docs/PT_BR/estudios/): estudos a fundo de energia, Knee Drop, ataques de chão do Duggan e seleção.
- [docs/PT_BR/notas/](docs/PT_BR/notas/): nota de cada versão b49–b95. O [docs/PT_BR/CHANGELOG_PT_BR.md](docs/PT_BR/CHANGELOG_PT_BR.md) é o resumo.
- [docs/PT_BR/MOVIMIENTOS_DUGGAN_WARRIOR_b92_PT_BR.md](docs/PT_BR/MOVIMIENTOS_DUGGAN_WARRIOR_b92_PT_BR.md): quais técnicas estão feitas, pela metade ou faltando.
- [docs/PT_BR/ESTUDIAR_PT_BR.md](docs/PT_BR/ESTUDIAR_PT_BR.md): dúvidas abertas.

As notas de cada versão são mantidas literalmente. Os caminhos que elas citam (`/workspace/...`, `01_port_sgdk/...`, `02_arcade_decompilado/...`, `05_referencias/...`) são do backup privado e não estão aqui se contêm dados do arcade.

## Pendências principais (detalhes em [docs/PT_BR/PENDIENTES_PT_BR.md](docs/PT_BR/PENDIENTES_PT_BR.md))

1. **Extrator de recursos** a partir da ROM própria: [tools/extractor/README_PT_BR.md](tools/extractor/README_PT_BR.md).
2. **Golpes que faltam**:
   - Duggan: High Knee, Body Slam, Headlock, Bulldog, Back Suplex, Back Body Drop, Dropkick contra quem está correndo, Pick Up, Dropkick do córner.
   - Warrior: Shoulder Tackle, Body Slam, Headlock, Gorilla Press, Atomic Drop, ataques contra quem está correndo, Pick Up, Dropkick do córner.
3. **Energia frente a pin, kickout e levantar**: faltam as regras nativas fora do Knee.
4. **Passar para o relógio do arcade (`arcTick`)** o andar, o arranque e a freada da corrida, a clothesline e as quedas. Hoje vão por frame do MD.
5. Frames perdidos correndo entre as cordas (40 de 580; causa não investigada).
6. Problemas relatados: som picotado do público, «Macho verde», variantes de clothesline que faltam.
7. Ainda sem verificar: hardware real/Everdrive, PAL perto dos córneres, choque contra a corda em arremessos.
8. BAIXA, «polir no final»: cadência visível do Knee do córner e do Elbow do Duggan.

## Estrutura

```
README.md, README_PT_BR.md, README_ENG.md   este documento e suas traduções
LICENSE                                    MIT (código e notas próprios)
Makefile                                   make GDK=/caminho/para/SGDK
src/        main.c e cabeçalhos próprios; boot/ (SGDK)
src/gen/    (ignorado pelo git) cabeçalhos gerados a partir da ROM: ropes.h, gs69.h, hud.h, select89_data.h
res/        res.res (lista de recursos), crowd_b49.h; os .bin/.wav são gerados (ignorados pelo git)
docs/       notas em espanhol: REGLAS, PENDIENTES, ESTUDIAR, INDICE, PATRON_MOVIMIENTOS, COMPILAR,
            ARQUITECTURA, MOVIMIENTOS, CHANGELOG, notas/, analisis/, estudios/
docs/PT_BR/, docs/ENG/   traduções (*_PT_BR.md, *_ENG.md), mesma estrutura
tools/mame/        testes MAME vigentes (b95)
tools/analisis/    ferramentas de análise do programa do arcade (leem a sua própria ROM)
tools/extractor/   PENDENTE: especificação do extrator de recursos
```
