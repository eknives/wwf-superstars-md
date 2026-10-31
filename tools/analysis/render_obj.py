import struct,sys,numpy as np,glob
from PIL import Image
P=open('tools/prog.bin','rb').read()
def L(a):return struct.unpack('>I',P[a:a+4])[0]
def W(a):return struct.unpack('>H',P[a:a+2])[0]
def sb(a):return struct.unpack('b',P[a:a+1])[0]
T=np.load('/workspace/wwf/port_35/sprtiles.npy')
sys.path.insert(0,'/workspace/wwf_sgdk/rec4');from load import frames
def pens():
    for r in sorted(glob.glob('/workspace/wwf_sgdk/rec*/**/rec.bin',recursive=True)):
        F=frames(r);
        if F: return F[len(F)//2]['pens'],r
PN,src=pens()
def frame(bank,pose,log):
    tb=L(0x6cd8+bank*4);a3=L(tb+pose*4);n=W(a3);a3+=2;pcs=[]
    log.append(f'banco {bank:#x} tabla {tb:#x} pose {pose:#x} -> {a3-2:#x}, {n} bloques')
    for b in range(n):
        bx,by=sb(a3),sb(a3+1);d=L(a3+2);a3+=6
        typ=P[d]&1;cnt=P[d+1];pal=(P[d]>>4)&7;fl=(P[d]&0xc)<<4
        ptr=L(d+2);mask=L(ptr);offs=ptr+2
        log.append(f'  bloque {b}: desc {d:#x} tipo {"lista" if typ==0 else "consecutivo"} piezas {cnt} offs {ptr:#x} dx {bx} dy {by}')
        code=W(d+6)&0x7fff if typ else None
        for i in range(cnt):
            h=32 if mask>>(31-i)&1 else 16
            if typ==0: c=W(d+6+2*i)&0x3fff
            else: c=code&0x3fff
            pcs.append((bx+sb(offs+2*i),by+sb(offs+2*i+1)-(16 if h==32 else 8),c,h,fl))
            if typ: code+=2 if h==32 else 1
    return pcs
def render(pcs,pal,out):
    pcs=[(x,-y-h,c,h,f) for x,y,c,h,f in pcs]
    x0=min(p[0] for p in pcs);y0=min(p[1] for p in pcs)
    w=max(p[0]+16 for p in pcs)-x0;h=max(p[1]+p[3] for p in pcs)-y0
    im=np.zeros((h,w,4),np.uint8)
    for x,y,c,hh,fl in pcs:
        for part in range(hh//16):
            t=T[c+part]
            if fl&0x80:t=t[:,::-1]
            if fl&0x40:t=t[::-1]
            for yy in range(16):
                for xx in range(16):
                    v=t[yy,xx]
                    if v: p=PN[128+pal*16+v];im[y-y0+part*16+yy,x-x0+xx]=[(p>>16)&255,(p>>8)&255,p&255,255]
    Image.fromarray(im).resize((w*3,h*3),Image.NEAREST).save(out)
