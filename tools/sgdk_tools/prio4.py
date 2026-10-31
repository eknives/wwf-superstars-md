exec(open('/workspace/wwf_sgdk/tools/walk4.py').read().split("def run(")[0])
from PIL import ImageDraw,ImageFont
Fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
cases=[('Dentro, junto a cuerda lateral dcha.\n(prioridad baja: delante de lateral)',(915,330)),('Fuera, abajo (y<280)\n(prioridad alta: delante de las cuerdas)',(760,250)),('Dentro, borde delantero y=288\n(prioridad baja)',(760,288))]
ims=[]
for lab,(x,y) in cases:
    c=Core('/workspace/wwf_sgdk/out/WWF_SGDK_s04.bin',{b"genesis_plus_gx_region_detect":b"ntsc-u"}); c.run(60)
    for _ in range(40): poke(c,OX,x); poke(c,OY,y); c.run(1)
    im=c.image().convert('RGB').crop((0,0,256,224)).resize((512,448),0); d=ImageDraw.Draw(im); d.rectangle((0,0,512,34),fill=(0,0,0)); d.multiline_text((6,2),lab,font=Fnt,fill=(255,255,0)); ims.append(im)
out=Image.new('RGB',(512*3+16,448),(32,32,32))
for i,im in enumerate(ims): out.paste(im,(i*(512+8),0))
out.save('/workspace/wwf_sgdk/out/s04_prioridad.png')
