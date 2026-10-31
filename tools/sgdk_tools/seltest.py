# s05b: pantalla de seleccion MD vs MAME 0.276, cuadro a cuadro
import sys,os,pickle; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
from PIL import Image
ROM=os.environ.get('ROMV','/workspace/wwf_sgdk/out/rom.bin')
SYM={l.split()[2]:int(l.split()[0],16)&0xffffff for l in open(os.environ.get('SYMV','/workspace/wwf_sgdk/out/symbol.txt')) if len(l.split())==3}
def peek(c,a): a&=0xffff; return c.wram[a]|c.wram[a+1]<<8
q=lambda v:np.minimum(7,(np.asarray(v,float)/34+0.5).astype(int))
MAP={'Up':'UP','Down':'DOWN','Left':'LEFT','Right':'RIGHT','Button 1':'A'}
def run_md(sched,vs,N,lat=1):
    """sched: (cnt, 'P1 Down') pulsado 12 cuadros a partir del cuadro logico cnt; devuelve imagenes por cuadro logico (k = cnt del cuadro mostrado)"""
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'})
    a=SYM['selCnt']; frames={}; k0=None
    for step in range(N+700):
        cnt=peek(c,a); p0=[];p1=[]
        for s,n in sched:
            if s-lat<=cnt<s-lat+12:
                pl,b=n.split(' ',1); (p0 if pl=='P1' else p1).append(MAP[b])
        if vs and cnt<3: p1.append('START')
        c.run(1,pad0=tuple(p0),pad1=tuple(p1))
        if k0 is None and peek(c,a)>=1: k0=step
        if k0 is not None:
            frames[step-k0]=np.array(c.image().convert('RGB'))[:224]
            if step-k0>=N: break
    return frames
def mame(d,pre,a,b):
    return {f:np.array(Image.open('%s/%s%04d.png'%(d,pre,f)).convert('RGB'))[8:232] for f in range(a,b+1)}
Mc=q(np.array(Image.open('/tmp/sel_clean.png').convert('RGB'))[8:232])
def dyn(mf,df,Dc):
    a=q(mf); b=q(df)
    ch=(a!=Mc).any(2)|(b!=Dc).any(2)
    st=(Mc!=Dc).any(2)
    return (a!=b).any(2) & (ch | ~st)
_masks=pickle.load(open('/tmp/selmasks.pkl','rb')); _ov=pickle.load(open('/tmp/selov2.pkl','rb'))[1]
NAMES=['Savage','Hogan','Warrior','Honky','Duggan','BigBoss']
def state(img):
    a=q(img); s=''
    for n in NAMES:
        m=_masks[n][8:232]; v=a[m]; vals,cn=np.unique(v[:,0]*64+v[:,1]*8+v[:,2],return_counts=True); c=vals[cn.argmax()]
        s+={3*64+3*8+7:'A',7*64+7:'M',7*8:'V'}.get(int(c),'?')
    cur=[]
    for (pl,n),(m,im) in _ov.items():
        mm=m[8:232]
        if (a[mm]==q(im[8:232])[mm]).all(): cur.append(pl+n)
    return s,' '.join(sorted(cur))
def timeline(fr):
    out=[];p=None
    for k in sorted(fr):
        s=state(fr[k])
        if s!=p: out.append((k,)+s); p=s
    return out
