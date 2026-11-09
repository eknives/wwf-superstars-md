import json,sys,re
R=json.load(open('tools/cg.json'))
L=[l.rstrip() for l in open('arc.dis') if re.match(r'[0-9a-f]{6} ',l)]
idx={int(l[:6],16):i for i,l in enumerate(L)}
for a in sys.argv[2:]:
    k=hex(int(a,16))
    if k not in R: print("=====",k,"NO ALINEADA");continue
    v=R[k];s=int(k,16)
    print('=====',k,'callers',len(v['callers']),[hex(c) for c in v['callers']][:6])
    i=idx[s];n=0
    while i<len(L) and int(L[i][:6],16)<v['end'] and n<int(sys.argv[1]):print(L[i]);i+=1;n+=1
