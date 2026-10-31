import json,sys
d=json.load(open('tools/rdis.json'));I={int(k):v for k,v in d['ins'].items()};E={int(k):v for k,v in d['ents'].items()}
n=int(sys.argv[1])
for a in sys.argv[2:]:
    p=int(a,16);print('=====%06x %s'%(p,E.get(p,'')))
    for k in range(n):
        if p not in I:break
        s,m,o=I[p];print('%06x %s %s'%(p,m,o));p+=s
        if m in('rts','rte'):break
