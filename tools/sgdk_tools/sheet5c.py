# s05c: hoja pelo de Duggan (MAME | s05c | Diferencias), con s05b como referencia
exec(open('/tmp/skip.py').read())
import os
from PIL import ImageDraw, ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
q=lambda v:np.minimum(7,(np.asarray(v,float)/34+0.5).astype(int))
rows=[('pB',15,'Patada: preparación'),('pB',22,'Patada: golpe (pierna arriba)'),('pA',26,'Puñetazo: golpe'),('lk',45,'Agarre: forcejeo')]
img={}
for rom in ('WWF_SGDK_s05c.bin',):
    os.environ['ROMV']=rom
    exec(open('/workspace/wwf_sgdk/tools/sheet5.py').read().split("C=[('pA'")[0])
    for n,f,_ in rows:
        m,(e,par,yp,s)=best(n); s,im=run(n,par,yp,shots=(f,)); img[(rom,n,f)]=im[f]
Z=4; cw=60*Z; ch=80*Z
out=Image.new('RGB',(170+3*(cw+8),30+len(rows)*(ch+8)),(30,30,30)); d=ImageDraw.Draw(out)
for i,t in enumerate(('MAME (original)','s05c (Mega Drive)','Diferencias (magenta)')): d.text((170+i*(cw+8),8),t,font=F,fill=(255,255,0))
for r,(n,f,lab) in enumerate(rows):
    A=np.array(Image.open('rec5/p23/%s_%03d.png'%(n,120+f)).convert('RGB'))[8:232]
    mk=mask2(T[n][119+f],banks=(0,))[16:240]&~mask2(T[n][119+f],banks=(2,6))[16:240]
    ys,xs=np.nonzero(mk); y0,x0=ys.min()-4,xs.min()-4
    C=img[('WWF_SGDK_s05c.bin',n,f)]
    bad=mk&(np.abs(q(A)-q(C)).max(2)>1)
    v=(C//3).astype(np.uint8); v[mk]=C[mk]; v[bad]=(255,0,255)
    y=30+r*(ch+8)
    for i,X in enumerate((A,C,v)): out.paste(Image.fromarray(X[y0:y0+80,x0:x0+60].astype(np.uint8)).resize((cw,ch),0),(170+i*(cw+8),y))
    d.multiline_text((6,y+6),'%s\nprueba %s fot. %d\nDuggan, píxeles\nde color distinto:\n%d'%(lab,n,f,bad.sum()),font=F,fill=(255,255,255))
    print(lab,bad.sum())
out.save('/workspace/wwf_sgdk/out/s05c_hoja_pelo.png')
