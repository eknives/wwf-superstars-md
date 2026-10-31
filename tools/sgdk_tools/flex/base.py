import numpy as np,collections
BT=np.load('/workspace/wwf/v01/bgtiles.npy')
I=np.load('/workspace/wwf_sgdk/tools/bgidx.npy'); R0=np.load('/workspace/wwf_sgdk/tools/ropeidx.npy')
def load(fn):
    allv=[];tests=[]
    for l in open(fn):
        a=l.split()
        if a[0]=='V':
            t=int(a[1])
            if t==150 or not tests: tests.append({})
            v=a[2][2048*4:]; tests[-1][t]=[int(v[i:i+4],16) for i in range(0,len(v),4)]
    return tests
def cellidx(row,col): return (col&15)+((row&15)<<4)+((col&16)<<4)+((row&16)<<5)
def render(w,cells=None):
    img=np.zeros((512,512),np.int32)
    for row in range(32):
        for col in range(32):
            if cells is not None and (row,col) not in cells: continue
            i=cellidx(row,col); a=w[2*i]&255; b=w[2*i+1]&255
            t=((a&15)<<8)|b; c=(a>>4)&7; f=(a>>7)&1
            tl=BT[t][:,::-1] if f else BT[t]
            img[row*16:row*16+16,col*16:col*16+16]=c*16+tl
    return img
