# measure drawn P1 sprite offset (MD vs MAME) by masked template matching, background aligned
import sys; sys.argv=[sys.argv[0]]
exec(open('/workspace/wwf_sgdk/tools/climb4c.py').read().split("\nif __name__")[0])
from PIL import Image
import numpy as np
ROMN=sys.argv_rom if hasattr(sys,'argv_rom') else None
def mask_of(r):
    g=[x for x in dec(r['spr']) if x['bank']==0]
    M=np.zeros((272,288),bool)
    for s in g:
        for part in range(s['h']//16):
            t=T[s['code']+part]
            if s['fx']: t=t[:,::-1]
            if s['fy']: t=t[::-1]
            yy=s['y']+16+(part*16 if not s['fy'] else (s['h']//16-1-part)*16); xx=s['x']+16
            if 0<=yy<=256 and 0<=xx<=272: M[yy:yy+16,xx:xx+16]|=(t>0)
    return M[16:256,16:272]   # screen 256x240
def best(A,B,m,R=12):
    ys,xs=np.nonzero(m); bb=None
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            y2=ys+dy; x2=xs+dx; ok=(y2>=0)&(y2<B.shape[0])&(x2>=0)&(x2<B.shape[1])
            if ok.sum()<50: continue
            e=np.abs(A[ys[ok],xs[ok]].astype(int)-B[y2[ok],x2[ok]].astype(int)).sum(1).mean()
            if bb is None or e<bb[0]: bb=(e,dx,dy)
    return bb
PR=[('U',648,330,'izq.'),('U',888,330,'der.'),('UL',700,373,'izq.'),('UR',840,373,'der.')]
MOM=[('aprox. (andar)',-20),('aprox. (parado)',-4),('subida A',4),('subida B',12),('subida C',20),('subida D',28),('subida E',36),('en el poste F',80),('bajada E',302),('bajada C',318),('bajada A',332),('tras bajar',360)]
def measure(want_imgs=False):
    res=[]; imgs=[]
    for d,x0,y0,lado in PR:
        m=mame(d,x0,y0); tr=next(i for i,a in enumerate(m) if a['y']==377)-1
        bb=None
        for par in (0,1):
            for yp in (0,1):
                s,_=run(d,x0,y0,par,yp)
                e=1000*sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m,s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
                if bb is None or e<bb[0]: bb=(e,par,yp)
        fr=[tr+k for _,k in MOM]
        # pick nearest frame with equal camera for each moment
        _,par,yp=bb; s,_=run(d,x0,y0,par,yp)
        fr2=[]
        for f in fr:
            c=[(abs(ff-f),ff) for ff in range(max(1,f-6),min(479,f+7)) if (m[ff]['cx'],m[ff]['cy'])==(s[ff]['cx'],s[ff]['cy']) and m[ff]['sig']==m[f]['sig']]
            g=min(c)[1] if c else f
            fr2.append(g)
        s,im=run(d,x0,y0,par,yp,shots=fr2)
        tr9={r['pt']:r for r in T9['m%s_%d_%d'%(d,x0,y0)]}
        for (lab,_),f in zip(MOM,fr2):
            A=np.array(Image.open('/workspace/wwf_sgdk/rec5/p9/m%s_%d_%d_%03d.png'%(d,x0,y0,120+f)).convert('RGB'))
            mk=mask_of(tr9[120+f])
            self_=best(A,A,mk,2)          # dec->png constant check (expect 0,0)
            A2=A[8:232]; mk2=mk[16:240]; B=im[f]
            # background alignment: compare ring rows outside the sprite
            bgm=np.zeros_like(mk2); bgm[60:200:3,8:248:3]=True; bgm&=~np.pad(mk2,0)
            bga=best(A2,B,bgm,4)
            spr=best(A2,B,mk2,12)
            res.append((d,x0,y0,lado,lab,f,m[f]['sig'][:1],s[f]['pose'],self_[1:],bga[1:],spr[1:],round(spr[0],1)))
            imgs.append(('%s\n%s (%d,%d) poste %s\nfot. %d'%(lab,d,x0,y0,lado,f),A2,B,mk2))
    return res,imgs
if __name__=='__main__':
    res,_=measure()
    for r in res: print(r)
