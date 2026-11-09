/* b83: Warrior remate suelo EXACTO arcade: C798 X=ox b7=vface (sin ox±48), destino 111D0 ±0x20, p1face=!vface, 112F0 fase0=1 tick, 1152A 7D flip opuesto+x±4 en draw. */
/* b81: cuerdas cortas por fase visual arcade y Warrior suelo 0xC706/0x10A5E/0x1173A, sin trayectoria sp-port. */
/* b77: pin Warrior / capas arcade BD10-BEC0; kickout B012 + fisica 27D2/3E20; referee VRAM fragmentada sin saltar bancos. */
/* b79 (base b78): vibracion corta al chocar y caer = pasos arcade 0x21324 d0=1 + mapas 0x2146e con redibujo real; sc[] largo intacto. */
/* b78 (base b77): solo vibracion corta de cuerda al chocar y caer (0x21324 paso 2); rebote correr intacto. */
/* b75 (base b74): eje Y lanzamiento/pin = arcade BD10/BEF2 + pista (z0=q[3]; S0C oy+=dy s62). */
/* b71: arbitro cuenta pin (3) y fuera (20) -> reset combate; 1.a cuenta = se libra solo; salto Warrior = arcade 0x0C.
   b58 (Emilio): b57 + arbitro camina por el ring.
   Arbitro: HIGH + zonas color + orden por pies; rodea luchadores; piezas que tocan HUD -> LOW;
   no pisa laterales (margen 16); walk/follow + refAvoid (serie s). Paletas b57. */
#include <genesis.h>
#include "res.h"
#include "crowd_b49.h"
#include "gen/hud.h"
#include "gen/ropes.h"
#include "native81.h"
#include "knee90.h"
#include "gen/gs69.h"
#include "select89.h"

#define NEX 505
#define MW 88
#define MH 68
#define VW 33
#define VH 29
#define NT (NB49+NCA+NEX+1)
#define POOLN 1000          /* deja 1016.. para sprites; cuerdas VT=1120 */
#define SPR_BASE 1016
#define SLOTP1 72
#define HUD_H 34
#define ROPE_FRONT_R0 39
#define MIRB 35
#define PDLY 2
#define CLIMB_LEN 340
#define RING_Y0 229
#define RING_Y1 373
#define RING_XL 616
#define RING_XR 917
#define CAMX_MIN (-32)
#define CAMX_MAX 352
#define WX0 32
#define WY0 16
#define CLIMB_XL 648
#define CLIMB_XR 888
#define CLIMB_XB 622
#define CLIMB_XE 913
#define SX_NX 62
#define SX_NE 54
#define SX_HOLD 27
#define SX_OUTR 1016
#define SX_OUTL 512
#define SX_YOUT 456
#define SX_YIN0 288
#define SX_YIN1 394
#define SX_YMIN 293
#define BX_NX 65
#define BX_NE 67
#define BX_XL 640
#define BX_XR 895
#define BX_YO0 192
#define BX_YO1 224
#define HUD_SAFE 116
#define DREQ_LAG 4

typedef struct { s16 dx, dy; u16 sz, line, toff; } Piece;
typedef struct { u16 n, t0, nt; Piece p[12]; } Pose;
typedef struct { s16 k, x, y, z; } CK;

static u16 refc[NT], slotOf[NT], fstk[POOLN], nf;
static u16 W[MW*MH];
static u16 AQ[32*64];
static s16 tx, ty, cx, cy;
static u16 rcur[2];
static s16 rk[2] = {-1, -1};
/* b79: caida corta = maquina de pasos arcade (no saltar sc[] a 48). 0x213A4 duraciones, 0x2146e mapas. */
static u16 rFall[2], rStep[2], rTimer[2];
static const u8 ropeDurA[8] = {0x10, 0x08, 0x06, 0x04, 0x03, 0x02, 0x02, 0x01}; /* 0x213A4 */
/* 213AC is STEP->PHASE; 2146E is PHASE->drawing, not STEP->drawing.
   Captured mp[] banks have different deduplicated indices. Late phase 2/3:
   left mp6/mp7, right mp3/mp4. Never index these banks with 2146E[step]. */
static const u8 ropePhaseA[8] = {1,2,3,2,3,2,3,0}; /* 0x213AC */
static const u8 ropeShortMap[2][4] = {{0,7,6,7},{0,4,3,4}};

static const Pose *poseTab;
static u16 sat[80 * 4], nsat;
static s16 ox, oy, oxf, oyf, z0 = 187;
static s16 dox, doy, dz0 = 187;
static s16 camx = 128, camy = 128, tgx, tgy;
static u16 curPose, wantPose, walkPh, p1face, lastBase = 0xFFFF;
static u16 climb, ck, afterPose, dreq;
static u16 sx, sxk, sxR, outK, pushC, sxLim; static s16 pushD, sxX0, sxY0;
static u16 bx, bxk; static s16 bxX0, bxY0;
static u16 rn, rnk, rnb, rnW; static s16 rnd; static s32 rnx;
static u16 mvh, moving, tick, pendBtn;
static u16 slotP1;
static s16 gvoff = 16;
static const s16 ptX[2] = {602, 939}, ptY[2] = {338, 280}; /* b56: apron arcade/s35 (Macho izq, Hogan dcha) */
static const u16 ptT[2] = {1736, 1941}; /* b67: Warrior 1680..1735 (56 t); punch0 en 1736 */
#define RF_T0 1088
#define RF_T1 1512
#define RF_HOME_X 768
#define RF_HOME_Y 352
#define RF_MARGIN 16   /* b58: never step on side ropes (s51 refAvoid slack) */
#define RF_WFRONT 618  /* b62 */
#define RF_WBACK 622
#define RF_KEEP 56     /* keep-away from Duggan before refAvoid */
#define RF_IDLE 8
#define REFB 494       /* walk poses use H-flip when >= REFB (s41) */
/* b65: Ultimate Warrior (sin pelea/IA/colision). START = seguir / dejar de seguir. Poses arcade 6 idle, 69-72 walk (move_seq 704), PAL2 (Duggan+Warrior, s-port). */
#define WR_T 1672   /* b69: 1672..1735 (64 t) libre tras la ventana HUD (H32, 4 filas) */
#define WR_IDLE 6
#define WR_KEEP 40
/* b69: dos luchadores con el MISMO motor (andar, correr, salir/entrar, esquineros, golpes). 0 = Duggan, 1 = Warrior.
   Y cambia SOLO a quien controla el mando (b89; antes C) (ctl). START = el oponente (el que no controlas) te persigue / se para.
   Las poses del motor estan en "espacio Duggan"; Warrior las dibuja con xl_w (equivalente arcade banco 0, mismo indice).
   Las reacciones/caidas estan en "espacio Warrior"; Duggan las dibuja con xl_d (equivalente arcade banco 3). */
static u16 gs, gk; static s16 gX0, gY0, gM, gD, gH;
typedef struct { s16 ox, oy, oxf, oyf, z0; u16 curPose, walkPh, p1face, lastBase, climb, ck, afterPose, dreq;
 u16 sx, sxk, sxR, outK, pushC, sxLim; s16 pushD, sxX0, sxY0; u16 bx, bxk; s16 bxX0, bxY0;
 u16 rn, rnk, rnb, rnW; s16 rnd; s32 rnx; u16 mvh, moving, tick, pendBtn, mv, mk, dFl, dFace, pAlt, pAcc, gs, gk; s16 gX0, gY0, gM, gD, gH; } FC;
static FC fd[2];
/* Warrior only: 0xC sub 0xC (dive) / sub 5 (stomp), one arcade tick / 2 VBlanks. */
static u16 w81Phase, w81Time, w81Var, w81Draw;
/* b90: energy 7FEC/16488. Both actors HUMAN; never shared with vdmg. */
static u16 energy90[2];
static void hurt90(u16 f,u16 n){energy90[f]=(energy90[f]>n)?energy90[f]-n:0;}
static u16 kneePost90,kneeFloor90;
/* Preserve a pre-clip origin for Knee only; ordinary outside movement is untouched. */
static s32 kneeRawX91,kneeClipX91;static s16 kneeRawY91;static u16 kneeRawValid91;
/* 21ED0/22140, table221B2: floor128, Y=192..456, X=488..1040,
   slope /6 and inner margin48. ACA4 tests +48 then -8, word-only. */
static void kneeOutsideClamp91(FC *q,u16 left){
 if(q->oy<192)q->oy=192;if(q->oy>456)q->oy=456;
 s16 e=(q->oy-192)/6,lo=488+e,hi=1040-e;
 if(q->oy>=217){if(left)hi=lo+48;else lo=hi-48;}
 if(q->ox<lo)q->ox=lo;if(q->ox>hi)q->ox=hi;
}
static void kneeOutsideVictim91(u16 o,u16 face){
 FC *q=&fd[o];const u16 left=q->ox<768;const s16 a=face?48:-48,b=face?8:-8;
 q->ox+=a;kneeOutsideClamp91(q,left);q->ox-=a;
 q->ox-=b;kneeOutsideClamp91(q,left);q->ox+=b;
}


/* Native ground counter is tracked without changing other moves/get-up. */
static u16 ground90[2],groundSeen90[2],kvPhase90[2],kvTime90[2];
static s32 kvZ90[2];static s16 kvVz90[2];
static s16 w81Vx,w81Vy,w81Vz;
static s32 w81X,w81Y,w81Z;
static u16 ctl, follow, curF;
static u16 fs[2], fsP[2], koF[2]; static s16 fsVz[2]; static s32 fsZ[2]; /* b76 caida accion 8 */
static s16 fsVx[2], fsDir[2]; static u16 fsTick[2]; static s32 fsX[2]; /* b77: 1C, tabla 29B4 */
static u16 vh[2], vk[2], vdmg[2], vlast[2], vface[2], vjolt[2];
static u16 dPose[2], dFlip[2], dLoaded[2] = {0xFFFF, 0xFFFF}, dLog[2]; static s16 dX[2], dY[2], dZ[2], dLyo[2];
static u16 dSx[2], dBx[2], dClimb[2], dOutK[2];
static const u16 dSlot[2] = {1016, WR_T}, dMax[2] = {72, 64};
/* b86: A = combo arcade FC84: FD70 (0x150-152) / FD7C (0x153-155). Encadenar = NUEVA pulsacion A
   en la ultima pose (+0x114 → +0x22; NO hold). Duraciones FD70/FD7C: 4+3+3.
   move_seq 0..9 = FD70; 10..19 = FD7C. B = patada (33, 31 f). Impacto mk=10; alcance 40/42 x 7.
   Clothesline (A en carrera, rn=3 / arcade sub 0x14 @ 0x12E7A): hit + rival accion 8 sub 0x17 (rec_lanzado_20). */
#define MV_HIT_PUN 10
#define MV_HIT_KIK 18
#define MV_REACH_PUN 40
#define MV_REACH_KIK 42
#define MV_REACH_Y 7
#define CL_REACH_X 0x60  /* arcade 0x16634 filtro proximidad */
#define CL_REACH_Y 8
#define CL_HIT_UNTIL 20  /* arcade conecta antes de paso 0x10 (~20 f de 0x1302E) */
static u16 mv, mk, dFl, dFace; /* dFl: H-flip de Duggan en golpes mirando a la izq */
static u16 pAlt; /* +0xC0 bit0 — 0=FD70, 1=FD7C */
#include "cl87.h"
/* Native refresh: 17.408ms (MAME wwfsstar), one logic tick / 2 refreshes.
   1/0.034816 = 28.722426 ticks/s. 3125/6528 at NTSC, 3125/5440 PAL.
   Use VBlank elapsed time, not loop iterations (DMA may cost a refresh). */
static u32 arcClock, arcLast; static u16 arcTick, arcDen;
static u16 clInit[2], clStep[2], clTimer[2], clHeld[2], clPose[2], pEnd[2];
static u16 clFallTime[2];
static u16 pAcc; /* b86: +0x22 acumulador de pulsaciones nuevas durante ultima pose */
/* Warrior: wrHit 1 = reaccion punetazo (seq 64, 13 f), 2 = reaccion patada (seq 77, 41 f), 3 = derribo (tumbado + levantarse + atontado) */

static const u16 wrDown[][2] = {{45,8},{626,6},{114,140},{115,30},{116,16},{117,16},{116,16},{117,16},{116,16},{117,16},{0,0}}; /* b68: 626 = Warrior boca abajo REAL (arcade b0 p157); hold boca arriba 114 */
static u16 gBx; /* bx state mirror for priority */
static s16 rfx = RF_HOME_X, rfy = RF_HOME_Y;
static u16 rfPose = RF_IDLE, rfFl, rfPh, rfMoving, rfLoaded = 0xFFFF;

static const CK climbL[] = {{2,630,377,180},{18,630,377,225},{26,624,377,233},{44,632,374,233},{298,624,377,233},{312,630,377,225},{320,630,377,180},{336,630,377,187},{338,640,373,187},{-1,0,0,0}};
static const CK climbR[] = {{2,902,377,180},{18,902,377,225},{26,912,377,232},{34,912,377,228},{44,900,374,233},{298,912,377,228},{304,912,377,232},{312,902,377,225},{320,902,377,180},{336,902,377,187},{338,896,373,187},{-1,0,0,0}};
static const CK climbB[] = {{2,610,232,183},{14,607,232,231},{24,604,221,235},{278,607,232,231},{284,610,232,183},{296,610,232,187},{298,616,232,187},{-1,0,0,0}};
static const CK climbE[] = {{2,921,232,183},{14,922,232,231},{24,932,221,235},{278,922,232,231},{284,921,232,183},{296,921,232,187},{298,920,232,187},{-1,0,0,0}};
static const s16 cD0[4] = {298, 298, 278, 278}, cPOST[4] = {44, 44, 24, 24}, cEND[4] = {340, 340, 300, 300}, cPAN[4] = {296, 296, 276, 276}, cYH[4] = {336, 336, 296, 296};
static const u16 rnPos[6] = {0, 48, 96, 137, 178, 198};
/* b95: carrera arcade 0x945C: velocidad byte 0x95BC[id] -> +0x21 (Warrior id0 = 28, Duggan id3 = 27); 0x3DF0: vel/4 px por tick */
static const u8 rnSpd[2] = {27, 28}; static u16 rnT[2];
static const u16 mvOffR[8] = {1452, 1476, 1500, 1548, 1596, 1636, 1676, 1696}; /* runR runL bncR bncL atkR atkL brkR brkL */

static u16 acq(u16 e){
 u16 id=e&0x1FFF; if(!id) return 0;
 if(!refc[id]){ if(!nf) return 0; u16 s=fstk[--nf]; slotOf[id]=s;
  const u8 *src=(id<=NB49)?t_bin+(u32)(id-1)*32:(id<=NB49+NCA)?ca_tiles+(u32)(id-NB49-1)*32:ex_tiles+(u32)(id-NB49-NCA-1)*32;
  VDP_loadTileData((const u32*)src,s,1,CPU);}
 refc[id]++;
 return ((e&0x8000)>>2)|((e&0x6000)>>2)|slotOf[id];}
static void rel(s16 r,s16 c){ u16 *a=&AQ[(r&31)*64+(c&63)]; u16 id=*a; if(id&&!--refc[id]) fstk[nf++]=slotOf[id]; *a=0;}
static u16 ropeA(s16 r,s16 c){
 if(c>=X0&&c<X0+W0&&r>=Y0&&r<Y0+H0) return mp0[rcur[0]][(r-Y0)*W0+c-X0];
 if(c>=X1&&c<X1+W1&&r>=Y1&&r<Y1+H1) return mp1[rcur[1]][(r-Y1)*W1+c-X1];
 if(c>=XH&&c<XH+WH&&r>=YH&&r<YH+HH) return mph[(r-YH)*WH+c-XH];
 return 0;}
static void put(s16 r,s16 c){ u16 e=W[r*MW+c]; u16 v=acq(e); AQ[(r&31)*64+(c&63)]=v?(e&0x1FFF):0; VDP_setTileMapXY(BG_B,v,c&63,r&31);
 VDP_setTileMapXY(BG_A,ropeA(r,c),c&63,r&31);}
/* b95: streaming de columnas/filas por DMA en cola. b94 cargaba cada tile nuevo por CPU (VDP_loadTileData CPU) en
   pantalla activa: ~0,2-0,6 frame por columna/fila -> frames perdidos junto a los postes (camara X+Y).
   Ahora: tile (ROM->VRAM) y entradas BG_B en la cola DMA; SYS_doVBlankProcess la vuelca en el vblank, antes del scroll
   nuevo, asi la columna/fila aparece completa el mismo frame que antes. BG_A (cuerdas) sigue por CPU (sin slots).
   Presupuesto ST_BUD tiles/frame; si se pasa (salto de camara) se vacia la cola antes de seguir, sin perder orden. */
#define ST_BUD 40
#define ST_BUFN 256
static u16 stBuf[ST_BUFN], stBN, stTiles;
static u16 acqQ(u16 e){
 u16 id=e&0x1FFF; if(!id) return 0;
 if(!refc[id]){ if(!nf) return 0; u16 s=fstk[--nf]; slotOf[id]=s;
  const u8 *src=(id<=NB49)?t_bin+(u32)(id-1)*32:(id<=NB49+NCA)?ca_tiles+(u32)(id-NB49-1)*32:ex_tiles+(u32)(id-NB49-NCA-1)*32;
  if(((u32)src&0x1FFFF)<=0x1FFE0) DMA_queueDmaFast(DMA_VRAM,(void*)src,s*32,16,2); else DMA_queueDma(DMA_VRAM,(void*)src,s*32,16,2); stTiles++;} /* Fast si no cruza banco 128 KB */
 refc[id]++;
 return ((e&0x8000)>>2)|((e&0x6000)>>2)|slotOf[id];}
static void stRoom(u16 n){ if(stTiles+n>ST_BUD||stBN+2*n>ST_BUFN||DMA_getQueueSize()+n+8>DMA_QUEUE_SIZE_DEFAULT){ DMA_flushQueue(); stTiles=0; stBN=0; } }
static void stCol(s16 c,s16 r0,s16 n){ /* columna c, filas r0..r0+n-1; BG_B y BG_A en tramos sin vuelta (fila 32) */
 stRoom(n); u16 *b=&stBuf[stBN], *a=b+n; stBN+=2*n;
 for(s16 i=0;i<n;i++){ const s16 r=r0+i; const u16 e=W[r*MW+c]; const u16 v=acqQ(e); AQ[(r&31)*64+(c&63)]=v?(e&0x1FFF):0; b[i]=v; a[i]=ropeA(r,c); }
 for(s16 i=0;i<n;){ const s16 rr=(r0+i)&31; s16 m=32-rr; if(m>n-i) m=n-i;
  DMA_queueDmaFast(DMA_VRAM,b+i,VDP_getPlaneAddress(BG_B,c&63,rr),m,planeWidth*2);
  DMA_queueDmaFast(DMA_VRAM,a+i,VDP_getPlaneAddress(BG_A,c&63,rr),m,planeWidth*2); i+=m; } }
static void stRow(s16 r,s16 c0,s16 n){ /* fila r, columnas c0..c0+n-1; tramos sin vuelta (col 64) */
 stRoom(n); u16 *b=&stBuf[stBN], *a=b+n; stBN+=2*n;
 for(s16 i=0;i<n;i++){ const s16 c=c0+i; const u16 e=W[r*MW+c]; const u16 v=acqQ(e); AQ[(r&31)*64+(c&63)]=v?(e&0x1FFF):0; b[i]=v; a[i]=ropeA(r,c); }
 for(s16 i=0;i<n;){ const s16 cc=(c0+i)&63; s16 m=64-cc; if(m>n-i) m=n-i;
  DMA_queueDmaFast(DMA_VRAM,b+i,VDP_getPlaneAddress(BG_B,cc,r&31),m,2);
  DMA_queueDmaFast(DMA_VRAM,a+i,VDP_getPlaneAddress(BG_A,cc,r&31),m,2); i+=m; } }
static void ropeDraw(u16 sd){
 const s16 x0=sd?X1:X0, y0=sd?Y1:Y0, w=sd?W1:W0, hh=sd?H1:H0;
 for(s16 r=y0;r<y0+hh;r++) if(r>=ty&&r<ty+VH) for(s16 c=x0;c<x0+w;c++) if(c>=tx&&c<tx+VW) VDP_setTileMapXY(BG_A,ropeA(r,c),c&63,r&31);}

/* ---- publico (igual b52) ---- */
static u8 ca183e[8], ca1854[4], ca184a[5];
static u16 caZone=1, caPar, caCur=0xFFFF, caPos, caRR;
static u16 caLast[6]={0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF}, caPend[6]={0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF};
static const u8 caPh[12]={0,1,2,1,2,1,2,1,2,1,2,0};
static void caWant(u16 cat,u16 id){ if(caLast[cat]==id) return; caLast[cat]=id; caPend[cat]=id; }
static void caLogic(void){
 const s16 acx=cx-32-64;
 { const u16 z=(acx<0x40)?0:(acx<0xC0)?1:2; if(z>caZone) caZone++; else if(z<caZone) caZone--; }
 if((caPar^=1)) return;
 if(!(ca1854[0]&0x80)&&(ca183e[0]&0xC0)){
  if(!(ca183e[0]&0x20)){ ca183e[0]|=0x20; ca183e[4]=caZone; ca183e[2]=10; ca183e[3]=6; ca183e[0]=0xE5; }
  ca183e[0]|=0x10;
  if(ca183e[3]--==0){ if(ca183e[2]--==0) ca183e[0]=0x80; else ca183e[3]=6; } }
 if((ca1854[0]&0x40)||((ca1854[0]&0x80)&&caZone==1)){
  if(!(ca1854[0]&0x20)){ ca1854[0]|=0x20; ca1854[2]=0; ca1854[3]=3; }
  ca1854[0]|=0x10;
  if(ca1854[3]--==0){ if(++ca1854[2]==2) ca1854[0]=0; else ca1854[3]=32; } }
 if(!(ca184a[0]&0x40)){ ca184a[0]|=0x40;
  static u16 caRng=0x1234; caRng=caRng*25173+13849; const u16 r=caRng>>8;
  ca184a[1]=r&3; ca184a[2]=(r>>2)&3; ca184a[3]=0; ca184a[4]=10; ca184a[0]|=0x20; }
 if(--ca184a[4]==0){ ca184a[0]|=0x10; ca184a[3]++; ca184a[4]=10;
  if(ca184a[3]==2){ if(ca184a[2]--==0) ca184a[0]=0; else ca184a[3]=0; } }
}
static void caDraw(void){
 if(ca1854[0]){ if(caZone==1&&(ca1854[0]&0x10)&&ca1854[3]==1&&ca1854[2]<2) caWant(4,36+2+ca1854[2]); }
 else if((ca183e[0]&0x10)&&ca183e[3]<4) caWant(ca183e[3],(caZone*4+ca183e[3])*3+caPh[ca183e[2]]);
 if(!(ca183e[0]&0x80)&&(ca184a[0]&0x20)&&ca184a[3]<2) caWant(5,42+ca184a[1]*2+ca184a[3]);
}
#define CA_BUD 120
static void caApply(void){
 const u16 *o=(const u16*)ca_bin; u16 n=0, scan=0;
 while(n<CA_BUD&&scan<600){
  if(caCur==0xFFFF){ u16 k=0; while(k<6&&caPend[caRR]==0xFFFF){ caRR=(caRR+1)%6; k++; } if(k==6) break;
   caCur=caPend[caRR]; caPend[caRR]=0xFFFF; caRR=(caRR+1)%6; caPos=o[caCur]; }
  if(caPos>=o[caCur+1]){ caCur=0xFFFF; continue; }
  if(nf<16) break;
  const u16 *q=o+CA_NL+1+caPos*3; caPos++; scan++;
  const u16 m=q[1]>>1, e=q[2]; if(m<4*MW||W[m]==e) continue;
  W[m]=e; n++;
  const s16 r=q[0]>>7, c=q[0]&127;
  if(r>=ty&&r<ty+VH&&c>=tx&&c<tx+VW){ rel(r,c); put(r,c); }
 }
}
static const u8 seq50[]={3,7,10, 3,3,20, 3,0,100, 3,0,100, 3,0,100, 3,0,100, 3,0,100, 3,3,150, 3,5,255, 0};
static const u8 seq51[]={4,7,10, 4,3,20, 4,0,100, 4,0,100, 4,0,100, 4,0,100, 4,0,100, 4,3,150, 4,5,255, 0};
static const u8 attVol[9]={15,10,8,5,4,3,2,1,1};
static const u8 *sqP; static u16 sqT, sqAcc;
static void smpPlay(u8 s,SoundPCMChannel ch,u8 att){
 if(s==3) SND_PCM4_startPlay(snd03,sizeof(snd03),ch,FALSE); else SND_PCM4_startPlay(snd04,sizeof(snd04),ch,FALSE);
 SND_PCM4_setVolume(ch,attVol[att]);}
static void sqStep(void){ if(!sqP[0]){ SND_PCM4_stopPlay(SOUND_PCM_CH1); sqP=NULL; return; } smpPlay(sqP[0],SOUND_PCM_CH1,sqP[1]); sqT=sqP[2]; sqP+=3; }
static void sndCmd(u8 id){
 if(id==0x22) smpPlay(3,SOUND_PCM_CH2,0); else if(id==0x23) smpPlay(4,SOUND_PCM_CH2,0);
 else if(id==0x50||id==0x51){ sqP=(id==0x50)?seq50:seq51; sqAcc=0; sqStep(); } }
static void sqTick(void){ if(!sqP) return; sqAcc+=100; while(sqAcc>=60&&sqP){ sqAcc-=60; if(--sqT==0) sqStep(); } }
#define CA_TRIG() (ca183e[0]|=0x80)
#define CA_FENCE() (ca1854[0]|=0x80)

static void hudInit(void){
VDP_loadTileData(hudT,1,HUD_NT,CPU);
 for(u16 r=0;r<4;r++) for(u16 c=0;c<32;c++)
  VDP_setTileMapXY(WINDOW,TILE_ATTR_FULL(PAL1,1,0,0,1+hudMap[r][c]),c,r);
 VDP_setWindowVPos(FALSE,4);}

static void walkStep(s16 hx, s16 hy){
 const s32 sp = (hx && hy) ? 0x240 : 0x2C0;
 s32 X = ((s32) ox << 8 | oxf) + hx * sp, Y = ((s32) oy << 8 | oyf) + hy * sp;
 if (Y < ((s32) RING_Y0 << 8)) Y = (s32) RING_Y0 << 8;
 if (Y > ((s32) RING_Y1 << 8)) Y = (s32) RING_Y1 << 8;
 { const s16 e = ((u16) ((Y >> 8) - RING_Y0)) / 6;
   if (X < ((s32) (RING_XL + e) << 8)) X = (s32) (RING_XL + e) << 8;
   if (X > ((s32) (RING_XR - e) << 8)) X = (s32) (RING_XR - e) << 8; }
 ox = X >> 8; oxf = X & 0xFF; oy = Y >> 8; oyf = Y & 0xFF;
}

static void camera(void){
 tgx = ox - 0x200; tgy = 0x200 - oy + 56;
 const s16 want = tgx - 0x80;
 s16 nx = camx;
 if (nx < want) { nx += 2; if (nx > want) nx = want; }
 else if (nx > want) { nx -= 2; if (nx < want) nx = want; }
 if (nx < CAMX_MIN) nx = CAMX_MIN;
 if (nx > CAMX_MAX) nx = CAMX_MAX;
 s16 ny = camy;
 static u16 yt;
 if (++yt & 1) {
  s16 cY = 0x200 - camy; const s16 d = oy + z0;
  if (d <= cY + 64) { if (cY >= 240) { cY -= 2; if (cY < 240) cY = 239; } }
  else if (d > cY + 128) cY += 2;
  ny = 0x200 - cY;
 }
 { const s16 d = oy + z0, cY = 0x200 - ny; if (!climb && d > cY + HUD_SAFE) ny = 0x200 - (d - HUD_SAFE); }
 if (climb) {
  const u16 sd = climb - 1;
  const u16 pan = (ck < cPAN[sd]) && !(dreq && ck + 2 >= dreq);
  const s16 wx = pan ? ((climb == 4) ? (0x32D - 0x200) : (climb != 2) ? (0x1F9 - 0x200) : (0x302 - 0x200)) : want;
  const s16 st = pan ? 2 : 4;
  nx = camx;
  if ((yt & 1) && ck >= 18) { if (nx < wx) { nx += st; if (nx > wx) nx = wx; } else if (nx > wx) { nx -= st; if (nx < wx) nx = wx; } }
  if (ck < cYH[sd] && !(climb >= 3 && ck < 2)) {
   const s16 wy = (climb == 3) ? (0x200 - 350) : (climb == 4) ? (0x200 - 341) : (0x200 - 0x1FB); ny = camy;
   if ((yt & 1) && ck < cD0[sd] && !(dreq && ck + 2 >= dreq) && climb != 3) {
    if (ny < wy) { ny += 2; if (ny > wy) ny = wy; } else if (ny > wy) { ny -= 2; if (ny < wy) ny = wy; } }
  }
 }
 { static u16 yret; if (climb == 4 && ck >= cYH[3]) yret = 1;
   if (yret) { const s16 wy = 0x200 - 348; ny = camy;
    if (yt & 1) { if (ny < wy) { ny += 2; if (ny > wy) ny = wy; } else if (ny > wy) { ny -= 2; if (ny < wy) ny = wy; } }
    if (ny == wy) yret = 0; } }
 const s16 *t = (const s16*) camtab + ((nx - CAMX_MIN) >> 1) * 2;
 if (ny < t[0] || ny > t[1]) {
  if (ny < t[0] - 2 || ny > t[1] + 2) nx = camx;
  const s16 *u = (const s16*) camtab + ((nx - CAMX_MIN) >> 1) * 2;
  if (ny < u[0]) ny = (camy + 2 < u[0]) ? camy + 2 : u[0];
  if (ny > u[1]) ny = (camy - 2 > u[1]) ? camy - 2 : u[1];
 }
 if (((nx + WX0) >> 3) != ((camx + WX0) >> 3) && ((ny + gvoff + WY0) >> 3) != ((camy + gvoff + WY0) >> 3)) ny = camy;
 camx = nx; camy = ny;
}

static u16 sxCross(void) { return sx == 1 || sx == 3 || (sx == 2 && outK <= 65); }


/* ---- b58: arbitro (walk + avoid + clamp; fuente s49/s51/s53 + PT_RWK) ---- */
static u16 rfTile(u16 toff){ return (toff < 28) ? (RF_T0 + toff) : (RF_T1 + toff - 28); }
static void rfLoadEx(u16 np, TransferMethod tm){
 if (np == rfLoaded) return;
 const Pose *P = &poseTab[np]; if (!P->n || P->nt > 41) return;
 if (P->nt <= 28) VDP_loadTileData((const u32*)(spr_tiles + (u32)P->t0 * 32), RF_T0, P->nt, tm);
 else {
  VDP_loadTileData((const u32*)(spr_tiles + (u32)P->t0 * 32), RF_T0, 28, tm);
  VDP_loadTileData((const u32*)(spr_tiles + (u32)(P->t0 + 28) * 32), RF_T1, P->nt - 28, tm);
 }
 rfLoaded = np; rfPose = np;
}
static void rfLoad(u16 np){ rfLoadEx(np, DMA); }
/* b77: RF_T0 y RF_T1 NO son contiguos. Una pieza puede cruzar el tile
   logico 28 (503: toff26, 506: toff18); no sumar sobre rfTile(toff).
   Cada columna conserva su secuencia vertical y se corta tambien al salto VRAM.
   No altera el orden arcade por Y ni el bit de prioridad de las cuerdas. */
static void rfColumn(s16 x, s16 y, u16 off, u16 h, u16 attr){
 while (h && nsat < 78) {
  const u16 n = (off < 28 && off + h > 28) ? 28 - off : h;
  u16 *e = &sat[nsat * 4];
  e[0] = 128 + y; e[1] = ((n - 1) << 8) | (nsat + 1);
  e[2] = attr | rfTile(off); e[3] = 128 + x; nsat++;
  off += n; h -= n; y += n << 3;
 }
}

static void rfClamp(s16 ylim){
 if (rfy < RING_Y0 + 8) rfy = RING_Y0 + 8;
 if (rfy > RING_Y1 - 4) rfy = RING_Y1 - 4;
 if (ylim < rfy) rfy = ylim;
 { const s16 e = (rfy > RING_Y0) ? ((u16)(rfy - RING_Y0)) / 6 : 0;
   const s16 lo = RING_XL + e + RF_MARGIN, hi = RING_XR - e - RF_MARGIN;
   if (rfx < lo) rfx = lo; if (rfx > hi) rfx = hi; }
}
static void rfExtPose(u16 pz, s16 x, u16 fl, s16 *l, s16 *r){
 const Pose *P = &poseTab[pz]; s16 a = 32767, b = -32767;
 for (u16 k = 0; k < P->n; k++) {
  const Piece *c = &P->p[k]; if (c->dx >= 256 || c->dx <= -256) continue;
  const s16 w = (((c->sz >> 2) & 3) + 1) << 3, xx = fl ? (4 - c->dx - w) : c->dx;
  if (xx < a) a = xx; if (xx + w > b) b = xx + w;
 }
 if (a > b) { *l = x - 16; *r = x + 16; } else { *l = x + a; *r = x + b; }
}
/* s51 refAvoid (1 actor = Duggan): no solapar en X con pies mas abajo en pantalla (oy menor). */
static void refAvoid(s16 ylim){
 s16 ra, rb, wl, wr;
 { s16 rl, rr; rfExtPose(rfPose, rfx, rfFl, &rl, &rr); ra = rl - rfx; rb = rr - rfx; }
 { rfExtPose(curPose, ox, dFl, &wl, &wr); }  /* b57: Duggan MIRB copies, sin H-flip */
 #define RFBAD(rx,ry) ((ry) < oy + 4 && (rx) + rb > wl - 4 && (rx) + ra < wr + 4)
 if (!RFBAD(rfx, rfy)) return;
 s16 ymax = RING_Y1 - 4; if (ylim < ymax) ymax = ylim;
 s16 best = 32767, bx = rfx, by = rfy;
 for (s16 d = 1; d < 400 && d < best; d++)
  for (u16 c = 0; c < 3; c++) {
   const s16 tx = rfx + ((c == 1) ? -d : (c == 2) ? d : 0), ty = rfy + ((c == 0) ? d : 0);
   if (ty > ymax) continue;
   const s16 e = (ty > RING_Y0) ? ((u16)(ty - RING_Y0)) / 6 : 0;
   if (tx < RING_XL + e + RF_MARGIN || tx > RING_XR - e - RF_MARGIN) continue;
   const s16 m = c ? 8 : 0;
   if (ty < oy + 4 && tx + (rb + m) > wl - 4 && tx + (ra - m) < wr + 4) continue;
   best = d; bx = tx; by = ty; break;
  }
 if (best == 32767)
  for (s16 d = 1; d < 200 && best == 32767; d++)
   for (u16 c = 0; c < 2; c++) {
    const s16 tx = rfx + (c ? d : -d), ty = ymax;
    const s16 e = (ty > RING_Y0) ? ((u16)(ty - RING_Y0)) / 6 : 0;
    if (tx < RING_XL + e + RF_MARGIN || tx > RING_XR - e - RF_MARGIN) continue;
    if (RFBAD(tx, ty)) continue;
    best = d; bx = tx; by = ty; break;
   }
 rfx = bx; rfy = by;
 #undef RFBAD
}
/* b58: sigue a Duggan (s41 1 px/f) + refAvoid s51; anim idle 8 / 508-509 (PT_RWK 510-512 sin cabeza). */
static void rfStep(void){
 const Pose *P = &poseTab[rfPose]; s16 mdy = 0;
 for (u16 k = 0; k < P->n; k++) if (P->p[k].dy < mdy && P->p[k].dx < 256 && P->p[k].dx > -256) mdy = P->p[k].dy;
 s16 lim = 0x200 - camy - 16 + mdy - HUD_H - 2; if (lim < RING_Y0 + 8) lim = RING_Y0 + 8;
 s16 hx = 0, hy = 0; const s16 sx0 = rfx, sy0 = rfy; /* b63 */
 { const s16 dx = ox - rfx, dy = oy - rfy;
   const s16 adx = dx < 0 ? -dx : dx, ady = dy < 0 ? -dy : dy;
   if (adx > RF_KEEP || ady > RF_KEEP) {
    if (adx >= ady) hx = (dx > 0) ? 1 : -1;
    else hy = (dy > 0) ? 1 : -1;
    if (adx > RF_KEEP && ady > RF_KEEP / 2) { hx = (dx > 0) ? 1 : -1; hy = (dy > 0) ? 1 : -1; }
   }
 }
 rfx += hx; rfy += hy; /* b64: anim se decide tras clamp/avoid */
 rfClamp(lim);
 { const s16 ax = rfx, ay = rfy;  /* b63: refAvoid max 2 px/f hacia su destino */
   refAvoid(lim);
   const s16 ddx = rfx - ax, ddy = rfy - ay;
   rfx = ax + (ddx > 2 ? 2 : ddx < -2 ? -2 : ddx); rfy = ay + (ddy > 2 ? 2 : ddy < -2 ? -2 : ddy); }
 rfClamp(lim);
 /* b63: todo movimiento real anima (seguir, clamp o refAvoid) */
 { const s16 ndx = rfx - sx0, ndy = rfy - sy0;
   const s16 e = (rfy > RING_Y0) ? ((u16)(rfy - RING_Y0)) / 6 : 0;
   const u8 edge = (rfx <= RING_XL + e + RF_MARGIN) || (rfx >= RING_XR - e - RF_MARGIN);
   /* b64: en el limite, empujones de 1 px no cuentan como andar */
   const u8 mv = (ndx || ndy) && !(edge && ndx >= -1 && ndx <= 1 && ndy >= -1 && ndy <= 1 && !hy);
 if (!mv) rfMoving = 0; else {
  rfPh = (rfPh + 1) & 31;
  rfMoving = 1;
  rfPose = ((oy > rfy) ? RF_WBACK : RF_WFRONT) + ((rfPh >> 3) & 3);
  if (ox != rfx) rfFl = (ox < rfx);
 } }
}


#define FX X(ox) X(oy) X(oxf) X(oyf) X(z0) X(curPose) X(walkPh) X(p1face) X(lastBase) X(climb) X(ck) X(afterPose) X(dreq) \
 X(sx) X(sxk) X(sxR) X(outK) X(pushC) X(sxLim) X(pushD) X(sxX0) X(sxY0) X(bx) X(bxk) X(bxX0) X(bxY0) \
 X(rn) X(rnk) X(rnb) X(rnW) X(rnd) X(rnx) X(mvh) X(moving) X(tick) X(pendBtn) X(mv) X(mk) X(dFl) X(dFace) X(pAlt) X(pAcc) X(gs) X(gk) X(gX0) X(gY0) X(gM) X(gD) X(gH)
static void ctxLoad(u16 i){
#define X(f) f = fd[i].f;
 FX
#undef X
 curF = i; }
static void ctxSave(u16 i){
#define X(f) fd[i].f = f;
 FX
#undef X
}
/* b69: boca arriba / boca abajo / levantarse: cabeza al lado contrario de donde mira (mira dcha -> cabeza izq) */
static u16 invFl(u16 p){ return p == 626 || (p >= 114 && p <= 117); }
/* b93: native +A bit7 of a prone victim = the flip it is drawn with (vface^1). Arcade 10A5E/A554 never change it. */
static u16 oriVictima(u16 o){ return vface[o]^1; }
static u16 vDownIdx(u16 k){ u16 a = 0, i = 0; while (wrDown[i][1] && a + wrDown[i][1] < k) { a += wrDown[i][1]; i++; } return i; }
static u16 lyingNow(u16 o){ return vh[o] == 3 && vDownIdx(vk[o]) == 2; }
/* A554 / 28EC: A2, vz=200,g=40; AB7A preserves remaining ground timer. */
static u16 kneeVictimStep90(u16 f){
 FC *q=&fd[f];u16 ph=kvPhase90[f];
 if(arcTick){
  if(ph==1){
   if(kvTime90[f]>=9){kvPhase90[f]=2;kvTime90[f]=0;}
   else{kvTime90[f]++;kvZ90[f]+=2*(s32)kvVz90[f];kvVz90[f]-=0x80;}
  }else if(ph==2){if(ground90[f])ground90[f]--;if(!ground90[f]){kvPhase90[f]=3;kvTime90[f]=1;}}
  else if(++kvTime90[f]>8){kvPhase90[f]=0;vh[f]=0;koF[f]=0;q->p1face=q->dFace=!vface[f];q->lastBase=0xffff;return f?((const u16*)xl_w)[0]:0;}
 }
 q->z0=kvPhase90[f]==1?(kvZ90[f]>>8):((q->sx==2||q->bx==2)?128:187);
 return kneePose90[f][kvPhase90[f]==1?0:(kvPhase90[f]==2?1:2)];
}
static void kneeVictimStart90(u16 f){
 FC *q=&fd[f];s16 floor=(q->sx==2||q->bx==2)?128:187;
 kvPhase90[f]=kvTime90[f]=1;kvZ90[f]=(s32)(floor+4)<<8;kvVz90[f]=0x180;
 q->z0=floor+4;q->mv=q->gs=q->rn=q->pendBtn=0;vh[f]=vjolt[f]=0;
 /* Victim (Duggan) was already dispatched this loop: publish same-tick A2. */
 dPose[f]=kneePose90[f][0];dFlip[f]=oriVictima(f);dX[f]=q->ox;dY[f]=q->oy;dZ[f]=q->z0;dLyo[f]=0;
}
/* b94: sin desplazamiento de dibujo del tumbado (antes lyoOf ±32, b74). La pose 114/626 sin lyo ocupa
   lo mismo que la nativa arcade 0x17 en Xv (±6 px), asi que se dibuja en el ox arcade, como 10A5E/ACA4. */
static s16 bodyX(u16 o){ return fd[o].ox; }
static u16 pnS, pnA, pnV; /* b71 pin */
static u16 gr, grk, grCool, tr[2]; static u16 hittable(u16 o){ const FC *q = &fd[o]; return !gr && !pnS && !tr[o] && !fs[o] && !q->sx && !q->bx && !q->climb && !q->rn && !q->gs && vh[o] != 3; }
static void soilNudge(u16 v);
static s16 ringClampXf(s16 x, s16 y){ const s16 e = (y > RING_Y0) ? ((u16)(y - RING_Y0)) / 6 : 0; const s16 lo = RING_XL + e, hi = RING_XR - e; if (x < lo) x = lo; if (x > hi) x = hi; return x; }
static void bounceRope(u16 goingR, u16 fall);
/* b76: poses arcade convertidas (banco 0 Warrior / banco 3 Duggan, mismo origen que el punetazo) */
enum { AP_9F, AP_A0, AP_9B, AP_15, AP_16, AP_9C };
static const u16 apPose[2][6] = {{771, 772, 773, 774, 775, 777}, {766, 767, 768, 769, 770, 776}};
/* b76: accion 8 (0x99BE) en el ring: fs 1 = sub 0x1C (lanzado al zafar, 0x9B66), 2 = sub 1 (0x9B7E), 3 = sub 2 contra cuerda (0x9F02), 4 = sub 0xC (0xA4C8) */
#define FS_G 0x30   /* 0xA4C8: +0x22 = 0x30; 0x3E20: vz -= 2*g, z += 2*vz (8.8) */
static void fsAir(u16 f){ fsZ[f] += 2 * (s32)fsVz[f]; fsVz[f] -= 2 * ((fs[f] == 1) ? 0x40 : (fs[f] == 3) ? 0x10 : FS_G); /* b95: 0x9F02 -> 27D2 idx 0x11 (tabla 0x2934): g 0x10 */ if (fsVz[f] < (s16)0xF800) fsVz[f] = (s16)0xF800; }
static u16 fsInit[2];
/* b95: 0x21E5A/0x22140 tabla 0x221AA: izq toca si X <= 616+e, dcha si X > 920-e (e = (Y-229)/6) */
static s16 arcRope(u16 r, s16 y){ const s16 e = (y > RING_Y0) ? ((u16)(y - RING_Y0)) / 6 : 0; return r ? 920 - e : RING_XL + e; }
static u16 fsRope(s16 x, s16 y){ const s16 e = (y > RING_Y0) ? ((u16)(y - RING_Y0)) / 6 : 0; return x <= RING_XL + e || x >= RING_XR - e; }
static void fsStart(u16 f, u16 s, u16 bit7){ /* bit7 = arcade +0xA bit7 (mira a la dcha) */
 FC *q = &fd[f]; s16 d = (s == 1) ? fsDir[f] * 0x10 : (bit7 ? -0x10 : 0x10);
 q->ox = ringClampXf(q->ox + d, q->oy); q->oxf = 0;      /* 0x9BBE impulso 0x10 */
 fs[f] = s; fsVz[f] = (s == 1) ? 0x100 : 0; vface[f] = bit7;
 if (s == 1) { fsVx[f] = fsDir[f] * 0x100; fsX[f] = (s32)q->ox << 8; fsTick[f] = 0; koF[f] = 2; }
 fsZ[f] = (s32)((s == 1) ? (187 + 4 + 0x18) : (187 + 0x10)) << 8; /* a2+0xE: 0x18 (sub 0x1C) / 0x10 (sub 1) */
 fsP[f] = (s == 1) ? AP_9B : AP_15; q->gs = 0; q->mv = 0; q->rn = 0; q->pendBtn = 0; }
static void clFallStart(u16 f, s16 direction){
 FC *q=&fd[f]; clHeld[f]=0;fs[f]=5;koF[f]=3;vface[f]=(direction>0);
 /* 9B9A/9BBE: +/-0x20, height+0x18; A8BE->2964 vx=0x80,vz=0x100,g=0x30. */
 q->ox+=direction*0x20;q->oxf=0;fsX[f]=(s32)q->ox<<8;
 fsZ[f]=(s32)(187+0x18)<<8;fsVz[f]=0x100;fsVx[f]=direction*0x80;
 fsP[f]=0;q->mv=q->rn=q->gs=q->pendBtn=0;vh[f]=0;
}
static u16 fsStep(u16 f){
 FC *q = &fd[f];
 if(koF[f]==3){
  if(arcTick){
   if(fs[f]==7){ if(++clFallTime[f]>=22){fs[f]=0;koF[f]=0;vh[f]=3;vk[f]=154;vlast[f]=180;} }
   else {
    /* 3E20: apply velocity before subtracting 2*g. No arbitrary y arc. */
    fsX[f]+=2*(s32)fsVx[f];q->ox=fsX[f]>>8;q->oxf=fsX[f]&255;
    fsZ[f]+=2*(s32)fsVz[f];fsVz[f]-=0x60;
    if(fs[f]==5 && fsVz[f]<0){s16 h=(fsZ[f]>>8)-187;fsP[f]=(h>=0x18)?0:1;} /* 9E4C, A8BE */
    if((fsZ[f]>>8)<=187){
     /* 9C44/A530 write only the integer word: preserve the subpixel fraction. */
     fsZ[f]=((s32)187<<8)|(fsZ[f]&255);
     if(fs[f]==5){fs[f]=6;fsVx[f]=0;fsVz[f]=0x100;fsP[f]=1;} /* 9C94 -> A4C8 */
     else{fs[f]=7;fsP[f]=2;clFallTime[f]=0;} /* ABBC pose 17 */
    }
   }
  }
  q->z0=fsZ[f]>>8;return clFallPose[f][fsP[f]];
 }
 /* Arcade 27D2/29B4: vx=0x100, vz=0x100, g=0x40, 1 tick/2 frames.
    El signo X se invierte al pasar del eje arcade al del port. No se reusa
    el bit de dibujo (B084 lo gira al lanzarlo). Las otras caidas no cambian. */
 if (koF[f] == 2 && !(++fsTick[f] & 1)) { q->z0 = fsZ[f] >> 8; return apPose[f][fsP[f]]; }
 u16 hit = 0;
 if (fs[f] == 3 && fsInit[f]) { /* b95: 0x9F02 init (tick siguiente a 0x9CD0): 9700 marca cuerda d0=1, z>=0xCB, pose 0x16, 27D2 idx 0x11 (vx 0x100, vz 0, g 0x10), neg +0x24 -> rebote hacia dentro */
  const u16 R = q->ox > 768; fsInit[f] = 0; bounceRope(R, 1);
  if (fsZ[f] < ((s32)0xCB << 8)) fsZ[f] = (s32)0xCB << 8;
  fsP[f] = AP_16; fsVx[f] = R ? -0x100 : 0x100; fsVz[f] = 0; fsX[f] = (s32)q->ox << 8 | q->oxf; }
 if (fs[f] == 1 || fs[f] == 3) { fsX[f] += 2 * (s32)fsVx[f]; q->ox = fsX[f] >> 8; q->oxf = fsX[f] & 255; } /* 0x3DCE sin clamp */
 if (fs[f] == 1) { /* b95: 0x9E78 prueba X+-0x10 hacia donde vuela con 0x21E5A y la deshace; si toca: X = limite -+0x10 (con z>=0xDB 0x21E7A no recorta) */
  const s16 d = fsDir[f] * 0x10, t = q->ox + d, L = arcRope(0, q->oy), Rr = arcRope(1, q->oy);
  if (t <= L || t > Rr) { hit = 1; if ((fsZ[f] >> 8) < 0xDB) { q->ox = ((t <= L) ? L : Rr) - d; fsX[f] = (s32)q->ox << 8 | q->oxf; } } }
 /* 0x9CD0: cmpi.b #$1c,$44 compara el byte alto -> nunca 1: cualquier contacto pasa a sub 2 (0x9F02) */
 if (fs[f] == 2 && fsRope(q->ox, q->oy)) { fs[f] = 3; fsInit[f] = 1; }
 fsAir(f);
 if (fs[f] == 1 || fs[f] == 2) { const s16 h = (fsZ[f] >> 8) - 187; /* 0x9E4C anim por altura (cayendo) */
  if (fsVz[f] < 0) fsP[f] = (fs[f] == 1) ? ((h >= 0x18) ? AP_9B : AP_9C) : ((h >= 0x10) ? AP_15 : AP_16); }
 const u16 pend = (fs[f] == 3 && fsInit[f]); /* b95: contacto de sub 1 en este tick (0x9CD0 -> 0x9C3C sigue con d1=0xBB) */
 if ((fs[f] == 3 && !pend) ? (fsZ[f] < ((s32)187 << 8)) : (fsZ[f] <= (187 << 8))) { /* b95: 0x9F4E aterriza si z < 0xBB */
  fsZ[f] = 187 << 8;
  if (pend) { fsInit[f] = 0; fs[f] = 4; fsVz[f] = 0x100; fsP[f] = AP_16; } /* b95: 0x9C94 sub 0xC (0x9F02 no llega a correr) */
  else if (fs[f] == 1 && !hit) { s16 d = fsDir[f] * 0x20; q->ox = q->ox + d; q->oxf = 0; fs[f] = 4; fsVz[f] = 0x100; fsP[f] = AP_16; } /* 0x9C5A: +0x45=0x1C -> x+-0x20 (sin clamp), sub 0xC */
  else if (fs[f] == 1) { fs[f] = 4; fsVz[f] = 0x100; fsP[f] = AP_16; } /* b95: 0x9CD0 ya puso sub 2 -> 0x9C94 sub 0xC sin -+0x20 */
  else { fsInit[f] = 0; fs[f] = 0; vh[f] = 3; vk[f] = 110; if (koF[f] != 2) koF[f] = 1; vlast[f] = 180; soilNudge(f); } /* -> accion 0xB (tumbado 44 f, 0x8 34+0xB 44+0x5 16 medido) */
 }
 else if (hit && fs[f] == 1) { fs[f] = 3; fsInit[f] = 1; } /* b95: 0x9CD0 sub 2, +0x2C=8 -> 0x9F02 en el tick siguiente */
 q->z0 = fsZ[f] >> 8;
 return apPose[f][fsP[f]];
}
/* reaccion / derribo (codigo b66-b68 de Warrior, ahora para los dos) */
static u16 victimStep(u16 f){
 const u8 *sq = (const u8*)move_seq; u16 p = curPose; vk[f]++; z0 = ((fd[f^1].gs==12)&&(sx==2||bx==2))?128:187; /* b76: reacciones/suelo con z al suelo (0xAB1E/0xA90E) */
 if (vh[f] == 3 && (fd[f ^ 1].gs || (pnS && pnV == f)) && vDownIdx(vk[f]) == 2 && vDownIdx(vk[f] + 1) != 2) vk[f]--; /* b69: sigue tumbado mientras le golpean en el suelo */ pendBtn = 0; mv = 0; gs = 0;
 if (vjolt[f]) vjolt[f]--;
 if (vh[f] < 3) {
  const u16 o = (vh[f] == 1) ? 64 : 77, L = (vh[f] == 1) ? 13 : 41;
  if (vk[f] > 2) p = sq[o + ((vk[f] - 3 >= L) ? L - 1 : vk[f] - 3)];
  if (vk[f] >= L + 2) vh[f] = 0;
 } else {
  const u16 i = vDownIdx(vk[f]);
  if (!wrDown[i][1] || (koF[f] && (i >= 4 || (koF[f] == 2 && vk[f] >= 170)))) { vh[f] = 0; koF[f] = 0; } else p = wrDown[i][0]; /* b76: tras zafar/caida: 0xB -> 0x5 -> 0 (sin atontado) */
 }
 if (!vh[f]) { p = 0; vjolt[f] = 0; p1face = dFace = (vface[f] ? 0 : 1); if (p1face) p += MIRB; lastBase = 0xFFFF; tick = 1; afterPose = 0; mvh = 0; dFl = 0; }
 return p;
}
/* ===== b71: constantes arcade (sp_trk s-port: pin.h s41 / pin2.h s42 / gm62.h S0C) ===== */
#define PT_PIN 2731   /* Duggan cubre (494-499) */
#define PN_PIN 329
#define PT_PKO 3060   /* Duggan se quita (kick-out) */
#define PN_PKO 29
#define PT_RPIN 3089  /* arbitro: se tira y cuenta (500-506) */
#define PN_RPIN 329
#define PT_RUP 3418   /* arbitro se levanta (507-509) */
#define PN_RUP 30
#define PT_WPIN 3480  /* Warrior cubre (513-515) */
#define PN_WPIN 325
#define PT_WKO 3805
#define PN_WKO 25
#define PIN_C 28      /* frames de cubrir antes de la cuenta (Duggan); Warrior 24 */
#define WP_C 24
#define PIN_ZONE 24   /* B a menos de 24 px del cuerpo = cubrir; 24..100 = salto */
#define S0C_O 4425    /* b71: salto de Warrior sobre el rival tumbado (arcade 0x0C, MAME p77 c20) */
#define S0C_N 88
#define S0C_K 40
#define GH_SIGN (-1)
/* arcade BD10/BEF2: z asiento pin = 0xBB - dz (D↔W dz=13).
   Pista PT_PIN/PKO: q[3] = Z absoluto (s41/s42 z0=q[3]). WPIN/WKO: q[3]=flags <128 → fallback BEF2. */
#define ARC_BB 0xBB
#define BEF2_DZ_DW 13
static s16 pinZof(s16 q3){ return (q3 >= 128) ? q3 : (s16)(ARC_BB - BEF2_DZ_DW); }
#define DIG_T 1525    /* 10 tiles libres 1525..1534 (cifra grande 1-3) */
#define RO_T 1779     /* 10 tiles libres 1779..1788 (cifras 0-9 cuenta fuera) */
#define RO_TICK 64    /* arcade 0xDEE4/0xDA38: +1 cada 4 pasos x 8 ticks (2 f) = 64 f */
#define RESET_WAIT 120
#define RF_CFRONT 757  /* b72: arbitro contando fuera, de frente (arcade 0xA-0xD) */
#define RF_CBACK 761   /* de espaldas (arcade 0xE-0x11) */
static const s16 *spT(u16 i);
static void pinStart(u16 a, u16 v);
static s16 rsSy; static u16 roOut, roLd = 0xFFFF; static u16 pnK, pnEnd, pnWin, pnN[2], winK, rsS, rsK, roC, roT, roDone, digPin, digLd = 0xFFFF, resetReq; static s16 pnM, pnX, pnY, pnEx, pnEy, rsX0, rsY0, rfM, rfX;
/* arcade 0x9700 + 0x21324: d0==0 → paso 0 (larga, sc[]); d0!=0 → paso 2 (corta, ropeMapA/ropeDurA).
   b78 saltaba sc[] a 48 (fase 6↔7); eso no es el arranque arcade y apenas se lee como vibracion.
   b79: corta = pasos 2..7 con mapas 0x2146e y duraciones 0x213A4×2; fuerza rcur invalidado → ropeDraw. */
static void bounceRope(u16 goingR, u16 fall){
 u16 sd = goingR ? 1 : 0;
 if (fall) {
  /* 0x9700 siempre pone bit15 → 0x21324 reinicia aunque ya vibrara; 0x213B4 redibuja al cambiar */
  u16 f;
  rFall[sd] = 1; rStep[sd] = 2; rTimer[sd] = ropeDurA[2]; rk[sd] = 0;
  f = ropeShortMap[sd][ropePhaseA[2]];
  rcur[sd] = f; ropeDraw(sd);
 } else if (rk[sd] < 0) { rFall[sd] = 0; rk[sd] = 0; }
}
/* b73: arcade 0x1190C/0x11A72 = cubrir si rival tumbado DENTRO y atacante no fuera.
   0xACA4 empuja el cuerpo al caer (0x30/8). "Al lado" de cuerdas OK; "sobre" (= fuera de 0x21E5A) no.
   El arbitro se coloca donde cabe (refSideY); ya no bloquea el pin. */
static s16 ropeIn(s16 x, s16 y, s16 m){ const s16 e = (y > RING_Y0) ? ((u16)(y - RING_Y0)) / 6 : 0; return x >= RING_XL + e + m && x <= RING_XR - e - m && y >= RING_Y0 + 4 && y <= RING_Y1 - 4; }
static s16 ringClampX(s16 x, s16 y){ const s16 e = (y > RING_Y0) ? ((u16)(y - RING_Y0)) / 6 : 0; const s16 lo = RING_XL + e, hi = RING_XR - e; if (x < lo) x = lo; if (x > hi) x = hi; return x; }
static s16 refSideY(s16 y, s16 dy){ return (y + dy <= RING_Y1 - 4) ? dy : -dy; }  /* arbitro del pin: detras si cabe; si no, delante */
/* arcade 0xACA4: prueba +0x30 y -8 segun orientacion; el clamp de 0x21E5A deja el cuerpo dentro (no sobre la cuerda) */
static void soilNudge(u16 v){
 FC *q = &fd[v]; s16 d1 = 0x30, d2 = 8, x = q->ox, y = q->oy;
 if (q->sx == 2 || q->bx == 2) return; /* fuera: no */
 if (!oriVictima(v)) { d1 = -d1; d2 = -d2; } /* b95: bit7 de +0xA = oriVictima (vface^1, convencion b93); b94 usaba vface (lado contrario) */
 x = ringClampX(x + d1, y); x -= d1;          /* intento 0x30 (efecto si choca) */
 x = ringClampX(x - d2, y) + d2;              /* intento 8: empuja dentro si estaba en la cuerda */
 q->ox = x;
}
static u16 groundOK(u16 a, u16 v, s16 ax, s16 ay, u16 pin){
 const FC *q = &fd[v]; const s16 y = q->oy;
 /* arcade 0x1190C/0x11A72: rival tumbado DENTRO (+0x19==0) y atacante no fuera.
    Al lado de la cuerda (ox dentro de 0x21E5A) = OK. Sobre/fuera = no.
    No usar extents del sprite (lyo) para vetar: eso bloqueaba el pin junto a la cuerda. */
 (void)a; (void)pin;
 if (!ropeIn(ax, ay, 0)) return 0;           /* atacante fuera/sobre limite */
 if (q->sx == 2 || q->bx == 2) return 0;     /* rival fuera del ring */
 if (!ropeIn(q->ox, y, 0)) return 0;         /* rival ox sobre/fuera de cuerda */
 return 1;
}
/* b83 Grounded input = arcade 0xC798..0xC8A8 + 0xC928..0xC95A, CB3C Warrior.
   Port ox == arcade $c; vface == arcade bit7 de +0xA (fsStart lo copia asi).
   b82 invento X=ox±48 y b7=!vface: desde el torso lanzaba cuando el arcade no.
   Ancla = ox_rival + (bit7 ? +0x28 : -0x28). |dy|<0x18.
   Delante del ancla d<0x20 -> zona1 B=sub0C salto. Detras d<0x30 -> zona2 A=sub5 / B=sub6
   (pin solo si d4==0 y d<0x20, si no B=sub1). Probe MAME: ori00 B dx-64..-40 = 0C. */
static u16 w82PinOK;
static u16 warriorGroundZone(u16 o){
 const u16 b7 = oriVictima(o);
 const s16 X = fd[o].ox;
 s16 dy=oy-fd[o].oy, d1=X+(b7?0x28:-0x28)-ox; u16 d4=0;
 w82PinOK=0;
 if (!lyingNow(o)) return 0;
 if (dy<0){dy=-dy;d4=1;}
 if (dy>=0x18) return 0;
 if (d1>=0){ if(b7) goto behind; goto front; }
 d1=-d1; if(b7) goto front; goto behind;
front: return d1<0x20 ? 1 : 0;
behind: if (d1>=0x30) return 0; w82PinOK=(!d4 && d1<0x20); return 2;
}
static void warriorGroundStart(u16 kind,u16 o){
 gs=kind;gk=0;pendBtn=0;w81Phase=0;w81Time=(kind==12)?1:0;w81Var=(oy+2<fd[o].oy);
 kneeFloor90=(sx==2||bx==2)?128:187;
 if(kind==12 && kneeFloor90==128){
  if(kneeRawValid91 && (((s32)ox<<8)|oxf)==kneeClipX91 && oy==kneeRawY91){ox=kneeRawX91>>8;oxf=kneeRawX91&255;}
  FC q=fd[curF];q.ox=ox;q.oy=oy;kneeOutsideClamp91(&q,ox<768);ox=q.ox;oy=q.oy;
  kneeOutsideVictim91(o,oriVictima(o));dX[o]=fd[o].ox;dY[o]=fd[o].oy;
 }
 if(kind==12)kneeRawValid91=0;

 w81X=((s32)ox<<8)+oxf;w81Y=((s32)oy<<8)+oyf;w81Z=(s32)z0<<8;
 w81Vx=w81Vy=0;w81Vz=0x500;
 if(kind==12){
  /* 111D0/159AC: single-step solver, including origin height and fractions. */
  s32 z=w81Z;s16 vz=0x500;u16 n=0;
  do{z+=vz;vz-=0x50;if(vz<(s16)0xf800)vz=(s16)0xf800;n++;}while(vz>=0||(z>>8)>=kneeFloor90);
  s16 off=(kneeFloor90==128)?16:32;
  s32 dx=(s32)(fd[o].ox+(oriVictima(o)?off:-off)-ox)*256; /* 15A6C uses integer word */
  s32 dy=(s32)(fd[o].oy-oy)*256; /* 15AD8 uses integer word */
  w81Vx=dx/n;w81Vy=dy/n;
  if(w81Vx>0x2000)w81Vx=0x2000;if(w81Vx< -0x2000)w81Vx=-0x2000;
  if(w81Vy>0x2000)w81Vy=0x2000;if(w81Vy< -0x2000)w81Vy=-0x2000;
  if(kneePost90){
   /* 10B5E/110E4: far-post override relative to victim +/-64. */
   s16 tx=fd[o].ox+(oriVictima(o)?64:-64),dxp=tx-ox,dyp=fd[o].oy-oy;
   if(dxp>=96||dxp<=-96)w81Vx=(dxp<0)?-0x200:0x200;
   if(dyp>=80||dyp<=-80)w81Vy=(dyp<0)?-0x100:0x100;
  }
  p1face=(w81Vx<0); /* 10BB2: native bit7; MD world X is screen-positive. */
 }
 dFace=dFl=p1face;w81Draw=w81Pose[kind==13?6:0];gH=0;
}
static u16 warriorGroundEnd(void){
 gs=0;gH=0;z0=kneeFloor90;dFl=0;lastBase=0xFFFF;tick=1;afterPose=0;mvh=0;
 return p1face?MIRB:0;
}
static u16 warriorGroundStep(u16 o){
 gk++;pendBtn=0;
 if(gs==13){if(!(gk&1))return w81Draw;}else if(!arcTick)return w81Draw;
 if(gs==13){ /* 1173A: 159/8 ticks -> 15A/4 ticks. No jump, no pin Z. */
  ++w81Time;
  if(w81Time==8 && lyingNow(o)) {hurt90(o,1);vjolt[o]=10;vk[o]=14;vlast[o]=180;CA_TRIG();}
  if(w81Time>=12)return warriorGroundEnd();
  w81Draw=w81Pose[w81Time<8?6:7];return w81Draw;
 }
 if(w81Phase==0){ /* 10F54/10FB2: four ticks, not table112F0[0]+1 */
  w81Draw=w81Pose[0];if(++w81Time>=4){w81Phase=1;w81Time=0;}return w81Draw;
 }
 if(w81Phase==6){ /* missed dive -> action8 sub5, 9FCC / 27D2[19]. */
  if(!w81Time){p1face^=1;dFace=dFl=p1face;}
  w81Time++;w81Z+=2*(s32)w81Vz;w81Vz-=0x80;z0=w81Z>>8;
  w81Draw=w81Pose[w81Time<=9?11:12];
  if(z0<=kneeFloor90){
   warriorGroundEnd();
   static const u16 wait[4]={112,82,54,22};ground90[1]=wait[energy90[1]/12>3?3:energy90[1]/12];
   kvPhase90[1]=2;kvTime90[1]=0;vface[1]=!p1face;vh[1]=0;
   dFl=vface[1]^1;return 114;
  }
  return w81Draw;
 }
 if(w81Phase==5){ /* action 5: pose 1A, AA00[0] = 8 ticks */
  if(w81Time>=8)return warriorGroundEnd();w81Draw=w81Pose[10];++w81Time;return w81Draw;
 }
 if(w81Phase==4){
  ++w81Time;w81Draw=w81Pose[w81Var?5:(w81Time>=12?3:8)];
  if(w81Time>=12){w81Phase=5;w81Time=0;}return w81Draw;
 }
 w81X+=2*(s32)w81Vx;w81Y+=2*(s32)w81Vy;w81Z+=2*(s32)w81Vz;
 w81Vz-=0xA0;if(w81Vz<(s16)0xF800)w81Vz=(s16)0xF800;
 ox=w81X>>8;oxf=w81X&255;oy=w81Y>>8;oyf=w81Y&255;z0=w81Z>>8;
 if(w81Vz<0 && lyingNow(o) && ((fd[o].sx==2||fd[o].bx==2)?128:187)==kneeFloor90 && z0<=kneeFloor90+16){
  /* 10FCC: exact hit point/rectangle (11084 / 110A4, id0).
     Victim center x +/-48, asymmetric [-16,+48] or [-48,+16];
     point attacker x, y+4, victim y+8 +/-8. */
  const s16 vx=fd[o].ox, py=oy+4, vy=fd[o].oy;
  const s16 lo=vx+(oriVictima(o)?0:-64),hi=vx+(oriVictima(o)?64:0);
  if(ox>lo && ox<=hi && py>vy && py<=vy+16){
   /* 10D9E/10F04/1152A: ground BB, y=opponent-1+10;
      extra opposite-facing hands 7D at y-10,z+10 (baked only in art). */
   z0=kneeFloor90;w81Z=((s32)kneeFloor90<<8)|(w81Z&255);
   oy=vy+(w81Var?-1:9);w81Y=((s32)oy<<8)|(w81Y&255);oyf=w81Y&255;w81Phase=4;w81Time=1;
   hurt90(o,kneePost90?10:5);kneeVictimStart90(o);CA_TRIG();
   w81Draw=w81Pose[w81Var?5:8];return w81Draw;
  }
 }
 if(z0<=kneeFloor90){ /* 10C4A: missed dive -> 8/sub5, not a false pin. */
  hurt90(curF,2);z0=kneeFloor90;w81Z=((s32)kneeFloor90<<8)|(w81Z&255);
  ox+=(w81Vx>=0)?-24:24;w81X=((s32)ox<<8)|(w81X&255);oxf=w81X&255;
  w81Phase=6;w81Time=0;w81Vz=0x300;dFl=!p1face;
  w81Draw=w81Pose[11];return w81Draw;
 }
 /* 112F0: phase1 9 ticks, phase2 5 ticks, phase3 waits for contact. */
 w81Draw=w81Pose[w81Phase==1?1:(w81Phase==2?(w81Var?4:2):(w81Var?5:3))];
 if(++w81Time>(w81Phase==1?8:4) && w81Phase<3){w81Phase++;w81Time=0;}
 return w81Draw;
}
#include "duggan92.h"
/* 12E7A / 1302E: same subaction for both native banks. Motor 627..634. */
static u16 clStep87(u16 o){
 const u16 f=curF,R=rnd>0; pendBtn=0;dFl=!R;p1face=dFace=!R;
 if(!arcTick)return clInit[f]?clPose[f]:curPose;
 if(clInit[f]==2){rn=0;clInit[f]=0;lastBase=0xffff;tick=1;dFl=0;return p1face?MIRB:0;}
 if(!clInit[f]){clInit[f]=1;clStep[f]=0;clTimer[f]=6;clPose[f]=627;rnx=(s32)ox<<8|oxf;}
 rnk++;
 /* 12EB6 moves BEFORE latch and timer. 12F04 stops speed during hold. */
 if(rnW!=1){rnx+=rnd*(clStep[f]==0?0x6c0:0x400);ox=rnx>>8;oxf=rnx&255;}
 if(rnW==2){ /* 12EE8: latch next logic tick, pose 1D2+victim id. */
  rnW=1;clHeld[o]=2;clStep[f]=2;clTimer[f]=8;clPose[f]=curF?630:629;
  return clPose[f];
 }
 if(--clTimer[f]==0){
  clStep[f]++;
  if(clStep[f]>(rnW?5:3)){clInit[f]=2;return clPose[f];} /* exit tick keeps last drawing until next tick */
  static const u16 dur[6]={6,4,4,6,3,3};
  static const u16 pose[6]={627,628,631,632,633,634};
  clTimer[f]=dur[clStep[f]];clPose[f]=pose[clStep[f]];
  if(clStep[f]==3 && rnW==1){ /* 12FAA launches after the 8-tick catch, not on contact. */
   rnW=3;clFallStart(o,-rnd) /* 12F16/12F1C: rival faces opposite; 9BC6/27D2 reverse X */;clHeld[o]=0;
  }
 }
 /* 16634 is only broad-phase! 1672C->1890C attack box 18C2A
    (-20,12,48,16), mirrored to canonical MD right; idle defence
    18B02 (-8,16,0,80). 16C60/16CA8 inclusive overlap. */
 if(!rnW && (clStep[f]==1 || clStep[f]==2) && !clHeld[o] && hittable(o)){
  s16 dx=(fd[o].ox-ox)*rnd,dy=fd[o].oy-oy;
  if(dy<0)dy=-dy;
  if(dx>=(clStep[f]==1?0:-20) && dx<=(clStep[f]==1?28:24) && dy<8 && fd[o].z0+80>=z0+(clStep[f]==1?48:0) && fd[o].z0<=z0+(clStep[f]==1?64:72)){
   hurt90(o,clStep[f]==1?4:2);rnW=2;clHeld[o]=1;vdmg[o]+=(clStep[f]==1?4:2);vlast[o]=180;
   fd[o].mv=fd[o].rn=fd[o].gs=fd[o].pendBtn=0;
  }
 }
 /* Keep the original ring limits; only this move's body is replaced. */
 {s16 e=(oy-RING_Y0)/6,edge=R?RING_XR-e:RING_XL+e;
 if(R?ox>=edge:ox<=edge){ox=edge;rnx=(s32)ox<<8;rn=2;rnk=0;rnb++;clInit[f]=0;
 if(clHeld[o]){clHeld[o]=0;fsDir[o]=rnd;fsStart(o,2,!R);}bounceRope(R,0);}}
 return clPose[f];
}
static u16 engine(s16 hx, s16 hy, u16 ai){
  const u16 o = curF ^ 1;
  u16 np = curPose;
  if(!curF&&(gs==14||gs==15))return dugStep92(o);
  if(!curF&&!gs&&!mv&&!rn&&!climb&&(pendBtn&(BUTTON_A|BUTTON_B))!=0){
   u16 b=pendBtn&(BUTTON_A|BUTTON_B),zone=dugZone92(o);
   if(b==BUTTON_B&&zone==2&&!ai&&!pnS&&lyingNow(o)&&groundOK(curF,o,ox,oy,1)){pinStart(curF,o);pendBtn=0;return curPose;} /* b94: CB75 fila cuerpo K=06 cubrir */
   if((b==BUTTON_A&&zone==2)||(b==BUTTON_B&&zone==1)){
    if(!arcTick)return curPose;return dugStart92(b==BUTTON_A?14:15,o,0);
   }
  }
  if(curF && !gs && !mv && !rn && !climb && (pendBtn&(BUTTON_A|BUTTON_B))==BUTTON_B && warriorGroundZone(o)==1 &&
     ((sx==2||bx==2)==(fd[o].sx==2||fd[o].bx==2)) && arcTick){
   kneePost90=0;warriorGroundStart(12,o);return w81Draw;
  }
  if(rn==3)return clStep87(o);
  if (rn) {
   const u8 *sq = (const u8*)move_seq; const s16 *rp = (const s16*)run_pos; const u16 R = rnd > 0;
   const s16 e = ((u16)(oy - RING_Y0)) / 6, ropeX = R ? RING_XR - e : RING_XL + e;
   u16 done = 0; rnk++; p1face = 0;
   if (rn == 1) {
    if (rnk <= 3) rnT[curF] = 0; else if (arcTick) rnT[curF]++; /* b95: 0x94CE poses 0x95C4 x 2 ticks */
    if (arcTick) { /* b95: un paso por tick arcade (antes tick&1 = frame MD) */
     if ((pendBtn & (BUTTON_A | BUTTON_B)) == (BUTTON_A | BUTTON_B)) { /* keep running */ }
     else if (pendBtn & BUTTON_A) { rn = 3; rnk = 0; rnW = 0; clInit[curF]=0; rnx = (s32)ox << 8 | oxf; }
     else {
      s32 X = ((s32)ox << 8 | oxf) + rnd * ((s32)rnSpd[curF] << 6); ox = X >> 8; oxf = X & 0xFF;
      if (R ? ox >= ropeX : ox <= ropeX) {
       ox = ropeX; rnx = (s32)ox << 8 | oxf; rn = 2; rnk = 0; rnb++; bounceRope(R, 0); rnW = 0;
      } else if (hx == -rnd) { rn = 4; rnk = 0; rnx = (s32)ox << 8 | oxf; }
     }
     pendBtn = 0;
    }
    { const u16 f = rnk - 1; np = (rnk >= 1) ? sq[mvOffR[R ? 0 : 1] + ((f < 3) ? f : 3 + ((rnT[curF] >> 1) % 6) * 4)] : curPose; }
   } else if (rn == 2) {
    pendBtn = 0; const u16 i = (rnk > 47) ? 47 : rnk;
    { const s32 X = rnx + rp[rnPos[R ? 0 : 1] + i]; ox = X >> 8; oxf = X & 0xFF; }
    np = (rnk >= 1) ? sq[mvOffR[R ? 2 : 3] + ((rnk > 48) ? 47 : rnk - 1)] : curPose;
    if (rnk >= 48) { if (rnb >= 2) done = 1; else { rnd = -rnd; rn = 1; rnk = 0; } }
   } else {
    const u16 a = (rn == 3), L = a ? 40 : 20, i = (rnk > L) ? L : (rnk == L && !a) ? L - 1 : rnk;
    { const s32 X = rnx + rp[rnPos[(a ? 2 : 4) + !R] + i]; ox = X >> 8; oxf = X & 0xFF; } pendBtn = 0;
    if (a && (R ? ox >= ropeX : ox <= ropeX)) { ox = ropeX; rnx = (s32)ox << 8 | oxf; rn = 2; rnk = 0; rnb++; bounceRope(R, 0); }
    np = (rnk >= 1) ? sq[mvOffR[(a ? 4 : 6) + !R] + ((rnk - 1 >= L) ? L - 1 : rnk - 1)] : curPose;
    if (rn != 2 && rnk >= L) done = 1;
   }
   if (done) { rn = 0; lastBase = 0xFFFF; tick = 1; afterPose = 0; mvh = 0; }
  } else if (curF && (gs==12 || gs==13)) {
   np=warriorGroundStep(o);
  } else if (gs) { /* b69: golpe al rival tumbado (0x05 codazo / 0x11 salto), mismo codigo para los dos */
   const u16 N = (gs == 5) ? GS5_N : (gs == 12) ? S0C_N : GS11_N, K = (gs == 5) ? GS5_K : (gs == 12) ? S0C_K : GS11_K; gk++; pendBtn = 0;
   const u16 jj = (gk - 1 >= N) ? N - 1 : gk - 1;
   np = (gs == 5) ? gs5P[jj] : gs11P[jj]; dFl = p1face;
   if (gs == 11) { ox = gX0 + gM * (s16) (((s32) gD * gs11X[jj]) / 7); oxf = 0;
    z0 = (jj >= K) ? pinZof(0) : 187; }
   else if (gs == 5) { z0 = (jj >= K) ? pinZof(0) : 187; }
   if(jj==K && gk-1==K){
    const s16 bdx=bodyX(o)-ox,bdy=fd[o].oy-oy;
    if(lyingNow(o)&&bdx>=-48&&bdx<=48&&bdy>=-16&&bdy<=16){hurt90(o,gs==5?1:5);vjolt[o]=10;vk[o]=14;vlast[o]=180;CA_TRIG();}
    else if(gs==11)hurt90(curF,2); /* 10C6A; native sub11 ->10A5E */
   }
   if (gk >= N) { if (gs == 12) np = p1face ? MIRB : 0; gs = 0; gH = 0; z0 = 187; dFl = 0; lastBase = 0xFFFF; tick = 1; afterPose = 0; mvh = 0; }
  } else if(mv==1){
   /* FCFC samples edges only while +36==12, before FD04 consumes the timer. */
   if(mk>=10 && mk<=12)pAcc|=pendBtn;
   if(!arcTick)return curPose;
   pendBtn=0;
   if(pEnd[curF]){mv=0;pEnd[curF]=0;pAlt=pAcc=0;mk=0;dFl=0;lastBase=0xffff;tick=1;return p1face?MIRB:0;}
   mk++;
   const u8 *sq=(const u8*)move_seq;
   np=(mk>=3)?sq[(pAlt?10:0)+((mk-3<10)?mk-3:9)]:curPose;
   dFl=p1face;
   if(mk==10 && hittable(o)){
    s16 dx=(fd[o].ox-ox)*(p1face?-1:1),dy=fd[o].oy-oy;if(dy<0)dy=-dy;
    if(dx>=0 && dx<=MV_REACH_PUN && dy<=MV_REACH_Y){hurt90(o,1);vdmg[o]++;vlast[o]=180;vk[o]=0;vface[o]=ox>fd[o].ox;fd[o].mv=fd[o].pendBtn=0;
     if(vdmg[o]>=8){vh[o]=3;vdmg[o]=0;soilNudge(o);}else vh[o]=1;}
   }
   if(mk>=13){if(!ai && (pAcc&(BUTTON_A|BUTTON_B))==BUTTON_A){pAlt^=1;mk=2;pAcc=0;}else pEnd[curF]=1;}
  } else if (mv) { /* b66/b86: golpe; punch = FD70/FD7C, combo por pulsaciones (FC84) */
   const u8 *sq = (const u8*)move_seq;
   const u16 edge = pendBtn; /* +0x114 este frame (pendBtn ya es flanco) */
   mk++; pendBtn = 0;
   /* arcade FC84: con +0x36==0xB/0xC (ultima pose 0x152/0x155, mk 10..12) OR edge en +0x22 */
   if (mv == 1 && mk >= 10 && mk <= 12) pAcc |= edge;
   const u16 so = (mv == 1) ? (pAlt ? 10 : 0) : 33, L = (mv == 1) ? 10 : 31; /* FD70/FD7C: 4+3+3 */
   np = (mk > 2) ? sq[so + mk - 3] : curPose;
   if (np <= 4) { dFl = 0; if (p1face) np += MIRB; } else dFl = p1face;
   if (mk == ((mv == 1) ? MV_HIT_PUN : MV_HIT_KIK) && hittable(o)) {
    s16 dx = fd[o].ox - ox, dy = fd[o].oy - oy; const u16 front = p1face ? (dx <= 0) : (dx >= 0);
    if (dx < 0) dx = -dx; if (dy < 0) dy = -dy;
    if (front && dx <= ((mv == 1) ? MV_REACH_PUN : MV_REACH_KIK) && dy <= MV_REACH_Y) {
     hurt90(o,(mv==1)?1:(4+((fd[o].rn==1||tr[o])?2:0)));vdmg[o] += (mv == 1) ? 1 : 4; vlast[o] = 180; vk[o] = 0; vface[o] = (ox > fd[o].ox);
     fd[o].mv = 0; fd[o].pendBtn = 0;
     if (vdmg[o] >= 8) { vh[o] = 3; vdmg[o] = 0; soilNudge(o); } else vh[o] = mv;
    }
   }
   if (mk >= L + 2) {
    /* arcade FD2E: +0x22&3 == 1 (solo boton 1 recien pulsado en ventana) → eori +0xC0 bit0 y repite */
    if (mv == 1 && !ai && (pAcc & (BUTTON_A | BUTTON_B)) == BUTTON_A) {
     pAlt ^= 1; mk = 2; pAcc = 0; /* $8=1 del arcade → carga la 1ª pose del otro half al siguiente frame */
    } else { mv = 0; pAlt = 0; pAcc = 0; dFl = 0; lastBase = 0xFFFF; tick = 1; afterPose = 0; mvh = 0; }
   }
  } else if (bx == 1 || bx == 3) {
   const u16 N = (bx == 1) ? BX_NX : BX_NE; bxk++;
   const s16 *q = (const s16*)bx_seq + 4 * (((bx == 1) ? 0 : BX_NX) + bxk - 1);
   ox = bxX0 + q[1]; oy = bxY0 + q[2]; z0 = q[3]; oxf = oyf = 0; np = q[0]; pendBtn = 0;
   if (bxk >= N) {
    if (bx == 1) { bx = 2; z0 = 128; } else { bx = 0; z0 = 187; }
    tick = 0; afterPose = 0; mvh = (hx || hy) ? 0xFFFF : 0; lastBase = 0xFFFF; pushC = 0;
   }
  } else if (sx == 1 || sx == 3) {
   const u16 N = (sx == 1) ? SX_NX : SX_NE; sxk++;
   const s16 *q = (const s16*)sx_seq + 4 * ((sxR ? 0 : 116) + ((sx == 1) ? 0 : 62) + sxk - 1);
   ox = sxX0 + q[1]; oy = sxY0 + q[2]; z0 = q[3]; oxf = oyf = 0; np = q[0]; pendBtn = 0;
   if (sxk >= N) {
    if (sx == 1) { sx = 2; outK = sxk; z0 = 128; } else { sx = 0; z0 = 187; }
    tick = 0; afterPose = 0; mvh = (hx || hy) ? 0xFFFF : 0; lastBase = 0xFFFF; sxLim = 0; pushC = 0;
   }
  } else if (climb) {
   if(!curF&&ck>=cPOST[climb-1]&&ck<cD0[climb-1]&&dugLying92(o)&&pendBtn&&arcTick){
    /* F6EF=2F: either Punch or Kick while victim is prone. */
    climb=0;dreq=0;return dugStart92(15,o,1);
   }
   if(curF && ck>=cPOST[climb-1] && ck<cD0[climb-1] && lyingNow(o) && pendBtn && arcTick){
    /* F35A/F636/F6E6: P or K ->sub2C; no head-zone requirement. */
    kneePost90=1;climb=0;dreq=0;warriorGroundStart(12,o);return w81Draw;
   }
   { const u16 sd = climb - 1;
     if (!dreq && ck < cD0[sd] && ((climb >= 3) ? (hy > 0) : (hy < 0))) {
      dreq = ck + DREQ_LAG; if (dreq < cPOST[sd] + 2) dreq = cPOST[sd] + 2; } }
   ck++;
   if(!(ck>=cPOST[climb-1] && ck<cD0[climb-1] && (curF?lyingNow(o):dugLying92(o))))pendBtn=0;
   if (dreq && ck == dreq) { ck = cD0[climb - 1]; dreq = 0; }
   { const CK *t = (climb == 1) ? climbL : (climb == 2) ? climbR : (climb == 3) ? climbB : climbE;
     for (; t->k >= 0; t++) if (t->k == ck) { ox = t->x; oy = t->y; z0 = t->z; oxf = oyf = 0; } }
   { const s16 lk = cEND[climb - 1] - 2;
     if (ck == lk) oyf = (climb == 3) ? 0xC0 : 0x40;
     if ((hx || hy) && ((climb >= 3) ? (ck == lk || ck == lk + 2) : (ck == lk + 2))) walkStep(hx, hy); }
   np = ((const u8*)climb_pose)[(climb - 1) * CLIMB_LEN + ck - 1];
   if (ck >= cEND[climb - 1]) { dreq = 0; tick = 1; afterPose = np; climb = 0; mvh = 0; }
  } else {
   if(curF && (bx==2||sx==2) && (pendBtn&(BUTTON_A|BUTTON_B))==BUTTON_B && warriorGroundZone(o)==1 && (fd[o].sx==2||fd[o].bx==2)){
    if(!arcTick)return curPose;kneePost90=0;warriorGroundStart(12,o);return w81Draw;
   }
   if (bx == 2 || sx == 2) {
    pendBtn = 0; if (outK < 255) outK++;
    const s16 tw = (ox > 768) ? -1 : 1;
    if (bx == 2 && oy == BX_YO1 && hy > 0 && ox >= BX_XL && ox <= BX_XR && (tick & 1)) {
     bx = 3; bxk = 0; bxX0 = ox; bxY0 = oy;
    } else if (sx == 2 && sxLim && hx == tw && !(tick & 1)) {
     sxR = (tw < 0); sx = 3; sxk = 0; sxX0 = ox; sxY0 = oy; sxLim = 0;
    } else if (tick & 1) {
     const s32 sp = (hx && hy) ? 0x240 : 0x2C0;
     s32 X = ((s32)ox << 8 | oxf) + hx * sp, Y = ((s32)oy << 8 | oyf) + hy * sp;
     const s32 rawX91=X,rawY91=Y;
     if (Y < ((s32)BX_YO0 << 8)) Y = (s32)BX_YO0 << 8;
     if (Y > ((s32)SX_YOUT << 8)) Y = (s32)SX_YOUT << 8;
     { const s16 yy = Y >> 8, oL = (yy > RING_Y1) ? 504 + (yy - 293) / 6 : SX_OUTL, oR = (yy > RING_Y1) ? 1024 - (yy - 293) / 6 : SX_OUTR;
       if (X < ((s32)oL << 8)) X = (s32)oL << 8;
       if (X > ((s32)oR << 8)) X = (s32)oR << 8; }
     if (Y > ((s32)BX_YO1 << 8) + 0xFF) {
      const s16 e = ((Y >> 8) - RING_Y0) / 6, inR = RING_XR - e + 66, inL = RING_XL + e - 74;
      const s16 x = X >> 8;
      if (x > inL && x < inR) {
       if (oy <= BX_YO1) Y = ((s32)BX_YO1 << 8);
       else if (ox > 768) X = (s32)inR << 8; else X = (s32)inL << 8;
       if ((Y >> 8) > BX_YO1) {
        const s16 e2 = ((Y >> 8) - RING_Y0) / 6, iR = RING_XR - e2 + 66, iL = RING_XL + e2 - 74;
        if (ox > 768) { if ((X >> 8) < iR) X = (s32)iR << 8; } else { if ((X >> 8) > iL) X = (s32)iL << 8; }
       }
      }
     }
     if(curF){
      if(X!=rawX91 && Y==rawY91){kneeRawX91=rawX91;kneeClipX91=X;kneeRawY91=Y>>8;kneeRawValid91=1;}
      else if(X!=kneeClipX91 || (Y>>8)!=kneeRawY91)kneeRawValid91=0;
     }
     ox = X >> 8; oxf = X & 0xFF; oy = Y >> 8; oyf = Y & 0xFF;
     if (oy <= BX_YO1) { if (sx == 2) { sx = 0; bx = 2; } }
     else if (bx == 2) { bx = 0; sx = 2; outK = 255; }
     if (sx == 2) {
      sxR = (ox > 768);
      const s16 e = (oy - RING_Y0) / 6, lim = sxR ? RING_XR - e + 66 : RING_XL + e - 74;
      sxLim = (hx == tw && ox == lim && oy >= SX_YIN0 && oy <= SX_YIN1);
     } else sxLim = 0;
    }
   } else if ((tick & 1) && (pendBtn & (BUTTON_A | BUTTON_B)) == (BUTTON_A | BUTTON_B)) {
    rn = 1; rnk = 0; rnb = 0; rnW = 0; pendBtn = 0;
    rnd = hx ? hx : (p1face ? -1 : 1);
    if (hx || hy) walkStep(hx, hy);
   } else if ((tick & 1) && pendBtn && !bx && !sx) { /* b66: A = punetazo, B = patada; se orienta hacia Warrior si esta a tiro */
    const u16 btA = (pendBtn & BUTTON_A) != 0;
    if(curF){
     const u16 zone=warriorGroundZone(o);
     if(!ai && !btA && zone==2 && w82PinOK && !pnS && groundOK(curF,o,ox,oy,1)){
      pinStart(curF,o);pendBtn=0;return curPose;
     }
     if((btA && zone==2) || (!btA && zone==1 && !(fd[o].sx==2||fd[o].bx==2))){
      if(!btA && !arcTick)return curPose;kneePost90=0;warriorGroundStart(btA?13:12,o);
     }
    } else {
    { /* b94: el pin de Duggan entra por la zona cuerpo C706/CB75 (dugZone92==2, B) al principio de engine(). */
      /* b92: Duggan ground attacks use C706 zones above, not the old gs5/gs11 aliases. */ }
    }
    if (!gs) {
    mv = btA ? 1 : 2; mk = 0; if (btA) { pAlt = 0; pAcc = 0; pEnd[curF]=0; } pendBtn = 0;
    { s16 dx = fd[o].ox - ox, dy = fd[o].oy - oy; if (dy < 0) dy = -dy;
      if (dy <= 24 && dx >= -64 && dx <= 64 && dx) p1face = dFace = (dx < 0); } }
   } else if (tick & 1) {
    const s32 sp = (hx && hy) ? 0x240 : 0x2C0;
    s32 X = ((s32)ox << 8 | oxf) + hx * sp, Y = ((s32)oy << 8 | oyf) + hy * sp;
     const s32 rawX91=X,rawY91=Y;
    if (Y < ((s32)RING_Y0 << 8)) Y = (s32)RING_Y0 << 8;
    if (Y > ((s32)RING_Y1 << 8)) Y = (s32)RING_Y1 << 8;
    { const s16 e = ((u16)((Y >> 8) - RING_Y0)) / 6;
      if (X < ((s32)(RING_XL + e) << 8)) X = (s32)(RING_XL + e) << 8;
      if (X > ((s32)(RING_XR - e) << 8)) X = (s32)(RING_XR - e) << 8; }
    ox = X >> 8; oxf = X & 0xFF; oy = Y >> 8; oyf = Y & 0xFF;
    if (ai) { }
    else if (oy == RING_Y1 && hy > 0 && (ox <= CLIMB_XL || ox >= CLIMB_XR)) { climb = (ox <= CLIMB_XL) ? 1 : 2; ck = 0; dreq = 0; }
    else if (oy == RING_Y0 && hy < 0 && (ox <= CLIMB_XB || ox >= CLIMB_XE)) { climb = (ox <= CLIMB_XB) ? 3 : 4; ck = 0; dreq = 0; }
    else if (oy == RING_Y0 && hy < 0 && !hx && ox >= BX_XL && ox <= BX_XR && !rn) { bx = 1; bxk = 0; bxX0 = ox; bxY0 = oy; pushC = 0; }
   }
   if (sx == 0 && !bx && !climb && !rn && !ai) {
    if (hx && !hy && hx == pushD) { if (pushC < 0xFFFF) pushC++; } else { pushD = hy ? 0 : hx; pushC = (hx && !hy) ? 1 : 0; }
    const s16 e = ((u16)(oy - RING_Y0)) / 6;
    if (pushC >= SX_HOLD && oy >= SX_YMIN && oy < RING_Y1 && ox == ((hx > 0) ? RING_XR - e : RING_XL + e)) {
     sx = 1; sxk = 0; sxR = (hx > 0); sxX0 = ox; sxY0 = oy; pushC = 0;
    }
   }
   mvh = (mvh << 1) | (hx || hy);
   moving = (mvh >> PDLY) & 1;
   np = moving ? 1 + (walkPh >> 3) : (afterPose ? afterPose : 0);
   if (moving) { walkPh = (walkPh + 1) & 31; afterPose = 0; }
   /* facing: desde hx al caminar (solo); sin oponente */
   { u16 face = dFace;
     if (np <= 4) {
      if (hx && !mv) face = (hx < 0);
      else if (ai && !hx && fd[o].ox != ox) face = (fd[o].ox < ox);   /* b69: el que no controlas mira al rival (como Warrior b68) */
      dFace = face;
      if (np != lastBase) lastBase = np;
      if (face) np += MIRB;
      p1face = face;
     } else lastBase = 0xFFFF;
   }
   if(curF && (gs==12 || gs==13)) np=w81Draw;
   else if (climb || rn || mv || gs || sx == 1 || sx == 3 || bx == 1 || bx == 3) np = curPose;
  }
  return np;
}

/* ===== b70: agarre (lock-up arcade) ===== */
static s16 lkS; static u16 lkPush, lkC1, lkC2, lkBlk, lkL1;
static u16 trk[2], trO[2], trN[2], trPose[2], rwPh[2], rwLoop[2], rwLast[2]; static s16 trX0[2], trY0[2], trM, rwOff[2];
static const s16 *spT(u16 i){ return (const s16*)sp_trk + i * 4; }
static s16 ropeAt(u16 R, s16 y){ const s16 e = (y - RING_Y0) / 6; return R ? RING_XR - e : RING_XL + e; }
static u16 grFree(u16 f){ const FC *q = &fd[f]; return !vh[f] && !tr[f] && !fs[f] && !q->sx && !q->bx && !q->climb && !q->rn && !q->gs && !q->mv; }
static void grTry(void){
 if (pnS) return;
 if (gr || grCool) { if (grCool) grCool--; return; }
 if (!grFree(0) || !grFree(1) || !(fd[0].tick & 1)) return;
 if (!fd[0].moving && !fd[1].moving) return;
 const s16 dx = fd[0].ox - fd[1].ox, dy = fd[0].oy - fd[1].oy;
 if (dx <= -32 || dx >= 32 || dy <= -16 || dy >= 16) return;
 lkS = (fd[0].ox < fd[1].ox) ? 1 : -1;
 const s16 mx = (fd[0].ox + fd[1].ox) >> 1, my = (fd[0].oy + fd[1].oy) >> 1;
 for (u16 f = 0; f < 2; f++) { fd[f].ox = mx; fd[f].oy = my; fd[f].oxf = fd[f].oyf = 0; fd[f].pendBtn = 0; fd[f].z0 = 187; } /* b76: forcejeo 0xB1D0 de pie, z = 0xBB */
 gr = 1; grk = 0; lkPush = 8; lkC1 = lkC2 = 0; lkBlk = 0; lkL1 = 0;
}
static void trStart(u16 win){
 /* S_1E: Duggan lanza (0,25) a Warrior (25,237); W1E: Warrior lanza (2248,25) a Duggan (2007,241) */
 if (win == 0) { trO[0] = 0; trN[0] = 25; trO[1] = 25; trN[1] = 237; } else { trO[0] = 2007; trN[0] = 241; trO[1] = 2248; trN[1] = 25; }
 trM = lkS;
 for (u16 f = 0; f < 2; f++) { tr[f] = 1; trk[f] = 2; trX0[f] = fd[f].ox; trY0[f] = fd[f].oy; trPose[f] = fd[f].curPose; rwPh[f] = 0; rwOff[f] = 0; rwLoop[f] = 0; rwLast[f] = 0; }
 gr = 0;
}
/* lockup: devuelve 1 si sigue */
static void grStep(u16 btnCtl){
 const u8 *sq = (const u8*)move_seq; grk++;
 if (btnCtl && !lkBlk) lkL1 = 1;
 if (grk > 2 && (grk & 1)) {
  if (lkPush) lkPush--;
  else if (!lkBlk) { lkC1++;
   if (lkL1 && lkC1 >= 17) { trStart(ctl); return; }
   if (!lkL1 && lkC1 >= 16) { lkBlk = 1; lkPush = 8; lkC1 = lkC2 = 0; } }
  else { lkC2++; if (lkC2 >= 32) { trStart(ctl ^ 1); return; } }
 }
 const u16 t = (grk < 3) ? 0 : 3 + (grk - 3) % 222;
 for (u16 f = 0; f < 2; f++) { trPose[f] = (t < 1) ? fd[f].curPose : sq[(f ? 343 : 118) + t - 1]; }
}
/* recorrido de la victima con contacto real con las cuerdas (rwInit/rwX s-port) */
static u16 trR1(u16 f){ return (trM * spT(trO[f] + 50)[1] > 0); }
static u16 trReached(u16 R, s16 x, s16 y){ return R ? x >= ropeAt(1, y) : x <= ropeAt(0, y); }
static u16 trCF(u16 f, u16 from){ /* primer frame con accion 2 (contacto cuerda) desde 'from' tras un tramo sin 2 */
 u16 i = from; while (i < trN[f] && spT(trO[f] + i)[3] == 2) i++;
 while (i < trN[f] && spT(trO[f] + i)[3] != 2) i++; return i; }
static u16 trStep(u16 f){
 trk[f]++; const u16 n = trN[f];
 FC *c = &fd[f];
 u16 j = (trk[f] - 2 >= n) ? n - 1 : trk[f] - 2;
 const s16 *q = spT(trO[f] + j);
 if (trN[f] > 100 && (rwPh[f] == 0 || rwPh[f] == 2)) { /* victima: carrera hasta la cuerda real (rwInit/rwX s-port) */
  const u16 R = rwPh[f] ? !trR1(f) : trR1(f);
  const u16 cf = trCF(f, rwPh[f] ? rwLast[f] : 0);
  const s16 y = trY0[f] + q[2];
  if (cf < n && j <= cf) {
   if (trReached(R, trX0[f] + trM * q[1] + rwOff[f], y) && j < cf) { const s16 *qc = spT(trO[f] + cf); rwOff[f] = (trX0[f] + trM * q[1] + rwOff[f]) - (trX0[f] + trM * qc[1]); j = cf; trk[f] = cf + 2; q = qc; }
   else if (j == cf && !trReached(R, trX0[f] + trM * q[1] + rwOff[f], y) && rwLoop[f] < 30) { const s16 *qb = spT(trO[f] + j - 12); rwOff[f] += trM * (q[1] - qb[1]); j -= 12; trk[f] = j + 2; q = qb; rwLoop[f]++; }
   if (j == cf) { const s16 rp = ropeAt(R, y); rwOff[f] += rp - (trX0[f] + trM * q[1] + rwOff[f]); bounceRope(R, 0); rwPh[f]++; rwLast[f] = cf; }
  }
 } else if (rwPh[f] == 1 && trN[f] > 100 && q[3] != 2 && j > rwLast[f]) rwPh[f] = 2;
 if (trN[f] < 100 && q[3] == 12) { /* b76: 0xF94C accion 0xC dentro + contacto cuerda (+0x9E&3) -> 0xF9B0 */
  const u16 v = f ^ 1; const u16 jv = (trk[v] - 2 >= trN[v]) ? trN[v] - 1 : trk[v] - 2;
  if (spT(trO[v] + jv)[3] != 16 && fsRope(c->ox, c->oy)) { /* rival ya no en 0x10 -> accion 8 sub 1 (sub 0x1E no esta en la lista 1B/21/22/07/29/28) */
   bounceRope(c->ox > 768, 1); tr[f] = 0; /* 0xF9B0 marcar_cuerda d0=1 → vibrar paso 2 */ grCool = 40; c->curPose = 0; c->lastBase = 0xFFFF; c->afterPose = 0; c->mvh = 0; c->moving = 0;
   fsStart(f, 2, trM * spT(trO[v] + 20)[1] > 0); return 0xFFFF; } }   /* bit7 = mira a la dcha = hacia donde sale el lanzado */
 c->oy = trY0[f] + q[2];
 { s16 nx = trX0[f] + trM * q[1] + rwOff[f]; const s16 lo = ropeAt(0, c->oy), hi = ropeAt(1, c->oy); if (nx < lo) nx = lo; if (nx > hi) nx = hi; c->ox = nx; }
 c->z0 = 187; c->oxf = c->oyf = 0;
 { const u16 j0 = (j >= 2) ? j - 2 : 0; trPose[f] = (trk[f] > 3) ? (u16)spT(trO[f] + j0)[0] : c->curPose; }
 if (trk[f] - 2 >= n + 2) { tr[f] = 0; grCool = 40;
  c->curPose = 0; c->lastBase = 0xFFFF; c->afterPose = 0; c->mvh = 0; c->moving = 0; c->mv = 0; c->mk = 0; c->dFl = 0; c->pendBtn = 0;
  c->dFace = (fd[f ^ 1].ox < c->ox); c->p1face = c->dFace; return 0xFFFF; }
 return trPose[f];
}
/* ===== b71: PIN (arcade 0x06/0x17, s41/s42) + arbitro cuenta + cuenta fuera 20 + reset ===== */
static u16 pnOff;
static s16 pnVX, pnKD; /* origen visible del cubierto y signo X arcade convertido */
#define WP_BODY 778
#define WP_BODY_N 2
/* B012 no coloca al que cubre hasta B0AC (2.a pose). 8+4 ticks = 24 f.
   Actualizacion comun ANTES de ambos actores: no depende de ctl ni del orden. */
static void pinAdvance(void){
 if (!pnS) return;
 pnK++;
 if (pnS == 1 && pnK >= pnEnd) {
  if (pnWin) { pnS = 3; winK = 0; }
  else { pnS = 2; pnK = 0; rsS = 2; rsK = 0; rsX0 = rfx; rsY0 = rfy; }
 } else if (pnS == 2 && pnK >= 24) {
  const u16 v = pnV, a = pnA;
  FC *q = &fd[v]; q->ox = pnVX + pnKD * 8; q->oxf = q->oyf = 0; q->z0 = 187;
  vk[v] = 154; koF[v] = 2;
  fsDir[a] = pnKD; fsStart(a, 1, !vface[v]);
  fd[a].lastBase = 0xFFFF; fd[a].tick = 1; fd[a].afterPose = fd[a].mvh = fd[a].moving = fd[a].pendBtn = 0;
  pnS = 0;
 }
}
static void pinStart(u16 a, u16 v){
 const u16 fl = vface[v] ^ 1;
 pnM = fl ? 1 : -1;              /* b94: arcade BD10/11A72: neg.w d1 si bit7 de +0xA del rival = 0 (fl = oriVictima) */
 rfM = -pnM;                     /* arbitro/levantarse: coreografia b71-b77 sin cambios respecto a la pareja */
 /* b94: pistas s41/s62 son relativas al x arcade del rival: PIN dx 0->36 (BEF2[3][0], Y-1, Z 174),
    WPIN dx 55->32 (BEF2[0][3], Y+1). Origen = ox del tumbado (ya sin lyo). B012/B0A0: zafarse +-8 / +-0x28 por bit7. */
 pnA = a; pnV = v; pnX = fd[v].ox; pnY = fd[v].oy; pnVX = fd[v].ox; pnKD = pnM;
 rfX = fd[v].ox + (fl ? 64 : -64); /* arbitro: mismo sitio respecto al cuerpo visible que b77 (antes pnX=ox-lyo, cuerpo en ox+lyo) */
 const u16 T = a ? PT_WPIN : PT_PIN, C = a ? WP_C : PIN_C;
 pnEx = ox - (pnX + pnM * spT(T)[1]); pnEy = oy - (pnY + spT(T)[2]);
 pnS = 1; pnK = 0; pnOff = PIN_C - C; if (pnN[v] < 9) pnN[v]++;
 if (pnN[v] == 1) { pnWin = 0; pnEnd = a ? WP_C + 136 : PIN_C + 128; }   /* 1.er pin: se libra solo tras el "1" (arcade +128/+136) */
 else { pnWin = 1; pnEnd = PIN_C + 296 - pnOff; }                      /* siguientes: cuenta de 3 */
 rsSy = 73; /* b76: arcade 0xDD4E no se pone delante: va hacia la pareja y 0x21E5A lo deja dentro (antes refSideY lo mandaba fuera, tras la cuerda frontal) */ rsS = 1; rsK = pnOff; rsX0 = rfx; rsY0 = rfy; digPin = 0; roC = roT = 0;
 mv = 0; rn = 0; gs = 0; pendBtn = 0; p1face = dFace = (rfM < 0); oxf = oyf = 0;
}
static u16 pinStepA(void){   /* atacante durante el pin (contexto cargado); devuelve pose directa */
 const u16 a = pnA, T = a ? PT_WPIN : PT_PIN, N = a ? PN_WPIN : PN_PIN, C = a ? WP_C : PIN_C;
 const s16 *q; u16 j;
 if (pnS == 2) {
  if (pnK >= 16) { /* B0AC: a3 pose9B solo durante A0 (4 ticks), no durante 9F */
   ox = pnVX + pnKD * (8 + 0x28); oy = pnY - 1; z0 = 187 + 4; oxf = oyf = 0;
   return apPose[a][AP_9B];
  }
  /* 9F: el que cubre todavia conserva su pin. */
  q = spT(T + N - 1); ox = pnX + pnM * q[1]; oy = pnY + q[2];
  z0 = a ? 203 : pinZof(q[3]);
  return a ? WP_BODY : (u16)q[0];
 }
 j = (pnK > N - 1) ? N - 1 : pnK; q = spT(T + j);
 ox = pnX + pnM * q[1] + ((pnK < C) ? pnEx * (s16)(C - pnK) / (s16)C : 0);
 oy = pnY + q[2] + ((pnK < C) ? pnEy * (s16)(C - pnK) / (s16)C : 0); z0 = pinZof(q[3]); /* b75: s41/s42 z0=q[3]; WPIN → 0xBB-dz */
 if (pnS == 3) { if (++winK >= RESET_WAIT) resetReq = 1; }
 /* Warrior: BEF2[0][3] dx=32 dz=16, BE04 y=v+1, BE7C Z=BB+16.
    WPIN historica trae ese Z YA plegado en sus pixeles. No volver a restar
    13 como b75/b76. Para el asiento usamos 7F y 80 originales, dos capas. */
 if (a && pnK >= C + 2) { z0 = 203; return WP_BODY; }
 if (a) z0 = 187; /* pista de aproximacion con Z plegado */
 return (u16)spT(T + ((j > 2) ? j - 2 : 0))[0];
}

static void refPinStep(void){
 const s16 *q; u16 j; rsK++;
 if (rsS == 1) {
  j = (rsK > PN_RPIN - 1) ? PN_RPIN - 1 : rsK; q = spT(PT_RPIN + j);
  s16 tx = rfX + rfM * q[1], ty = pnY + ((rsSy < 0) ? -q[2] : q[2]);
  if (rsK < PIN_C) { const s16 *q0 = spT(PT_RPIN); const s16 x0 = rfX + rfM * q0[1], y0 = pnY + ((rsSy < 0) ? -q0[2] : q0[2]);
   tx += (rsX0 - x0) * (s16)(PIN_C - rsK) / PIN_C; ty += (rsY0 - y0) * (s16)(PIN_C - rsK) / PIN_C;
   rfFl = ((rfX + rfM * spT(PT_RPIN + PIN_C)[1]) < rsX0); }
  else rfFl = (rfM < 0);
  rfx = tx; rfy = ty; rfClamp(0x7FFF); rfPose = (u16)spT(PT_RPIN + ((j > 2) ? j - 2 : 0))[0]; /* b76: 0xDECC jsr 0x21E5A */
 } else {
  j = (rsK > PN_RUP - 1) ? PN_RUP - 1 : rsK; q = spT(PT_RUP + j);
  rfx = rsX0 + rfM * q[1]; rfy = rsY0 + ((rsSy < 0) ? -q[2] : q[2]); rfFl = (rfM < 0); rfClamp(0x7FFF); rfPose = (u16)spT(PT_RUP + ((j > 2) ? j - 2 : 0))[0];
  if (rsK >= PN_RUP) { rsS = 0; rfPose = RF_IDLE; rfFl = 0; }
 }
}
static void countStep(void){
 /* cifra del pin: arcade 0x17 +94/+194/+294 */
 digPin = 0;
 if (pnS == 1 || pnS == 3) { const u16 pc = pnK + pnOff; digPin = (pc >= PIN_C + 294) ? 3 : (pc >= PIN_C + 194) ? 2 : (pc >= PIN_C + 94) ? 1 : 0; }
 /* cuenta fuera del ring (arcade estado 3, 0xDEE4): hasta 20, se borra si vuelven los dos */
 if (roDone) { if (++roDone > RESET_WAIT) resetReq = 1; return; }
 const u16 out = !pnS && (fd[0].sx == 2 || fd[0].bx == 2 || fd[1].sx == 2 || fd[1].bx == 2);
 roOut = out;
 if (!out) { roC = 0; roT = 0; return; }
 if (++roT >= RO_TICK) { roT = 0; if (++roC >= 20) roDone = 1; }
}
static void fighterInit(u16 f){
 if(f)kneeRawValid91=0;
 if(!f){dugPhase92=dugTime92=dugVictimPending92=0;}
 energy90[f]=48;ground90[f]=groundSeen90[f]=kvPhase90[f]=kvTime90[f]=0;
 ox = f ? 660 : 736; oy = f ? 262 : 288; oxf = oyf = 0; z0 = 187; curPose = 0; walkPh = 0; p1face = dFace = 0; lastBase = 0xFFFF;
 climb = ck = afterPose = dreq = 0; sx = sxk = sxR = 0; outK = 0; pushC = sxLim = 0; pushD = 0; bx = bxk = 0; bxX0 = bxY0 = 0; sxX0 = sxY0 = 0; rn = rnk = rnb = rnW = 0; rnd = 0; rnx = 0;
 mvh = moving = tick = pendBtn = mv = mk = dFl = pAlt = pAcc = 0; gs = gk = 0; gX0 = gY0 = gM = gD = gH = 0;
 vh[f] = vk[f] = vdmg[f] = vlast[f] = vface[f] = vjolt[f] = 0; tr[f] = 0; pnN[f] = 0; fs[f] = 0; koF[f] = 0;
 ctxSave(f);
}
static void matchReset(void){   /* b71: reinicia el combate (estado de salida, sin reiniciar la consola) */
 for (u16 f = 0; f < 2; f++){fighterInit(f);clInit[f]=clHeld[f]=pEnd[f]=0;}
 gr = 0; grk = 0; grCool = 0; pnS = 0; pnK = 0; rsS = 0; winK = 0; roC = roT = roDone = 0; roOut = 0; roLd = 0xFFFF; digPin = 0; resetReq = 0;
 rfx = RF_HOME_X; rfy = RF_HOME_Y; rfPose = RF_IDLE; rfFl = 0; rfPh = 0; rfMoving = 0;
 /* camara: no se salta; vuelve con su paso normal (un salto grande de mapa congela ~30 f) */
}
static void fLoad(u16 f){
 const u16 np = dPose[f]; if (np == dLoaded[f]) return;
 const Pose *P = &poseTab[np]; if (!P->n || P->nt > dMax[f]) return;
 VDP_loadTileData((const u32*)(spr_tiles + (u32)P->t0 * 32), dSlot[f], P->nt, DMA);
 dLoaded[f] = np;
}
/* b83: dos capas. 778 pin BE96 (misma ori, y-2). 787/788 impacto 1152A: 7D ori opuesta, x±4
   (bit7 clear:-4 / set:+4), y-10/z+10 (screen Y se cancela; sort usa y-10). */
static u16 layN(u16 p){ return p == WP_BODY ? WP_BODY_N : p == w81Pose[8] ? w82AuxN[0] : p == w81Pose[9] ? w82AuxN[1] : 0; }
static s16 layDy(u16 p){ return p == WP_BODY ? -2 : -10; }
static u16 layOpp(u16 p){ return p == w81Pose[8] || p == w81Pose[9]; }
static void drawF(u16 f, u16 hands){
 if(clHeld[f]==2)return;
 const Pose *P = &poseTab[dLoaded[f]];
 const s16 cX = camx + 0x200, cY = 0x200 - camy;
 const u16 diveAux = hands && layOpp(dLoaded[f]);
 const s16 bx_ = dX[f] + dLyo[f] - cX + (diveAux ? (dFlip[f] ? -4 : 4) : 0), by_ = cY - dY[f] - 16 - (dZ[f] - 187);
 const s16 gy = dY[f], ox_ = dX[f];
 const s16 ee = (gy > RING_Y0) ? ((u16) (gy - RING_Y0)) / 6 : 0;
 u16 inside = 1;
 if (dSx[f]) { inside = (ox_ > RING_XL + ee && ox_ < RING_XR - ee) ? 1 : 0; if (dSx[f] == 2 && !(dOutK[f] <= 65)) inside = 0; }
 if (dBx[f] == 2) inside = 0;
 const u16 orange = !inside && gy >= RING_Y0 && gy <= RING_Y1 + 24;
 const u16 pri2 = (dClimb[f] >= 3) ? 2 : inside ? 1 : 0;
 const u16 pz = dLog[f], fl = dFlip[f];
 const u16 bxHi = (dBx[f] == 3 || (dBx[f] == 1 && pz >= 188 && pz <= 191));
 const u16 useFl = (hands && layOpp(dLoaded[f])) ? (u16)(fl ? 0 : 1) : fl;
 const u16 flBit = useFl ? 0x0800 : 0, sBase = dSlot[f];
 for (u16 k = 0; k < P->n && nsat < 70; k++) {
  { const u16 ln = layN(dLoaded[f]);
    if (ln && ((k >= ln) != hands)) continue;
    if (!ln && hands) continue; }
  const Piece *c = &P->p[k];
  const s16 x = bx_ + (useFl ? (4 - c->dx - ((((c->sz >> 2) & 3) + 1) << 3)) : c->dx), y = by_ + c->dy;
  if (x <= -32 || x >= 256 || y <= -32 || y >= 224) continue;
  if (y + ((((c->sz) & 3) + 1) << 3) <= HUD_H) continue;
  u16 *e = &sat[nsat * 4];
  e[0] = 128 + y; e[1] = (c->sz << 8) | (nsat + 1);
  u16 pq = 0x8000;
  const u16 hc = ((c->sz) & 3) + 1, wc = ((c->sz >> 2) & 3) + 1;
  const s16 top = camy + 16 + WY0 + y, rl = ROPE_FRONT_R0 * 8;
  if (pri2 == 1 && !bxHi && top + (hc << 3) - 1 >= rl) {
   const s16 hu = (top < rl) ? (rl - top) >> 3 : 0;
   if (hu == 0 || nsat + 2 * wc > 78) pq = 0;
   else {
    const u16 hl = hc - hu, tb = flBit | (c->line << 13) | (sBase + c->toff);
    for (u16 i = 0; i < wc; i++) {
     const s16 xc = x + ((useFl ? (wc - 1 - i) : i) << 3);
     e = &sat[nsat * 4]; e[0] = 128 + y; e[1] = ((hu - 1) << 8) | (nsat + 1); e[2] = 0x8000 | (tb + i * hc); e[3] = 128 + xc; nsat++;
     e = &sat[nsat * 4]; e[0] = 128 + y + (hu << 3); e[1] = ((hl - 1) << 8) | (nsat + 1); e[2] = tb + i * hc + hu; e[3] = 128 + xc; nsat++;
    }
    continue;
   }
  }
  if (y < HUD_H) pq = 0;
  if (pri2 == 0 && orange) pq = 0;
  if (bxHi) pq = 0x8000;
  e[2] = pq | flBit | (c->line << 13) | (sBase + c->toff); e[3] = 128 + x;
  nsat++;
 }
}

/* s49 priority */
/* s49 priority: HIGH default; LOW purple (inside @ bottom ropes) / orange (outside laterals). Trocea si cruza rl. */
static void buildSat(void){
 nsat = 0;
 const s16 cX = camx + 0x200, cY = 0x200 - camy;
 /* b71: cuenta del arbitro (pantalla x 120, y 92; PAL0 fondo, prioridad alta) */
 if (digPin && digLd == digPin) {
  u16 *e = &sat[nsat * 4]; e[0] = 128 + 92; e[1] = (7 << 8) | (nsat + 1); e[2] = 0x8000 | DIG_T; e[3] = 128 + 120; nsat++;
  e = &sat[nsat * 4]; e[0] = 128 + 124; e[1] = (4 << 8) | (nsat + 1); e[2] = 0x8000 | (DIG_T + 8); e[3] = 128 + 120; nsat++;
 } else if (roC) {
  /* b72: cifras grandes rojas como el pin (unidades en DIG_T, decenas en RO_T); mismo sitio que el pin */
  const u16 t = roC / 10; const s16 x0 = t ? 104 : 120; u16 *e;
  if (roLd == roC) {
   if (t) { e = &sat[nsat * 4]; e[0] = 128 + 92; e[1] = (7 << 8) | (nsat + 1); e[2] = 0x8000 | RO_T; e[3] = 128 + x0; nsat++;
    e = &sat[nsat * 4]; e[0] = 128 + 124; e[1] = (4 << 8) | (nsat + 1); e[2] = 0x8000 | (RO_T + 8); e[3] = 128 + x0; nsat++; }
   e = &sat[nsat * 4]; e[0] = 128 + 92; e[1] = (7 << 8) | (nsat + 1); e[2] = 0x8000 | DIG_T; e[3] = 128 + x0 + (t ? 16 : 0); nsat++;
   e = &sat[nsat * 4]; e[0] = 128 + 124; e[1] = (4 << 8) | (nsat + 1); e[2] = 0x8000 | (DIG_T + 8); e[3] = 128 + x0 + (t ? 16 : 0); nsat++; }
 }
 /* b58: orden por pies Duggan vs arbitro (menor oy = delante). Companeros siempre al final (LOW). */
 { const u16 aux = layN(dLoaded[1]) != 0, n = aux ? 4 : 3;
   const s16 fk[4] = {dY[0] + (aux ? 0 : dZ[0] - 187), rfy, dY[1] + (aux ? 0 : dZ[1] - 187), dY[1] + layDy(dLoaded[1])};
   u16 ord[4] = {0, 1, 2, 3};
   /* 45AE compara entrada+8 = Y de suelo, NO Y+Z. BE96: manos Y-2. */
   for (u16 a = 0; a < n - 1; a++) for (u16 b = 0; b < n - 1 - a; b++) if (fk[ord[b]] > fk[ord[b + 1]]) { const u16 t = ord[b]; ord[b] = ord[b + 1]; ord[b + 1] = t; }
   for (u16 pass = 0; pass < n; pass++) {
    const u16 who = ord[pass];
    if (who == 3) drawF(1, 1);
    else if (who != 1) drawF(who ? 1 : 0, 0);
    else {
     /* arbitro: HIGH + zonas; piezas que tocan HUD -> LOW; H-flip si walk */
     const Pose *Q = &poseTab[rfPose];
     const u16 fl = rfFl; /* b58: H-flip en idle 8 al ir a la derecha; 508/509 ya orientados */
     const s16 qx = rfx - cX, qy = cY - rfy - 16;
     const s16 gy = rfy;
     const s16 ee = (gy > RING_Y0) ? ((u16)(gy - RING_Y0)) / 6 : 0;
     const u16 inside = (rfx > RING_XL + ee && rfx < RING_XR - ee) ? 1 : 0;
     const u16 orange = !inside && gy >= RING_Y0 && gy <= RING_Y1 + 24;
     const u16 pri2 = inside ? 1 : 0;
     const u16 flBit = fl ? 0x0800 : 0;
     for (u16 k = 0; k < Q->n && nsat < 62; k++) {
      const Piece *c = &Q->p[k];
      const s16 x = qx + (fl ? (4 - c->dx - ((((c->sz >> 2) & 3) + 1) << 3)) : c->dx), y = qy + c->dy;
      if (x <= -32 || x >= 256 || y <= -32 || y >= 224) continue;
      if (y + ((((c->sz) & 3) + 1) << 3) <= HUD_H) continue;
      u16 *e = &sat[nsat * 4];
      e[0] = 128 + y; e[1] = (c->sz << 8) | (nsat + 1);
      u16 pq = 0x8000;
      const u16 hc = ((c->sz) & 3) + 1, wc = ((c->sz >> 2) & 3) + 1;
      const s16 top = camy + 16 + WY0 + y, rl = ROPE_FRONT_R0 * 8;
      /* b58: cualquier pieza que toque el HUD (y < HUD_H) va en BAJA */
      if (y < HUD_H) pq = 0;
      else if (pri2 == 1 && top + (hc << 3) - 1 >= rl) {
       const s16 hu = (top < rl) ? (rl - top) >> 3 : 0;
       if (hu == 0 || nsat + 2 * wc > 78) pq = 0;
       else {
        const u16 hl = hc - hu;
        for (u16 i = 0; i < wc; i++) {
         const s16 xc = x + ((fl ? (wc - 1 - i) : i) << 3);
         /* split: upper HIGH unless HUD; lower LOW (purple) */
         u16 pqU = (y < HUD_H) ? 0 : 0x8000;
         rfColumn(xc, y, c->toff + i * hc, hu, pqU | flBit | (c->line << 13));
         rfColumn(xc, y + (hu << 3), c->toff + i * hc + hu, hl, flBit | (c->line << 13));
        }
        continue;
       }
      }
      if (pri2 == 0 && orange) pq = 0;
      if (c->toff < 28 && c->toff + wc * hc > 28) {
       for (u16 i = 0; i < wc; i++) {
        const s16 xc = x + ((fl ? (wc - 1 - i) : i) << 3);
        rfColumn(xc, y, c->toff + i * hc, hc, pq | flBit | (c->line << 13));
       }
      } else { e[2] = pq | flBit | (c->line << 13) | rfTile(c->toff); e[3] = 128 + x; nsat++; }
     }
    }
   }
 }
 /* b56: relevo siempre LOW al final */
 for (u16 q = 0; q < 2; q++) {
  const Pose *Q = &poseTab[449 + q];
  const s16 qx = ptX[q] - cX, qy = cY - ptY[q] - 16;
  for (u16 k = 0; k < Q->n && nsat < 62; k++) {
   const Piece *c = &Q->p[k];
   const s16 x = qx + c->dx, y = qy + c->dy;
   if (x <= -32 || x >= 256 || y <= -32 || y >= 224) continue;
   if (y + ((((c->sz) & 3) + 1) << 3) <= HUD_H) continue;
   u16 *e = &sat[nsat * 4];
   e[0] = 128 + y; e[1] = (c->sz << 8) | (nsat + 1);
   e[2] = (c->line << 13) | (ptT[q] + c->toff); e[3] = 128 + x;
   nsat++;
  }
 }
 if (nsat) sat[(nsat - 1) * 4 + 1] &= 0xFF00;
 else { sat[0] = 0; sat[1] = 0; sat[2] = 0; sat[3] = 0; nsat = 1; }
}


int main(bool h){
 (void)h;
 for (u16 i = 0; i < POOLN; i++) fstk[i] = 16 + i; nf = POOLN;
 memcpy(W, m_bin, sizeof(W));
 SND_PCM4_loadDriver(TRUE);
 VDP_setScreenWidth256(); VDP_setPlaneSize(64, 32, FALSE);
 VDP_setBGBAddress(0xE000); VDP_setBGAAddress(0xC000); VDP_setWindowAddress(0xD000);
 VDP_setSpriteListAddress(0xF000); VDP_setHScrollTableAddress(0xF800);
 VDP_clearPlane(BG_B, TRUE); VDP_clearPlane(BG_A, TRUE);
 selectScreen89(); /* Only called once, never by matchReset. */
 PAL_setColors(0, (const u16*)pal_bin, 32, CPU);
 hudInit();
 PAL_setColors(32, (const u16*)spr_pal, 32, CPU);
 VDP_loadTileData((const u32*)ropes_bin, VT, NR, CPU);
 poseTab = (const Pose*)spr_tab;
 for (u16 q = 0; q < 2; q++) VDP_loadTileData((const u32*)(spr_tiles + (u32)poseTab[449 + q].t0 * 32), ptT[q], 43, CPU);
 rfx = RF_HOME_X; rfy = RF_HOME_Y; rfPose = RF_IDLE; rfFl = 0; rfPh = 0; rfMoving = 0; rfLoaded = 0xFFFF;
 rfLoadEx(RF_IDLE, CPU);
 slotP1 = SPR_BASE;
 const u16 *xlw = (const u16*)xl_w, *xld = (const u16*)xl_d;
 /* b69: estado inicial = b68 (Duggan 736,288 / Warrior 660,262 mirando a Duggan) */
 for (u16 f = 0; f < 2; f++) {
  fighterInit(f);
  dX[f] = ox; dY[f] = oy; dZ[f] = 187; dLog[f] = 0; dPose[f] = f ? xlw[0] : 0; dFlip[f] = 0; dLyo[f] = 0;
  { const Pose *P = &poseTab[dPose[f]]; VDP_loadTileData((const u32*)(spr_tiles + (u32)P->t0 * 32), dSlot[f], P->nt, CPU); dLoaded[f] = dPose[f]; }
 }
 ctxLoad(0);
 camx = 128; camy = 128; camera();
 cx = camx + 96; cy = camy + 32;
 if (cx < 0) cx = 0; if (cx > MW * 8 - 256) cx = MW * 8 - 256;
 if (cy < 0) cy = 0; if (cy > MH * 8 - 224) cy = MH * 8 - 224;
 tx = cx >> 3; ty = cy >> 3;
 for (s16 r = ty; r < ty + VH; r++) for (s16 c = tx; c < tx + VW; c++) put(r, c);
 sndCmd(0x22);

 VDP_setEnable(TRUE);selPhase89=4;
 arcDen=IS_PAL_SYSTEM?5440:6528;arcLast=vtimer;
 u16 prev = 0;
 while (1) {
  {u32 now=vtimer,delta=now-arcLast;arcLast=now;arcClock+=3125*delta;arcTick=arcClock>=arcDen;if(arcTick)arcClock-=arcDen;}
  u16 j = joy89(JOY_readJoypad(JOY_1)), pr = j & ~prev, prev0 = prev; prev = j;
  s16 jhx = 0, jhy = 0;
  if (j & BUTTON_LEFT) jhx = -1; if (j & BUTTON_RIGHT) jhx = 1;
  if (j & BUTTON_UP) jhy = 1; if (j & BUTTON_DOWN) jhy = -1;
  u16 btn = 0;
  { static u16 stUsed; /* START solo (sin A/B/C) al soltar = el oponente persigue / se para */
    if (pr & BUTTON_START) stUsed = 0;
    if ((j & BUTTON_START) && (pr & (BUTTON_A | BUTTON_B | BUTTON_Y))) stUsed = 1;
    if ((prev0 & BUTTON_START) && !(j & BUTTON_START) && !stUsed) follow ^= 1; }
  if (j & BUTTON_START) {
   if (pr & BUTTON_A) { CA_TRIG(); sndCmd(0x50); }
   if (pr & BUTTON_B) { CA_TRIG(); sndCmd(0x51); }
   if (pr & BUTTON_Y) { CA_FENCE(); sndCmd(0x22); }
  } else {
   btn = pr & (BUTTON_A | BUTTON_B);
   if (pr & BUTTON_Y) ctl ^= 1;   /* b89: Y swaps; C is normalized to A+B before edge detection. */
  }
  if (gr) grStep(btn);
  pinAdvance();
  for (u16 f = 0; f < 2; f++) {
   ctxLoad(f);
   if (vlast[f] && !--vlast[f]) vdmg[f] = 0;
   s16 hx = 0, hy = 0; const u16 ai = (f != ctl);
   if (!ai) { hx = jhx; hy = jhy; pendBtn |= btn; }
   else if (follow) { /* persecucion (logica b65 de Warrior) hacia el luchador controlado */
    const s16 ddx = fd[ctl].ox - ox, ddy = fd[ctl].oy - oy;
    const s16 adx = ddx < 0 ? -ddx : ddx, ady = ddy < 0 ? -ddy : ddy;
    if (adx > WR_KEEP) hx = ddx > 0 ? 1 : -1; else if (adx < WR_KEEP / 2 && ady < 12) hx = ddx > 0 ? -1 : 1; /* b69: no se monta encima */
    if (ady > WR_KEEP / 2 && (adx > 8 || ady > WR_KEEP)) hy = ddy > 0 ? 1 : -1;
    if (adx <= WR_KEEP && ady > 6 && adx > WR_KEEP / 2) hy = ddy > 0 ? 1 : -1;
   }
   tick++;
   u16 np, fl;
   if(!kvPhase90[f]){
    u16 lying=lyingNow(f);
    if(lying){if(!groundSeen90[f]){static const u16 t[4]={112,82,54,22};ground90[f]=t[energy90[f]/12>3?3:energy90[f]/12];}else if(arcTick&&ground90[f])ground90[f]--;}
    groundSeen90[f]=lying;
   }
   if(kvPhase90[f]){ctxSave(f);u16 p=(f==1&&dugVictimPending92)?(dugVictimPending92=0,kneePose90[1][0]):kneeVictimStep90(f);ctxLoad(f);curPose=kvPhase90[f]?p:0;dLog[f]=curPose;dPose[f]=p;dFlip[f]=oriVictima(f);dLyo[f]=0;
    dX[f]=ox;dY[f]=oy;dZ[f]=z0;dSx[f]=sx;dBx[f]=bx;dClimb[f]=0;ctxSave(f);continue;}
   if(clHeld[f]){pendBtn=0;ctxSave(f);continue;}
   if (fs[f]) { ctxSave(f); const u16 p = fsStep(f); ctxLoad(f);   /* b76: accion 8 (caida arcade) */
    curPose = p; dLog[f] = p; dPose[f] = p; dFlip[f] = vface[f] ^ 1; dLyo[f] = 0; pendBtn = 0;
    dX[f] = ox; dY[f] = oy; dZ[f] = z0; dSx[f] = dBx[f] = dClimb[f] = 0; ctxSave(f); continue; }
   if (pnS == 2 && f == pnV) { const u16 p = apPose[f][(pnK < 16) ? AP_9F : AP_A0];  /* b76: 0xB012 zafarse (tabla 0xB0EA) */
    curPose = p; dLog[f] = p; dPose[f] = p; dFlip[f] = vface[f] ^ 1; dLyo[f] = 0;
    dX[f] = pnVX + pnKD * 8; dY[f] = oy; dZ[f] = 187; dSx[f] = dBx[f] = dClimb[f] = 0; pendBtn = 0; ctxSave(f); continue; }
   if (pnS && f == pnA) { const u16 p = pinStepA();   /* b71: cubriendo (pose directa) */
    if (p != 0xFFFF) { curPose = p; dLog[f] = p; dPose[f] = p; dFlip[f] = f ? ((pnM < 0) ^ (p == 513)) : (rfM < 0); dLyo[f] = 0; /* b94: Warrior 11A8A +A=rival^0x80 (=!oriVictima); 514/778 convertidas espejadas (match69 flip1), 513 sin espejar (arc pose 2 flip0) -> volteo inverso; Duggan sin cambios */
     dX[f] = ox; dY[f] = oy; dZ[f] = z0; dSx[f] = dBx[f] = dClimb[f] = 0; ctxSave(f); continue; } }
   if (gr || tr[f]) {
    u16 p = gr ? trPose[f] : trStep(f);
    if (p != 0xFFFF) { ctxLoad(f); np = p; fl = (trM < 0 && tr[f]) || (gr && lkS < 0);
     curPose = np; dLog[f] = np; dPose[f] = np; dFlip[f] = fl; dLyo[f] = 0;
     dX[f] = ox; dY[f] = oy; dZ[f] = z0; dSx[f] = dBx[f] = dClimb[f] = 0; ctxSave(f); continue; }
    ctxLoad(f);
    if (fs[f]) continue; /* b76: empezo la caida (accion 8) */
   }
   if (vh[f]) { np = victimStep(f); fl = vh[f] ? (vface[f] ^ invFl(np)) : 0; }
   else { np = engine(hx, hy, ai); fl = dFl; }
   curPose = np;
   dLog[f] = np; dPose[f] = (gs == 12 || gs == 13 || gs == 14 || gs == 15) ? np : f ? xlw[np] : xld[np]; dFlip[f] = fl;
   dLyo[f] = 0; /* b94: tumbado en el ox arcade (sin lyo b74) */
   dX[f] = ox; dY[f] = oy + ((vjolt[f] > 5) ? 3 : vjolt[f] ? 1 : 0) + GH_SIGN * gH; dZ[f] = z0;
   dSx[f] = sx; dBx[f] = bx; dClimb[f] = climb; dOutK[f] = outK;
   ctxSave(f);
  }
  grTry();
  countStep();
  if (resetReq) matchReset();
  ctxLoad(ctl);
  camera();
  ctxSave(ctl);
  cx = camx + 96; cy = camy + 32;
  if (cx < 0) cx = 0; if (cx > MW * 8 - 256) cx = MW * 8 - 256;
  if (cy < 0) cy = 0; if (cy > MH * 8 - 224) cy = MH * 8 - 224;

  s16 nx = cx >> 3, ny = cy >> 3;
  s16 nwx = (nx + VW > MW) ? MW - VW : nx, nwy = (ny + VH > MH) ? MH - VH : ny;
  caLogic(); caDraw(); caApply(); /* b95: publico (CPU) antes del streaming en cola: mismo W y mismo resultado, sin pisar slots en cola */
  /* b95: cuerdas antes del streaming (la columna/fila en cola lleva ya el frame de cuerda nuevo) */
  for (u16 sd = 0; sd < 2; sd++) if (rk[sd] >= 0) {
   if (rFall[sd]) {
    /* 21324: initialize THEN decrement on the same 30Hz tick; draw AFTER
       advancing the phase (213B4). Both sides share this exact clock. */
    if (!(rk[sd]++ & 1) && --rTimer[sd] == 0) {
     if (++rStep[sd] >= 8) {rFall[sd]=0;rk[sd]=-1;}
     else rTimer[sd]=ropeDurA[rStep[sd]];
    }
    const u16 f=rFall[sd]?ropeShortMap[sd][ropePhaseA[rStep[sd]]]:0;
    if (f != rcur[sd]) {rcur[sd]=f;ropeDraw(sd);}
   } else {
    const u8 *sc = sd ? sc1 : sc0; const u16 n = sd ? NS1 : NS0; const u16 f = (rk[sd] < n) ? sc[rk[sd]] : 0;
    if (f != rcur[sd]) { rcur[sd] = f; ropeDraw(sd); }
    if (++rk[sd] > n) rk[sd] = -1;
   }
  }
  while (tx < nwx) { for (s16 r = ty; r < ty + VH; r++) { rel(r, tx); } stCol(tx + VW, ty, VH); tx++; }
  while (tx > nwx) { tx--; for (s16 r = ty; r < ty + VH; r++) { rel(r, tx + VW); } stCol(tx, ty, VH); }
  while (ty < nwy) { for (s16 c = tx; c < tx + VW; c++) { rel(ty, c); } stRow(ty + VH, tx, VW); ty++; }
  while (ty > nwy) { ty--; for (s16 c = tx; c < tx + VW; c++) { rel(ty + VH, c); } stRow(ty, tx, VW); }

  sqTick();

  ctxLoad(0);
  if (rsS) refPinStep(); else if (!pnS) { rfStep();
   if (roOut) { /* b72: cuenta fuera = arcade 0xDEE4 + 0xDA38 tabla 0xDB04 (gestos 0xA-0x11 -> 757-764), 4 poses x 16 f = 1 numero */
    const u16 w = (fd[0].sx == 2 || fd[0].bx == 2) ? 0 : 1;
    rfPose = ((fd[w].oy > rfy) ? RF_CBACK : RF_CFRONT) + ((roT >> 4) & 3);
    if (fd[w].ox != rfx) rfFl = (fd[w].ox < rfx); } } /* b71: arbitro cuenta el pin; si no, sigue a Duggan (igual b68) */
  SYS_doVBlankProcess(); stTiles = 0; stBN = 0; /* b95: la cola de streaming se vuelca aqui (vblank) */
  fLoad(0); fLoad(1);
  rfLoad(rfPose);
  if (!digPin && roC && roC != roLd) { /* b72 */
   VDP_loadTileData((const u32*)(big_dig + (u32)(roC % 10) * 320), DIG_T, 10, CPU);
   if (roC >= 10) VDP_loadTileData((const u32*)(big_dig + (u32)(roC / 10) * 320), RO_T, 10, CPU);
   roLd = roC; digLd = 0xFFFF; }
  if (digPin && digPin != digLd) { roLd = 0xFFFF; VDP_loadTileData((const u32*)(pin_glyph + (u32)(digPin - 1) * 320), DIG_T, 10, CPU); digLd = digPin; }
  buildSat();
  VDP_setHorizontalScroll(BG_B, -cx); VDP_setVerticalScroll(BG_B, cy);
  VDP_setHorizontalScroll(BG_A, -cx); VDP_setVerticalScroll(BG_A, cy);
  DMA_doDma(DMA_VRAM, sat, 0xF000, nsat * 4, 2);
 }
 return 0;
}
