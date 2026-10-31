import sys; sys.path.append('/workspace/wwf_sgdk/rec4'); from load import frames,dec
from arcr import *; from arcdec import poses,bt
F=frames('/workspace/wwf_sgdk/rec4/nofg/rec.bin')
def w(f,a): a-=0x1c0000; return f['ram'][a]<<8|f['ram'][a+1]
f=F[200]
for o in range(4):
    b=0x1c0100+o*0x11a; print(o,[hex(w(f,b+k)) for k in (0,2,4,6)])
codes=sorted(x['code'] for x in dec(f['spr']))
for bk in (0,3):
    c=sorted(s[2]+k for s in arc_spr(poses(bk)[0]) for k in range(2 if s[3] else 1))
    print(bk,c, all(x in codes for x in c))
print(codes)
