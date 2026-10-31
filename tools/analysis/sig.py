import json,sys,re,bisect
sys.path.insert(0,'tools');from anot import A
d=json.load(open('tools/rdis.json'));I={int(k):v for k,v in d['ins'].items()};E=sorted(int(k) for k in d['ents']);EN={int(k):v for k,v in d['ents'].items()}
ks=sorted(I);callers={}
for p in ks:
    m=I[p]
    if m[1] in('jsr','bsr','bsr.w','bsr.b','bsr.s') :
        t=re.fullmatch(r'\$([0-9a-f]+)(\.[wl])?',m[2].strip())
        if t: callers.setdefault(int(t.group(1),16),[]).append(p)
def body(e):
    j=E.index(e);nx=E[j+1] if j+1<len(E) else 0x40000
    return [(p,I[p]) for p in ks[bisect.bisect_left(ks,e):bisect.bisect_left(ks,nx)]]
def sig(e,n):
    b=body(e);sz=sum(x[1][0] for x in b)
    ram=sorted(set(re.findall(r'\$(1c[0-9a-f]{4})',' '.join(x[1][2] for x in b))))
    fld=sorted(set(re.findall(r'\$([0-9a-f]+)\(a0\)',' '.join(x[1][2] for x in b))),key=lambda s:int(s,16))
    calls=sorted(set(x[1][2] for x in b if x[1][1].startswith(('jsr','bsr'))))
    snd=[b[k-1][1][2] for k,x in enumerate(b) if k and '25e6' in x[1][2]]
    print('== %06x sz%d cal%d %s | ram %s | a0 %s | calls %s | snd %s'%(e,sz,len(callers.get(e,[])),EN[e][:14],','.join(ram[:8]),','.join(fld[:14]),' '.join(c[:9] for c in calls[:8]),' '.join(s[:10] for s in snd[:3])))
    for p,(s,m,o) in b[:n]: print('   %06x %s %s'%(p,m,o[:40]))
if __name__=='__main__':
    n=int(sys.argv[1]);lo=int(sys.argv[2],16);hi=int(sys.argv[3],16)
    for e in E:
        if lo<=e<hi and e not in A: sig(e,n)
