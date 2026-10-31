import pickle,numpy as np,collections
states,blk,imgs,uses=pickle.load(open('world_states.pkl','rb'))
subs=[];W=[]
for e,im in imgs.items():
    q=im[...,0]+8*im[...,1]+64*im[...,2]
    for sy in (0,8):
        for sx in (0,8): subs.append(q[sy:sy+8,sx:sx+8]); W.append(uses[e])
subs=np.array(subs); W=np.array(W,float)
H=np.zeros((len(subs),512)); 
for i,s in enumerate(subs): H[i]=np.bincount(s.ravel(),minlength=512)*W[i]
cols=np.array([[c&7,(c>>3)&7,c>>6] for c in range(512)],float)
tot=H.sum(0); order=np.argsort(-tot)
print('distinct',int((tot>0).sum()))
BLACK=0
def fitline(h,init):
    P=init.copy()
    used=np.nonzero(h)[0]
    for it in range(20):
        d=((cols[used][:,None,:]-cols[P][None,:,:])**2).sum(2); a=d.argmin(1)
        for k in range(len(P)):
            if P[k]==BLACK: continue
            m=a==k
            if not m.any(): continue
            w=h[used][m]; c=(cols[used][m]*w[:,None]).sum(0)/w.sum()
            # snap to nearest existing colour used (keeps exact colours)
            cand=used[m]; P[k]=cand[((cols[cand]-c)**2).sum(1).argmin()]
    return P
def err(h,P):
    used=np.nonzero(h)[0]; d=((cols[used][:,None,:]-cols[P][None,:,:])**2).sum(2).min(1); return (d*h[used]).sum()
# init: line0 top-15 colours of cells, line1 next
top=[c for c in order if tot[c]>0]
P0=np.array([BLACK]+[c for c in top if c!=BLACK][:14]); P1=np.array([BLACK]+[c for c in top if c!=BLACK][14:28])
for it in range(12):
    e0=np.array([err(h,P0) for h in H]) if it==0 else None
    E0=np.array([err(h,P0) for h in H]); E1=np.array([err(h,P1) for h in H]); A=E1<E0
    P0=fitline(H[~A].sum(0),P0); P1=fitline(H[A].sum(0),P1)
    print(it,'err',float(np.minimum(E0,E1).sum()),'cells line1',int(A.sum()))
pickle.dump((P0,P1),open('quant.pkl','wb'))
print([tuple(cols[c].astype(int)) for c in P0]); print([tuple(cols[c].astype(int)) for c in P1])
