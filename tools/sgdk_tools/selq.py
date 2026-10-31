# s05b: cuantizacion pantalla de seleccion a 4x15 (planos B + cursores en A)
import numpy as np, pickle, itertools, sys
Crgb,o2,win=pickle.load(open('/tmp/selov2.pkl','rb'))
q=lambda v:np.minimum(7,(np.asarray(v)/34+0.5).astype(int))
C=q(Crgb[8:232].astype(int))                     # 224x256x3 md3
cells={'Savage':(2,4),'Hogan':(12,2),'Warrior':(22,4),'Honky':(2,16),'Duggan':(12,18),'BigBoss':(22,16)}
names=list(cells)
AZ=np.array(q([102,102,255]))
key=lambda a:a[...,0]*64+a[...,1]*8+a[...,2]
K=key(C)
CUR0=[48,56,316,480,488,504]
cols=np.unique(np.concatenate([K.ravel(),CUR0])); ci={c:i for i,c in enumerate(cols)}
rgb=np.stack([cols//64,(cols//8)%8,cols%8],1).astype(float)
D=((rgb[:,None]-rgb[None])**2).sum(2)          # colour distance
# bg mask per cell (azul inside cell window, md coords)
bgcell=-np.ones((224,256),int)
for k,n in enumerate(names):
    tx,ty=cells[n]; y0=ty*8-8; x0=tx*8
    m=(K[y0:y0+72,x0:x0+64]==key(AZ)); bgcell[y0:y0+72,x0:x0+64][m]=k
W=np.ones((224,256))
for n,(tx,ty) in cells.items(): W[ty*8:ty*8+64,tx*8:tx*8+64]=4.0   # caras/retratos
# cursor colours
cur=set()
for (pl,n),(m,img) in o2.items():
    if n=='Savage':
        for c in map(tuple,img[m]): cur.add(int(key(q(np.array(c)))))
cur=sorted(cur); print('cursor md3',cur)
# tiles
T=[]
for ty in range(28):
    for tx in range(32):
        sl=(slice(ty*8,ty*8+8),slice(tx*8,tx*8+8))
        idx=np.vectorize(ci.get)(K[sl]).ravel(); bc=bgcell[sl].ravel(); w=W[sl].ravel()
        cells_in=set(bc[bc>=0].tolist())
        h=np.zeros(len(cols))
        for i,ww,b in zip(idx,w,bc):
            if b<0: h[i]+=ww
        T.append((h,cells_in))
NT=len(T); H=np.stack([t[0] for t in T])
def tilecost(h,pal):  # pal: list colour indices
    if not pal: return 1e9
    return (h[:,None]*D[:, pal]).min(1).sum() if h.ndim==1 else None
def choose(hist,n,forced):
    sel=list(forced)
    while len(sel)<n:
        best=None
        for c in range(len(cols)):
            if c in sel: continue
            s=sel+[c]; e=(hist*D[:,s].min(1)).sum()
            if best is None or e<best[0]: best=(e,c)
        if best[0]>=(hist*D[:,sel].min(1)).sum() if sel else False: break
        sel.append(best[1])
    # swap refine
    imp=True
    while imp:
        imp=False; e0=(hist*D[:,sel].min(1)).sum()
        for j in range(len(forced),len(sel)):
            for c in range(len(cols)):
                if c in sel: continue
                s=sel.copy(); s[j]=c; e=(hist*D[:,s].min(1)).sum()
                if e<e0-1e-9: sel=s; e0=e; imp=True
    return sel
def run(assign,curpal,iters=6):
    nbg=[sum(1 for k in range(6) if assign[k]==p) for p in range(4)]
    allowed=[]
    for h,cs in T:
        a=set(range(4))
        for k in cs: a&={assign[k]}
        allowed.append(sorted(a))
    # init: by allowed, else round robin by dominant colour
    tp=np.array([al[0] if len(al)==1 else (i%4) for i,al in enumerate(allowed)])
    for it in range(iters):
        pals=[]
        for p in range(4):
            hist=H[tp==p].sum(0)
            forced=[ci[c] for c in cur] if p==curpal else []
            forced=[f for f in forced]
            pals.append(choose(hist,15-nbg[p],forced))
        cost=np.array([[ (H[i]*D[:,pals[p]].min(1)).sum() if p in allowed[i] else 1e18 for p in range(4)] for i in range(NT)])
        ntp=cost.argmin(1); tot=cost.min(1).sum()
        if (ntp==tp).all(): break
        tp=ntp
    return tot,tp,pals
if __name__=='__main__':
    best=None
    for pair1 in itertools.combinations(range(6),2):
        rest=[k for k in range(6) if k not in pair1]
        for pair2 in itertools.combinations(rest,2):
            if pair2<pair1: continue
            singles=[k for k in rest if k not in pair2]
            for order in (singles,singles[::-1]):
                a=[0]*6
                for k in pair1: a[k]=0
                for k in pair2: a[k]=1
                a[order[0]]=2; a[order[1]]=3
                tot,tp,pals=run(a,3,iters=3)
                if best is None or tot<best[0]: best=(tot,a); print(tot,a,flush=True)
    tot,tp,pals=run(best[1],3,iters=12)
    print('final',tot,best[1])
    pickle.dump(dict(assign=best[1],tp=tp,pals=pals,cols=cols,cells=cells,names=names,cur=cur,bgcell=bgcell),open('/tmp/selq.pkl','wb'))
