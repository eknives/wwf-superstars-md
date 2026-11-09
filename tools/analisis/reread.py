import re,sys
ns={};exec(open('tools/anot2.py').read(),ns);R=ns['R']
L=open('arc_rec.dis').read().split('\n')
starts={}
for i,l in enumerate(L):
    m=re.match(r'; ---- rutina ([0-9a-f]+)',l)
    if m: starts[int(m.group(1),16)]=i
ks=sorted(a for a in R if a>=0x13000)
i0,i1=int(sys.argv[1]),int(sys.argv[2])
for a in ks[i0:i1]:
    n,dsc,st=R[a];print(f'##### {a:06X} {n} [{st}] :: {dsc}')
    if a not in starts: print('  (sin cabecera)');continue
    j=starts[a]+1
    while j<len(L) and not L[j].startswith('; ----'):
        if L[j].strip(): print(L[j])
        j+=1
