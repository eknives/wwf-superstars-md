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
# ---- s04d: bottom-left post climb (MAME rec5/traj11 'cDL', a15 at pt 153), 300 frames, padded to 340
_n2={}; exec(open('/workspace/wwf_sgdk/rec5/an8.py').read().replace('traj9.txt','traj11.txt'),_n2); TR11=_n2['T']
tr={r['pt']:r for r in TR11['cDL']}; t0=153
def rgb_(k):
    r=tr[t0+k]; p=tr[t0+k-1]; z=p['o'][0x14]<<8|p['o'][0x15]
    ax=p['x']-r['cx']; ay=r['cy']-p['y']-(z-187)
    return [dict(x,x=x['x']-ax,y=x['y']-ay) for x in dec(r['spr']) if x['bank']==0]
seq=[]; names={}
for k in range(1,301):
    g=rgb_(k); sig=tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g))
    if sig not in names: names[sig]='cB%d'%len(names); poses[(0,names[sig])]=g
    seq.append(names[sig])
seq+= [seq[-1]]*40
CLIMB['B']=(t0,seq); print('climb B distinct poses',len(names))
# ---- s04e: bottom-right post climb (MAME rec5/traj17 'rD', a15 at pt 121)
_n3={}; exec(open('/workspace/wwf_sgdk/rec5/an8.py').read().replace('traj9.txt','traj17.txt'),_n3); TR17=_n3['T']
tr={r['pt']:r for r in TR17['rD']}; t0=121
seq=[]; names={}
for k in range(1,301):
    g=rgb_(k); sig=tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g))
    if sig not in names: names[sig]='cE%d'%len(names); poses[(0,names[sig])]=g
    seq.append(names[sig])
seq+= [seq[-1]]*40
CLIMB['E']=(t0,seq); print('climb E distinct poses',len(names))
# ---- s05: P1 strikes / lock-up and P2 (Warrior) reactions, MAME rec5 traj23 (1P vs 2P, P1 Duggan, P2 Warrior idle)
sys.path.insert(0,'/workspace/wwf_sgdk/tools'); import mv5
T23=mv5.load('/workspace/wwf_sgdk/rec5/traj23.txt','/workspace/wwf_sgdk/rec5/traj23b.txt')
MVN={}; MVSEQ={}
def mvpose(bank,tr,t):
    g,sig=mv5.grp(tr,t,bank)
    k=(bank,sig)
    nz=lambda p:sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in p)
    base=(0,'idle') if bank==0 else (2,'line')
    if nz(g)==nz(poses[base]): return base
    if k not in MVN: MVN[k]=(bank,'v%d'%len(MVN)); poses[MVN[k]]=g
    return MVN[k]
def mvseq(name,test,bank,t1,t2):
    tr=T23[test]; MVSEQ[name]=[mvpose(bank,tr,t) for t in range(t1,t2+1)]
mvseq('PUN','pA',0,122,154); mvseq('KIK','pB',0,122,152)
mvseq('RPU','pA',2,146,158); mvseq('RKI','pB',2,140,180)
mvseq('LK1','lk',0,156,380); mvseq('LK2','lk',2,156,380)
# s07: P2 (Warrior) walk and strikes, P1 reactions (MAME rec5 traj28, P2 controlled, VS)
T28=mv5.load('/workspace/wwf_sgdk/rec5/traj28.txt','/workspace/wwf_sgdk/rec5/traj28b.txt')
def mvseq2(name,test,bank,t1,t2):
    tr=T28[test]; MVSEQ[name]=[mvpose(bank,tr,t) for t in range(t1,t2+1)]
mvseq2('PUN2','qA',2,122,156); mvseq2('KIK2','qB',2,122,154); mvseq2('RPU1','qA',0,140,160); mvseq2('RKI1','qB',0,136,182); mvseq2('WLK2','wL',2,130,161)
T30=mv5.load('/workspace/wwf_sgdk/rec5/traj30.txt','/workspace/wwf_sgdk/rec5/traj30b.txt')
tr=T30['lw']
MVSEQ['THR1']=[mvpose(0,tr,t) for t in range(315,495)]
_z=mv5.z; mv5.z=lambda o:187
MVSEQ['THR2']=[mvpose(2,tr,t) for t in range(315,635)]
def zz(o): return struct.unpack('>h',bytes(o[0x14:0x16]))[0]
tp=bytearray()
for t in range(315,635):
    r=tr[t]; r0=tr[315]; tp+=struct.pack('>4h',r['x']-r0['x'],r['cx']-r0['cx'],r['x2']-r0['x2'],r['cy']-r0['cy'])+struct.pack('>h',zz(tr[t-1]['o'])-187 if t<495 else 0)+b'\0\0'
open(OUT+'thr_pos.bin','wb').write(tp); mv5.z=_z
# s12: throw stopped by the ropes (MAME rec5 traj36 'le': P1 x < 616 -> both fall, state 08, no damage), frames 397..504
T36=mv5.load('/workspace/wwf_sgdk/rec5/traj36.txt','/workspace/wwf_sgdk/rec5/traj36b.txt'); tr=T36['le']
MVSEQ['RF1']=[mvpose(0,tr,t) for t in range(397,505)]
mv5.z=lambda o:187; MVSEQ['RF2']=[mvpose(2,tr,t) for t in range(397,505)]; mv5.z=_z
rp=bytearray(); r0=tr[395]
for t in range(397,505):
    r=tr[t]; rp+=struct.pack('>6h',r['x']-616,r['x2']-616,zz(tr[t-1]['o'])-187,r['cx']-r0['cx'],r['cy']-r0['cy'],0)
open(OUT+'rf_pos.bin','wb').write(rp)
# s14: running, rope bounce, running attack, brake (MAME rec5 traj37-41, P1 Duggan, A+B)
R=lambda n:mv5.load('/workspace/wwf_sgdk/rec5/traj%d.txt'%n,'/workspace/wwf_sgdk/rec5/traj%db.txt'%n)
T39=R(39); T38=R(38); T40=R(40); T41=R(41)
RSEG=[('RUNR',T39['rl'],122,24,None),('RUNL',T39['rl'],214,24,None),('BNCR',T39['rl'],166,48,909),('BNCL',T39['rl'],294,48,627),
 ('RATR',T40['aR'],128,40,0),('RATL',T38['q100'],221,40,0),('BRKR',T41['bk'],132,20,0),('BRKL',T39['qH'],215,20,0)]
rnp=bytearray()
for nm,tr,s0,ln,ref in RSEG:
    MVSEQ[nm]=[mvpose(0,tr,t) for t in range(s0,s0+ln)]
    if ref is not None:
        X=lambda t:tr[t]['x']*256+tr[t]['o'][0xe]   # s14: 8.8, relative to the action's first frame (arcade keeps the sub-pixel)
        lp=ln+(1 if nm[:3]=='RAT' else 0)   # attack: the first idle tick still moves (MAME q100 f261)
        rnp+=struct.pack('>%dh'%lp,*[X(t)-X(s0) for t in range(s0,s0+lp)])
open(OUT+'run_pos.bin','wb').write(rnp)
print('s05 move poses',len(MVN),{k:len(v) for k,v in MVSEQ.items()}); print('RPU end',MVSEQ['RPU'][-1],'RKI end',MVSEQ['RKI'][-1],'PUN end',MVSEQ['PUN'][-1])

# ---- s24: side-rope exit / re-entry (MAME VS probe tools/sx_probe.lua, traj_sx_sR / sL: P1 Duggan x 900|640 y 340, hold out 60-360, back 420-720)
SXN={}; SXSEQ={}
for sd in ('sR','sL'):
    TS=mv5.load('/workspace/wwf_sgdk/rec5/traj_sx_%s.txt'%sd,'/workspace/wwf_sgdk/rec5/traj_sx_%sb.txt'%sd)[sd]
    for ph,t0,N in (('x',87,62),('e',457,54)):
        sq=[]
        for k in range(1,N+1):
            g,sig=mv5.grp(TS,t0+k,0)
            nz=lambda p:sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in p)
            if nz(g)==nz(poses[(0,'idle')]): key=(0,'idle')
            else:
                if sig not in SXN: SXN[sig]=(0,'x%d'%len(SXN)); poses[SXN[sig]]=g
                key=SXN[sig]
            r=TS[t0+k]; r0=TS[t0]
            sq.append((key,r['x']-r0['x'],r['y']-r0['y'],mv5.z(r['o'])))
        SXSEQ[sd+ph]=sq
print('s24 sx poses',len(SXN))
# ---- s04d: left-facing idle/walk = MAME fx0 poses: mirror of fx1 about x = -12 - x (measured, rec5 traj11 eR, same for all 4)
for k in ('idle','w0','w1','w2','w3'):
    poses[(0,'m'+k)]=[dict(q,x=-12-q['x']-16+16-16+16 if False else -12-q['x'],fx=1-q['fx']) for q in poses[(0,k)]]
def bitmap(g):
    x0=min(x['x'] for x in g); y0=min(x['y'] for x in g); x1=max(x['x']+16 for x in g); y1=max(x['y']+x['h'] for x in g)
    # align origin to the anchor grid of 8 so pieces have stable offsets
    x0-=(x0%8); y0-=(y0%8)
    W=(x1-x0+7)//8*8; H=(y1-y0+7)//8*8; img=np.zeros((H,W),np.uint8)
    for s in g:   # s05c: MAME draws later list entries on top (hair layer 5616/5618 over the head)
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
order=[(0,'idle'),(0,'w0'),(0,'w1'),(0,'w2'),(0,'w3'),(1,'line'),(2,'line'),(3,'line'),(6,'line')]+sorted([k for k in poses if k[1][0]=='c'],key=lambda k:(k[1][1],int(k[1][2:])))+[(0,'m'+k) for k in ('idle','w0','w1','w2','w3')]+sorted(set(MVN.values()),key=lambda k:int(k[1][1:]))+sorted(set(SXN.values()),key=lambda k:int(k[1][1:]))
D=dict(pose_tab); tiles=bytearray(); tab=bytearray(); maxt=[]
print('P1 line==idle', [p[4] for p in D[(0,'line')]]==[p[4] for p in D[(0,'idle')]])
for k in order:
    pcs=D[k]; t0=len(tiles)//32; n=sum(p[2]*p[3] for p in pcs)
    tab+=struct.pack('>HHH',len(pcs),t0,n); off=0
    for (dx,dy,wc,hc,tl,line) in pcs:
        tab+=struct.pack('>hhHHH',dx,dy,((wc-1)<<2)|(hc-1),line,off); off+=wc*hc; tiles+=tl
    assert len(pcs)<=12,(k,len(pcs)); tab+=b"\0"*10*(12-len(pcs))
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
for side in ('L','R','B','E'):
    t0,seq=CLIMB[side]
    ct+=bytes(OID[(0,nm)] for nm in seq)
open(OUT+'climb_pose.bin','wb').write(ct)
print('MIRB',OID[(0,'midle')])
print('P1 max tiles',max(sum(p[2]*p[3] for p in D[k]) for k in order if k[0]==0))
for side in ('L','R','B'): print(side,[ (i+1,OID[(0,n)]) for i,n in enumerate(CLIMB[side][1]) if i==0 or n!=CLIMB[side][1][i-1]])

ms=bytearray()
for nm in ('PUN','KIK','RPU','RKI','LK1','LK2','PUN2','KIK2','RPU1','RKI1','WLK2','THR1','THR2','RF1','RF2','RUNR','RUNL','BNCR','BNCL','RATR','RATL','BRKR','BRKL'):
    ms+=bytes(OID[k] for k in MVSEQ[nm])
open(OUT+'move_seq.bin','wb').write(ms)
NMS=('PUN','KIK','RPU','RKI','LK1','LK2','PUN2','KIK2','RPU1','RKI1','WLK2','THR1','THR2','RF1','RF2','RUNR','RUNL','BNCR','BNCL','RATR','RATL','BRKR','BRKL'); print('move_seq offsets',[sum(len(MVSEQ[x]) for x in NMS[:i]) for i in range(len(NMS))],'len',[len(MVSEQ[x]) for x in NMS])
print('npose',len(order))
print('P2 max tiles',max(sum(p[2]*p[3] for p in D[k]) for k in order if k[0]==2))

sx=bytearray()
for nm in ('sRx','sRe','sLx','sLe'):
    for key,dx,dy,z in SXSEQ[nm]: sx+=struct.pack('>hhhh',OID[key],dx,dy,z)
open(OUT+'sx_seq.bin','wb').write(sx); print('SXB',OID[sorted(set(SXN.values()),key=lambda k:int(k[1][1:]))[0]],'sx max tiles',max(sum(p[2]*p[3] for p in D[k]) for k in SXN.values()))
