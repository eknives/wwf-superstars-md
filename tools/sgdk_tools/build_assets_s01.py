import numpy as np,struct,sys
sys.argv=['x']
from rend import tiles,D
import numpy as np
OUT='/workspace/wwf_sgdk/res/'
I=np.load('bgidx.npy'); R0=np.load('ropeidx.npy'); R=np.where(R0>0, np.where(I==0,1,I), 0).astype(np.uint8)
cram=struct.unpack('>32H',open(D+'ring_cram.bin','rb').read()[:64])
MAT=18
rgb=lambda m:np.array([m>>1&7,m>>5&7,m>>9&7])
def enc(t):
    b=bytearray()
    for row in t:
        for x in range(0,8,2): b.append((int(row[x])<<4)|int(row[x+1]))
    return bytes(b)
class TS:
    def __init__(s,base): s.base=base; s.d={}; s.l=[]
    def add(s,t):  # t: 8x8 values 0..15
        for fl,(tt) in ((0,t),(0x800,t[:,::-1]),(0x1000,t[::-1]),(0x1800,t[::-1,::-1])):
            k=enc(tt)
            if k in s.d: return s.d[k]|fl
        s.d[enc(t)]=s.base+len(s.l); s.l.append(enc(t)); return s.base+len(s.l)-1
    def blob(s): return b''.join(s.l)
def cell(img,r,c): return img[r*8:r*8+8,c*8:c*8+8]
# --- plane B: world 64x64, only rows 11..49 kept (camera range rows 12..48 + margin)
ts=TS(1); mapB=[0]*4096
for r in range(11,50):
    for c in range(64):
        x=cell(I,r,c)
        if (x==MAT).all(): continue
        pl=1 if x.max()>=16 else 0
        if ((x>0)&(x<16)).any() and pl: raise SystemExit('mixed')
        v=np.where(x==0, 4 if pl else 1, x-16*pl)
        mapB[r*64+c]=ts.add(v.astype(np.uint8))|(pl<<13)
nB=len(ts.l)
# --- plane A ropes: world rows 18..45 -> plane rows mod 32, 64x32, HIGH priority
ta=TS(1+nB); mapA=[0]*4096; rr=set()
for r in range(64):
    for c in range(64):
        x=cell(R,r,c)
        if not x.any(): continue
        rr.add(r)
        pl=1 if x.max()>=16 else 0
        v=np.where(x==0,0,x-16*pl)
        if pl and ((x>0)&(x<16)).any():
            # mixed-line cell: map line0 px to nearest line1 colour
            pass
        if pl and ((x>0)&(x<16)).any():
            for g in set(x[(x>0)&(x<16)].ravel()):
                k=min(range(1,16),key=lambda i:((rgb(cram[16+i])-rgb(cram[g]))**2).sum()); v[x==g]=k
            print('mixed rope cell',r,c,'L0 px -> nearest L1')
        mapA[r*64+c]=ta.add(v.astype(np.uint8))|(pl<<13)|0x8000
print('rope rows',min(rr),max(rr))
nA=len(ta.l)
open(OUT+'bgb_tiles.bin','wb').write(ts.blob()); open(OUT+'bgb_map.bin','wb').write(struct.pack('>4096H',*mapB))
open(OUT+'ropa_tiles.bin','wb').write(ta.blob()); open(OUT+'ropa_map.bin','wb').write(struct.pack('>4096H',*mapA))
# --- HUD from v30 plane A (arcade fg), colours nearest into the 2 fixed lines
H=np.load('/workspace/wwf_sgdk/ref/hudidx.npy')
v30=struct.unpack('>64H',open('/workspace/wwf_sgdk/ref/v30_cram.bin','rb').read())
md=[((x&7)<<1)|(((x>>3)&7)<<5)|(((x>>6)&7)<<9) for x in v30]
rgb=lambda m:np.array([m>>1&7,m>>5&7,m>>9&7])
def near(col,line):
    best=min(range(1,16),key=lambda i:((rgb(cram[line*16+i])-rgb(col))**2).sum())
    return best,((rgb(cram[line*16+best])-rgb(col))**2).sum()**.5
# line choice: line 1 holds e80/ccc/aee, line0 has 00a/0ae/888; choose per cell the best line
errs={}
def hudcell(src):
    best=None
    for line in (0,1):
        m={};e=0
        for v in set(src.ravel())-{0}:
            m[v],ee=near(md[v],line); e=max(e,ee)
        if best is None or e<best[0]: best=(e,line,m)
    e,line,m=best
    out=np.zeros_like(src)
    for v,k in m.items(): out[src==v]=k; errs[md[v]]=max(errs.get(md[v],0),((rgb(cram[line*16+k])-rgb(md[v]))**2).sum()**.5)
    return out,line
# top HUD: plane y 8..39 is visible arcade band -> window, shifted so arcade line 8 lands at screen y=10 ; band black from 0
SH=10
top=np.zeros((48,256),np.uint8); top[:,:]=0
top[0:SH+32]=1  # black band (v30 line0 idx1 = 000)
top[SH:SH+32]=H[8:40,0:256]
tw=TS(1+nB+nA); mapW=[0]*(32*6)
for r in range(6):
    for c in range(32):
        x=cell(top,r,c)
        if not x.any(): continue
        o,line=hudcell(x)
        if not o.any() and x.any(): o=np.where(x>0,1,0).astype(np.uint8)  # black -> line idx1 black
        mapW[r*32+c]=tw.add(o.astype(np.uint8))|(line<<13)|0x8000
nW=len(tw.l)
open(OUT+'win_tiles.bin','wb').write(tw.blob()); open(OUT+'win_map.bin','wb').write(struct.pack('>192H',*mapW))
# bottom HUD sprites: plane y 224..239, x 56..231 -> 5x(32x16) + 1x(16x16); sprite tiles column-major
bot=H[224:240,56:232].copy()
sprt=[];spr=[];base=1+nB+nA+nW
x=0
for w in (4,4,4,4,4,2):
    blk=bot[:,x*8:(x+w)*8]; o,line=hudcell(blk)
    spr.append((x*8,w,line,base+len(sprt)))
    for cx in range(w):
        for cy in range(2): sprt.append(enc(o[cy*8:cy*8+8,cx*8:cx*8+8]))
    x+=w
open(OUT+'hud_spr_tiles.bin','wb').write(b''.join(sprt))
pal=list(cram)
open(OUT+'pal.bin','wb').write(struct.pack('>32H',*pal))
with open(OUT+'layout.h','w') as f:
    f.write('#define NB %d\n#define NA %d\n#define NW %d\n#define NSPRT %d\n#define TB 1\n#define TA %d\n#define TW %d\n#define TS %d\n#define MAT_IDX %d\n'%(nB,nA,nW,len(sprt),1+nB,1+nB+nA,base,MAT))
    f.write('static const u16 hudspr[6][4]={'+','.join('{%d,%d,%d,%d}'%s for s in spr)+'};\n')
print('B',nB,'A',nA,'W',nW,'S',len(sprt),'total',base+len(sprt))
print('hud colour err (3-bit levels):',{('%03x'%k):round(v,2) for k,v in errs.items()})
