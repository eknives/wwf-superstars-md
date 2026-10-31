# s04 frame-by-frame check: every frame vs a model = bg (RAM world map + ROM tiles, plane A priority) + wrestlers rendered from ROM pose data at RAM positions
exec(open('/workspace/wwf_sgdk/tools/fcheck4.py').read().split('tot=0')[0])
import pickle
pt,L2,L3=pickle.load(open('../tools/s04_poses.pkl','rb')); D=dict(pt)
order=[(0,'idle'),(0,'w0'),(0,'w1'),(0,'w2'),(0,'w3'),(1,'line'),(2,'line'),(3,'line'),(6,'line')]
cr2=list(cr)+L2+L3; LUT=np.array([[((v>>1)&7)*36,((v>>5)&7)*36,((v>>9)&7)*36] for v in cr2],np.uint8)
def pbit(key):
    out=[]
    for dx,dy,wc,hc,tl,line in D[key]:
        a=np.frombuffer(tl,np.uint8).reshape(wc,hc,8,4); a=np.stack([a>>4,a&15],-1).reshape(wc,hc,8,8)
        img=a.transpose(1,2,0,3).reshape(hc*8,wc*8); out.append((dx,dy,np.where(img>0,img+16*line,0)))
    return out
PB=[pbit(k) for k in order]
def g16(r,a): a&=0xffff; v=r[a]<<8|r[a+1]; return v-65536 if v>32767 else v
def hi_from(VX,VY):
    m=np.zeros((68*8,80*8),bool)
    for rr in range(68):
        for cc in range(80):
            if AM[rr,cc]&0x8000:
                t=TA_[(AM[rr,cc]&0x7ff)-1]
                if AM[rr,cc]&0x800: t=t[:,::-1]
                if AM[rr,cc]&0x1000: t=t[::-1]
                m[rr*8:rr*8+8,cc*8:cc*8+8]=t>0
    return m
HI=hi_from(0,0)
def model(r,x0,y0,ys):
    WI=world_from_ram(r,x0,y0)[ys[:,None]+y0,(np.arange(256)+x0)[None,:]].copy()
    hi=HI[ys[:,None]+y0,(np.arange(256)+x0)[None,:]]
    camx=g16(r,sym['camx']); camy=g16(r,sym['camy'])
    ox=[g16(r,sym['ox']+2*k) for k in range(5)]; oy=[g16(r,sym['oy']+2*k) for k in range(5)]; cp=[g16(r,sym['curPose']+2*k) for k in range(5)]
    ordr=sorted(range(5),key=lambda k:(oy[k],k))
    scr=np.zeros((224,256),np.uint8); filled=np.zeros((224,256),bool); spri=np.zeros((224,256),bool)
    for o in ordr:
        bx=ox[o]-(camx+0x200); by=(0x200-camy)-oy[o]-8; pri= oy[o]<229
        for dx,dy,img in PB[cp[o]]:
            h,w=img.shape
            for j in range(h):
                y=by+dy+j
                if not 0<=y<224: continue
                for i in range(w):
                    x=bx+dx+i
                    if 0<=x<256 and img[j,i] and not filled[y,x]: filled[y,x]=True; scr[y,x]=img[j,i]; spri[y,x]=pri
    yi={y:k for k,y in enumerate(ys)}
    for k,y in enumerate(ys):
        f=filled[y]&(spri[y]|~hi[k]); WI[k][f]=scr[y][f]
    return WI
tot=0; cmpd=0
reg='ntsc-u'
plan=[(120,('RIGHT',)),(60,('UP',)),(60,('LEFT',)),(90,('DOWN','LEFT')),(60,('UP','RIGHT')),(40,()),(80,('LEFT','UP')),(80,('RIGHT','DOWN')),(30,('UP',)),(200,('RIGHT',)),(200,('LEFT',)),(40,())]
c=Core(rom,{b'genesis_plus_gx_region_detect':reg.encode()}); c.run(60); bad=0; first=None; PR=None; PR2=None
for n,p in plan:
  for f in range(n):
    PR2=PR; PR=bytes(c.ram_bytes()); c.run(1,pad0=p); v=bytes(c.vram_bytes()[:65536])
    hs=s(struct.unpack('>H',v[0xDC02:0xDC04])[0]); vs=s(c.vsram_words()[1])
    img=np.array(c.image())[:224,:256,:3]; x0=-hs; y0=vs; ys=np.r_[48:200]
    ok=False; nd=None
    for RR in (PR,PR2):
        if RR is None: continue
        e=LUT[model(RR,x0,y0,ys)]; d=(np.abs(img[ys].astype(int)-e).max(2)>40)
        if not d.sum(): ok=True; break
        nd=int(d.sum()) if nd is None else min(nd,int(d.sum()))
    cmpd+=1
    if not ok:
        bad+=1
        if first is None: first=(cmpd,p,nd); c.shot('glitch5_%d.png'%cmpd)
print('frames',cmpd,'bad',bad,'first',first)
