import numpy as np,struct
from arcdec import P,L,W,sb,poses
T=np.load('/workspace/wwf/port_35/sprtiles.npy')
def arc_spr(p):
    n=W(p); q=p+2; r=[]
    for k in range(n):
        pdx,pdy=sb(P[q]),sb(P[q+1]); d=L(q+2); q+=6
        typ=P[d]&1; cnt=P[d+1]; lay=L(d+2); mask=L(lay); xy=lay+2
        gfl=(P[d]&0xC)<<4
        c=W(d+6)
        for j in range(cnt):
            tall=(mask>>(31-j))&1
            lx,ly=sb(P[xy+2*j]),sb(P[xy+2*j+1])
            if typ==0: cw=W(d+6+2*j); code=cw&0x3fff; fl=((cw>>8)&0xC0)|gfl
            else: code=c&0x3fff; fl=gfl; c+=2 if tall else 1
            r.append((-(pdx+lx)-16, -(pdy+ly-(8 if tall else 0))-(32 if tall else 16), code, tall, fl))
    return r
def img(spr):
    if not spr: return None
    xs=[s[0] for s in spr]; ys=[s[1] for s in spr]
    x0,y0=min(xs),min(ys); w=max(xs)-x0+16; h=max(s[1]+(32 if s[3] else 16) for s in spr)-y0
    im=np.zeros((h,w),np.uint8)
    for x,y,code,tall,fl in spr:
        if tall: code&=~1
        efx=not fl&0x80; efy=fl&0x40
        tt=[T[code],T[code+1]] if tall else [T[code]]
        tt=[x[::-1] if efy else x for x in tt]; tt=[x[:,::-1] if efx else x for x in tt]
        if efy: tt=tt[::-1]
        t=np.vstack(tt)
        sub=im[y-y0:y-y0+t.shape[0],x-x0:x-x0+16]; m=t>0; sub[m]=t[m]
    return im
