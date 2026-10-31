# s05 sheets: MAME (original) | s05 (Mega Drive) | Diferencias (magenta), strikes and lock-up
import os,sys,pickle; os.environ.setdefault('ROMV','WWF_SGDK_s05.bin')
exec(open('/workspace/wwf_sgdk/tools/mv5test.py').read().rsplit("\nif __name__=='__main__':",1)[0])
src=open('/workspace/wwf_sgdk/tools/sheet4d2.py').read()
exec(src.split("res=measure_cases()")[0].split("import collections",1)[1])   # zone_of, md_sil, dev, fonts
Tt=np.load('/workspace/wwf/port_35/sprtiles.npy')
def mask2(r,banks=(0,2)):
    Mk=np.zeros((272,288),bool)
    for s in mv5.dec(r['spr']):
        if s['bank'] not in banks: continue
        for part in range(s['h']//16):
            t=Tt[s['code']+part]
            if s['fx']: t=t[:,::-1]
            if s['fy']: t=t[::-1]
            yy=s['y']+16+(part*16 if not s['fy'] else (s['h']//16-1-part)*16); xx=s['x']+16
            if 0<=yy<=256 and 0<=xx<=272: Mk[yy:yy+16,xx:xx+16]|=(t>0)
    return Mk[16:256,16:272]
C=[('pA','Puñetazo (botón 1): reposo',2),('pA','Puñetazo: preparación',12),('pA','Puñetazo: golpe',26),('pA','Puñetazo: reacción del rival',30),('pA','Puñetazo: vuelta a reposo',40),
   ('pB','Patada (botón 2): preparación',15),('pB','Patada: golpe',22),('pB','Patada: rival tocado',40),('pB','Patada: rival recuperado',62),
   ('pA0','Puñetazo al aire (rival lejos)',26),('pB0','Patada al aire (rival lejos)',22),
   ('lk','Agarre: acercamiento andando',30),('lk','Agarre: contacto',38),('lk','Agarre: forcejeo A',45),('lk','Agarre: forcejeo B',62),('lk','Agarre: cambio de lado',152),('lk','Agarre: ciclo repetido',264)]
cache={}; res=[]
for n,lab,f in C:
    if n not in cache:
        m,(e,par,yp,s)=best(n); fs=sorted(set(ff for nn,_,ff in C if nn==n)); s,im=run(n,par,yp,shots=fs); cache[n]=(m,s,im)
    m,s,im=cache[n]; tr=T[n]
    A=np.array(Image.open('/workspace/wwf_sgdk/rec5/p23/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]
    mk=mask2(tr[119+f])[16:240]
    B=im[f]; res.append((n,lab,f,A,B,mk,(m[f]['x'],m[f]['y'],m[f]['x2'],m[f]['y2']),(s[f]['x'],s[f]['y'],s[f]['x2'],s[f]['y2'])))
S=2; W=256*S; H=224*S; LW=300; tot=[]
for part,(i0,i1) in enumerate(((0,6),(6,11),(11,17))):
    R=res[i0:i1]
    img=Image.new('RGB',(LW+3*(W+8),28+len(R)*(H+8)),(32,32,32)); dr=ImageDraw.Draw(img)
    for c,t in enumerate(('MAME (original)','s05 (Mega Drive)','Diferencias (magenta = desviación)')): dr.text((LW+c*(W+8)+8,6),t,font=F,fill=(255,255,0))
    for k,(n,lab,f,A,B,mk,pm,ps) in enumerate(R):
        z=zone_of(mk); z[:40]=False
        bad=dev(A,B,mk,z)&z
        v=(B//3).astype(np.uint8); v[z]=B[z]; v[bad]=[255,0,255]
        y=28+k*(H+8)
        for c,x in enumerate((A,B,v)): img.paste(Image.fromarray(x.astype(np.uint8)).resize((W,H),Image.NEAREST),(LW+c*(W+8),y))
        txt=lab.replace(': ',':\n')
        dr.multiline_text((6,y+6),'%s\n\nprueba %s, fot. %d\nMAME J1 %d,%d J2 %d,%d\ns05  J1 %d,%d J2 %d,%d\npíxeles desviados: %d\n(siluetas J1+J2,\nzona ±12 px)'%((txt,n,f)+pm+ps+(bad.sum(),)),font=F,fill=(255,255,255))
        print(lab,'fot',f,'desviados',bad.sum()); tot.append((lab,int(bad.sum())))
    img.save('/workspace/wwf_sgdk/out/s05_hoja_%d.png'%(part+1))
# frame table
R5=pickle.load(open('/tmp/mv5_rows.pkl','rb'))
names={'pA':'Puñetazo (botón 1), J2 a 40 px','pB':'Patada (botón 2), J2 a 40 px','pA0':'Puñetazo al aire, J2 a 100 px','pB0':'Patada al aire, J2 a 100 px','lk':'Agarre: J1 anda a la derecha hacia J2'}
with open('/workspace/wwf_sgdk/out/s05_tabla_fotogramas.txt','w') as o:
    o.write('s05 vs MAME 0.276 (1P contra 2P, J1 Duggan, J2 Warrior quieto), NTSC, por fotograma\nfot | MAME J1 x,y  J2 x,y  cam  poseJ1 poseJ2 | s05 igual | * = difiere\n(pose: + = cambia de dibujo en ese fotograma)\n')
    for n in R5:
        m,s,par,yp=R5[n]; tr=T[n]
        m1=[mv5.grp(tr,119+f,0)[1] for f in range(len(m))]; m2=[mv5.grp(tr,119+f,2)[1] for f in range(len(m))]
        o.write('\n== %s (%s) ==\n'%(n,names[n])); nd=0
        for f in range(len(m)):
            a=m[f]; b=s[f]
            ca='+' if f and m1[f]!=m1[f-1] else ' '; cb='+' if f and m2[f]!=m2[f-1] else ' '
            da='+' if f and b['p1']!=s[f-1]['p1'] else ' '; db='+' if f and b['p2']!=s[f-1]['p2'] else ' '
            ka=(a['x'],a['y'],a['x2'],a['y2'],a['cx'],a['cy']); kb=(b['x'],b['y'],b['x2'],b['y2'],b['cx'],b['cy'])
            d=ka!=kb or (ca,cb)!=(da,db); nd+=d
            o.write('%3d | %d,%d %d,%d %d,%d %s%s | %d,%d %d,%d %d,%d %s%s %s\n'%((f,)+ka+(ca,cb)+kb+(da,db,'*' if d else '')))
        print(n,'filas distintas',nd,'de',len(m))
