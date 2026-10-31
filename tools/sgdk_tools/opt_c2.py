import pickle,numpy as np,random
subs,W,R=pickle.load(open('subs_c.pkl','rb'))
LV=np.array([0,34,68,102,136,170,204,238])
def rgb(c): return np.array([LV[c&7],LV[(c>>3)&7],LV[c>>6]])
MAT=0+8*3+64*6
C=np.unique(subs); C=C[C!=MAT]; idx={c:i for i,c in enumerate(C)}
H0=np.zeros((len(subs),len(C)))
for i,s in enumerate(subs):
    for c in s:
        if c!=MAT: H0[i,idx[c]]+=1
H=H0*(W*np.where(R,8.0,1.0))[:,None]; H0=H0*W[:,None]
CANDS=np.arange(512)
D=((np.array([rgb(c) for c in C])[:,None,:]-np.array([rgb(c) for c in CANDS])[None,:,:])**2).sum(2).astype(float)
def lerr(Hs,P): return Hs@D[:,P].min(1)
def refine(h,L):
    L=list(L); base=h@D[:,L].min(1)
    while True:
        imp=False
        for k in range(15):
            others=[L[j] for j in range(15) if j!=k]; mo=D[:,others].min(1)
            e=h@np.minimum(mo[:,None],D)          # every candidate at slot k
            c=int(e.argmin())
            if e[c]<base-1e-6: L[k]=c; base=e[c]; imp=True
        if not imp: return L,base
def run(P0,P1):
    for it in range(15):
        A=lerr(H,P1)<lerr(H,P0)
        P0,_=refine(H[~A].sum(0),P0); P1,_=refine(H[A].sum(0),P1)
    return float(np.minimum(lerr(H,P0),lerr(H,P1)).sum()),P0,P1
order=np.argsort(-H.sum(0)); best=None; random.seed(1)
for r in range(16):
    if r==0: a=list(C[order[:15]]); b=list(C[order[15:30]])
    else: p=list(C); random.shuffle(p); a=p[:15]; b=p[15:30]
    e,a,b=run(a,b); print('restart',r,'%.4g'%e)
    if best is None or e<best[0]: best=(e,a,b)
e,P0,P1=best
pickle.dump((P0,P1),open('quant_c.pkl','wb'))
A=lerr(H,P1)<lerr(H,P0)
E=np.where(A[:,None],D[:,P1].min(1)[None,:],D[:,P0].min(1)[None,:])**.5
px=H0.sum(0); err=(H0*E).sum(0)/np.maximum(px,1)
print('mean err (all px, 8-bit dist):',round(float((H0*E).sum()/px.sum()),2))
for j in np.argsort(-px):
    if err[j]>0.5: print('  ',tuple(int(x) for x in rgb(C[j])),'px',int(px[j]),'mean err',round(float(err[j]),1))
print('P0',[tuple(int(x) for x in rgb(c)) for c in P0]); print('P1',[tuple(int(x) for x in rgb(c)) for c in P1])
