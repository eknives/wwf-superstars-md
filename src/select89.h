/* b89, isolated pre-match screen. Native refs: 704E/7240/729C/749E/7552,
   73E8/747A (timeout), 1F5C/1F86 (flash), 2034A/20404 (art).
   HINT reuses portrait palettes in empty Y gaps; all native pens retained. */
#include "gen/select89_data.h"
static volatile u16 selPhase89,selFrame89,selTimer89,selMode89;
static u16 selCursor89[2],selCount89[2],selMask89,selClose89,selReady89;
static volatile u16 selPicks89[4];
static u16 selFlash89[6],selFlashStep89[6],selFlashDelay89[6],selFlashPlayer89[6];
static u16 selColors89[96],selOverlay89[896];
static s16 selTarget89[2];
static volatile u16 selRaster89;
static u16 joy89(u16 j){return (j & BUTTON_C) ? ((j & ~BUTTON_C)|BUTTON_A|BUTTON_B) : j;}
static volatile u16 selPending91,selDirtyN91;
static volatile u16 selShown91[896],selDirty91[896];
static void selV89(void){
 if(selPending91){
  for(u16 j=0;j<selDirtyN91;j++){u16 i=selDirty91[j],v=selOverlay89[i];VDP_setTileMapXY(BG_A,v,i&31,i>>5);selShown91[i]=v;}
  selPending91=0;
 }
 PAL_setColors(0,selColors89,48,CPU);selRaster89=0;VDP_setHIntCounter(23);
}
HINTERRUPT_CALLBACK selH89(void){
 /* Fixed 24-line period: register10 changes take effect only on the next reload.
    Writes occur in empty gaps (Hogan ends at87, logo104..143, Duggan starts152). */
 const u16 line=GET_VCOUNTER;
 /* Use actual scanline, not IRQ count: a delayed IRQ during a cursor-map write
    must not shift portrait palette bands for the rest of the frame. */
 if(line>=95 && !(selRaster89&1)){PAL_setColors(16,((const u16*)select89_pal)+96,16,CPU);selRaster89|=1;}
 if(line>=119 && !(selRaster89&2)){PAL_setColors(0,selColors89+48,16,CPU);PAL_setColors(32,selColors89+80,16,CPU);selRaster89|=2;}
 if(line>=143 && !(selRaster89&4)){PAL_setColors(16,selColors89+64,16,CPU);selRaster89|=4;}
}
static u16 selNeed89(void){return selMode89==1?1:2;}
static u16 selAll89(void){return selCount89[0]>=selNeed89() && (!selMode89 || selCount89[1]>=selNeed89());}
static void selConfirm89(u16 p){
 const u16 id=selCursor89[p];if(selCount89[p]>=selNeed89() || (selMask89&(1<<id)))return;
 selMask89|=1<<id;selPicks89[p*2+selCount89[p]++]=id;
 selFlash89[id]=0x40;selFlashStep89[id]=0;selFlashDelay89[id]=2;selFlashPlayer89[id]=p;
}
static void selMove89(u16 p,u16 dir){u16 id=selNav89[selCursor89[p]*16+(dir&15)];if(id<6)selCursor89[p]=id;}
static void selFlashTick89(void){
 for(u16 id=0;id<6;id++)if(selFlash89[id]){
  if(!--selFlash89[id]){if(selFlashStep89[id]==2)continue;selFlash89[id]=1;}
  if(!--selFlashDelay89[id]){selFlashStep89[id]=(selFlashStep89[id]+1)%3;selFlashDelay89[id]=2;}
 }
}
static void selPal89(void){
 SYS_disableInts();
 memcpy(selColors89,select89_pal,192);
 for(u16 id=0;id<6;id++)if(selMask89&(1<<id))selColors89[id*16+flashPen89[id]]=flashColor89[selFlashPlayer89[id]*3+selFlashStep89[id]];
 SYS_enableInts();
}
static void selAuto89(u16 p){
 if(!(selFrame89&15)){
  u16 id;do{id=(u16)(random()+selFrame89)%6;}while(selMask89&(1<<id));selTarget89[p]=id;
 }else if(selTarget89[p]>=0){
  u16 id=(u16)selTarget89[p];if(selCursor89[p]!=id)selMove89(p,autoNav89[selCursor89[p]*6+id]);
  if((selFrame89&63)==63)selConfirm89(p);
 }
}
static void selTick89(u16 *dirs,u16 *btns){
 if(selClose89){if(!--selClose89)selPhase89=3;}
 else if(selReady89){selClose89=0x40;selReady89=0;}
 else if(selTimer89){
  selTimer89--;
  for(u16 p=0;p<(selMode89?2:1);p++)if(selCount89[p]<selNeed89()){
   /* 749E dispatches on new buttons: 0=move, 1=confirm, 2/3=no-op. */
   if(!btns[p])selMove89(p,dirs[p]);else if(btns[p]==1)selConfirm89(p);
  }
  if(selAll89() && selTimer89>=1)selTimer89=1;
 }else if(selAll89()){
  if(selMode89==2)selClose89=0x70;else selReady89=1;
 }else{
  if(selCount89[0]<selNeed89())selAuto89(0);else if(selMode89)selAuto89(1);
 }
 dirs[0]=dirs[1]=btns[0]=btns[1]=0;
 selFlashTick89();selFrame89++;
}
static u16 selDir89(u16 j){return ((j&BUTTON_RIGHT)?1:0)|((j&BUTTON_LEFT)?2:0)|((j&BUTTON_UP)?4:0)|((j&BUTTON_DOWN)?8:0);}
static void selDraw89(void){
 static u16 old=0xffff;
 u16 c0=selCount89[0]<selNeed89()?selCursor89[0]:7;
 u16 c1=selMode89 && selCount89[1]<selNeed89()?selCursor89[1]:7;
 /* 75C8: if both cursors coincide, alternate each 16 native refreshes. */
 if(c0==c1 && c0<6){if(selFrame89&16)c0=7;else c1=7;}
 const u16 state=c0|(c1<<3);if(state==old)return;old=state;
 memset(selOverlay89,0,sizeof(selOverlay89));
 for(u16 p=0;p<2;p++){
  const u16 c=p?c1:c0;if(c>=6)continue;const u16 *m=((const u16*)select89_cursors)+(p*6+c)*896;
  for(u16 i=0;i<896;i++)if(m[i]&0x7ff)selOverlay89[i]=m[i];
 }
 selDirtyN91=0;
 for(u16 i=0;i<896;i++)if(selShown91[i]!=selOverlay89[i])selDirty91[selDirtyN91++]=i;
 __asm__ volatile("":::"memory");selPending91=selDirtyN91!=0;
 /* Only changed cursor cells go to VRAM, entirely inside VBlank. */
}
static void selectScreen89(void){
 /* b88 had no title/start phase. Minimal static native title is only a START gate,
    not a new attract sequence. Pad1 START = 1P; pad2 START = coop; both = versus. */
 selPhase89=1;
 JOY_setSupport(PORT_1,JOY_SUPPORT_6BTN);JOY_setSupport(PORT_2,JOY_SUPPORT_6BTN);
 VDP_setEnable(FALSE);VDP_setWindowHPos(FALSE,0);VDP_setWindowVPos(FALSE,0);
 VDP_clearSprites();VDP_updateSprites(1,CPU);
 VDP_setHorizontalScroll(BG_B,0);VDP_setVerticalScroll(BG_B,0);VDP_setHorizontalScroll(BG_A,0);VDP_setVerticalScroll(BG_A,0);
 VDP_loadTileData((const u32*)title89_tiles,0,TITLE89_NT,CPU);PAL_setColors(0,(const u16*)title89_pal,16,CPU);
 VDP_setTileMapDataRect(BG_B,(const u16*)title89_map,0,0,32,28,32,CPU);VDP_setEnable(TRUE);
 u16 prev[2]={0,0};
 while(1){
  SYS_doVBlankProcess();u16 a=JOY_readJoypad(JOY_1),b=JOY_readJoypad(JOY_2);
  if((a|b)&BUTTON_START){selMode89=(a&BUTTON_START)?((b&BUTTON_START)?2:0):1;break;}
 }
 VDP_setEnable(FALSE);VDP_loadTileData((const u32*)select89_tiles,0,SEL89_NT,CPU);
 VDP_clearPlane(BG_A,TRUE);VDP_setTileMapDataRect(BG_B,(const u16*)select89_map,0,0,32,28,32,CPU);
 selCursor89[0]=0;selCursor89[1]=2;selTimer89=0x180;selFrame89=0;selTarget89[0]=selTarget89[1]=-1;
 prev[0]=joy89(JOY_readJoypad(JOY_1));prev[1]=joy89(JOY_readJoypad(JOY_2));
 selPal89();PAL_setColors(48,((const u16*)select89_pal)+112,16,CPU);selDraw89();
 VDP_setTileMapDataRect(BG_A,selOverlay89,0,0,32,28,32,CPU);for(u16 i=0;i<896;i++)selShown91[i]=selOverlay89[i];selPending91=0;
 SYS_setVIntCallback(selV89);SYS_setHIntCallback(selH89);VDP_setHIntCounter(23);VDP_setHInterrupt(TRUE);
 selPhase89=2;VDP_setEnable(TRUE);
 const u32 den=IS_PAL_SYSTEM?5440:6528;u32 clock=0,last=vtimer;u16 dirs[2]={0,0},btns[2]={0,0};
 while(selPhase89==2){
  SYS_doVBlankProcess();u32 now=vtimer;clock+=(now-last)*6250;last=now;
  for(u16 p=0;p<2;p++){
   u16 j=joy89(JOY_readJoypad(p?JOY_2:JOY_1)),edge=j&~prev[p];prev[p]=j;
   dirs[p]|=selDir89(edge);btns[p]|=((edge&BUTTON_A)?1:0)|((edge&BUTTON_B)?2:0);
  }
  while(clock>=den && selPhase89==2){clock-=den;selTick89(dirs,btns);}
  selPal89();selDraw89();
 }
 VDP_setHInterrupt(FALSE);SYS_setHIntCallback(NULL);SYS_setVIntCallback(NULL);
 VDP_setEnable(FALSE);VDP_clearPlane(BG_A,TRUE);VDP_clearPlane(BG_B,TRUE);
}
