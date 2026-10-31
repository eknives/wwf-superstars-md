# CROWD_ARC prep (s67): decode arcade crowd scripts (0x22640/0x22760 via 0x225B0), fence (0x23170), 184a (0x233F6)
# and render the bg0 entries missing from imgs (ROM 24j7/24j6 + palette recovered from imgs). Output: crowdarc_src.pkl
import sys,struct,pickle,numpy as np,collections
sys.path.insert(0,'/tmp/crowd/bg'); import dec_bg
from world_img import imgs
B=open('/workspace/wwf/port_29/patched.bin','rb').read()
def L(a): return struct.unpack('>I',B[a:a+4])[0]
def W(a): return struct.unpack('>H',B[a:a+2])[0]
def cellof(addr):
    x=(addr-0xC0000)//4; return ((x&15)|((x>>8)&1)<<4, ((x>>4)&15)|((x>>9)&1)<<4)
def run(el,a2):
    st,en,stride=B[0x22760+el*4],B[0x22761+el*4],W(0x22762+el*4)
    a1=L(0x22640+el*16)+st*4; d6=0; d5=st; out=[]
    for _ in range(4000):
        d7=B[a2]; a2+=1
        if d7==0:
            d7=B[a2]; a2+=1
            if d7==0xFD: break
            if d7==0xFC: d6=B[a2]; a2+=1; continue
            a2-=1
        else: out.append((cellof(a1),(d6&0xff,d7)))
        d5+=1
        if d5==en: d5=st; a1+=stride
        else: a1+=4
    return out
def alias(z,col,row):
    if z==0 and col>=26: col-=32
    if z==2 and col<=5: col+=32
    return col,row
SEL=list(B[0x22634:0x22640])
crowd={}   # (z,s3,ph) -> list of ((tx,ty),key)
for z in range(3):
    for s3 in range(4):
        for ph in range(3):
            o=[]
            for d in range(3):
                el=SEL[s3*3+d]+z
                o+=[(alias(z,*c),k) for c,k in run(el,L(0x22640+el*16+4+4*ph))]
            crowd[(z,s3,ph)]=o
fence={}   # (z? only zone 1) step 0..1 -> list   record 0x23170 + zone*12 + [2]*12
for z in range(3):
    for s2 in range(2):
        a=0x23170+z*12+s2*12; o=[]
        for k in (0,6):
            el=W(a+k); o+=[(alias(z,*c),kk) for c,kk in run(el,L(a+k+2))]
        fence[(z,s2)]=o
small={}   # (r1,s3) -> 16 cells: cols 12-15 r29, 16-19 r29, 12-15 r30, 16-19 r30 ; d0 incrementing
for r1 in range(4):
    for s3 in range(2):
        d0=W(0x233F6+r1*4+s3*2); o=[]
        for row,c0 in ((29,12),(29,16),(30,12),(30,16)):
            for c in range(c0,c0+4): o.append(((c,row),((d0>>8)&0xff,d0&0xff))); d0+=1
        small[(r1,s3)]=o
keys=set(k for d in (crowd,fence,small) for v in d.values() for _,k in v)
# palette per colour bank from imgs
pal=collections.defaultdict(collections.Counter)
for (a,t),im in imgs.items():
    ix=dec_bg.entry_idx(a,t); b=(a>>4)&7
    for i in range(16):
        m=ix==i
        if m.any():
            for c in map(tuple,im[m].reshape(-1,3)): pal[(b,i)][c]+=1
P={k:v.most_common(1)[0][0] for k,v in pal.items()}
miss=[k for k in keys if k not in imgs]; nofb=collections.Counter()
new={}
for a,t in miss:
    ix=dec_bg.entry_idx(a,t); b=(a>>4)&7; im=np.zeros((16,16,3),np.int16)
    for i in range(16):
        c=P.get((b,i))
        if c is None:
            nofb[(b,i)]+=int((ix==i).sum())
            c=next((P[(bb,i)] for bb in range(8) if (bb,i) in P),(0,0,0))
        im[ix==i]=c
    new[(a,t)]=im
print('keys',len(keys),'missing',len(miss),'pal entries',len(P),'fallback px',dict(nofb))
pickle.dump(dict(crowd=crowd,fence=fence,small=small,new=new),open('crowdarc_src.pkl','wb'))
ok=tot=0
for (a,t),im in list(imgs.items()):
    ix=dec_bg.entry_idx(a,t); b=(a>>4)&7
    r=np.array([[P[(b,i)] for i in row] for row in ix]); ok+=(r==im).all(2).sum(); tot+=256
print('palette check px',ok/tot)
