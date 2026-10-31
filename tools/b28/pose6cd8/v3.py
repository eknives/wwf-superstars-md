import sys; sys.path.append('/workspace/wwf_sgdk/rec4'); from load import frames,dec
from arcr import *; from arcdec import poses
F=frames('/workspace/wwf_sgdk/rec4/nofg/rec.bin'); f=F[200]
R=dec(f['spr']); rc=set(x['code'] for x in R)
for i,p in enumerate(poses(0)):
    s=arc_spr(p); c=set(q[2] for q in s)
    if c and c<=rc: 
        print(i,len(s))
        for q in s: print(' arc',q)
        for x in R:
            if x['code'] in c: print(' mame',x['code'],x['x'],x['y'],x['h'],x['fx'],x['fy'])
        break
