# drawn P1 pixels vs MAME (background aligned) at the bottom/side ropes and the new climbs
import sys,os; os.environ.setdefault('ROMV','WWF_SGDK_s04d.bin')
exec(open('/workspace/wwf_sgdk/tools/climb4d.py').read().split("\nif __name__")[0])
exec(open('/workspace/wwf_sgdk/tools/pix4d.py').read().split("\nif __name__")[0].split("PR=[")[0].split("exec(open('/workspace/wwf_sgdk/tools/climb4c.py')")[1].split("\n",1)[1])
PR.update({'eD':(760,300,[("D",0,220)]),'eL':(700,300,[("L",0,220)]),'eR':(820,300,[("R",0,220)])})
CASES=[('dD120','Poste sup. izq.: aproximación',20),('dD120','Poste sup. izq.: inicio de la subida',40),('dD120','Poste sup. izq.: en el poste',100),
       ('dRD120','Poste sup. der.: aproximación',20),('dRD120','Poste sup. der.: inicio de la subida',40),('dRD120','Poste sup. der.: en el poste',100),
       ('eD','Cuerda inferior: andando',40),('eD','Cuerda inferior: contacto',52),('eL','Cuerda lateral izq.: contacto',60),('eR','Cuerda lateral der.: contacto',70),
       ('cDL','Poste inferior izq.: aproximación',28),('cDL','Poste inferior izq.: inicio de la subida',40),('cDL','Poste inferior izq.: en el poste',120),('cDL','Poste inferior izq.: bajada',320),
       ('dD80','Bajada con dirección contraria (ABAJO, poste sup. izq.)',100),('dRD120','Bajada con dirección contraria (ABAJO, poste sup. der.)',140),('bU120','Bajada con dirección contraria (ARRIBA, poste inf. izq.)',132),('dD120','Tras bajar con ABAJO (sigue andando)',175)]
def measure_cases():
    res=[]; cache={}
    for n,lab,f0 in CASES:
        if n not in cache:
            m,(e,par,yp,s)=best2(n,{'eD':52,'eL':75,'eR':87}.get(n,480)); x0,y0,sg=PR[n]
            fr=[f for nn,_,f in CASES if nn==n]; shots=sorted(set(ff for f in fr for ff in range(f,f+12)))
            s,im=run2(x0,y0,sg,par,yp,shots=shots); cache[n]=(m,s,im)
        m,s,im=cache[n]; tr={r['pt']:r for r in TT[n]}
        pick=None
        for f in range(f0,f0+12):
            dd='p11' if os.path.exists('/workspace/wwf_sgdk/rec5/p11/%s_%03d.png'%(n,120+f)) else 'p13'
            A=np.array(Image.open('/workspace/wwf_sgdk/rec5/%s/%s_%03d.png'%(dd,n,120+f)).convert('RGB'))[8:232]
            mk=mask_of(tr[119+f])[16:240]; B=im[f]
            bgm=np.zeros_like(mk); bgm[60:200:3,8:248:3]=True; bgm&=~mk
            ga=best(A,B,bgm,4)[1:]; sp=best(A,B,mk,12)[1:]
            if pick is None: pick=(f,A,B,mk,ga,sp)
            if ga==(0,0): pick=(f,A,B,mk,ga,sp); break
        f,A,B,mk,ga,sp=pick
        res.append((n,lab,f,ga,sp,(m[f]['x'],m[f]['y'],m[f]['z']),(s[f]['x'],s[f]['y'],s[f]['z']),A,B,mk))
    return res
if __name__=='__main__':
    for r in measure_cases(): print(r[0],r[1],'fot',r[2],'fondo',r[3],'sprite',r[4],'M',r[5],'S',r[6])
