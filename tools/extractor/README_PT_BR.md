# Extrator de recursos — **PENDENTE**

Este utilitário **ainda não existe**. Sua função será ler **a sua própria ROM** (set MAME `wwfsstar`, obtido legalmente) e gerar os recursos de que o port precisa para compilar, sem que o repositório tenha que conter nenhum dado do arcade. Enquanto ele não existir, o código não pode ser compilado com conteúdo real (ver `docs/PT_BR/COMPILAR_PT_BR.md`).

## Requisitos

1. Conferir o set (CRC32/SHA1 de cada arquivo segundo `mame -listxml wwfsstar`) antes de extrair qualquer coisa.
2. Gerar, **idênticos byte a byte** aos usados na b95, os 32 arquivos de `res/` e os 4 cabeçalhos de `src/gen/` listados abaixo.
3. As saídas nunca são enviadas ao repositório: o `.gitignore` exclui `res/**/*.bin`, `res/**/*.wav` e `src/gen/*.h`.
4. Os conversores originais foram feitos versão a versão (b42–b92) e estão no backup privado do projeto. É preciso reuni-los num único processo reproduzível; as notas de cada versão (`docs/notas/`) descrevem como cada recurso foi obtido.
5. **Exceção:** os córneres superiores e o logo WWF do fundo (`bgb_tiles.bin`/`bgb_map52.bin`/`pal.bin`, «fundo do Emilio» desde a b42) têm edições manuais do Emilio que **não são publicadas**. O extrator vai gerar a versão do arcade; por isso o MD5 da ROM não vai coincidir com a b95, a menos que essas edições sejam aplicadas de outra forma.

## Recursos de `res/` (32, referenciados por `res/res.res`)

| Arquivo | Bytes | Conteúdo | Origem nas notas |
|---|---:|---|---|
| `graficos/paletas/pal.bin` | 64 | Paletas do fundo (2×16 cores MD) | b42/b49 (fundo do Emilio) |
| `graficos/fondos_cuerdas_publico/bgb_tiles.bin` | 113280 | Tiles do fundo (ringue, chão, arquibancadas) | b42/b49 |
| `graficos/mapas/bgb_map52.bin` | 11968 | Mapa do mundo de fundo (88×68) | b52 |
| `datos/crowd_b52.bin` | 61566 | Animação do público por zonas | b49/b52 |
| `graficos/fondos_cuerdas_publico/crowd_b49_tiles.bin` | 19456 | Tiles do público | b49 |
| `graficos/fondos_cuerdas_publico/ex52_tiles.bin` | 16160 | Tiles de preenchimento do lado de fora | b50/b52 |
| `sonidos/oki_s03.wav` | 65580 | Amostra OKI 0x03 decodificada: WAV mono, 16 bits, 8000 Hz, 32768 amostras (PCM4 no SGDK) | análise de som |
| `sonidos/oki_s04.wav` | 65580 | Amostra OKI 0x04 decodificada, mesmo formato | análise de som |
| `graficos/fondos_cuerdas_publico/ropes_tiles.bin` | 12512 | Tiles das cordas (391 tiles, na VRAM 1120) | b53/b61 |
| `graficos/luchadores/spr_tiles.bin` | 933600 | Tiles de todas as poses (Duggan, Warrior, árbitro…) | b55/b56 e acréscimos b81–b92 |
| `datos/spr_tab.bin` | 108486 | 861 `Pose` × 126 bytes (ver `docs/PT_BR/ARQUITECTURA_PT_BR.md`) | b55/b56 e acréscimos |
| `graficos/paletas/spr_pal.bin` | 64 | Paletas de sprites | b53 |
| `datos/move_seq.bin` | 1716 | Sequências de movimento (pose, duração) | b65/b85 |
| `datos/sx_seq.bin` | 1856 | Sair/entrar no ringue | — |
| `datos/bx_seq.bin` | 1056 | Sequência do lado de fora | — |
| `datos/climb_pose.bin` | 1360 | Subida no córner | — |
| `datos/run_pos.bin` | 436 | Posições da corrida/rebote | — |
| `datos/camtab.bin` | 772 | Tabela da câmera | — |
| `graficos/luchadores/part_tiles.bin` | 2752 | Tiles parciais remapeados para PAL2 | b56 |
| `datos/xl_w.bin` | 1276 | Pose lógica → pose do port (Warrior) | b76/b84 |
| `datos/xl_d.bin` | 1276 | Pose lógica → pose do port (Duggan) | b84 |
| `datos/sp_trk.bin` | 48720 | Trilhas do arcade de arremessos/voos | b69/b70 |
| `datos/pin_glyph.bin` | 1472 | Dígitos da contagem do pin | b76 |
| `datos/credit_dig.bin` | 320 | Dígitos de créditos | — |
| `datos/big_dig.bin` | 3200 | Dígitos grandes da contagem fora do ringue | b72 |
| `graficos/seleccion/select89_tiles.bin` | 16512 | Tela de seleção | b89 |
| `graficos/seleccion/select89_map.bin` | 1792 | Mapa da seleção | b89 |
| `graficos/seleccion/select89_cursors.bin` | 21504 | Cursores e retratos | b89 |
| `graficos/paletas/select89_pal.bin` | 256 | Paletas da seleção | b89 |
| `graficos/titulo/title89_tiles.bin` | 21888 | Tela de título | b89 |
| `graficos/titulo/title89_map.bin` | 1792 | Mapa do título | b89 |
| `graficos/paletas/title89_pal.bin` | 32 | Paleta do título | b89 |

«—» = a origem exata ainda precisa ser localizada nas notas e scripts históricos do backup. No backup há mais 3 arquivos que o `res.res` não usa (`bgb_map50.bin`, `ex50_tiles.bin`, `crowd_b49.bin`) e que não são necessários. O `res/crowd_b49.h` (3 constantes de tamanho) está publicado.

## Cabeçalhos de `src/gen/` (4)

Declarações que o código espera. Os valores saem da ROM e **não são publicados**:

```c
/* src/gen/ropes.h — mapas de tiles das cordas (vibração) e 2 paletas */
#define X0 22
#define Y0 19
#define W0 6
#define H0 27
#define NS0 84
static const u16 mp0[8][162];  static const u8 sc0[84];
#define X1 60
#define Y1 18
#define W1 6
#define H1 28
#define NS1 84
static const u16 mp1[5][168];  static const u8 sc1[84];
#define XH 20
#define YH 39
#define WH 48
#define HH 9
static const u16 mph[432];  static const u16 palR2[16];  static const u16 palR3[16];
#define VT 1120
#define NR 391

/* src/gen/gs69.h — trilhas sp_trk 0x05 (cotovelada no chão) e 0x11 (salto sobre o lutador deitado) */
#define GS5_N 29
#define GS5_K 16
#define GS11_N 83
#define GS11_K 40
static const u16 gs5P[29];  static const u16 gs11P[83];  static const s8 gs11X[83];  static const s8 gs11Z[83];

/* src/gen/hud.h — moldura do HUD: 12 tiles 4bpp e seu mapa */
static const u32 hudT[12*8];  static const u8 hudMap[4][32];
#define HUD_NT 12

/* src/gen/select89_data.h — navegação e cores da seleção (747A, 2048, 2054) */
#define SEL89_NT 516
#define TITLE89_NT 684
static const u8 selNav89[96];  static const u8 autoNav89[36];  static const u16 flashColor89[6];  static const u8 flashPen89[6];
```

As constantes `#define` são geometria e tamanhos de que o código precisa. Com essas declarações inicializadas com `{0}` e os arquivos de `res/` zerados, o projeto compila (testado em 09/11/2026) e sai uma ROM preta.
