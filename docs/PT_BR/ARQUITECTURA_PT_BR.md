# Arquitetura do `src/main.c` (b95)

O `main.c` (~1600 linhas) é um único módulo C para SGDK. Cada bloco traz um comentário `bNN:` com a versão que o introduziu e os endereços do arcade que ele reproduz. As linhas são aproximadas para a b95.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `src/main.c` | Motor completo: loop principal, lutadores, câmera, fundo, cordas, público, árbitro, pin, sprites. |
| `src/select89.h` | Tela de título e seleção de lutadores (arcade 704E/7240/749E…); `joy89()` normaliza C = A+B. |
| `src/duggan92.h`, `duggan92_poses.h` | Ataques de chão do Duggan (Stomp, Elbow, Elbow do córner; C79E/CB6C). |
| `src/knee90.h`, `native81.h`, `cl87.h` | Índices de pose do port para o Knee Drop, o banco nativo do Warrior e a queda por clothesline. |
| `src/gen/*.h` | **Gerados a partir da ROM** (não publicados): mapas e paletas das cordas (`ropes.h`), trilhas de chão (`gs69.h`), moldura do HUD (`hud.h`), navegação da seleção (`select89_data.h`). |
| `res/res.res` | Recursos binários que o `rescomp` vincula (ver `tools/extractor/README_PT_BR.md`). |

## Relógio

- A lógica dos atores do arcade avança a cada 2 refreshes de 57,44 Hz, ou seja, um tick a 28,72 Hz.
- No MD, o loop principal acumula `arcClock += 3125·Δvtimer` e ativa `arcTick` quando passa de `arcDen` (5440 em PAL, 6528 em NTSC). Há no máximo 1 tick por volta.
- Desde a b95, a corrida e alguns ataques de chão avançam por `arcTick`. O resto (andar, quedas `fs`, rebote, freada) continua avançando por volta ou por frame do MD: está nas PENDÊNCIAS.

## Loop principal (`main()`, ~l. 1434)

1. **Início:** VDP 256×224, planos 64×32, carga de paletas, HUD, cordas e poses iniciais; `selectScreen89()` (uma única vez); preenchimento inicial do fundo.
2. **A cada volta:**
   1. relógio `arcTick`;
   2. controle (`joy89`, bordas, START = seguir; Y = trocar o controle);
   3. `grStep` (agarrão) e `pinAdvance`;
   4. **para cada lutador** `f = 0, 1`, com `ctxLoad(f)`/`ctxSave(f)`, que copiam o contexto do lutador para variáveis globais (`ox`, `oy`, `z0`, `rn`, `sx`…). Prioridade dos estados, da maior para a menor:
      - `kvPhase90` (vítima do Knee);
      - `clHeld` (pego na clothesline);
      - `fs` (queda da ação 8: voo, choque contra a corda 9F02, aterrissagem);
      - escapar do pin (`pnS==2`);
      - quem está cobrindo no pin (`pinStepA`);
      - agarrão ou arremesso (`gr`, `tr` com `trStep`);
      - vítima de golpe (`vh` com `victimStep`);
      - caso contrário, `engine()` (controle normal).
   5. `grTry`, `countStep` (contagens), `matchReset` quando necessário;
   6. `camera()`;
   7. público (`caLogic`/`caDraw`/`caApply`);
   8. vibração das cordas (`ropeDraw`, passos 0x21324/0x213A4);
   9. **streaming do fundo** (`stCol`/`stRow`: fila DMA com o orçamento `ST_BUD`, desde a b95);
   10. `sqTick` (sequências de som);
   11. árbitro (`rfStep`, `refPinStep`, contagem fora do ringue).
3. **VBlank:** `SYS_doVBlankProcess()` esvazia a fila DMA. Depois vêm `fLoad` (tiles das poses dos lutadores), `rfLoad` (árbitro), dígitos da contagem, `buildSat()` (tabela de sprites), scroll e o DMA da SAT.

## Módulos dentro do `main.c`

| Bloco | Funções (linha aprox.) | O que faz |
|---|---|---|
| Fundo e VRAM | `acq`, `rel`, `put` (~196), `acqQ`, `stCol`, `stRow` (~219–238) | Mundo de 88×68 células (`W`), pool de tiles com contagem de referências, colunas e linhas novas pela fila DMA (b95). |
| Cordas | `ropeA`, `ropeDraw` (~204–248), constantes de `gen/ropes.h` | Cordas desenhadas nos planos; vibração pelas fases do arcade (0x213A4/0x213AC/0x2146E). |
| Público | `caLogic`, `caDraw`, `caApply` (~249–290) | Animação do público por zonas (23170). |
| Som | `smpPlay`, `sndCmd`, `sqTick` (~291–300) | Amostras PCM4 (2 WAV OKI) e sequências. |
| HUD | `hudInit` (~302) | Moldura do HUD (`gen/hud.h`). |
| Movimento e câmera | `walkStep`, `camera` (~308–368) | Andar, limites do ringue, câmera com margens. |
| Árbitro | `rfLoadEx`, `rfColumn`, `rfClamp`, `rfExtPose`, `refAvoid`, `rfStep` (~369–480) | Árbitro que anda, desvia e conta (DD4E/DFE0/DECC). |
| Contexto | `ctxLoad`, `ctxSave` (~481–497) | Troca do lutador ativo. |
| Knee (vítima) | `kneeVictimStep90`, `kneeVictimStart90` (~498–534) | Reação A2 da vítima (A554/28EC). |
| Quedas, ação 8 | `fsStart`, `clFallStart`, `fsStep`, `fsAir`, `arcRope` (~530–600) | Voo, choque contra a corda 9E78/9CD0/9F02 (b95), aterrissagem 9C3C/9C94. |
| Vítima | `victimStep`, `bounceRope`, `soilNudge` (~600–676) | Reação aos golpes, rebote na corda, empurrão ao deitar (ACA4). |
| Chão do Warrior | `groundOK`, `warriorGroundZone/Start/Step/End` (~677–805) | Knee Drop e golpes finais no chão (C706/10A5E/112F0). |
| Clothesline | `clStep87` (~806) | Clothesline na corrida (CD14/12E7A). |
| Controle | `engine` (~845–1100) | Estados do lutador controlado: `rn` (1 correr, 2 rebote, 3 clothesline; freada segundo `mvOffR`), `sx` (sair/entrar no ringue), `bx`, `climb` (córner), `gs` (5/11/12 trilhas de chão, 14/15 Duggan), combo de socos e chute, pin do Duggan. |
| Agarrão e arremesso | `grTry`, `trStart`, `grStep`, `trCF`, `trStep` (~1101–1175) | Agarrão e arremesso contra as cordas (trilhas `sp_trk`). |
| Pin e contagens | `pinAdvance`, `pinStart`, `pinStepA`, `refPinStep`, `countStep` (~1176–1258) | Pin (BD10/11A72/B012/B0A0), contagem de 3 e de 20; ao terminar, a luta recomeça. |
| Luta | `fighterInit`, `matchReset` (~1259–1274) | Estado inicial. |
| Desenho | `fLoad`, `drawF`, `buildSat` (~1275–1433) | Carga dos tiles de pose (tabela `spr_tab`) e composição dos sprites com prioridades. |

## Dados de recursos que o código usa

- `spr_tab` é uma tabela de `Pose { u16 n, t0, nt; Piece p[12]; }` com `Piece { s16 dx, dy; u16 sz, line, toff; }`, 126 bytes por pose, e `spr_tiles` contém os tiles delas.
- `xl_w`/`xl_d` traduzem a pose lógica para a pose do port do Warrior e do Duggan.
- `move_seq`, `sx_seq`, `bx_seq`, `climb_pose`, `run_pos`, `sp_trk` são trilhas de animação e posição.
- `camtab` é a tabela da câmera; `crowd_b52` + `crowd_b49_tiles` são o público; `bgb_tiles` + `bgb_map52` + `ex52_tiles` são o fundo.
- A lista completa com tamanhos está em `tools/extractor/README_PT_BR.md`.
