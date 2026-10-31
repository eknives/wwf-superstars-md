from port import *; from arcr import *; from arcdec import poses
import pickle
def cr(m):
    ys,xs=np.nonzero(m); return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
A=[]
for bk in (3,0):
    for i,p in enumerate(poses(bk)):
        try: im=img(arc_spr(p))
        except Exception: continue
        if im is None or not im.any(): continue
        m=cr(im>0)
        for f in (0,1): A.append((bk,i,f,m[:,::-1] if f else m))
def iou(a,b):
    h=max(a.shape[0],b.shape[0]);w=max(a.shape[1],b.shape[1])
    A_=np.zeros((h,w),bool);B=np.zeros((h,w),bool);A_[:a.shape[0],:a.shape[1]]=a;B[:b.shape[0],:b.shape[1]]=b
    return (A_&B).sum()/(A_|B).sum()
for k in (0,5,10,15,100,300):
    m=cr(pimg(k)>0); best=max(A,key=lambda t:iou(m,t[3])); print(k,m.shape,best[:3],best[3].shape,round(iou(m,best[3]),3))
