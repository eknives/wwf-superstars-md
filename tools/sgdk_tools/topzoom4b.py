exec(open('/workspace/wwf_sgdk/tools/edge4b.py').read().split("if __name__")[0])
from PIL import ImageDraw,ImageFont
Fn=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
PARK=[(768,300),(600,120),(880,120),(1000,120),(760,110)]
cases=[('U',60,1,'Cuerda superior: luchador DELANTE de la cuerda'),('UL',106,0,'Esquina sup.-izq.: luchador DELANTE del poste'),('UR',108,0,'Esquina sup.-dcha.: luchador DELANTE del poste')]
S=3; out=Image.new('RGB',(2*(150*S)+40+8,30+len(cases)*(110*S+40)),(32,32,32)); d=ImageDraw.Draw(out)
d.text((20,6),'MAME (original)',font=Fn,fill=(255,255,0)); d.text((20+150*S+8,6),'s04b (Mega Drive)',font=Fn,fill=(255,255,0))
for i,(dr,k,yp,lab) in enumerate(cases):
    tr,im=probe(dr,1,yp,shots=(k,)); x,y=tr[k][0]-tr[k][2],(tr[k][3]-tr[k][1])-8
    a=np.array(Image.open('/workspace/wwf_sgdk/rec5/p6/c_%s_%03d.png'%(dr,120+k)).convert('RGB'))[8:232]
    x0=max(0,min(256-150,x-75)); y0=max(0,min(224-110,y-20))
    yy=30+i*(110*S+40); d.text((20,yy),lab+'  (P1 %d,%d)'%tr[k][:2],font=Fn,fill=(255,255,255))
    for j,img in enumerate((a,im[k])): out.paste(Image.fromarray(img[y0:y0+110,x0:x0+150]).resize((150*S,110*S),Image.NEAREST),(20+j*(150*S+8),yy+22))
out.save('/workspace/wwf_sgdk/out/s04b_cuerda_superior_zoom.png')
