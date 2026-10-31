# s06: hoja MAME | s06 | Diferencias (P1 a la derecha del rival: golpes espejados, agarre, barra de energía)
exec(open('/tmp/mv6.py').read())
exec(open('/workspace/wwf_sgdk/tools/sheet5.py').read().split("C=[('pA'")[0].split("exec(open('/workspace/wwf_sgdk/tools/mv5test.py')")[0]+"\n")
src5=open('/workspace/wwf_sgdk/tools/sheet5.py').read()
exec(src5.split("src=open('/workspace/wwf_sgdk/tools/sheet4d2.py').read()")[1].split("C=[('pA'")[0].replace("\n","\n",1) if False else "")
src=open('/workspace/wwf_sgdk/tools/sheet4d2.py').read()
exec(src.split("res=measure_cases()")[0].split("import collections",1)[1])
Tt=np.load('/workspace/wwf/port_35/sprtiles.npy')
exec("def mask2"+src5.split("def mask2",1)[1].split("C=[('pA'")[0])
from PIL import ImageDraw, ImageFont
FF=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
q=lambda v:np.minimum(7,(np.asarray(v,float)/34+0.5).astype(int))
C=[('rA',26,'Puñetazo mirando a la izquierda'),('rB',22,'Patada mirando a la izquierda'),('rB',85,'Barra WARRIOR tras patada (48 -> 44)'),('rk',45,'Agarre desde la derecha')]
S=2; W=256*S; H=224*S; LW=260
img=Image.new('RGB',(LW+3*(W+8),30+len(C)*(H+8)),(30,30,30)); d=ImageDraw.Draw(img)
for i,t in enumerate(('MAME (original)','s06 (Mega Drive)','Diferencias (magenta)')): d.text((LW+i*(W+8)+8,6),t,font=FF,fill=(255,255,0))
cache={}
for r,(n,f,lab) in enumerate(C):
    if n not in cache:
        m,(e,par,yp,s)=best(n); fs=[ff for nn,ff,_ in C if nn==n]; s,im=run(n,par,yp,shots=fs); cache[n]=im
    B=cache[n][f]; A=np.array(Image.open('rec5/p26/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]
    mk=mask2(T[n][119+f])[16:240]; z=zone_of(mk); z[:40]=False
    bad=dev(A,B,mk,z)&z
    hud=np.zeros_like(mk); hud[18:34,60:125]=True
    badh=hud&(np.abs(q(A)-q(B)).max(2)>1)
    v=(B//3).astype(np.uint8); v[z]=B[z]; v[bad]=(255,0,255)
    y=30+r*(H+8)
    for i,X in enumerate((A,B,v)): img.paste(Image.fromarray(X.astype(np.uint8)).resize((W,H),0),(LW+i*(W+8),y))
    d.multiline_text((6,y+6),'%s\nprueba %s fot. %d\npíxeles desviados\n(luchadores): %d'%(lab,n,f,bad.sum()),font=FF,fill=(255,255,255))
    print(lab,bad.sum(),badh.sum())
img.save('/workspace/wwf_sgdk/out/s06_hoja.png')
