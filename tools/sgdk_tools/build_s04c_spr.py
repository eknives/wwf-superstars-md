# s04 wrestler assets from MAME 0.276 recordings (rec4/nofg = lineup, rec4/walk = P1 walk cycle)
import sys,struct,pickle,numpy as np
sys.path.insert(0,'/workspace/wwf_sgdk/rec4'); from load import frames,dec
OUT='/workspace/wwf_sgdk/res/'
T=np.load('/workspace/wwf/port_35/sprtiles.npy')
def w(f,a): a-=0x1c0000; return f['ram'][a]<<8|f['ram'][a+1]
# ---- pair_table merge (same rules as /workspace/wwf/v30/err.py)
d=open('/workspace/wwf/port_30/port.bin','rb').read(); m=open('/workspace/wwf/port_30/wmeta.bin','rb').read()
def tab(i): return [0]+[struct.unpack('>H',d[0x2B0E+30*i+2*j:0x2B0E+30*i+2*j+2])[0]&0xeee for j in range(15)]
LAY=[list(m[8+16*t:24+16*t]) for t in range(8)]
WT=[struct.unpack('>16H',m[136+32*t:168+32*t]) for t in range(8)]
def merge(members):
    acc=np.zeros((16,4))
    for t,p in members:
        P=tab(p)
        for j in range(1,16):
            s=LAY[t][j]; wt=WT[t][j]; c=P[j]
            acc[s,0]+=wt; acc[s,1]+=wt*(c&0xE); acc[s,2]+=wt*((c>>4)&0xE); acc[s,3]+=wt*((c>>8)&0xE)
    line=[0]*16
    for s in range(1,16):
        W=acc[s,0]
        if W==0: continue
        ch=[int((acc[s,k]+W)//(2*W))&7 for k in (1,2,3)]
        line[s]=(ch[0]<<1)|(ch[1]<<5)|(ch[2]<<9)
    return line
# bank -> (name, type, pal, obj, line)
W_={0:('Duggan',3,10,0,2),1:('Savage',2,15,1,3),2:('Warrior',0,18,2,2),3:('Hogan',1,17,3,3),6:('Referee',None,23,4,None)}
L2=merge([(3,10),(0,18)]); L3=merge([(2,15),(1,17)])
cram_s=[int(x) for x in struct.unpack('>32H',open(OUT+'pal.bin','rb').read()[:64])]
def rgb3(c): return np.array([(c>>1)&7,(c>>5)&7,(c>>9)&7])
# ---- poses
FL=frames('/workspace/wwf_sgdk/rec4/nofg/rec.bin'); FW=frames('/workspace/wwf_sgdk/rec4/walk/rec.bin')
def group(f,bank,obj):
    cx=w(f,0x1c002a); cy=w(f,0x1c002e); ox=w(f,0x1c0100+obj*0x11a+0xc); oy=w(f,0x1c0100+obj*0x11a+0x10)
    g=[x for x in dec(f['spr']) if x['bank']==bank]
    return [dict(x,x=x['x']-(ox-cx),y=x['y']-(cy-oy)) for x in g]
poses={}   # (bank,name) -> sprite list relative to obj anchor
f=FL[200]
for b,(nm,t,p,o,l) in W_.items(): poses[(b,'line')]=group(f,b,o)
# P1 walk/idle from walk rec (stable variants: P1 rel min x == -14)
for _ in ():
    pass
seq={}
for f in FW[300:340*3]:
    g=group(f,0,0)
    if g and min(x['x'] for x in g)==-14: seq.setdefault(tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g)),g)
def idof(t):
    g=group(FW[t],0,0); return tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g)),g
# R segment at 612: frames 615(pose a),623,631,639 ; L at 660 etc. use known cycle positions
cyc=[]
for t in (615,623,631,351):   # 4 walk poses (stable variant, rel x -14)
    k,g=idof(t); assert min(x['x'] for x in g)==-14,(t,min(x['x'] for x in g)); cyc.append(g)
k,gi=idof(640+10)             # idle
poses[(0,'idle')]=gi
for i,g in enumerate(cyc): poses[(0,'w%d'%i)]=g

# ---- s04c: post-climb poses from MAME 0.276 (rec5/probe9: mUL_700_330 / mUR_840_330)
# sprite at frame t is drawn from the object's position/height of frame t-1 with the camera of frame t:
# rel = sprite - ((x(t-1) - camX(t)), (camY(t) - y(t-1) - (z(t-1) - 187)))
import pickle as _pk
CR=_pk.load(open('/workspace/wwf_sgdk/tools/climb_rec.pkl','rb'))
sys.path.insert(0,'/workspace/wwf_sgdk/rec5')
_ns={}; exec(open('/workspace/wwf_sgdk/rec5/an8.py').read(),_ns); TR9=_ns['T']
CLIMB={}
for side,n in (('L','mUL_700_330'),('R','mUR_840_330')):
    tr={r['pt']:r for r in TR9[n]}; t0=CR[side][0]
    def rg(k):
        r=tr[t0+k]; p=tr[t0+k-1]; z=p['o'][0x14]<<8|p['o'][0x15]
        ax=p['x']-r['cx']; ay=r['cy']-p['y']-(z-187)
        return [dict(x,x=x['x']-ax,y=x['y']-ay) for x in dec(r['spr']) if x['bank']==0]
    seq=[]; names={}
    for k in range(1,341):
        g=rg(k); sig=tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g))
        if sig not in names: names[sig]='c%s%d'%(side,len(names)); poses[(0,names[sig])]=g
        seq.append(names[sig])
    CLIMB[side]=(t0,seq)
    print('climb',side,'distinct poses',len(names))
def bitmap(g):
    x0=min(x['x'] for x in g); y0=min(x['y'] for x in g); x1=max(x['x']+16 for x in g); y1=max(x['y']+x['h'] for x in g)
    # align origin to the anchor grid of 8 so pieces have stable offsets
    x0-=(x0%8); y0-=(y0%8)
    W=(x1-x0+7)//8*8; H=(y1-y0+7)//8*8; img=np.zeros((H,W),np.uint8)
    for s in reversed(g):
        for part in range(s['h']//16):
            t=T[s['code']+part]
            if s['fx']: t=t[:,::-1]
            if s['fy']: t=t[::-1]
            yy=s['y']-y0+(part*16 if not s['fy'] else (s['h']//16-1-part)*16); xx=s['x']-x0
            sub=img[yy:yy+16,xx:xx+16]; sub[t>0]=t[t>0]
    return img,x0,y0
def enc(t):
    b=bytearray()
    for row in t:
        for x in range(0,8,2): b.append((int(row[x])<<4)|int(row[x+1]))
    return bytes(b)
def remap(img,bank):
    nm,t,p,o,l=W_[bank]
    if t is not None:
        lut=np.array([0]+[LAY[t][j] for j in range(1,16)],np.uint8); return lut[img],None
    # referee -> lines 0/1 nearest (MAME colours, 3-bit rounded)
    P=tab(p); out=None
    return img,P
# pieces: 32x32 blocks, trimmed to non-empty 8px cells
lib={}; blob=bytearray(); ntile=0; pose_tab=[]
for key,g in poses.items():
    bank=key[0]; img,x0,y0=bitmap(g); idx,refP=remap(img,bank)
    H,W=idx.shape; pieces=[]
    for by in range(0,H,32):
        for bx in range(0,W,32):
            blk=idx[by:by+32,bx:bx+32]; raw=img[by:by+32,bx:bx+32]
            if not raw.any(): continue
            rows=[r for r in range(0,blk.shape[0],8) if raw[r:r+8].any()]; cols=[c for c in range(0,blk.shape[1],8) if raw[:,c:c+8].any()]
            r0,r1=rows[0],rows[-1]+8; c0,c1=cols[0],cols[-1]+8
            pc=blk[r0:r1,c0:c1]; line=W_[bank][4]
            if refP is not None:   # referee: choose line 0/1 with min error, nearest colour per index
                best=None
                for L in (0,1):
                    m_={0:0}; e=0
                    for v in set(pc.ravel())-{0}:
                        c=rgb3(refP[v]); k=min(range(1,16),key=lambda k:((rgb3(cram_s[L*16+k])-c)**2).sum()); m_[v]=k; e+=((rgb3(cram_s[L*16+k])-c)**2).sum()
                    if best is None or e<best[0]: best=(e,L,m_)
                e,line,m_=best; pc=np.vectorize(lambda v:m_[v])(pc).astype(np.uint8)
            hc,wc=pc.shape[0]//8,pc.shape[1]//8
            tiles=b''.join(enc(pc[r*8:r*8+8,c*8:c*8+8]) for c in range(wc) for r in range(hc))  # column-major
            pieces.append((x0+bx+c0,y0+by+r0,wc,hc,tiles,line))
    pose_tab.append((key,pieces))
pickle.dump((pose_tab,L2,L3),open('/workspace/wwf_sgdk/tools/s04_poses.pkl','wb'))
for key,pc in pose_tab: print(key,len(pc),'pieces',sum(p[2]*p[3] for p in pc),'tiles',[(p[2]*8,p[3]*8) for p in pc])
print('L2',' '.join('%03x'%x for x in L2[1:])); print('L3',' '.join('%03x'%x for x in L3[1:]))
# ---- export
order=[(0,'idle'),(0,'w0'),(0,'w1'),(0,'w2'),(0,'w3'),(1,'line'),(2,'line'),(3,'line'),(6,'line')]+sorted([k for k in poses if k[1][0]=='c'],key=lambda k:(k[1][1],int(k[1][2:])))
D=dict(pose_tab); tiles=bytearray(); tab=bytearray(); maxt=[]
print('P1 line==idle', [p[4] for p in D[(0,'line')]]==[p[4] for p in D[(0,'idle')]])
for k in order:
    pcs=D[k]; t0=len(tiles)//32; n=sum(p[2]*p[3] for p in pcs)
    tab+=struct.pack('>HHH',len(pcs),t0,n); off=0
    for (dx,dy,wc,hc,tl,line) in pcs:
        tab+=struct.pack('>hhHHH',dx,dy,((wc-1)<<2)|(hc-1),line,off); off+=wc*hc; tiles+=tl
    assert len(pcs)<=6,(k,len(pcs)); tab+=b'\0'*10*(6-len(pcs))
open(OUT+'spr_tiles.bin','wb').write(tiles); open(OUT+'spr_tab.bin','wb').write(tab)
open(OUT+'spr_pal.bin','wb').write(struct.pack('>32H',*(L2+L3)))
# rope priority: front ropes/posts high
AM=np.array(struct.unpack('>%dH'%(80*68),open('/workspace/wwf_sgdk/res_s03c/ropa_map.bin','rb').read())).reshape(68,80)&0x7fff
cov=np.load('/workspace/wwf_sgdk/tools/frontcov.npy'); hi=0
for r in range(68):
    for c in range(80):
        if AM[r,c] and (r>=39 or (r>=33 and cov[r*8:r*8+8,c*8:c*8+8].any()) or (r>=33 and (c<=15 or c>=56) and r>=37)):
            AM[r,c]|=0x8000; hi+=1
open(OUT+'ropa_map.bin','wb').write(struct.pack('>%dH'%(80*68),*[int(x) for x in AM.ravel()]))
print('tiles',len(tiles)//32,'rope cells high',hi,'of',int((AM!=0).sum()))

# climb timeline: per side, per frame k=1..340 the pose id shown (sprite frame k) + logic keyframes
OID={k:i for i,k in enumerate(order)}
ct=bytearray()
for side in ('L','R'):
    t0,seq=CLIMB[side]
    ct+=bytes(OID[(0,nm)] for nm in seq)
open(OUT+'climb_pose.bin','wb').write(ct)
print('P1 max tiles',max(sum(p[2]*p[3] for p in D[k]) for k in order if k[0]==0))
for side in ('L','R'): print(side,[ (i+1,OID[(0,n)]) for i,n in enumerate(CLIMB[side][1]) if i==0 or n!=CLIMB[side][1][i-1]])
