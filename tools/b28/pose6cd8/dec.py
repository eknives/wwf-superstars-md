import struct,numpy as np
a=open('24ac-0_j-1.34','rb').read();b=open('24ad-0_j-1.35','rb').read()
P=bytes(x for p in zip(a,b) for x in p)
L=lambda o:struct.unpack('>I',P[o:o+4])[0]; W=lambda o:struct.unpack('>H',P[o:o+2])[0]
sb=lambda v:v-256 if v>127 else v
bt=[L(0x6CD8+4*i) for i in range(19)]
def poses(bank):
    base=bt[bank]; ends=sorted(x for x in bt if x>base)+[0x40000]
    out=[]; i=0
    while True:
        o=base+4*i
        if o>=min(ends) : break
        p=L(o)
        if p<0x400 or p>=0x40000 or (i and o>=min(L(base+4*j) for j in range(i) )): break
        out.append(p); i+=1
    return out
def pieces(p):
    n=W(p); q=p+2; r=[]
    for k in range(n):
        dx,dy=sb(P[q]),sb(P[q+1]); d=L(q+2); q+=6
        typ=P[d]&1; cnt=P[d+1]; lay=L(d+2); mask=L(lay); xy=lay+2
        if typ==0:
            codes=[(W(d+6+2*j)) for j in range(cnt)]
        else:
            c0=W(d+6); codes=[]; c=c0
            for j in range(cnt):
                tall=(mask>>(31-j))&1; codes.append(c); c+= 2 if tall else 1
        for j in range(cnt):
            tall=(mask>>(31-j))&1
            r.append((codes[j]&0x3fff if typ==0 else codes[j]&0x3fff, tall))
    return r
if __name__=='__main__':
    print([hex(x) for x in bt])
    for bk in (0,1,2,3):
        ps=poses(bk); tiles=set()
        for p in ps:
            try:
                for c,t in pieces(p): tiles.add(c); 
                for c,t in pieces(p):
                    if t: tiles.add(c+1)
            except Exception as e: pass
        print(bk,len(ps),len(tiles))
