import pickle,collections,numpy as np,struct
from PIL import Image
c2,pal,ext,B=pickle.load(open('../rec/world3.pkl','rb')); cm,_=pickle.load(open('../rec/worldm.pkl','rb'))
T=np.load('/workspace/wwf/port_35/bgtiles.npy')
col=lambda i:((pal[i*2]<<8|pal[i*2+1])&0xfff)
def rgb3(c): return ((c&15)>>1,(c>>5)&7,(c>>9)&7)
AX0,AY0=-2,-1; AW,AH=40,34          # arcade 16px cells x -2..37, y -1..32
# per arcade cell: list of states (entries)
states={}
for (tx,ty),cnt in cm.items(): states[(tx,ty)]=[cnt.most_common(1)[0][0]]
blk={}
for (bx,by),cnt in B.items():
    st=[s for s,n in cnt.most_common()]
    if len(st)<2: continue
    blk[(bx,by)]=st
    for j in range(4):
        for i in range(4):
            states[(bx*4+i,by*4+j)]=None   # owned by block
def ent_img(e):
    a,b=e; t=((a&15)<<8)|b; bk=(a>>4)&7; tt=T[t]
    if a&0x80: tt=tt[:,::-1]
    lut=np.array([rgb3(col(256+bk*16+i)) for i in range(16)],np.int16)
    return lut[tt]          # 16x16x3 levels 0..7
# collect all arcade images: base cells and block variants
imgs={}   # entry -> 16x16x3
uses=collections.Counter()
for k,s in states.items():
    if s: imgs.setdefault(s[0],ent_img(s[0])); uses[s[0]]+=1
for k,st in blk.items():
    for si,s in enumerate(st):
        for e in s: imgs.setdefault(e,ent_img(e)); uses[e]+=1
print('arcade entries',len(imgs),'anim blocks',len(blk))
pickle.dump((states,blk,imgs,uses),open('world_states.pkl','wb'))
