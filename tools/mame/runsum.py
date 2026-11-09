import csv,sys,itertools
for fn in sys.argv[1:]:
  print('##',fn)
  R=list(csv.DictReader(open(fn)))
  for n,g in itertools.groupby(R,key=lambda r:r['case']):
    g=[r for r in g if r['rn']=='1' and int(r['rnk'])>4]
    if len(g)<10: print(n,'sin carrera',len(g)); continue
    t=[float(r['t']) for r in g]; x=[int(r['ox']) for r in g]
    # recta minimos cuadrados
    N=len(t);mt=sum(t)/N;mx=sum(x)/N;v=sum((a-mt)*(b-mx) for a,b in zip(t,x))/sum((a-mt)**2 for a in t)
    poses=sum(1 for i in range(1,N) if g[i]['pose']!=g[i-1]['pose']); dt=t[-1]-t[0]
    print(f"{n:6s} frames={N:3d} dur={dt:.3f}s v={abs(v):6.1f} px/s  x {x[0]}->{x[-1]}  cambios_pose/s={poses/dt:5.2f}")
