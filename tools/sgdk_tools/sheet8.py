# s06: hoja MAME | s06 | Diferencias (P1 a la derecha del rival: golpes espejados, agarre, barra de energía)
exec(open('/tmp/mv8.py').read())
PR['lw']=(740,300,820,300,[('R',0,60)]+[('1',70+i*8,73+i*8) for i in range(60)],520)
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
C=[('lw',150,'Agarre (Duggan aporrea 1)',0),('lw',230,'Duggan levanta a Warrior',0),('lw',260,'Lanzamiento en el aire',0),('lw',300,'Warrior en la lona',0),('lw',344,'Warrior se levanta',0)]
S=2; W=256*S; H=224*S; LW=260
img=Image.new('RGB',(LW+3*(W+8),30+len(C)*(H+8)),(30,30,30)); d=ImageDraw.Draw(img)
for i,t in enumerate(('MAME (original)','s10 (Mega Drive)','Diferencias (magenta)')): d.text((LW+i*(W+8)+8,6),t,font=FF,fill=(255,255,0))
for r,(n,f,lab,mvv) in enumerate(C):
    if mvv: B=runq(mvv,(f+1,))[f+1]; A=np.array(Image.open('rec5/p28/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]; tr=T28[n]
    else:
        s,im=run(n,0,0,shots=(f,)); B=im[f]; A=np.array(Image.open('rec5/p30/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]; tr=T[n]
    mk=mask2(tr[119+f])[16:240]; z=zone_of(mk); z[:40]=False
    bad=dev(A,B,mk,z)&z
    v=(B//3).astype(np.uint8); v[z]=B[z]; v[bad]=(255,0,255)
    y=30+r*(H+8)
    for i,X in enumerate((A,B,v)): img.paste(Image.fromarray(X.astype(np.uint8)).resize((W,H),0),(LW+i*(W+8),y))
    d.multiline_text((6,y+6),'%s\nprueba %s fot. %d\npíxeles desviados\n(luchadores): %d'%(lab,n,f,bad.sum()),font=FF,fill=(255,255,255))
    print(lab,bad.sum())
img.save('/workspace/wwf_sgdk/out/s12_hoja_centro.png')
