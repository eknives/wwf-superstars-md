# Superstars — índice mestre das descobertas

**Entrada recomendada:** **b95**, `docs/notas/NOTAS_b95.md` (corrida por tick do arcade W28/D27 igual em PAL/NTSC; fundo por DMA em fila sem frames perdidos perto dos córneres; choque contra a corda 9E78/9F02; base b94). Inventário de golpes: `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`. As cadências do Elbow do Duggan e do Knee do córner continuam BAIXA, «polir no final». Notas traduzidas: mesmos caminhos sob `docs/PT_BR/` com o sufixo `_PT_BR`.

Caminhos relativos à raiz do repositório. Endereços do 68000 do arcade, salvo indicação. **(np)** = não publicado: existe só no backup privado do projeto porque contém dados do arcade (desmontagem, capturas, dumps, traços de RAM volumosos) ou é material interno; é citado para que se saiba que existe e como foi obtido. As notas por versão são mantidas literais: seus caminhos `/workspace/...` e `01_port_sgdk/…`, `02_arcade_decompilado/…`, `03_roms/…`, `04_herramientas/…`, `05_referencias/…` são do backup privado. Uma nota antiga não é estado atual nem verificação nova.

## Receita geral de golpes por lutador

**[PATRON_MOVIMIENTOS_PT_BR.md](PATRON_MOVIMIENTOS_PT_BR.md)** — seletor→rotina→tabelas por id/dupla→física/contato→energia/reação/final; catálogo de slots dos oito lutadores, exceções e correspondência real com a b92. É estudo, não implementação; conteúdos não confirmados marcados U. Cadência visível do Elbow do Duggan chão/córner e do Knee do Warrior do córner: **BAIXA, «polir no final»**. Seções §6–§10: orientação do rival deitado (b93), pin (b94), pesquisa de corrida/córneres/cordas e b95.

- **Inversão do rival deitado no Knee/Elbow (b92):** o arcade nunca muda o `+A` da vítima; a b92 usava `vface` como bit7 em zonas/destino/caixa/A2 enquanto desenhava o deitado com `vface^1` → espelho no contato. Causa e proposta: `docs/PATRON_MOVIMIENTOS.md` §6; **corrigido na b93** (`docs/notas/NOTAS_b93.md`).
- **Pin do Warrior (cobrir) b93 vs arcade:** `11A72`/`BD10`/`BEF2`: X=Xv∓32 pelo bit7 do rival, Y=Yv+1, Z=203, orientação = rival^0x80. Proposta em §7, **implementada na b94** (§8).

## Procurar antes de pesquisar de novo

- Notas por versão: `docs/notas/NOTAS_b49.md` … `NOTAS_b95.md`; resumo em `docs/CHANGELOG.md`.
- Rotinas anotadas do arcade (endereço, nome, dedução): `docs/analisis/rutinas.md`.
- Exemplo: `grep -rn -i '10a5e\|stomp\|AF66' docs/`.
- (np) Índices do backup: `DESCUBRIMIENTOS.csv` (tema, resumo, endereços, caminho e linha), `DOCUMENTOS.csv`, `RUTINAS_DESENSAMBLADO.csv` (linhas do `arc_rec.dis`), `HERRAMIENTAS.csv`, `PROCEDENCIA.csv`, `INVENTARIO_TOTAL.csv`.

## Fontes, mapa geral e qualidade

| Tema / endereço | O que se sabe | Onde olhar |
|---|---|---|
| Descompilação geral | `arc_rec.dis` (np) é o alinhado preferido; o `arc.dis` (np) linear tem destinos desalinhados. São regenerados a partir da ROM própria com `tools/analisis/rdis.py`. | `docs/analisis/INDICE.md`; `docs/analisis/auditoria.md` |
| Rotinas anotadas | Tabela de endereço, nome e dedução, incluindo ramos e exceções. | `docs/analisis/rutinas.md`; `tools/analisis/anot2.py` |
| RAM/hardware | Estruturas de atores, memória compartilhada, registradores de vídeo/som. | `docs/analisis/ram.md`; `docs/analisis/sistemas/luchadores.md` |
| Tabelas da ROM | Despachos, poses, caixas, energia, IA, mapas e geometria por endereço (só endereços e descrição). | `docs/analisis/tablas.md` |
| Incertezas | Auditoria e discrepâncias históricas; «lido 100 %» não garante correção total. | `docs/analisis/sistemas/sin_confirmar.md`, `discrepancias_s66.md`, `cotejo_s66_wip19.md`; `docs/ESTUDIAR.md` |
| ROM de referência | Set do MAME `wwfsstar`; não incluída. Cada um usa sua cópia legal. | `README.md`; `tools/extractor/README.md` |

## Relógio, movimento e animação

| Tema / endereço | Resumo | Caminho |
|---|---|---|
| 1508–1510 / 155A–157C | Lógica de ator a cada 2 refreshes; MAME 57,444852941 Hz, tick 34,816 ms. O MD converte para 50/60 Hz (`arcTick`, 28,72 Hz). | `docs/estudios/KNEEDROP_arcade.md` §2; `docs/analisis/sistemas/reloj.md`; `docs/notas/NOTAS_b90.md` |
| 3DCE–3E20 | Integração de velocidades e altura; posição 16.16, velocidades 8.8. | `docs/estudios/KNEEDROP_arcade.md` §3; `docs/estudios/DUGGAN_SUELO_arcade.md` §2 |
| 156FA / 159AC–15B3E | Solver de salto por tabela, limites/truncamento/destino; não há trajetória fixa universal. | `docs/estudios/KNEEDROP_arcade.md`; `TABLAS_DUGGAN.txt` (np) |
| 6CD8 / 7FE2 | Banco gráfico ≠ casa do seletor: W0, Hogan1, Macho2, Duggan3, Bossman4, Honky5, DiBiase6, André7. | `docs/analisis/INDICE.md`; `docs/analisis/sprites/BANCOS.md` |
| 1761E / 172FA / 1636C | Caixas/dano por pose e id, reação por pose e filtro por ação. | `docs/estudios/ENERGIA_arcade.md`; `docs/analisis/tablas.md` |
| Pose→tiles / 46A0 | A b88 corrigiu o sentido do arremesso e o banco de paleta dos blocos emprestados. | `docs/notas/NOTAS_b88.md` |
| Corrida 93EE/945C/94CE, 0x95BC, 3DF0 | vel/4 px por tick (W 7 / D 6,75), poses 10–15 × 2 ticks; W 201,1 e D 193,9 px/s. Implementado na b95. | `docs/PATRON_MOVIMIENTOS.md` §9–§10; `docs/notas/NOTAS_b95.md` |

## Ataques — Duggan e Warrior

| Tema / endereço | Resumo | Caminho |
|---|---|---|
| Combo W FC84, FD70/FD7C | Poses 150..155, esperas e janela de pressionamento; não supor duração de tabela como frames de 60 Hz. | `docs/notas/NOTAS_b87.md`; `NOTAS_b86.md` como antecedente |
| Combo D FC4E→FC70→FDA0 / FE88 | O despacho humano do Duggan é diferente; a b89 usa FD70/FD7C para ambos. Dano 1 por golpe. | `docs/estudios/ENERGIA_arcade.md` |
| Chute FF3A / 188AB / 188C7 | Dano 4 humano, exceção CPU 0, bônus contra corrida conforme o percurso. | `docs/estudios/ENERGIA_arcade.md` |
| Clothesline CD14 / 12E7A / 1302E | Entrada na corrida, poses 1D0–1DB e proximidade 16634; contato/subtrações 4 ou 2. | `docs/notas/NOTAS_b87.md`; `src/cl87.h`; `src/main.c` |
| Queda da clothesline 9B9A | Ação 8/sub 17; direção de deslocamento/flip e paleta revisados na b88. | `docs/notas/NOTAS_b88.md` |
| Knee W C706 / 10A5E | Input exato K na cabeça; zonas, variantes, solver, impacto e final. | `docs/estudios/KNEEDROP_arcade.md` |
| Knee W 112F0 / 112FA / 10F54 | Poses 61/62/7A: 8/18/10 refreshes; variante 76/77, não 7D. | Mesmo estudo §§2–3; `src/knee90.h`; `docs/notas/NOTAS_b90.md` |
| Knee W A554 / 28EC | A2 da vítima com arco 4/7/9/10/10/9/7/4/0; não é queda genérica. | Estudo do Knee §4; `docs/notas/NOTAS_b90.md` |
| Knee W fora AB1E→ACA4 / 21ED0 | A b91 normaliza só o Knee: contato 528,75/309/128, não 540,125. | `docs/notas/NOTAS_b91.md` |
| Knee W córner F35A/F636/F6E6 | P ou K→sub 2C; trajetória conferida, cadência final irregular (**PENDIENTES, BAIXA**). | `docs/notas/NOTAS_b91.md` |
| **Stomp Duggan CB75 / 1173A / 118BC** | **P corpo, 159×14/15A×10 refreshes visíveis; impacto ao entrar na 15A; dano 1. Não é «cotovelada».** | **`docs/estudios/DUGGAN_SUELO_arcade.md` §1** |
| **Elbow Duggan CB72 / 10A5E / 11372** | **K cabeça, 61/62/1CB/1CC; variante 1CD/1CE; 8/18/10; offset −64, ponto de impacto ±8,+4; dano 5.** | **Mesmo estudo §2** |
| **Elbow Duggan córner F6EF / FC14** | **P/K→sub 2F; mesmos holds, trajetória 399/−462 em fixture; dano 10. Cadência visível pendente.** | **Mesmo estudo §3** |
| Erro 10C6A / 9FCC | −2 ao atacante humano, ação 8/sub 5, 1CF→16→17→1A; não é penalização de qualquer queda. | Estudos Knee/Duggan e energia |
| Chão D b92 | Motor do Duggan independente em vez das ativações antigas gs5/gs11; cadência do Elbow pendente. | `src/duggan92.h`; `docs/notas/NOTAS_b92.md` |
| Golpes restantes | Técnicas feitas/parciais/ausentes. | `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md` |

## Energia, chão, pin e árbitro

| Endereço / tema | Resumo | Caminho |
|---|---|---|
| 7EE6→7F76 / 7FEC | Humanos 48; CPU 8190/progressão/DIP diferente; HUD ceil(E/4) até 12. | `docs/estudios/ENERGIA_arcade.md` § Energia inicial |
| +3C/+3E / 16488–1649A | Energia/dano separados; subtração saturada em 0; sem regeneração passiva; 0 não é KO. | Mesmo estudo § Regras comuns; `src/main.c` |
| 1698A / 1642A / 16418 | CPU soco/chute 0, bônus contra ação 1/15/16 e duplicação F9.0. | Estudo de energia; não confundir a CPU com rival sem controle |
| 162BC–162DA | A exceção clothesline FFFE omite bônus e duplicação. | Estudo de energia; `docs/notas/NOTAS_b90.md` |
| 117E0 / 10DC0 / 10DCC | Stomp 1, drop 5 chão / 10 córner. Não usar a escala 2/3 do FAQ como RAM. | Estudos de energia, Knee e Duggan |
| AF66 / AF6A / AA00 | Esperas no chão 112/82/54/22 ticks, entradas 24/10/6/3, levantada 8..40 ticks por índice/flags. | Estudo de energia; estudo do Knee §4; `docs/analisis/sistemas/pin_cuenta.md` |
| AD12 / ADEA / AE7E / AF72 | Levantar/kickout leem a energia; E0 restringe o escape mas não dá vitória imediata. Integração no port pendente. | Estudo de energia |
| Disputa / 14CFC / 2209C | Chaves/whip/rebote comum sem dano próprio; choque especial do lado de fora 5 com condições. | Estudo de energia; `docs/analisis/sistemas/cuerdas.md` |
| Árbitro / contagens | Contagem 3/20 e animações; a b89 reinicia a luta sem voltar à seleção. | `docs/analisis/sistemas/arbitro.md`, `pin_cuenta.md`; `docs/notas/NOTAS_b89.md` |
| Pin W/D BD10/11A72/BEF2, B012/B0A0 | Cobre em Xv∓32 (W) / Xv∓36 (D); escapar perto da corda = arcade desde a b95. | `docs/PATRON_MOVIMIENTOS.md` §7–§10; `docs/notas/NOTAS_b94.md`, `NOTAS_b95.md` |

## Seleção, gráficos, cenário e som

| Tema / endereços | Resumo | Caminho |
|---|---|---|
| SELECT 704E / 7240 / 729C | 2×3 Savage/Hogan/Warrior / Honky/Duggan/Bossman, WWF no centro, escolher parceiro; 1P/VS/COOP. | `docs/estudios/SELECCION_arcade.md` |
| 749E/74F2/7552 / 7098/72A4 | Navegação sem wrap, botão 1 confirma, temporizador interno de 384 refreshes; autoplay/flash à parte. | Estudo da seleção; `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| 2034A / 20404 / 210A8 / 2FAE | Cena/mapa/retratos/cursores e paletas convertidos de dados do arcade. | Estudo da seleção; `src/gen/select89_data.h` e `res/` (gerados, np) |
| Flicker b91 | 896 tiles de overlay atrasavam a HINT; agora só são publicadas células sujas no VBlank. | `docs/notas/NOTAS_b91.md` |
| C=A+B / Y | Normalização antes da detecção de bordas; Y troca o lutador controlado (controle de 6 botões). | `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| Ringue 21E5A/21ED0 / 221B2 | Limites internos/externos e plano; não confundir coordenadas de mundo com as de tela. | `docs/analisis/sistemas/cuerdas.md`; `docs/notas/NOTAS_b91.md` |
| Cordas / paletas / HUD | Casos e discrepâncias históricas; preservar os córneres/logo editados pelo Emilio (não publicados). | `docs/analisis/sistemas/cuerdas.md`; `src/gen/ropes.h`, `src/gen/hud.h` (np); `docs/REGLAS.md` |
| Streaming do fundo | b95: colunas/linhas por fila DMA com orçamento; sem frames perdidos perto dos córneres. | `docs/notas/NOTAS_b95.md`; `docs/ARQUITECTURA.md` |
| Público 23170 | Tabelas de animação/câmera e recursos do público; áudio picotado relatado, sem causa certificada. | `docs/analisis/sistemas/publico.md` |
| Som 25E6 / OKI / Z80 | Driver, IDs e sino; WAV decodificados (np). | `docs/analisis/sistemas/sonido.md` |
| IA 18F16 em diante | Só referência do arcade, **não é autorização para IA no port**. | `docs/analisis/sistemas/ia.md`; `docs/analisis/rutinas.md`; `docs/REGLAS.md` |

## Código atual, entregas e ferramentas

- Compilar: `docs/COMPILAR.md`. Com os recursos reais, a ROM b95 dá MD5 **7be789d70d892c1efb86af8630b296a6**.
- Arquitetura do `main.c`: `docs/ARQUITECTURA.md`.
- Testes MAME vigentes (b95): `tools/mame/`. Ferramentas de análise: `tools/analisis/`. Extrator de recursos: **PENDENTE**, `tools/extractor/README.md`.
- ROMs b48–b95, cópias de código anteriores, capturas e traços: (np), no backup privado; MD5 de cada ROM em `docs/CHANGELOG.md`.

## Últimas versões

| Versão | Resumo | Caminho |
|---|---|---|
| b92 | Stomp/Elbow/Elbow do córner do Duggan; cadência do Elbow não fechada. | `docs/notas/NOTAS_b92.md`; `src/duggan92.h`, `src/duggan92_poses.h` |
| b93 | `oriVictima=vface^1` em zonas, destino, córner, caixa, lado de fora; A2 sem espelho. | `docs/notas/NOTAS_b93.md`; `docs/PATRON_MOVIMIENTOS.md` §6 |
| b94 | Deitado sem ±32; cobre em Xv∓32/∓36; Warrior olha ao contrário do deitado; pin do Duggan pela zona do corpo. | `docs/notas/NOTAS_b94.md`; §7–§8 |
| Pesquisa 9-11-2026 | Corrida, lentidão perto dos córneres e cordas (sem mudanças no port). | `docs/PATRON_MOVIMIENTOS.md` §9 |
| b95 | Corrida W28/D27 por arcTick, pose a cada 2 ticks; fundo por DMA em fila; choque contra a corda 16 px à frente → sub 2 → rebote para dentro e deitado; soilNudge com vface^1. | `docs/notas/NOTAS_b95.md`; §10 |
