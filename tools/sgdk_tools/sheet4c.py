import sys; sys.argv=[sys.argv[0]]
exec(open('/workspace/wwf_sgdk/tools/climb4c.py').read().split("\nif __name__")[0])
exec(open('/workspace/wwf_sgdk/tools/sheet4.py').read().split("if __name__")[0])
from PIL import Image
import numpy as np
SEL=[('U',648,330,'izq.'),('UL',700,373,'izq.'),('U',888,330,'der.'),('UR',840,373,'der.')]
rows=[]; tab=open('/workspace/wwf_sgdk/out/s04c_tabla_posiciones.txt','w')
tab.write('s04c vs MAME 0.276, NTSC, por fotograma (x,y,z logicos; camX,camY; * = difiere)\n')
for d,x0,y0,lado in SEL:
    m=mame(d,x0,y0)
    tr=next(i for i,a in enumerate(m) if a['y']==377)-1
    best=None
    for par in (0,1):
        for yp in (0,1):
            s,_=run(d,x0,y0,par,yp)
            e=1000*sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m,s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
            if best is None or e<best[0]: best=(e,par,yp)
    _,par,yp=best
    mom=[('Aproximación',tr-8),('Inicio de la subida',tr+12),('En el poste',tr+80)]
    s,im=run(d,x0,y0,par,yp,shots=[f for _,f in mom])
    for lab,f in mom:
        a=np.array(Image.open('/workspace/wwf_sgdk/rec5/p9/m%s_%d_%d_%03d.png'%(d,x0,y0,120+f)).convert('RGB'))[8:232]
        rows.append(('%s\n%s (%d,%d)\nposte %s, fot. %d'%(lab,d,x0,y0,lado,f),a,im[f]))
    tab.write('\n== %s desde (%d,%d), poste %s; disparo fot. %d ==\nfot  MAME x,y,z  cam   | s04c x,y,z  cam\n'%(d,x0,y0,lado,tr))
    for f in range(len(m)):
        a=m[f]; b=s[f]; ka=(a['x'],a['y'],a['z'],a['cx'],a['cy']); kb=(b['x'],b['y'],b['z'],b['cx'],b['cy'])
        tab.write('%3d  %d,%d,%d  %d,%d | %d,%d,%d  %d,%d %s\n'%((f,)+ka+kb+('*' if ka!=kb else '',)))
for i in range(4):
    st=sheet(rows[i*3:i*3+3],'/workspace/wwf_sgdk/out/s04c_poste_%d.png'%(i+1),cols=('MAME (original)','s04c (Mega Drive)'))
    print(i+1,['%.1f'%x for x in st])
