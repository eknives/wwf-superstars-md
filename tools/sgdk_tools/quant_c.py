import pickle,numpy as np,collections,struct
c2,pal,ext,B=pickle.load(open('../rec/world3.pkl','rb'))
states,blk,imgs,uses=pickle.load(open('world_states.pkl','rb'))
T=np.load('/workspace/wwf/port_35/bgtiles.npy')
M=[int(l,16) for l in open('../mame3/pal_centre.txt')]          # MAME 0.276 pen colours (8-bit)
def md3(v8): return min(7,int(v8/34+0.5))                       # nearest MD DAC level (34*k)
def ent_img(e):
    a,b=e; t=((a&15)<<8)|b; bk=(a>>4)&7; tt=T[t]
    if a&0x80: tt=tt[:,::-1]
    lut=np.array([[md3(M[256+bk*16+i]>>16&255),md3(M[256+bk*16+i]>>8&255),md3(M[256+bk*16+i]&255)] for i in range(16)],np.int16)
    lut8=np.array([[M[256+bk*16+i]>>16&255,M[256+bk*16+i]>>8&255,M[256+bk*16+i]&255] for i in range(16)],np.int16)
    return lut[tt],lut8[tt]
I3={};I8={}
for e in imgs: I3[e],I8[e]=ent_img(e)
pickle.dump((I3,I8),open('imgs_c.pkl','wb'))
# ring vs crowd: entries used only inside anim blocks = crowd
crowd=set(e for st in blk.values() for s in st for e in s)
ringE=set(s[0] for s in states.values() if s)
subs=[];W=[];R=[]
for e,im in I3.items():
    q=im[...,0]+8*im[...,1]+64*im[...,2]
    for sy in (0,8):
        for sx in (0,8): subs.append(q[sy:sy+8,sx:sx+8].ravel()); W.append(uses[e]); R.append(e in ringE)
# HUD cells (window top band + sprite bottom band), colours as used by the HUD build
Hh=np.load('/workspace/wwf_sgdk/ref/hudidx.npy'); v30=struct.unpack('>64H',open('/workspace/wwf_sgdk/ref/v30_cram.bin','rb').read())
hq=np.array([(x&7)+8*((x>>3)&7)+64*((x>>6)&7) for x in v30])
for band in (Hh[8:40,0:256],Hh[224:240,56:232]):
    for r in range(0,band.shape[0],8):
        for c in range(0,band.shape[1],8):
            x=band[r:r+8,c:c+8]
            if x.any(): subs.append(np.where(x>0,hq[x],0+8*3+64*6).ravel()); W.append(1); R.append(False)
subs=np.array(subs); W=np.array(W,float); R=np.array(R)
cnt=collections.Counter()
for s,w in zip(subs,W):
    for c in s: cnt[c]+=w
print('distinct ideal MD colours in bg:',len(cnt))
pickle.dump((subs,W,R),open('subs_c.pkl','wb'))
