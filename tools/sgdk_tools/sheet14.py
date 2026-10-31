# s06: hoja MAME | s06 | Diferencias (P1 a la derecha del rival: golpes espejados, agarre, barra de energía)
exec(open('/tmp/mv14.py').read())
PR['q100']=(760,300,900,380,[('R12',0,3),('1',100,103)],200)
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

T28=mv5.load('/workspace/wwf_sgdk/rec5/traj28.txt','/workspace/wwf_sgdk/rec5/traj28b.txt')
def runq(mvv,shots):
    PK=[(760,300),(600,120),(800,300),(1000,120),(760,110)]
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
    for _ in range(200):
        for k,(x,y) in enumerate(PK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        c.run(1)
    im={}
    for f in range(90):
        for k in (1,3,4): poke(c,OX+2*k,PK[k][0]); poke(c,OY+2*k,PK[k][1])
        if f==1: poke(c,SYM['mv2'],mvv); poke(c,SYM['mk2'],0)
        c.run(1)
        if f in shots: im[f]=np.array(c.image().convert('RGB'))[:224]
    return im
C=[('q100',20,'Carrera hacia\nlas cuerdas derechas',0),('q100',50,'Choque con las\ncuerdas derechas',0),('q100',76,'Rebote en las\ncuerdas derechas',0),('q100',96,'Vuelta corriendo\nhacia la izquierda',0),('q100',116,'Ataque en carrera',0),('q100',150,'Fin del ataque',0)]
S=2; W=256*S; H=224*S; LW=260
img=Image.new('RGB',(LW+3*(W+8),30+len(C)*(H+8)),(30,30,30)); d=ImageDraw.Draw(img)
for i,t in enumerate(('MAME (original)','s14 (Mega Drive)','Diferencias (magenta)')): d.text((LW+i*(W+8)+8,6),t,font=FF,fill=(255,255,0))
for r,(n,f,lab,mvv) in enumerate(C):
    if mvv: B=runq(mvv,(f+1,))[f+1]; A=np.array(Image.open('rec5/p28/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]; tr=T28[n]
    else:
        s,im=run(n,0,0,shots=(f,)); B=im[f]; A=np.array(Image.open('rec5/p38/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]; tr=T[n]
    mk=mask2(tr[119+f])[16:240]; z=zone_of(mk); z[:40]=False; z&=~mask2(tr[119+f],banks=(1,3,4,5,6,7))[16:240]   # s14: Savage/Hogan/arbitro fuera de la prueba (no comparados)
    bad=dev(A,B,mk,z)&z
    v=(B//3).astype(np.uint8); v[z]=B[z]; v[bad]=(255,0,255)
    y=30+r*(H+8)
    for i,X in enumerate((A,B,v)): img.paste(Image.fromarray(X.astype(np.uint8)).resize((W,H),0),(LW+i*(W+8),y))
    d.multiline_text((6,y+6),'%s\nprueba %s fot. %d\npíxeles desviados\n(P1 y P2): %d'%(lab,n,f,bad.sum()),font=FF,fill=(255,255,255))
    print(lab,bad.sum())
img.save('/workspace/wwf_sgdk/out/s14_hoja.png')
