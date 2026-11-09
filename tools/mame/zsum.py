import csv,itertools,sys
R=list(csv.DictReader(open(sys.argv[1])))
for n,g in itertools.groupby(R,key=lambda r:r['case']):
  g=[r for r in g if int(r['k'])>=255];prev=None;print('==',n)
  for r in g:
    key=(r['pnS'],r['fsv'],r['apose'],r['rf0'],r['rf1'])
    if key!=prev: print('  k',r['k'],'fs',r['fsv'],'X',r['ax'],'Z',r['az'],'pose',r['apose'],'rope',r['rf0'],r['rf1']);prev=key
    if int(r['k'])>330: print('  final X',r['ax']); break
