import re,json,collections
L=[]
for ln in open('/workspace/wwf_sgdk/analisis/arc.dis'):
    m=re.match(r'([0-9a-f]{6}) (.*)',ln.rstrip())
    if m:L.append((int(m.group(1),16),m.group(2)))
addr=[a for a,_ in L]
code=lambda s: not s.startswith('dc.') and not s.startswith('ori.b #$0, d0')
tgt=collections.defaultdict(set)
for a,s in L:
    m=re.match(r'(jsr|bsr\.[swb]|bsr|jmp|bra\.[swb])\s+\$([0-9a-f]+)(\.l)?$',s)
    if m and m.group(1)[0] in 'jb' and not m.group(1).startswith('bra') and not m.group(1)=='jmp':
        tgt[int(m.group(2),16)].add(a)
# vectors
import struct
ents=sorted(t for t in tgt if t<0x40000)
idx={a:i for i,(a,_) in enumerate(L)}
R={}
for i,e in enumerate(ents):
    end=ents[i+1] if i+1<len(ents) else 0x40000
    if e not in idx: continue
    body=[(a,s) for a,s in L[idx[e]:] if a<end]
    # stop at first rts/rte/jmp after start for size
    sz=0;n=0;ram=collections.Counter();calls=set();cut=end
    for a,s in body:
        n+=1
        for r in re.findall(r'\$(1c[0-9a-f]{4})',s): ram[r]+=1
        m=re.match(r'(jsr|bsr\S*)\s+\$([0-9a-f]+)',s)
        if m: calls.add(int(m.group(2),16))
        if s in('rts','rte') or s.startswith('jmp') :
            cut=a+2; break
    R[e]=dict(end=cut,n=n,callers=sorted(tgt[e]),calls=sorted(calls),ram=dict(ram.most_common(12)))
json.dump({hex(k):v for k,v in R.items()},open('/workspace/wwf_sgdk/analisis/tools/cg.json','w'))
tot=sum(v['end']-k for k,v in R.items())
print(len(R),'rutinas',tot,'bytes en rutinas')
codeb=sum(1 for a,s in L if code(s))
print('instr code',codeb)
