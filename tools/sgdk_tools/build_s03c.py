import pickle,numpy as np,struct,collections
from world_img import states,blk,imgs,uses,base_entry,AX0,AY0,AW,AH
OUT='/workspace/wwf_sgdk/res/'
P0,P1=pickle.load(open('quant_c.pkl','rb'))
I3,I8=pickle.load(open('imgs_c.pkl','rb')); imgs=I3
cols=np.array([[c&7,(c>>3)&7,c>>6] for c in range(512)])
LINES=[P0,P1]
cram=[0]*32
for l,P in enumerate(LINES):
    for i,c in enumerate(P): r,g,b=cols[c]; cram[l*16+1+i]=(b<<9)|(g<<5)|(r<<1)
cram[0]=(6<<9)|(3<<5)|(0<<1)   # backdrop = mat colour, CRAM 0 (never a pixel colour)
MATC=(0,3,6); MAT=0; MATQ=0+8*3+64*6
print('MAT idx',MAT)
def quant_sub(q):  # q 8x8 in 512 space -> (line, idx 1..15), sq error
    best=None
    for l,P in enumerate(LINES):
        d=((cols[q.ravel()][:,None,:]-cols[P][None,:,:])**2).sum(2); a=d.argmin(1)+1; mm=q.ravel()==MATQ
        a[mm]=0; e=d.min(1)[~mm].sum()
        if best is None or e<best[0]: best=(e,l,a.reshape(8,8).astype(np.uint8))
    return best
# convert each arcade entry into 4 MD subcells (line,idx)
conv={}; toterr=0; npx=0
for e,im in imgs.items():
    q=im[...,0]+8*im[...,1]+64*im[...,2]; out=[]
    for sy in (0,8):
        for sx in (0,8):
            er,l,ix=quant_sub(q[sy:sy+8,sx:sx+8]); out.append((l,ix)); toterr+=er*uses[e]; npx+=64*uses[e]
    conv[e]=out
print('quant rms levels',(toterr/npx)**.5)
def enc(t):
    b=bytearray()
    for row in t:
        for x in range(0,8,2): b.append((int(row[x])<<4)|int(row[x+1]))
    return bytes(b)
class TS:
    def __init__(s,base): s.base=base; s.d={}; s.l=[]
    def add(s,t):
        for fl,tt in ((0,t),(0x800,t[:,::-1]),(0x1000,t[::-1]),(0x1800,t[::-1,::-1])):
            k=enc(tt)
            if k in s.d: return s.d[k]|fl
        s.d[enc(t)]=s.base+len(s.l); s.l.append(enc(t)); return s.base+len(s.l)-1
    def blob(s): return b''.join(s.l)
def cell(img,r,c): return img[r*8:r*8+8,c*8:c*8+8]
MW,MH=AW*2,AH*2      # 80 x 68 MD cells
VIS_R0,VIS_R1=1,67   # rows ever visible (arcade y -7..520 -> +16)
ts=TS(1)
def mdentry(l,ix):
    if (ix==0).all(): return 0
    for fl,tt in ((0,ix),(1,ix[:,::-1]),(2,ix[::-1]),(3,ix[::-1,::-1])):
        k=enc(tt)
        if k in ts.d: return ts.d[k]|(fl<<12)|(l<<14)
    ts.d[enc(ix)]=1+len(ts.l); ts.l.append(enc(ix)); return len(ts.l)|(l<<14)
IDX=np.zeros((MH*8,MW*8),np.uint8)   # global colour index image (base state)
wmap=[0]*(MW*MH)
for ty in range(AY0,AY0+AH):
    for tx in range(AX0,AX0+AW):
        e=base_entry(tx,ty)
        if e is None: continue
        for k,(l,ix) in enumerate(conv[e]):
            r=(ty-AY0)*2+k//2; c=(tx-AX0)*2+k%2
            IDX[r*8:r*8+8,c*8:c*8+8]=ix+16*l
            if VIS_R0<=r<=VIS_R1: wmap[r*MW+c]=mdentry(l,ix)
# animation blocks
anim=[]
for (bx,by),st in sorted(blk.items()):
    c0=(bx*4-AX0)*2; r0=(by*4-AY0)*2
    if r0+8<VIS_R0 or r0>VIS_R1: continue
    def dark(s):  # recorded fade/transition frame: mostly solid black subcells
        n=0
        for e in s:
            for l,ix in conv[e]:
                if (ix==ix[0,0]).all() and cram[l*16+int(ix[0,0])]==0: n+=1
        return n>=32
    st=[s for s in st if not dark(s)]
    if len(set(map(tuple,st)))<2: continue
    S=[]
    for s in st:
        ent=[0]*64
        for j in range(4):
            for i in range(4):
                for k,(l,ix) in enumerate(conv[s[j*4+i]]):
                    rr=j*2+k//2; cc=i*2+k%2
                    if VIS_R0<=r0+rr<=VIS_R1: ent[rr*8+cc]=mdentry(l,ix)
        S.append(ent)
    anim.append((c0,r0,S))
nB=len(ts.l)
print('B tiles (base+anim variants)',nB,'anim blocks',len(anim),'states',sum(len(a[2]) for a in anim))
open(OUT+'bgb_tiles.bin','wb').write(ts.blob()); open(OUT+'bgb_map.bin','wb').write(struct.pack('>%dH'%len(wmap),*wmap))
ab=bytearray()
for c0,r0,S in anim:
    ab+=struct.pack('>HHH',c0,r0,len(S))
    for ent in S: ab+=struct.pack('>64H',*ent)
open(OUT+'anim.bin','wb').write(ab)
# ropes: ring_names coords + (32,16)
R0=np.load('ropeidx.npy'); M=np.zeros_like(IDX,bool); M[16:16+512,32:32+512]=R0>0
ta=TS(1); fold=[0]*(MW*MH)
for r in range(MH):
    for c in range(MW):
        m=cell(M,r,c)
        if not m.any(): continue
        x=cell(IDX,r,c); l=int(x.max()>=16); v=np.where(m,x-16*l,0).astype(np.uint8)
        fold[r*MW+c]=ta.add(v)|(l<<13)|0x8000
nA=len(ta.l)
open(OUT+'ropa_tiles.bin','wb').write(ta.blob()); open(OUT+'ropa_map.bin','wb').write(struct.pack('>%dH'%len(fold),*fold))
np.save('idx_s03.npy',IDX)
# HUD: reuse s01/s02 HUD code with the new palette
src=open('build_assets.py').read(); hud=src[src.index('# --- HUD'):src.index("pal=list(cram)")]
g=dict(np=np,struct=struct,TS=TS,enc=enc,cell=cell,OUT=OUT,cram=cram); exec(hud,g)
open(OUT+'pal.bin','wb').write(struct.pack('>32H',*cram))
with open(OUT+'layout.h','w') as f:
    f.write('#define NB %d\n#define NA %d\n#define NW %d\n#define NSPRT %d\n#define TA 1\n#define TW 1920\n#define TS %d\n#define MAT_IDX %d\n#define MW %d\n#define MH %d\n#define NANIM %d\n'%(nB,nA,g['nW'],len(g['sprt']),g['base'],MAT,MW,MH,len(anim)))
    f.write('static const u16 hudspr[6][4]={'+','.join('{%d,%d,%d,%d}'%s for s in g['spr'])+'};\n')
print('A',nA,'W',g['nW'],'hud err',{('%03x'%k):round(float(v),2) for k,v in g['errs'].items()})
# pool need: max unique ids in resident rect over camera range (base + all anim states of blocks touching rect)
W2=np.array(wmap).reshape(MH,MW)&0xfff
amask=collections.defaultdict(set)
for c0,r0,S in anim:
    for ent in S:
        for k,v in enumerate(ent):
            if v&0xfff: amask[(r0+k//8,c0+k%8)].add(v&0xfff)
best=0
for voff,NR in ((8,31),(16,29)):
  for sx in range(-32,353,8):
    for sy in range(-15,274,4):
      c0=(sx+32)>>3; r0=(sy+voff+16)>>3
      s=set(W2[r0:r0+NR,c0:c0+33].ravel())-{0}
      best=max(best,len(s))
print('pool need (base)',best)
# camera reach table from known cells: for each sx (step 2), sy range whose view (PAL 240 lines, top=sy+8) is fully known
Wr=np.load('world_rgb.npy'); K=(Wr[...,0]>=0)
cs=np.cumsum(np.cumsum(np.pad(~K,((1,0),(1,0))),0),1)
def bad(x0,y0,w,h): return cs[y0+h,x0+w]-cs[y0,x0+w]-cs[y0+h,x0]+cs[y0,x0]
tab=[]
for sx in range(-32,353,2):
    ok=[sy for sy in range(-15,274) if bad(sx+32,sy+8+16,256,240)==0 and bad(sx+32,sy+16+16,256,224)==0]
    tab.append((min(ok),max(ok)) if ok else (999,-999))
print('reach', tab[0], tab[len(tab)//2], tab[-1], 'no-reach sx', sum(1 for t in tab if t[0]>t[1]))
open(OUT+'camtab.bin','wb').write(b''.join(struct.pack('>hh',*t) for t in tab))
