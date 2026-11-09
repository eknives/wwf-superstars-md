# Seleção do arcade — estudo, sem mudanças no port

**Método:** MAME `wwfsstar`, ROM local; ficha + início + joystick/botão por meio do `observe.lua`. Só entradas, leituras de RAM e capturas: sem escrever na RAM, sem editar o port e sem compilar ROM. Quatro percursos curtos: 1P, versus, cooperativo e espera sem escolher. Evidência: `1P.log`, `VS.log`, `COOP.log`, `TIMEOUT.log`; vistas originais de 256×240, sem a interface do MAME. `RESUMEN_seleccion.png` reúne seis estados.

## Aparência e controles observados

- Fundo azul com padrão WWF; em cima **SELECT PLAYERS** e o logo WWF no centro. Seis retratos em duas linhas de três, com os centrais deslocados verticalmente. Nomes sob os retratos:

| ID de seleção | Em cima | ID | Embaixo |
|---|---|---|---|
| 0 | RANDY SAVAGE, esquerda | 3 | HONKY TONK MAN, esquerda |
| 1 | HULK HOGAN, centro | 4 | HACKSAW JIM DUGGAN, centro |
| 2 | ULTIMATE WARRIOR, direita | 5 | BIG BOSS MAN, direita |

- O 1P começa no Savage: moldura verde e rótulo **1P**. O 2P começa no Warrior: moldura amarela e **2P**. Direita a partir do Savage passa para o Hogan; baixo a partir do Hogan passa para o Duggan. O movimento é por novos pressionamentos, não deslocamento contínuo ao manter a direção. A tabela `0x74F2` liga os vizinhos da grade: as bordas **não dão a volta**.
- Confirma o **Button 1** do jogador. Não confundir com os três botões de início do gabinete. Código: leitura/bordas `0x7240–0x729A`; despacho `0x749E` (0 = mover, 1 = confirmar, 2/3 = retorno sem seleção). Confirmação `0x7552`: bloqueia duplicados por meio de bits em `0x1C0069` e faz piscar o fundo do retrato; veem-se mudanças verde/magenta. Teste: o P2 tentou confirmar o Duggan, já escolhido pelo P1, e seu contador continuou em zero.

## Equipes e transição, verificadas

- **Início A — 1P VS CPU:** na mesma tela você escolhe o lutador e depois o parceiro; não há outra tela de parceiro. Teste: Duggan e Honky; ambos aparecem no HUD da luta (`08_1P_combate.png`). Os dois rivais da CPU são sorteados entre os restantes (`0x71E8`).
- **Início B — 1P VS 2P:** cada jogador escolhe dois, sem repetir entre as equipes. Confirmação manual verificada: Duggan/Honky contra Big Boss Man/Warrior (`10` e `11`).
- **Início C — 1P/2P VS CPU:** cada jogador escolhe um e eles formam a mesma equipe. Verificado Duggan + Big Boss Man, juntos no HUD esquerdo (`13`). Código de união: `0x7392–0x73A6`; condições de fechamento `0x72DA–0x731E`.
- Ao confirmar, os cursores são retirados e os escolhidos piscam. Depois há uma transição: no 1P foi capturada a mensagem **THREE MORE VICTORIES TO GET TO THE TITLE MATCH!!**, a apresentação **WWF Live from NEW YORK**, a entrada e a luta. O laço `0x704E–0x71B2` espera ao fechar `0x40` refreshes, ou `0x70` no versus.

## Tempo e som

- **Não se vê um contador numérico** nas capturas da seleção, nem logo antes do limite. Existe sim um tempo interno: `0x7098` carrega `0x180` = 384 em `0x1C006A`; `0x72A4` desconta um por refresh. No registro: 383 no frame 602 e 363 no 622. Aproximadamente 6,68 s com o refresh configurado neste MAME (~57,44 Hz; não é medição da placa).
- Sem escolher, quando o tempo se esgota começa um sorteio animado que preenche as vagas livres: `0x7328`, `0x73E8`. No `TIMEOUT.log`, primeira escolha automática no frame 1049 e segunda no 1113. Não significa que a tela inteira dure só 384 frames: o sorteio e o fechamento acrescentam tempo.
- `0x705E–0x7066` prepara o comando musical **0x0A**, enviado por meio de `0x25E6`. **Nome da melodia e SFX não identificados**: os testes foram executados sem saída de áudio.

## Localização gráfica rápida, a partir do código/driver

- Cena 4: `0x7078 → 0x1F434 → 0x2034A`. Mapa base na ROM da CPU `0x210A8`, escrito na BG RAM `0x0C0000`; descompressor `0x203C2`. Retratos: `0x2035A–0x203B0`, blocos de 4×4 tiles de 16×16 por meio de `0x20404`:

| Retrato | Tiles BG inclusivos | Banco de cor BG |
|---|---|---|
| Savage | 0x383–0x392 | 0 |
| Hogan | 0x393–0x3A2 | 1 |
| Warrior | 0x3A3–0x3B2 | 2 |
| Honky | 0x3D3–0x3E2 | 3 |
| Duggan | 0x3C3–0x3D2 | 4 |
| Big Boss Man | 0x3B3–0x3C2 | 5 |

- Região `bgtiles` do driver: `24j7-0.113` em 0x00000 e `24j6-0.112` em 0x40000; formato de planos `tiles16x16_layout`. Não são offsets lineares de imagens completas. Texto/cursor: FG RAM `0x080000`, região `fgtiles`, ROM `24aa-0.58`; atualização do cursor `0x75B6`, tabelas `0x7686` e `0x782A`.
- Paleta da seleção: seletor **4** em `0x706C`; carga `0x29F6`. BG: tabela `0x2F0A`, entrada 4 → `0x2FAE`, oito ponteiros para cores: `0x3416/3434/3452/3470/348E/34AC/34CA/34CA`, destino `0x140200`. Piscar: `0x1F5C/0x1F86`. Referências conferidas com `analisis/tools/prog.bin` e `wwfsstar.cpp`; não foram extraídos nem modificados gráficos.

## Capturas principais (nesta pasta)

`01_1P_inicial.png`, `02_1P_cursor_hogan.png`, `03_1P_cursor_duggan.png`, `04_1P_primero_confirmado.png`, `05_1P_elegir_companero.png`, `06_1P_equipo_confirmado.png`, `07_1P_transicion.png`, `08_1P_combate.png`, `09_2P_versus_inicial.png`, `10_2P_versus_equipos.png`, `11_2P_versus_combate.png`, `12_2P_coop_inicial.png`, `13_2P_coop_combate.png`, `14_limite_sin_contador_visible.png`, `15_timeout_sorteo.png`.

**Limites:** observação do set local no MAME, não da placa física nem de outras revisões/regiões. Som não identificado; não foi feita a extração completa de todos os textos/tiles.
