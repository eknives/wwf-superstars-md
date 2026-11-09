# Ferramentas

Apenas as vigentes para a b95. As versões anteriores e os conversores históricos estão no backup privado. Nenhuma ferramenta contém dados do arcade: todas leem **a sua própria ROM** ou a ROM do MD que você compilar.

## `tools/mame/` — testes no MAME 0.276 usados para verificar a b95

| Script | O que mede |
|---|---|
| `mame95.sh rom.bin script.lua [genesis\|megadriv]` | Lançador sem vídeo nem som. Variáveis: `MAME`, `ROMPATH`, `SHOTS`. |
| `run95.lua` + `runsum.py` | Velocidade da corrida (px/s) e trocas de pose por segundo, W e D. |
| `post95.lua` + `postsum.py` | Frames perdidos andando em direção aos 4 córneres e integridade do fundo, lendo a VRAM pela porta do VDP. |
| `zafar95.lua` + `zsum.py` | Escapar do pin perto da corda: X final em Xv 760/728/708/693/832. |
| `kick95.lua` | Escapar no centro e contagem de 3. |
| `salir95.lua` | Sair e entrar no ringue. |
| `pinvis95.lua` | Sequência de estados do pin. |
| `fs2_95.lua` | Arremesso (sub 1) contra a corda. |
| `postes95.lua` | Capturas fixas dos córneres. |
| `cl95_clothesline.lua` | Clothesline (variáveis `SYM`, `CLD`, `MODE88`). |
| `prof95.lua` | Perfilamento dos frames perdidos. |

- Os scripts leem os endereços das variáveis do port em `out/symbol.txt` (variável `SYM`) e escrevem CSV no caminho de `OUT`.
- Alguns mantêm caminhos padrão `/workspace/...` da máquina original: ajuste-os com as variáveis ou editando o cabeçalho.
- Botões no MAME: `P1 A`/`P1 B`… Índice de lutador no port: 0 = Duggan, 1 = Warrior.

## `tools/analisis/` — análise do programa do arcade

`rdis.py` (desassemblador que gera `arc_rec.dis` a partir da sua ROM), `anot.py`/`anot2.py` (anotações das 964 rotinas que produzem `docs/analisis/rutinas.md`), `cg.py` (grafo de chamadas), `sig.py`, `rd.py`, `dump.py`, `reread.py`, `regen.py`, `audit_sample.py`, `oki.py` (decodificador ADPCM OKI), `z80rec.py`, `render_obj.py`, `sheets.py`. Vários têm caminhos `/workspace/...` que precisam ser ajustados.

## `tools/extractor/` — **PENDENTE**

Especificação do extrator de recursos: `tools/extractor/README_PT_BR.md`.
