import numpy as np,struct,sys
from PIL import Image
D='/workspace/wwf/port_35/'
def cram(b):
    c=struct.unpack('>%dH'%(len(b)//2),b); return [(((v>>1)&7)*36,((v>>5)&7)*36,((v>>9)&7)*36) for v in c]
def tiles(b):
    a=np.frombuffer(b,np.uint8); n=len(a)//32; t=np.zeros((n,8,8),np.uint8)
    t[:,:,0::2]=(a.reshape(n,8,4)>>4); t[:,:,1::2]=a.reshape(n,8,4)&15; return t
def render(names,w,h,T,pal):
    img=np.zeros((h*8,w*8),np.uint8)
    for r in range(h):
        for c in range(w):
            v=names[r*w+c]; t=T[v&0x7ff].copy() if (v&0x7ff)<len(T) else np.zeros((8,8),np.uint8)
            if v&0x800:t=t[:,::-1]
            if v&0x1000:t=t[::-1]
            img[r*8:r*8+8,c*8:c*8+8]=np.where(t>0,t+((v>>13)&3)*16,0)
    P=np.array(pal+[(0,0,0)]*(64-len(pal)),np.uint8); return Image.fromarray(P[img])
if __name__=='__main__':
    pal=cram(open(D+'ring_cram.bin','rb').read())
    T=tiles(open(D+'ring_tiles.bin','rb').read())
    N=struct.unpack('>4096H',open(D+'ring_names.bin','rb').read())
    render(N,64,64,T,pal).save('/workspace/wwf_sgdk/tools/ring_names.png')
    print(len(T), 'maxidx',max(v&0x7ff for v in N),'pals',set((v>>13)&3 for v in N),'prio',sum(v>>15 for v in N))
