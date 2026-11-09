/* b92 ONLY Duggan. Sources: C706/CB6C,1173A/118BC,10A5E/111F0/11372.
   Independent state/clock: the Warrior implementation is deliberately untouched. */
#include "duggan92_poses.h"
static u16 dugPhase92,dugTime92,dugVar92,dugDraw92,dugPost92,dugFloor92;
static u16 dugVictimPending92;
static s16 dugVx92,dugVy92,dugVz92;
static s32 dugX92,dugY92,dugZ92;
static u16 dugLying92(u16 o){return lyingNow(o)||kvPhase90[o]==2;}
static u16 dugZone92(u16 o){ /* C79E..C8A8: the same anchor, strict bounds; CB6C rows. */
 if(!dugLying92(o)||(sx==2||bx==2)!=(fd[o].sx==2||fd[o].bx==2))return 0;
 s16 dy=oy-fd[o].oy,dx=fd[o].ox+(oriVictima(o)?40:-40)-ox;
 if(dy<0)dy=-dy;if(dy>=24)return 0;
 if(dx>=0){if(oriVictima(o))return dx<48?2:0;return dx<32?1:0;}
 dx=-dx;if(oriVictima(o))return dx<32?1:0;return dx<48?2:0;
}
static void dugHit92(u16 o,u16 damage){
 hurt90(o,damage);kneeVictimStart90(o);dugVictimPending92=1;CA_TRIG();
}
static u16 dugEnd92(void){
 gs=0;gH=0;z0=dugFloor92;dFl=0;lastBase=0xffff;tick=1;afterPose=0;mvh=0;return 0;
}
static u16 dugStart92(u16 kind,u16 o,u16 post){
 gs=kind;gk=0;pendBtn=0;dugPhase92=0;dugTime92=1;dugPost92=post;
 dugVar92=oy+2<fd[o].oy;dugFloor92=(sx==2||bx==2)?128:187;gH=0;
 dugX92=((s32)ox<<8)|oxf;dugY92=((s32)oy<<8)|oyf;dugZ92=(s32)z0<<8;
 if(kind==14){dugVx92=dugVy92=dugVz92=0;dugDraw92=dugPose92[0];dFl=p1face;return dugDraw92;}
 /* 10A6C/10BB2: Duggan copies victim orientation, unlike Warrior's Vx rule. */
 p1face=dFace=oriVictima(o);
 dugX92=((s32)ox<<8)|oxf;dugY92=((s32)oy<<8)|oyf;dugZ92=(s32)z0<<8;
 /* 11180/11188 ->111F0; 159AC simulates single ticks and truncates word deltas. */
 s32 z=dugZ92;s16 vz=0x500;u16 n=0;
 do{z+=vz;vz-=0x50;if(vz<(s16)0xf800)vz=(s16)0xf800;n++;}while(vz>=0||(z>>8)>=dugFloor92);
 s16 off=dugFloor92==128?32:64;
 dugVx92=((s32)(fd[o].ox+(oriVictima(o)?off:-off)-ox)*256)/n;
 dugVy92=((s32)(fd[o].oy-oy)*256)/n;dugVz92=0x500;
 if(dugVx92>0x2000)dugVx92=0x2000;if(dugVx92< -0x2000)dugVx92=-0x2000;
 if(dugVy92>0x2000)dugVy92=0x2000;if(dugVy92< -0x2000)dugVy92=-0x2000;
 if(post){ /* 10B5E/110E4 */
  s16 dx=fd[o].ox+(oriVictima(o)?64:-64)-ox,dy=fd[o].oy-oy,lim=dugFloor92==128?112:80;
  if(dx>=96||dx<=-96)dugVx92=dx<0?-0x200:0x200;
  if(dy>=lim||dy<=-lim)dugVy92=dy<0?-0x100:0x100;
 }
 dFl=post?(dugVx92<0):p1face;dugDraw92=dugPose92[2];return dugDraw92;
}
static u16 dugStep92(u16 o){
 pendBtn=0;if(!arcTick)return dugDraw92;gk++;
 if(gs==14){ /* 11750 decrements on init: 159 seven ticks;15A four + exit hold. */
  dugTime92++;
  if(dugTime92==8){if(dugLying92(o)&&(sx==2||bx==2)==(fd[o].sx==2||fd[o].bx==2))dugHit92(o,1);}
  if(dugTime92>=13)return dugEnd92();
  dugDraw92=dugPose92[dugTime92<8?0:1];return dugDraw92;
 }
 if(dugPhase92==0){
  dugDraw92=dugPose92[2];dFl=dugPost92?(dugVx92<0):p1face;
  if(++dugTime92>=4){dugPhase92=1;dugTime92=0;}return dugDraw92;
 }
 if(dugPhase92==5||dugPhase92==8){ /* A90E/AA00[0]: eight ticks, no automatic pin. */
  if(dugTime92>=8)return dugEnd92();dugTime92++;dFl=p1face;return dugDraw92=dugPose92[8];
 }
 if(dugPhase92==7){ /* AB1E/AF66, human miss recovery. */
  static const u16 wait[4]={112,82,54,22};u16 ei=energy90[0]/12;if(ei>3)ei=3;
  if(++dugTime92>=wait[ei]){dugPhase92=8;dugTime92=0;}return dugDraw92=dugPose92[11];
 }
 if(dugPhase92==6){ /* 9FCC: flip once, 27D2[19] vz300/g40, height16 switches1CF->16. */
  if(!dugTime92){p1face^=1;dFace=p1face;}dugTime92++;dFl=p1face;
  dugZ92+=2*(s32)dugVz92;dugVz92-=0x80;z0=dugZ92>>8;
  dugDraw92=dugPose92[(dugVz92<0&&z0-dugFloor92<16)?10:9];
  if(z0<=dugFloor92){z0=dugFloor92;dugZ92=((s32)dugFloor92<<8)|(dugZ92&255);dugPhase92=7;dugTime92=0;}
  return dugDraw92;
 }
 if(dugPhase92==4){
  dFl=p1face;dugDraw92=dugPose92[dugVar92?7:5];
  if(++dugTime92>=12){dugPhase92=5;dugTime92=0;}return dugDraw92;
 }
 /* 3DCE/3E20: integrate first; 10BF8 tests descending after gravity. */
 dugX92+=2*(s32)dugVx92;dugY92+=2*(s32)dugVy92;dugZ92+=2*(s32)dugVz92;
 dugVz92-=0xa0;if(dugVz92<(s16)0xf800)dugVz92=(s16)0xf800;
 ox=dugX92>>8;oxf=dugX92&255;oy=dugY92>>8;oyf=dugY92&255;z0=dugZ92>>8;
 dFl=(dugPost92&&dugPhase92==1)?(dugVx92<0):p1face;
 if(dugVz92<0&&dugLying92(o)&&((fd[o].sx==2||fd[o].bx==2)?128:187)==dugFloor92&&z0<=dugFloor92+16){
  /* 11084 normal victim rectangle; 110BC/110C0 Duggan point(+/-8,+4). */
  s16 lo=fd[o].ox+(oriVictima(o)?0:-64),hi=fd[o].ox+(oriVictima(o)?64:0),px=ox+(p1face?-8:8),py=oy+4;
  if(px>lo&&px<=hi&&py>fd[o].oy&&py<=fd[o].oy+16){
   z0=dugFloor92;dugZ92=((s32)dugFloor92<<8)|(dugZ92&255);
   oy=fd[o].oy-1;dugY92=((s32)oy<<8)|(dugY92&255);oyf=dugY92&255;
   dugPhase92=4;dugTime92=1;dFl=p1face;
   dugHit92(o,dugPost92?10:5);return dugDraw92=dugPose92[dugVar92?7:5];
  }
 }
 if(z0<=dugFloor92){ /* 10C4A..10CB2; direction is +A, not Vx. */
  hurt90(0,2);z0=dugFloor92;dugZ92=((s32)dugFloor92<<8)|(dugZ92&255);
  ox+=p1face?24:-24;dugX92=((s32)ox<<8)|(dugX92&255);oxf=dugX92&255;
  dugPhase92=6;dugTime92=0;dugVz92=0x300;dFl=!p1face;
  return dugDraw92=dugPose92[9];
 }
 dugDraw92=dugPose92[dugPhase92==1?3:(dugPhase92==2?(dugVar92?6:4):(dugVar92?7:5))];
 if(++dugTime92>(dugPhase92==1?8:4)&&dugPhase92<3){dugPhase92++;dugTime92=0;}
 return dugDraw92;
}
