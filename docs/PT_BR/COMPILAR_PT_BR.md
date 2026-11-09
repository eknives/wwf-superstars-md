# Compilar o port (b95)

## Ambiente usado e verificado

| Componente | Versão | Notas |
|---|---|---|
| SGDK | **2.11** (abril de 2025) | `GDK` aponta para a raiz dele (`makefile.gen`, `bin/`, `inc/`, `lib/`). |
| Toolchain | **m68k-elf-gcc 13.1.0** + binutils m68k-elf | No `PATH` (`m68k-elf-gcc`, `m68k-elf-objcopy`…). |
| Java | **17** | Para o `rescomp.jar` e o `sizebnd.jar` do SGDK. |
| make | GNU make | Linux x86_64 (deve funcionar também no Windows com SGDK; não testado). |
| MAME | **0.276** | Só para testes: `genesis` = NTSC, `megadriv` = PAL, `wwfsstar` = arcade. |

Se a instalação do SGDK não trouxer `lib/libmd.a`, compile-a antes com `make -f $GDK/makelib.gen`.

## Passo a passo

1. **ROM própria.** Obtenha legalmente o set MAME `wwfsstar`. Ele não é distribuído aqui.
2. **Recursos.** Gere os 32 arquivos de `res/` e os 4 cabeçalhos de `src/gen/` com o extrator. **PENDENTE**: a especificação está em `tools/extractor/README_PT_BR.md`. Os caminhos esperados pelo `res/res.res` são `res/graficos/...`, `res/datos/...` e `res/sonidos/...`.
3. **Compilar** na raiz do repositório:
   ```sh
   export PATH=/caminho/toolchain/bin:/caminho/jdk17/bin:$PATH
   make clean
   make GDK=/caminho/para/SGDK-2.11
   md5sum out/rom.bin
   ```
   **Não use `make -B`**: o template do SGDK pode sobrescrever o `src/main.c`.
4. **Conferir.**
   - Com os recursos exatos da b95 (incluindo as edições do Emilio nos córneres e no logo, que não são publicadas), o MD5 é `7be789d70d892c1efb86af8630b296a6`. Verificado em 09/11/2026 com esta mesma estrutura (`src/gen/`).
   - Com recursos extraídos só do arcade, o fundo será o original e o MD5 será diferente.
5. **Testar** no MAME: `mame genesis -cart out/rom.bin` (ou `megadriv` para PAL). Em hardware real, com um flashcart (Everdrive): ainda não verificado na b95. Os testes automáticos estão em `tools/mame/`.

## Conferir só que compila (sem a ROM do arcade)

- Crie cada arquivo de `res/` com o tamanho da tabela de `tools/extractor/README_PT_BR.md`, cheio de zeros. Os `.wav` devem ser WAV PCM válidos com silêncio.
- Crie os 4 cabeçalhos com as declarações desse mesmo documento, inicializadas com `{0}`.
- O `make` termina sem erros e gera uma ROM de 1.703.936 bytes, sem gráficos nem som úteis. Testado em 09/11/2026: no MAME (`genesis`) a tela fica totalmente preta nos frames 300 e 900.
- Os dois `.wav` devem ser mono, de 16 bits, a 8000 Hz e com 32768 amostras. Com outro formato também compila, mas a ROM muda de tamanho.

## Memória de vídeo e tamanho

ROM de 1.703.936 bytes (alinhada a 128 KB pelo `sizebnd`). Mapa da VRAM, em `main()`: BG_B 0xE000, BG_A 0xC000, Window 0xD000, sprites 0xF000, HScroll 0xF800.
