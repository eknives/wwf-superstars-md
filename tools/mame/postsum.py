import csv,sys,collections
for fn in sys.argv[1:]:
  d=collections.OrderedDict()
  for r in csv.DictReader(open(fn)): d.setdefault(r['case'],[]).append(r)
  print('##',fn)
  for c,R in d.items():
    R=[r for r in R if 50<=int(r['k'])<=630]
    lost=[int(R[i]['k']) for i in range(1,len(R)) if R[i]['loops']==R[i-1]['loops']]
    win=max((sum(1 for k in lost if a<=k<a+59) for a in range(50,630)),default=0)
    L=R[-1]
    print(f"{c:22s} perdidos={len(lost):3d}/{len(R)-1} max_en_59={win:2d} fondo_mal={L['bad']} celdas_comprobadas={L['chk']} vacias(sin slot)={L['zero']} visible_dentro={L['visok']} cam_final=({L['camx']},{L['camy']}) x_final={L['ox']},{L['oy']}")
