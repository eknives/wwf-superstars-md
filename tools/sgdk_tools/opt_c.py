import pickle,numpy as np
subs,W,R=pickle.load(open('subs_c.pkl','rb'))
LV=np.array([0,34,68,102,136,170,204,238])     # approx MD output (GPGX 0..238)
def rgb(c): return np.array([LV[c&7],LV[(c>>3)&7],LV[c>>6]])
MAT=0+8*3+64*6        # (0,3,6) mat
C=np.unique(subs); C=C[C!=MAT]
cand=np.arange(512)
idx={c:i for i,c in enumerate(C)}
H=np.zeros((len(subs),len(C)))
for i,s in enumerate(subs):
    for c in s:
        if c!=MAT: H[i,idx[c]]+=1
WT=W*np.where(R,8.0,1.0)
H*=WT[:,None]
D=((np.array([rgb(c) for c in C])[:,None,:]-np.array([rgb(c) for c in cand])[None,:,:])**2).sum(2).astype(float)  # C x 512
def line_err(Hs,P):   # Hs: n x C, P list of cand ids -> per-sub error
    m=D[:,P].min(1); return Hs@m
tot=H.sum(0); order=np.argsort(-tot)
P0=list(C[order[:15]]); P1=list(C[order[15:30]])
for it in range(8):
    E0=line_err(H,P0); E1=line_err(H,P1); A=E1<E0
    for L,mask in ((P0,~A),(P1,A)):
        h=H[mask].sum(0); improved=True
        while improved:
            improved=False; base=(h*D[:,L].min(1)).sum()
            for k in range(15):
                best=(base,None)
                for c in C:          # candidates: used colours (exact) only
                    if c in L: continue
                    t=L.copy(); t[k]=c; e=(h*D[:,t].min(1)).sum()
                    if e<best[0]-1e-6: best=(e,c)
                if best[1] is not None: L[k]=best[1]; base=best[0]; improved=True
    print(it,'weighted err',float(np.minimum(line_err(H,P0),line_err(H,P1)).sum()),'line1 subs',int(A.sum()))
pickle.dump((P0,P1),open('quant_c.pkl','wb'))
# per-colour report: lost colours (no exact slot reachable for their subtiles)
E0=D[:,P0].min(1); E1=D[:,P1].min(1)
H0=np.zeros((len(subs),len(C)))
for i,s in enumerate(subs):
    for c in s:
        if c!=MAT: H0[i,idx[c]]+=W[i]
A=line_err(H,P1)<line_err(H,P0)
e=np.where(A[:,None],E1[None,:],E0[None,:])**.5   # per (sub,colour) error
px=H0.sum(0); err=(H0*e).sum(0)/np.maximum(px,1)
print('colours with mean err>0 (8-bit rgb dist):')
for j in np.argsort(-px):
    if err[j]>0.5: print('  ',tuple(rgb(C[j])),'px',int(px[j]),'mean err',round(float(err[j]),1))
print('P0',[tuple(rgb(c)) for c in P0]); print('P1',[tuple(rgb(c)) for c in P1])
