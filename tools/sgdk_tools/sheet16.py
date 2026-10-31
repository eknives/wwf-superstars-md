# hoja s16: cuerdas laterales, MAME 0.276 | s16 | Diferencias (magenta = solo s16, verde = solo MAME), por fotograma, con desplazamiento por franja vertical
import os,sys,numpy as np
from PIL import Image, ImageDraw
os.environ.setdefault('FS','2')
exec(open('/tmp/rope16.py').read().split("for x in res: print(x)")[0].replace("if os.environ.get('SAVE2'):","if True:"))
def bands(ra,rb,x0,x1):
    out=[]
    for y0 in range(48,200,38):
        a=np.nonzero(ra[y0:y0+38,x0:x1]); b=np.nonzero(rb[y0:y0+38,x0:x1])
        out.append('--' if len(a[1])<20 or len(b[1])<20 else '%+d'%round(float(np.median(b[1])-np.median(a[1]))))
    return out
for sd,(f0,f1) in (('derecha',(164,252)),('izquierda',(292,380))):
    fr=[f for f in range(f0,f1,4)]; W=3*112; H=224; T=34
    o=Image.new('RGB',(W+150,T+len(fr)*(H+14)),(0,0,0)); d=ImageDraw.Draw(o)
    for i,t in enumerate(('MAME 0.276','s16','Diferencias')): d.text((i*112+20,8),t,fill=(255,0,255) if i==2 else (255,255,255))
    d.text((W+6,8),'dx por franja (px)',fill=(255,255,0)); d.text((W+6,20),'arriba -> abajo',fill=(255,255,0))
    for j,f in enumerate(fr):
        im=np.array(Image.open('/tmp/rp_%03d.png'%f)); x0=144 if sd=='derecha' else 0
        A=im[:,x0:x0+112]; B=im[:,256+x0:256+x0+112]; D=im[:,512+x0:512+x0+112]
        ra=(D==[0,255,0]).all(2)|(D==[255,255,255]).all(2); rb=(D==[255,0,255]).all(2)|(D==[255,255,255]).all(2)
        y=T+j*(H+14); d.text((4,y),'fotograma %d (cuerda %s, %+d desde el rebote)'%(f,sd,f-(166 if sd=='derecha' else 294)),fill=(255,255,0))
        o.paste(Image.fromarray(np.concatenate([A,B,D],1)),(0,y+12))
        for k,v in enumerate(bands(ra,rb,0,112)): d.text((W+10,y+12+48+k*38+12),'franja %d: %s'%(k+1,v),fill=(255,255,255))
    o.save('/workspace/wwf_sgdk/out/s16_hoja_%s.png'%('der' if sd=='derecha' else 'izq')); print(sd,o.size)
