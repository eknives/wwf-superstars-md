import sys,struct; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
rom=sys.argv[1]
IDX=np.load('../tools/idx_s03.npy'); H,Wd=IDX.shape
cr=struct.unpack('>32H',open('../res/pal.bin','rb').read()[:64])
LUT=np.array([[((v>>1)&7)*36,((v>>5)&7)*36,((v>>9)&7)*36] for v in cr],np.uint8)
MASK=np.zeros_like(IDX,bool); q=np.frombuffer(open('../res/anim.bin','rb').read(),'>u2'); i=0
while i<len(q):
  c0,r0,n=q[i],q[i+1],q[i+2]; MASK[r0*8:r0*8+64,c0*8:c0*8+64]=True; i+=3+n*64
def s(v): return v-65536 if v>32767 else v
tot=0
for reg in sys.argv[2:]:
  hh=224
  for name,seq in [('up',[(400,('DOWN',)),(500,('UP',))]),('down',[(400,('UP',)),(500,('DOWN',))]),('dl',[(300,('RIGHT','UP')),(500,('LEFT','DOWN'))]),('ur',[(300,('LEFT','DOWN')),(500,('RIGHT','UP'))]),('ul',[(300,('RIGHT','DOWN')),(500,('LEFT','UP'))]),('dr',[(300,('LEFT','UP')),(500,('RIGHT','DOWN'))])]:
    c=Core(rom,{b'genesis_plus_gx_region_detect':reg.encode()}); c.run(60); bad=0; first=None
    for n,p in seq:
      for f in range(n):
        c.run(1,pad0=p); v=bytes(c.vram_bytes()[:65536])
        hs=s(struct.unpack('>H',v[0xDC02:0xDC04])[0]); vs=s(c.vsram_words()[1]&0x7ff if False else c.vsram_words()[1])
        img=np.array(c.image())[:hh,:256,:3]
        x0=-hs; y0=vs
        ys=np.r_[48:200,219:hh]; xs=(np.arange(256)+x0)
        if ys[0]+y0<0 or ys[-1]+y0>=H or xs[0]<0 or xs[-1]>=Wd: continue
        exp=LUT[IDX[ys[:,None]+y0,xs[None,:]]]; m=~MASK[ys[:,None]+y0,xs[None,:]]
        d=(np.abs(img[ys].astype(int)-exp).max(2)>40)&m
        cmpd=globals().get("cmpd",0)+1; globals()["cmpd"]=cmpd
        if d.sum():
          bad+=1
          if first is None: yy,xx=np.nonzero(d); first=(f,p,hs,vs,int(d.sum()),int(ys[yy.min()]),int(ys[yy.max()])); c.shot('glitch_%s_%s.png'%(reg,name))
    print(reg,name,"badframes",bad,"first",first,"compared",globals().get("cmpd",0)); tot+=bad
print('TOTAL',tot)
