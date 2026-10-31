from rend import *
pal=cram(open(D+'ring_cram.bin','rb').read())
R=tiles(open(D+'ring_tiles.bin','rb').read())
N=struct.unpack('>4096H',open(D+'ring_names.bin','rb').read())
def idximg(N,T,w=64,h=64):
    img=np.zeros((h*8,w*8),np.uint8)
    for r in range(h):
        for c in range(w):
            v=N[r*w+c]; t=T[v&0x7ff].copy()
            if v&0x800:t=t[:,::-1]
            if v&0x1000:t=t[::-1]
            img[r*8:r*8+8,c*8:c*8+8]=np.where(t>0,t+((v>>13)&3)*16,0)
    return img
I=idximg(N,R)
np.save('bgidx.npy',I)
