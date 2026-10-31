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
import struct as S
sym={l.split()[-1]:int(l.split()[0],16) for l in open('symbol.txt') if len(l.split())==3}
def tl(fn):
    T=np.frombuffer(open(fn,'rb').read(),np.uint8).reshape(-1,8,4); return np.stack([T>>4,T&15],-1).reshape(-1,8,8)
TB=tl('../res/bgb_tiles.bin'); TA_=tl('../res/ropa_tiles.bin')
AM=np.array(S.unpack('>%dH'%(80*68),open('../res/ropa_map.bin','rb').read())).reshape(68,80)
def cellpix(t,fh,fv,pl):
    if fh: t=t[:,::-1]
    if fv: t=t[::-1]
    return np.where(t>0,t+16*pl,0)
def world_from_ram(r,VX,VY):
    p=S.unpack('>I',bytes(r[sym['wram']&0xffff:][:4]))[0]&0xffff
    wm=np.array(S.unpack('>%dH'%(80*68),bytes(r[p:p+80*68*2]))).reshape(68,80)
    img=np.full((68*8,80*8),2,np.uint8)
    for rr in range(max(0,VY//8),min(68,VY//8+30)):
      for cc in range(max(0,VX//8),min(80,VX//8+34)):
        sub=img[rr*8:rr*8+8,cc*8:cc*8+8]; e=wm[rr,cc]
        if e&0xfff:
          px=cellpix(TB[(e&0xfff)-1],e&0x1000,e&0x2000,(e>>14)&1); sub[px>0]=px[px>0]
        a=AM[rr,cc]
        if a:
          px=cellpix(TA_[(a&0x7ff)-1],a&0x800,a&0x1000,(a>>13)&1); sub[px>0]=px[px>0]
    return img
tot=0
for reg in sys.argv[2:]:
  hh=224
  for name,seq in [('up',[(400,('DOWN',)),(500,('UP',))]),('down',[(400,('UP',)),(500,('DOWN',))]),('dl',[(300,('RIGHT','UP')),(500,('LEFT','DOWN'))]),('ur',[(300,('LEFT','DOWN')),(500,('RIGHT','UP'))]),('ul',[(300,('RIGHT','DOWN')),(500,('LEFT','UP'))]),('dr',[(300,('LEFT','UP')),(500,('RIGHT','DOWN'))])]:
    c=Core(rom,{b'genesis_plus_gx_region_detect':reg.encode()}); c.run(60); bad=0; first=None
    for n,p in seq:
      for f in range(n):
        globals()['PR']=bytes(c.ram_bytes()); c.run(1,pad0=p); v=bytes(c.vram_bytes()[:65536])
        hs=s(struct.unpack('>H',v[0xDC02:0xDC04])[0]); vs=s(c.vsram_words()[1]&0x7ff if False else c.vsram_words()[1])
        img=np.array(c.image())[:hh,:256,:3]
        x0=-hs; y0=vs
        ys=np.r_[48:200,219:hh]; xs=(np.arange(256)+x0)
        if ys[0]+y0<0 or ys[-1]+y0>=H or xs[0]<0 or xs[-1]>=Wd: continue
        rr_=globals().get('PR') or c.ram_bytes(); WI=world_from_ram(rr_,x0,y0); exp=LUT[WI[ys[:,None]+y0,xs[None,:]]]; m=np.ones_like(exp[...,0],bool)
        d=(np.abs(img[ys].astype(int)-exp).max(2)>40)&m
        cmpd=globals().get("cmpd",0)+1; globals()["cmpd"]=cmpd
        if d.sum():
          bad+=1
          if first is None: yy,xx=np.nonzero(d); first=(f,p,hs,vs,int(d.sum()),int(ys[yy.min()]),int(ys[yy.max()])); c.shot('glitch_%s_%s.png'%(reg,name))
    print(reg,name,"badframes",bad,"first",first,"compared",globals().get("cmpd",0)); tot+=bad
print('TOTAL',tot)
