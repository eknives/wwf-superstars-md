from PIL import Image, ImageDraw
# hoja s15: flexion de cuerdas, MAME | s15 | Diferencias (magenta); fotogramas de /tmp/fx_NNN.png (fx15.py SAVE=1)
F=[(164,'derecha: reposo'),(170,'derecha +3'),(200,'derecha +33'),(216,'derecha +49'),(228,'derecha +61'),(240,'derecha +75'),
   (298,'izquierda +3'),(328,'izquierda +33'),(344,'izquierda +49'),(356,'izquierda +61'),(370,'izquierda +75'),(378,'izquierda: reposo')]
T=30; o=Image.new('RGB',(768,T+len(F)*(224+16)),(0,0,0)); d=ImageDraw.Draw(o)
for i,t in enumerate(('MAME 0.276','s15','Diferencias')): d.text((i*256+90,10),t,fill=(255,0,255) if i==2 else (255,255,255))
for j,(f,lab) in enumerate(F):
    y=T+j*240; d.text((4,y+2),'fotograma %d - cuerda %s'%(f,lab),fill=(255,255,0)); o.paste(Image.open('/tmp/fx_%03d.png'%f),(0,y+16))
o.save('/workspace/wwf_sgdk/out/s15_hoja.png'); print(o.size)
