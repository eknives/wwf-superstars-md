# s24: pre-shifted P1 pose bitmaps for the plane A composite (side-rope crossing). For each pose and each x&7 shift:
# W cell columns x H pixel rows of u32 (4bpp, big-endian nibbles), column-major; SAT order (first piece on top).
import struct
tab=open('res/spr_tab.bin','rb').read(); til=open('res/spr_tiles.bin','rb').read()
NP=len(tab)//126
POSES=list(range(0,5))+list(range(35,40))+list(range(168,NP))
idx=[0xFFFF]*NP; blob=b''; offs=[]; recs=[]
for pid in POSES:
    b=tab[pid*126:(pid+1)*126]; n,t0,nt=struct.unpack('>HHH',b[:6]); P=[struct.unpack('>hhHHH',b[6+10*k:16+10*k]) for k in range(n)]
    x0=min(p[0] for p in P); y0=min(p[1] for p in P)
    x1=max(p[0]+(((p[2]>>2)&3)+1)*8 for p in P); y1=max(p[1]+((p[2]&3)+1)*8 for p in P)
    bw,bh=x1-x0,y1-y0; W=(bw+7)//8+1
    pix=[[0]*bw for _ in range(bh)]
    for (dx,dy,sz,line,toff) in reversed(P):
        tw=((sz>>2)&3)+1; th=(sz&3)+1
        for tc in range(tw):
            for tr in range(th):
                t=til[(t0+toff+tc*th+tr)*32:(t0+toff+tc*th+tr+1)*32]
                for y in range(8):
                    for x in range(8):
                        v=(t[y*4+x//2]>>(4*(1-x%2)))&15
                        if v: pix[dy-y0+tr*8+y][dx-x0+tc*8+x]=v
    rec=struct.pack('>hhHH',x0,y0,W,bh)
    rng=b''; dat=b''
    for sh in range(8):
        for c in range(W):
            col=[]
            for y in range(bh):
                w=0
                for k in range(8):
                    X=c*8+k-sh
                    v=pix[y][X] if 0<=X<bw else 0
                    w=w<<4|v
                col.append(w)
            nz=[y for y in range(bh) if col[y]]
            rng+=bytes([nz[0],nz[-1]+1] if nz else [0,0]); dat+=b'\0'*32+b''.join(struct.pack('>I',w) for w in col)+b'\0'*32
    rec+=rng+b'\0'*((-len(rng))%4)+dat; recs.append((pid,rec))
hlen=NP*2; hlen+=(-hlen)%4; base=hlen+4*len(recs)
for pid,rec in recs:
    a=base+len(blob)
    if a//131072 != (a+len(rec)-1)//131072: blob+=b'\0'*(131072-a%131072)
    idx[pid]=len(offs); offs.append(len(blob)); blob+=rec
hdr=struct.pack('>%dH'%NP,*idx); hdr+=b'\0'*((-len(hdr))%4)
out=hdr+b''.join(struct.pack('>I',base+o) for o in offs)+blob
open('res/sx_cmp.bin','wb').write(out); print(len(POSES),'poses',len(out),'bytes', 'NP',NP)
