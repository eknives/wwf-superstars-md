# s04b vs MAME edge probes: same start (P1 768,300, others parked as in MAME), same held direction
import sys,collections; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
from PIL import Image
ROM='/workspace/wwf_sgdk/out/WWF_SGDK_s04b.bin'
SYM={l.split()[2]:int(l.split()[0],16)&0xffffff for l in open('/workspace/wwf_sgdk/out/symbol.txt') if len(l.split())==3}
def poke(c,a,v): a&=0xffff; v&=0xffff; c.wram[a]=v&0xff; c.wram[a+1]=v>>8
def peek(c,a): a&=0xffff; v=c.wram[a]|c.wram[a+1]<<8; return v-65536 if v>32767 else v
OX,OY=SYM['ox'],SYM['oy']; TICK=[v for k,v in SYM.items() if k.startswith('tick')][0]; YT=[v for k,v in SYM.items() if k.startswith('yt')][0]
PARK=[(768,300),(600,120),(880,120),(1000,120),(760,110)]
M={'R':'RIGHT','L':'LEFT','U':'UP','D':'DOWN'}
T=collections.defaultdict(list)
for l in open('/workspace/wwf_sgdk/rec5/traj6.txt'):
    n,pt,x,y,cx,cy,_=l.split(); T[n].append((int(x),int(y),int(cx),int(cy)))
def probe(d,par,ypar,shots=()):
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
    for _ in range(200):
        for k,(x,y) in enumerate(PARK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        poke(c,SYM['oxf'],0); poke(c,SYM['oyf'],0); c.run(1)
    poke(c,TICK,par); poke(c,YT,ypar)
    tr=[]; im={}
    for f in range(204):
        for k,(x,y) in enumerate(PARK[1:],1): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        c.run(1,pad0=tuple(M[ch] for ch in d) if f<200 else ())
        tr.append((peek(c,OX),peek(c,OY),peek(c,SYM['camx'])+0x200,0x200-peek(c,SYM['camy'])))
        if f in shots: im[f]=np.array(c.image().convert('RGB'))[:224]
    return tr,im
if __name__=='__main__' and len(sys.argv)==1:
    for d in ('U','D','L','R','UL','UR','DL','DR'):
        m=T['c_'+d][120:]
        best=None
        for par in (0,1):
          for yp in (0,1):
            tr,_=probe(d,par,yp)
            for sh in (0,1,2):
                e=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(tr[sh:],m[:len(m)-3]))
                ec=sum(abs(a[2]-b[2])+abs(a[3]-b[3]) for a,b in zip(tr[sh:],m[:len(m)-3]))
                if best is None or (e,ec)<best[:2]: best=(e,ec,par,yp,sh)
        print(d,'best pos err',best[0],'cam err',best[1],'par',best[2],'ypar',best[3],'shift',best[4])
def contact(tr):
    for i in range(len(tr)-6):
        if all(tr[i+k][:2]==tr[i][:2] for k in range(6)): return i,tr[i][:2]
    return None,None
def table():
    rows=[]
    for d in ('U','D','L','R','UL','UR','DL','DR'):
        m=T['c_'+d][120:]
        tr,_=probe(d,1,0 if d!='U' else 1)
        im,mp=contact(m); it,tp=contact(tr)
        sh=it-im if im is not None and it is not None else 0
        pre=sum(abs(tr[i+sh][0]-m[i][0])+abs(tr[i+sh][1]-m[i][1]) for i in range(max(0,-sh),im+1))
        cam=(m[im][2],m[im][3]),(tr[it][2],tr[it][3])
        rows.append((d,mp,im,tp,it,pre,cam))
        print(d,'MAME contact',mp,'@',im,'s04b',tp,'@',it,'| path err before contact',pre,'| cam MAME',cam[0],'s04b',cam[1])
    return rows
if len(sys.argv)>1 and sys.argv[1]=='table': table()
