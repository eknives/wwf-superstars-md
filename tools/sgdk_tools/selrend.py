import numpy as np, pickle
from PIL import Image
exec(open('tools/selq.py').read().split("if __name__")[0])
R=pickle.load(open('/tmp/selq.pkl','rb')); tp,pals,assign=R['tp'],R['pals'],R['assign']
out=np.zeros((224,256,3),int); idxmap=np.zeros((224,256),int)
for t in range(NT):
    ty,tx=divmod(t,32); p=tp[t]; sl=(slice(ty*8,ty*8+8),slice(tx*8,tx*8+8))
    kk=np.vectorize(ci.get)(K[sl]); b=bgcell[sl]
    j=D[kk][:,:,pals[p]].argmin(2)
    out[sl]=rgb[np.array(pals[p])[j]].astype(int)
    out[sl][b>=0]=AZ
    idxmap[sl]=j
err=(np.abs(out-C).sum(2)>0)
print('pix distintos',err.sum(),'en retratos',(err&(W>1)).sum())
img=(out*36.43).clip(0,255).astype(np.uint8)
Image.fromarray(np.concatenate([(C*36.43).astype(np.uint8),img],1)).resize((1024,448),0).save('/tmp/selq.png')
