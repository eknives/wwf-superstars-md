# s67 CROWD_ARC: arcade crowd lists -> res/crowdarc.bin + res/crowdarc_tiles.bin (ids NB+1..; base tiles/map untouched)
import pickle,numpy as np,struct,re
src=open('build_s03c.py').read(); exec(src[:src.index('# convert each arcade entry')])   # cols, LINES, quant_sub, MATQ
from world_img import AX0,AY0,AW,AH
I3,_=pickle.load(open('imgs_c.pkl','rb'))
OUT='/workspace/wwf_sgdk/res/'
NB=int(re.search(r'#define NB (\d+)',open(OUT+'layout.h').read()).group(1))
MW,MH=AW*2,AH*2; VIS_R0,VIS_R1=1,67
def enc(t):
    b=bytearray()
    for row in t:
        for x in range(0,8,2): b.append((int(row[x])<<4)|int(row[x+1]))
    return bytes(b)
T=open(OUT+'bgb_tiles.bin','rb').read(); assert len(T)==NB*32
d={T[i*32:i*32+32]:i+1 for i in range(NB)}; new=[]
MAXNEW=4095-NB
EX=np.array([[ (b>>(4*(1-(x&1))))&15 for b in T[i*32:i*32+32] for x in (0,1)] for i in range(NB)],np.uint8)   # (NB,64) idx
EXF=[EX, EX.reshape(-1,8,8)[:,:,::-1].reshape(-1,64), EX.reshape(-1,8,8)[:,::-1].reshape(-1,64), EX.reshape(-1,8,8)[:,::-1,::-1].reshape(-1,64)]
PC=[np.vstack([[0,3,6],cols[np.array(P)]]).astype(np.int32) for P in LINES]   # idx0 = mat backdrop
subst={}; nsub=[0]; suberr=[]
def mdentry(l,ix):
    if (ix==0).all(): return 0
    for fl,tt in ((0,ix),(1,ix[:,::-1]),(2,ix[::-1]),(3,ix[::-1,::-1])):
        k=enc(tt)
        if k in d: return d[k]|(fl<<12)|(l<<14)
    k=(l,enc(ix))
    if k in subst: nsub[0]+=1; return subst[k]
    new.append(enc(ix)); d[enc(ix)]=NB+len(new); return (NB+len(new))|(l<<14)
def plan(cands):   # cands: {(l,enc): (ix,uses)} -> substitute the closest-matching ones by existing tiles until <= MAXNEW remain
    sc=[]
    for (l,k),(ix,u) in cands.items():
        c=PC[l][ix.ravel()]; best=(1<<30,0,0)
        for fl in range(4):
            e=((PC[l][EXF[fl]]-c[None])**2).sum((1,2)); i=int(e.argmin())
            if e[i]<best[0]: best=(int(e[i]),i+1,fl)
        sc.append((best[0],(l,k),best))
    sc.sort(key=lambda x:x[0]); nkeep=MAXNEW-8+int(__import__("os").environ.get("XK","140")); nsubst=max(0,len(sc)-nkeep)
    for err,key,(e,i,fl) in sc[:nsubst]: subst[key]=i|(fl<<12)|(key[0]<<14); suberr.append(err/64)
    print('candidates',len(sc),'substituted',nsubst,'max/mean err per px (sq levels)',max(suberr or [0]),sum(suberr)/max(1,len(suberr)))
CA=pickle.load(open('crowdarc_src.pkl','rb')); conv={}
def cv(e):
    if e not in conv:
        im=I3[e] if e in I3 else CA['new'][e]; q=im[...,0]+8*im[...,1]+64*im[...,2]
        conv[e]=[quant_sub(q[sy:sy+8,sx:sx+8])[1:] for sy in (0,8) for sx in (0,8)]
    return conv[e]
lists=[CA['crowd'][(z,s3,ph)] for z in range(3) for s3 in range(4) for ph in range(3)]+[CA['fence'][(z,s)] for z in range(3) for s in range(2)]+[CA['small'][(r,s)] for r in range(4) for s in range(2)]
cands={}
for li in lists:
    for (tx,ty),e in li:
        if not (AX0<=tx<AX0+AW and AY0<=ty<AY0+AH): continue
        for k,(l,ix) in enumerate(cv(e)):
            if (ix==0).all() or any(enc(tt) in d for tt in (ix,ix[:,::-1],ix[::-1],ix[::-1,::-1])): continue
            kk=(l,enc(ix)); cands[kk]=(ix,cands.get(kk,(0,0))[1]+1)
plan(cands)
offs=[];body=[]
for li in lists:
    offs.append(len(body)//3); seen={}
    for (tx,ty),e in li:
        if not (AX0<=tx<AX0+AW and AY0<=ty<AY0+AH): continue
        for k,(l,ix) in enumerate(cv(e)):
            r=(ty-AY0)*2+k//2; c=(tx-AX0)*2+k%2
            if VIS_R0<=r<=VIS_R1: seen[r*MW+c]=mdentry(l,ix)
    for m in sorted(seen):
        r,c=divmod(m,MW)
        if 18<=r<18+28 and (12<=c<20 or 52<=c<60): continue   # s67 opt: rope B cells (FX_R0/FX_NR) never written by caApply -> left out of the list
        body+=[(r<<7)|c,m*2,seen[m]]   # s67 opt: 3 words (key, wram byte offset, entry): no multiply in caApply
offs.append(len(body)//3)
assert NB+len(new)<4096
open(OUT+'crowdarc.bin','wb').write(struct.pack('>%dH'%len(offs),*offs)+struct.pack('>%dH'%len(body),*body))
open(OUT+'crowdarc_tiles.bin','wb').write(b''.join(new) or b'\0'*32)
open(OUT+'crowdarc.h','w').write('#define NCA %d\n#define CA_NL %d\n'%(len(new),len(lists)))
print('NB',NB,'new tiles',len(new),'lists',len(lists),'cells',len(body)//2)
# s67 test aid: arcade key -> 4 MD entries (as written in the lists), zone cell sets
KM={}
for li in lists:
    for (tx,ty),e in li: KM[e]=[mdentry(l,ix) for l,ix in cv(e)]
pickle.dump(dict(KM=KM,NB=NB),open('/tmp/crowd/km.pkl','wb'))
