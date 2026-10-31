from rope import *  # gives full (rope plane map), T2
import numpy as np
I=np.load('bgidx.npy')
A=np.array(render(full,64,64,T2,pal))  # unused
# build rope pixel index image from v35
def idx(Nm,T,w=64,h=64):
    img=np.zeros((h*8,w*8),np.uint8)
    for r in range(h):
        for c in range(w):
            v=Nm[r*w+c]
            if not v&0x7ff: continue
            t=T[v&0x7ff].copy()
            if v&0x800:t=t[:,::-1]
            if v&0x1000:t=t[::-1]
            img[r*8:r*8+8,c*8:c*8+8]=np.where(t>0,t+((v>>13)&3)*16,0)
    return img
R=idx(full,T2)
y0,y1,x0,x1=296,368,436,472
sub=I[y0:y1,x0:x1]; m=np.isin(sub,[17,20,21,22,23,25])
reg=R[y0:y1,x0:x1]; add=(reg==0)&m; reg[add]=sub[add]
print('added px',add.sum())
np.save('ropeidx.npy',R)
P=np.array(pal+[(0,0,0)]*32,np.uint8)
out=P[I].copy(); out[R>0]=[255,0,255]
Image.fromarray(out[270:380,380:480]).resize((400,440),0).save('/tmp/pr2.png')
y0,y1,x0,x1=300,352,426,456
sub=I[y0:y1,x0:x1]; m=np.isin(sub,[1,2,4,7,9,10,11,12,13,14]); reg=R[y0:y1,x0:x1]; add=(reg==0)&m; reg[add]=sub[add]; print('hooks',add.sum())
np.save('ropeidx.npy',R)
out=P[I].copy(); out[R>0]=[255,0,255]
Image.fromarray(out[270:380,380:480]).resize((400,440),0).save('/tmp/pr2.png')
