import sys; sys.path.insert(0,'/workspace/chiki/tools'); sys.path.insert(0,'/workspace/wwf_sgdk/rec4')
from lr import *; from load import frames,dec
import numpy as np, pickle
from PIL import Image
F=frames('/workspace/wwf_sgdk/rec4/walk/rec.bin')
w=lambda f,a:f['ram'][a-0x1c0000]<<8|f['ram'][a-0x1c0000+1]
plan=[(300,'')]+[(24,d) for k in range(12) for d in ('R','','L','','U','','D','','UR','DL','UL','DR','')]
def tag(t):
    acc=0
    for n,d in plan:
        if acc<=t<acc+n: return d
        acc+=n
    return ''
M={'R':'RIGHT','L':'LEFT','U':'UP','D':'DOWN'}
def poke(c,a,v):
    a&=0xffff; v&=0xffff; c.wram[a]=v&0xff; c.wram[a+1]=v>>8   # core stores words little-endian
def peek(c,a):
    a&=0xffff; return c.wram[a]|c.wram[a+1]<<8
SYM={l.split()[2]:int(l.split()[0],16)&0xffffff for l in open('/workspace/wwf_sgdk/out/symbol.txt') if len(l.split())==3}
OX,OY=SYM['ox'],SYM['oy']
A_PH,A_TICK,A_POSE,A_CAMX,A_OXF,A_OYF=SYM['walkPh'],[v for k,v in SYM.items() if k.startswith('tick')][0],SYM['curPose'],SYM['camx'],SYM['oxf'],SYM['oyf']
def setobj(c,f,ks):
    for k in ks: poke(c,OX+2*k,w(f,0x1c0100+k*0x11a+0xc)); poke(c,OY+2*k,w(f,0x1c0100+k*0x11a+0x10))
def run(lag,ph,par):
    c=Core('/workspace/wwf_sgdk/out/WWF_SGDK_s04b.bin',{b"genesis_plus_gx_region_detect":b"ntsc-u"}); c.run(60)
    setobj(c,F[300],range(5)); c.run(200); setobj(c,F[300],range(5))
    poke(c,A_PH,ph); poke(c,A_TICK,par); poke(c,A_OXF,0); poke(c,A_OYF,0)
    shots={}; pos={}
    for t in range(300,940):
        setobj(c,F[t],(1,2,3,4))
        d=tag(t-lag); c.run(1,pad0=tuple(M[x] for x in d))
        pos[t]=(peek(c,OX),peek(c,OY),peek(c,A_CAMX))
        if t in WANT: shots[t]=np.array(c.image().convert('RGB'))[:224]
    return pos,shots
WANT=set(range(300,940,4))
best=None
for lag in (0,1,2):
  for par in (0,1):
    pos,_=(None,None)
    WANT_=WANT; WANT=set()
    pos,_=run(lag,0,par); WANT=WANT_
    err=sum(abs(pos[t][0]-w(F[t],0x1c010c))+abs(pos[t][1]-w(F[t],0x1c0110)) for t in range(300,940))
    cam=sum(abs(pos[t][2]-(w(F[t],0x1c002a)-0x200)) for t in range(300,940))
    print('lag',lag,'par',par,'pos err',err,'cam err',cam)
    if best is None or err<best[0]: best=(err,lag,par)
print('best',best)
pickle.dump(best,open('/tmp/walkbest.pkl','wb'))
if len(sys.argv)>1:
    pos,_=(lambda W: (globals().__setitem__('WANT',set()),run(1,0,0))[1])(0)
    for t in range(300,520,2): print(t,tag(t),pos[t][0],w(F[t],0x1c010c),'cam',pos[t][2],w(F[t],0x1c002a)-0x200)
