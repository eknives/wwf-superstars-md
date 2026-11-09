import random,re
ns={};exec(open('tools/anot2.py').read(),ns);R=ns['R']
ks=sorted(R);mid=(ks[0]+ks[-1])//2
lo=[k for k in ks if k<mid];hi=[k for k in ks if k>=mid]
random.seed(20261031)
s=sorted(random.sample(lo,12)+random.sample(hi,26))
txt=open('arc_rec.dis').read().split('\n')
idx={}
for i,l in enumerate(txt):
  m=re.match(r'; ---- rutina ([0-9a-f]+)',l)
  if m: idx[int(m.group(1),16)]=i
for k in s:
  i=idx.get(k);out=[]
  if i is not None:
    j=i+1
    while j<len(txt) and not txt[j].startswith('; ---- rutina') and len(out)<90: out.append(txt[j]);j+=1
  print(f'=== {k:06X} {R[k][0]} [{R[k][2]}] :: {R[k][1]}')
  print('\n'.join(out));print()
