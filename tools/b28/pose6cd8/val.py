import sys; sys.path.insert(0,'/workspace/wwf_sgdk/rec4'); from load import frames,dec
from arcdec import *
S={}
for bk in (1,2,3,0):
    s=set()
    for p in poses(bk):
        for c,t in pieces(p): s.add(c); s.add(c+1) if t else None
    S[bk]=s
F=frames('/workspace/wwf_sgdk/rec4/nofg/rec.bin')+frames()
seen={};miss={}
for f in F[::5]:
    for x in dec(f['spr']):
        if x['bank'] in S:
            seen[x['bank']]=seen.get(x['bank'],0)+1
            if x['code'] not in S[x['bank']]: miss[x['bank']]=miss.get(x['bank'],0)+1
print(seen,miss)
U=set().union(*S.values()); A=set()
for bk in range(18):
  try:
    for p in poses(bk):
        for c,t in pieces(p): A.add(c); A.add(c+1) if t else None
  except: pass
codes=[x['code'] for f in F[::5] for x in dec(f['spr'])]
print(len(codes), sum(c in A for c in codes), sum(c in U for c in codes))
