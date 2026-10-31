import sys; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
from PIL import Image
seq=[(30,()),(200,('LEFT','UP')),(20,()),(300,('RIGHT','DOWN')),(20,()),(150,('LEFT',)),(60,('UP',)),(170,('LEFT','DOWN')),(400,('RIGHT','UP')),(100,('DOWN',)),(90,('LEFT',)),(20,())]
def boot(c):
    for f in range(120):
        c.run(1); a=np.array(c.image().convert('RGB'))
        if a.shape[0]>=224 and (a[100:120]>0).mean()>0.5: return
def shots(rom,reg,save=None):
    c=Core(rom,{b'genesis_plus_gx_region_detect':reg.encode()}); boot(c); out=[]
    for si,(n,p) in enumerate(seq):
        for k in range(n):
            c.run(1,pad0=p); out.append(np.array(c.image().convert('RGB')))
        if save and si in (0,2,4): c.shot('%s_%s_%s.png'%(save,reg,{0:'centre',2:'leftup',4:'rightdown'}[si]))
    r=c.ram_bytes(); return out,((r[0x70]<<24|r[0x71]<<16|r[0x72]<<8|r[0x73]), r[0x6e]<<8|r[0x6f])
if __name__=='__main__':
  for reg in ('ntsc-u','pal'):
    a,_=shots('WWF_SGDK_s01.bin',reg); b,dm=shots('WWF_SGDK_s02.bin',reg,'s02')
    d=[int((x!=y).any(2).sum()) for x,y in zip(a,b)]
    print(reg,'frames',len(d),'differing',sum(1 for v in d if v),'max px',max(d),'dmaMax bytes, vcMax',dm, [i for i,v in enumerate(d) if v][:10])
