# Análise WWF Superstars (arcade) — ÍNDICE
Estado (31-10-2026): 100 % lido, AUDITADO por amostra (auditoria.md). Amostra de 32 rotinas: 12,5 % erradas e 12,5 % incompletas, corrigidas. Recomenda-se reler a segunda metade. NÃO CONFIRMADO: 2 (0x1F86, 0x7E4A; 0x6BA0 confirmado pelo Emilio). Discrepâncias com a s66: sistemas/discrepancias_s66.md (contrastado e reverificado); discrepancias.md está obsoleto.
- arc_rec.dis: desmontagem recursiva com cabeçalhos de rotina (a boa). arc.dis: a linear (desalinhada em 94 destinos).
- rutinas.md: tabela de rotinas anotadas. ram.md: mapa de RAM e de hardware. tablas.md: tabelas da ROM.
- sistemas/: laço principal, lutadores, cordas, público, atordoamento, RNG e discrepâncias. As seções IA, árbitro, som e pin/contagem estão só esboçadas.
- Ferramentas: tools/rdis.py, rd.py, dump.py, sig.py, anot.py, cg.py.

> Nesta versão em português os arquivos estão em `docs/PT_BR/analisis/` com o sufixo `_PT_BR` (ex.: `sistemas/arbitro_PT_BR.md`). As desmontagens `.dis` e as ferramentas de análise não são publicadas.

## Acrescentado (100 %)
- sistemas/sonido.md: driver Z80, OKI, sino 0x20/0x21 e IDs (com sonido_ids_llamadas.txt).
- sistemas/arbitro.md, sistemas/pin_cuenta.md e sistemas/reloj.md.
- sistemas/discrepancias_s66.md: contraste com wip19, só leitura.
- Cobertura: 100 % dos bytes; 50.062/50.062 instruções 68K em rotinas lidas (sem contar os blocos de dados); Z80 com 1.200 instruções e 2.523 bytes alcançados, tudo lido.


## Nomes de banco (+0x2B / índice de 0x6CD8)
Verificado no MAME 31-10-2026 (demo de atração, /workspace/idp): +0x2B = banco (+3, copiado em 0x7F44); o letreiro de cada exibição coincide com o id do objeto 1 (Hogan 1, Warrior 0, Macho 2, Duggan 3, Bossman 4, Honky 5). A casa de seleção NÃO é o id: 0x7FE2 converte casa→banco (0→2,1→1,2→0,3→5,4→3,5→4,6→6,7→7).
| Banco | Conteúdo |
|---|---|
| 0 | Ultimate Warrior |
| 1 | Hulk Hogan |
| 2 | Macho Man |
| 3 | Jim Duggan |
| 4 | Big Bossman |
| 5 | Honky Tonk Man |
| 6 | Ted DiBiase |
| 7 | André the Giant |
| 8 | mesa |
| 9 | árbitro |
| 0x0A | postes |
| 0x0F | cadeira (NÃO CONFIRMADO) |
| 0x10 | efeitos |
| 0x11 | textos |

Atenção: 0x4D4C e 0x5F54 põem "banco 0x10" em objetos de lutador; aí o valor pode ser outro campo e não o banco gráfico (NÃO CONFIRMADO).
