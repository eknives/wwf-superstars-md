import json
ns={};exec(open('tools/anot.py').read(),ns);A=ns['A']
ns={};exec(open('tools/anot2.py').read(),ns);R=ns['R']
e=json.load(open('tools/rdis.json'))['ents'];ks=sorted(int(k) for k in e)
tot=cov=0
for i,k in enumerate(ks[:-1]):
  s=min(ks[i+1]-k,0x400);tot+=s;cov+=s*(k in R)
pct=round(100*cov/tot,1)
L=['# Rutinas (R = leída entera; A = firma antigua sin releer)','',
 f'Cobertura leída entera: {sum(k in R for k in ks)} rutinas, {pct}% de bytes (bytes por entrada = min(distancia a la siguiente, 0x400)).','',
 'Estado: C = confirmado leyendo el código entero; "SC: motivo" = SIN CONFIRMAR; P(A) = anotación antigua por firma, pendiente de releer.','',
 '| Dir | Nombre | Estado | Fuente | Función |','|---|---|---|---|---|']
for k in sorted(set(A)|set(R)):
  if k in R: n,d,s=R[k];src='R'
  else: n,d,s=A[k];s='P(A)' if s!='C' else 'C(A)';src='A'
  L.append(f'| {k:06X} | {n} | {s} | {src} | {d.replace("|","/")} |')
open('rutinas.md','w').write('\n'.join(L)+'\n')
sc=[(k,R[k][2]) for k in sorted(R) if R[k][2].startswith('SC')]
open('sistemas/sin_confirmar.md','w').write('# SIN CONFIRMAR\n\n'+'\n'.join(f'- {k:06X} {R[k][0]}: {s}' for k,s in sc)+'\n')
print(pct,len(sc))
