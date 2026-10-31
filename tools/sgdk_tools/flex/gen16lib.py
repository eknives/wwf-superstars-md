# s15: rope flex (MAME rec5 traj42 'rl'): bg tilemap cells + side-rope sprites (bank 4) per frame after the bounce start
import collections,struct,pickle
exec(open('/workspace/wwf_sgdk/tools/flex/base.py').read()); exec(open('/workspace/wwf_sgdk/tools/flex/spr.py').read())
IDX=np.load('/workspace/wwf_sgdk/tools/idx_s03.npy')        # MD world index image (16*line+idx)
TS42=load('/workspace/wwf_sgdk/rec5/traj42b.txt')[0]; tr=T42['rl']; TRL,TSRL=tr,TS42
RES='/workspace/wwf_sgdk/res/'
OUT=RES
side_codes=lambda s: s['code'] not in (15556,15558)
def sides(t): return sprimg(tr[t],codes=side_codes)
def ring2md(X,Y): return X+32,Y+16
# palette mapping from the base frame (right side visible): tilemap key -> MD index per line; sprite value -> MD index (line 1)
def build_map(t,x0,x1):
    A=render(TS42[t]); mb=[collections.defaultdict(collections.Counter) for _ in range(2)]
    for y in range(100,400):
        for x in range(x0,x1):
            v=int(IDX[y+16,x+32]); 
            if v==0: continue
            mb[v>=16][int(A[y,x])][v]+=1
    return mb
def sprmap(ts):
    m=collections.defaultdict(collections.Counter)
    for t in ts:
        S=sides(t); X,Y,v=toworld(tr[t],S)
        for a,b,c in zip(X,Y,v):
            q=int(IDX[b+16,a+32])
            if q>=16: m[int(c)][q]+=1
    return m
MW,MH=80,68
CR=[(8,24),(8,25),(9,24),(9,25),(10,24),(10,25),(11,24),(11,25)]+[(r,c) for r in range(12,19) for c in (25,26)]+[(12,24)]+[(r,c) for r in range(19,22) for c in (26,27)]
CL=[(r,31-c) for r,c in CR]
cramw=struct.unpack('>32H',open(RES+'pal.bin','rb').read())
RGB=np.array([[(c>>1)&7,(c>>5)&7,(c>>9)&7] for c in cramw])
def nearest(v,line):
    d=((RGB[line*16+1:line*16+16]-RGB[v])**2).sum(1); return line*16+1+int(d.argmin())
def enc(t):
    b=bytearray()
    for row in t:
        for x in range(0,8,2): b.append((int(row[x])<<4)|int(row[x+1]))
    return bytes(b)
class TSet:
    def __init__(s,blob,base):
        s.l=[blob[i:i+32] for i in range(0,len(blob),32)]; s.base=base; s.d={}
        for i,k in enumerate(s.l): s.d.setdefault(k,base+i)
        s.n0=len(s.l)
    def add(s,t,fb):  # fb: (h,v) flip bit values
        for (fh,fv),tt in (((0,0),t),((1,0),t[:,::-1]),((0,1),t[::-1]),((1,1),t[::-1,::-1])):
            k=enc(tt)
            if k in s.d: return s.d[k]|(fh*fb[0])|(fv*fb[1])
        s.d[enc(t)]=s.base+len(s.l); s.l.append(enc(t)); return s.base+len(s.l)-1
TB=TSet(open('/workspace/wwf_sgdk/res_s14/bgb_tiles.bin','rb').read(),1); TF={}; TA_=TSet(open('/workspace/wwf_sgdk/res_s14/ropa_tiles.bin','rb').read(),1)
WB=list(struct.unpack('>%dH'%(MW*MH),open(RES+'bgb_map.bin','rb').read()))
WA=list(struct.unpack('>%dH'%(MW*MH),open(RES+'ropa_map.bin','rb').read()))
def cellpix_B(e):
    if not e&0xfff: return None
    t=np.frombuffer(TB.l[(e&0xfff)-1],np.uint8); a=np.zeros((8,8),np.uint8); a[:,0::2]=t.reshape(8,4)>>4; a[:,1::2]=t.reshape(8,4)&15
    if e&0x1000: a=a[:,::-1]
    if e&0x2000: a=a[::-1]
    return a+16*((e>>14)&1)*(a>0)
SIDES={'R':(166,164,(300,500),range(52,60)),'L':(294,378,(0,200),range(12,20))}
ROWS=range(18,46)
out={}
def side_states(sd,b0,tb,mx0,mx1,COLS,TSx,trx,key):
    global tr,TS42
    tr,TS42=TRL,TSRL
    mb=build_map(tb,mx0,mx1)
    sm=collections.defaultdict(collections.Counter)
    for tt in (164,250,292):
        S0=sides(tt); X,Y,v=toworld(tr[tt],S0)
        for a,b,c in zip(X,Y,v): sm[int(c)][int(IDX[b+16,a+32])]+=1
    sm[14][3]+=1
    tr,TS42=trx,TSx   # sprite colour 14 never over the base ropes: MAME rl screenshots (0,119,221) -> nearest line-0 index 3
    def tmcol(k,line):
        c=mb[line].get(k)
        if c: return c.most_common(1)[0][0]
        o=mb[1-line].get(k)
        return nearest(o.most_common(1)[0][0],line) if o else None
    def spcol(v,line):
        c=sm.get(v); 
        if not c: return None
        best=c.most_common(1)[0][0]
        return best if (best>=16)==bool(line) else nearest(best,line)
    FC=CR if sd=='R' else CL
    def wimg_tm(t):
        A=render(TS42[t],cells=set(FC)); W=np.full((MH*8,MW*8),-1,np.int32); W[16:528,32:544]=A; return W
    def wimg_sp(t):
        S=sides(t); X,Y,v=toworld(tr[t],S); W=np.zeros((MH*8,MW*8),np.int32); W[Y+16,X+32]=v; return W
    Bt=wimg_tm(tb); Bs=wimg_sp(tb)
    states=[]; sched=[]
    for k in range(0,84):
        t=b0+k; Ft=wimg_tm(t); Fs=wimg_sp(t)
        reg=np.s_[ROWS[0]*8:ROWS[-1]*8+8, COLS[0]*8:COLS[-1]*8+8]
        key=(Ft[reg].tobytes(),Fs[reg].tobytes())
        if (Ft[reg]==Bt[reg]).all() and (Fs[reg]==Bs[reg]).all(): sched.append(0); continue
        if key not in [s[0] for s in states]: states.append((key,Ft,Fs))
        sched.append(1+[s[0] for s in states].index(key))
    print(sd,'states',len(states),'sched',sched)
    cells=[(r,c) for r in ROWS for c in COLS]
    ent=[]   # per state: list of (B,A) per cell
    nfall=0
    for _,Ft,Fs in states:
        E=[]
        for r,c in cells:
            ys=slice(r*8,r*8+8); xs=slice(c*8,c*8+8)
            eB=WB[r*MW+c]; eA=WA[r*MW+c]
            ft,bt,fs,bs=Ft[ys,xs],Bt[ys,xs],Fs[ys,xs],Bs[ys,xs]
            nB=eB
            if not (ft==bt).all():
                base=cellpix_B(eB); l0=int(base.max()>=16) if base is not None else 0
                for line in (l0,1-l0):
                    px=[tmcol(int(k),line) for k in ft.ravel()]
                    if None not in px: break
                px=np.array([p if p is not None else 0 for p in px]).reshape(8,8)
                ix=np.where(px>0,px-16*line,0).astype(np.uint8)
                nB=('px',ix,line)
            nA=eA
            if not ((fs==bs).all()):
                # A: flex side-rope sprite pixels; keep base A pixels not from the base side-rope sprites
                if eA:
                    t_=np.frombuffer(TA_.l[(eA&0x7ff)-1],np.uint8); a=np.zeros((8,8),np.uint8); a[:,0::2]=t_.reshape(8,4)>>4; a[:,1::2]=t_.reshape(8,4)&15
                    if eA&0x800: a=a[:,::-1]
                    if eA&0x1000: a=a[::-1]
                    la=(eA>>13)&3
                else: a=np.zeros((8,8),np.uint8); la=0
                keep=np.where(bs>0,0,a)
                if (fs>0).any():
                    cand=[spcol(int(v),0) for v in fs[fs>0]]
                    la=0 if None not in cand else 1
                    if keep.any() and eA: la=(eA>>13)&3
                pix=keep.astype(np.int32).copy()
                for (yy,xx) in zip(*np.nonzero(fs)):
                    q=spcol(int(fs[yy,xx]),la)
                    if q is None: nfall+=1; raise SystemExit('no colour for sprite value %d'%fs[yy,xx])
                    pix[yy,xx]=q-16*la
                pr=(eA&0x8000) if eA else (0x8000 if r>=39 else 0)
                nA=(TA_.add(pix.astype(np.uint8),(0x800,0x1000))|(la<<13)|pr) if pix.any() else 0
            E.append((nB,nA))
        ent.append(E)
    keepc=[i for i,(r,c) in enumerate(cells) if any(E[i]!=(WB[r*MW+c],WA[r*MW+c]) for E in ent)]
    keepc=list(range(len(cells)))
    # s16: a cell whose state pixels equal its base pixels keeps the pooled base entry; only the really changed tiles go to the side bank (dedupe + H/V flip)
    TFs=TF[key]=TSet(b'',0)
    def pix(e):
        if isinstance(e,tuple): return e[1]+16*e[2]*(e[1]>0)
        p=cellpix_B(e); return np.zeros((8,8),np.uint8) if p is None else p
    def fixB(e,w):
        q=pix(e)
        if (q==pix(WB[w])).all(): return WB[w]
        if not q.any(): return 0
        line=int(q.max()>=16); ix=np.where(q>0,q-16*line,0).astype(np.uint8)
        return 0x8000|TFs.add(ix,(0x1000,0x2000))|(line<<14)
    W_=[cells[i][0]*MW+cells[i][1] for i in keepc]
    baseE=[(WB[w],WA[w]) for w in W_]
    stE=[[(fixB(E[i][0],w),E[i][1]) for i,w in zip(keepc,W_)] for E in ent]
    return dict(cells=[cells[i] for i in keepc],allcells=cells,ent=[baseE]+stE,sched=sched,keepc=keepc)
