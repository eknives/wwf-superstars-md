# labelled Spanish comparison sheet: rows = moment, cols MAME (original) | s04 (Mega Drive) | Diferencias
import sys,numpy as np
from PIL import Image,ImageDraw,ImageFont
def sheet(rows,out,thr=40,cols=('MAME (original)','s04 (Mega Drive)','Diferencias')):
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
    S=2; W=256*S; H=224*S; LW=190; TH=28; NC=len(cols)
    im=Image.new('RGB',(LW+NC*(W+8),TH+len(rows)*(H+8)),(32,32,32)); d=ImageDraw.Draw(im)
    for i,t in enumerate(cols): d.text((LW+i*(W+8)+8,6),t,font=F,fill=(255,255,0))
    stats=[]
    for k,(lab,a,b) in enumerate(rows):
        a=a.astype(int); b=b.astype(int); m=np.zeros((224,256),bool); m[48:200]=True
        dd=(np.abs(a-b).max(2)>thr)&m; v=(b//3).astype(np.uint8); v[m]=b[m]; v[dd]=[255,0,255]; v[~m]//=2
        y=TH+k*(H+8)
        for i,x in enumerate((a.astype(np.uint8),b.astype(np.uint8),v)[:NC]):
            im.paste(Image.fromarray(x).resize((W,H),Image.NEAREST),(LW+i*(W+8),y))
        pct=100*dd.sum()/m.sum(); stats.append(pct)
        d.multiline_text((6,y+6),lab+'\n\ndif. %.1f%%\n(zona 48-199)'%pct,font=F,fill=(255,255,255))
    im.save(out); return stats
