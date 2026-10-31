# s05b: hoja pantalla de seleccion (MAME | s05b | Diferencias) + tabla de fotogramas del parpadeo
import os; os.environ['ROMV']='/workspace/wwf_sgdk/out/WWF_SGDK_s05c.bin'
exec(open('/workspace/wwf_sgdk/tools/seltest.py').read())
from PIL import ImageDraw, ImageFont
F=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s)
Dc=q(np.array(Image.open('/tmp/selq.png').convert('RGB').resize((512,224),0))[:,256:])
m1=pickle.load(open('/tmp/m1_tl.pkl','rb'))[0]; to=pickle.load(open('/tmp/to_tl.pkl','rb'))[0]
R=[('Cursor moviéndose (1P, derecha: Savage -> Hogan)','s5m','m',39,0,m1),
   ('Eligiendo / parpadeo (Hogan, 3 fotogramas tras elegir)','s5m','m',82,0,m1),
   ('Retrato verde (Hogan elegido, cabeza visible; cursor en Duggan)','s5m','m',150,0,m1),
   ('Elección del compañero (Duggan parpadea, Hogan verde, cursor borrado)','s5m','m',165,0,m1),
   ('Fin de tiempo (auto-elección: Duggan parpadea, cursor salta a Warrior)','s5t','t',666,216,to)]
S=2; W=256*S; H=224*S; top=60; rh=H+40
img=Image.new('RGB',(3*W+40,top+len(R)*rh),(24,24,24)); d=ImageDraw.Draw(img)
for i,t in enumerate(('MAME 0.276 (original)','s05b (Mega Drive)','Diferencias (magenta)')): d.text((10+i*(W+10),18),t,font=F(26),fill=(255,255,255))
for r,(tit,dd,pre,k,sh,md) in enumerate(R):
    f=602+k-sh; A=np.array(Image.open('/workspace/wwf_sgdk/rec5/%s/%s%04d.png'%(dd,pre,f)).convert('RGB'))[8:232]; B=md[k]
    df=(q(A)!=q(B)).any(2); dy=dyn(A,B,Dc)
    g=(A.mean(2,keepdims=True)*0.35).repeat(3,2).astype(np.uint8); g[df]=(255,0,255)
    y=top+r*rh
    d.text((10,y+4),'%s — MAME f%d / s05b cuadro %d — dif. %d px (todas de paleta; %d de cursor/parpadeo)'%(tit,f,k,int(df.sum()),int(dy.sum())),font=F(17),fill=(230,230,230))
    for i,a in enumerate((A,B,g)): img.paste(Image.fromarray(a).resize((W,H),0),(10+i*(W+10),y+30))
img.save('/workspace/wwf_sgdk/out/s05b_hoja_1.png')
# tabla
A=pickle.load(open('/tmp/vs_tl.pkl','rb')); md=A[0]
M=mame('/workspace/wwf_sgdk/rec5/s5b','v',602,1199)
L=['s05b - tabla de fotogramas del parpadeo (MAME 0.276 vs s05b; NTSC; f = fotograma desde la elección)',
   'Color del fondo del retrato: A azul (original), M magenta, V verde. 1P: Duggan elegido por 1P en el cuadro 119; 2P: Warrior elegido por 2P en el cuadro 49 (prueba VS).',
   '','f    1P MAME  1P s05b   2P MAME  2P s05b']
def col(img,i):
    return state(img)[0][i]
for f in range(0,68):
    a1=col(M[602+119+f],4); b1=col(md[119+f],4); a2=col(M[602+49+f],2); b2=col(md[49+f],2)
    L.append('%-4d %-8s %-9s %-8s %-8s%s'%(f,a1,b1,a2,b2,'' if (a1,a2)==(b1,b2) else '  <-- DIF'))
L+=['','Resumen: 1P  f1-62 ciclo M,M,V,V,A,A (10 vueltas + M,M), desde f63 verde fijo.',
    '         2P  f1-62 ciclo A,A,M,M,V,V, desde f63 magenta fijo (en la imagen se ve el primer magenta en f3).',
    '','Tiempos de la pantalla (cuadro 0 = primer cuadro de la selección):',
    'evento                                MAME        s05b',
    'tiempo límite                          384         600 (10 s)',
    'primer salto auto del cursor           385         601   (= límite + 1, igual)',
    'saltos auto                            cada 16     cada 16',
    '1ª elección auto                       447         663   (límite + 63, igual)',
    '2ª elección auto (compañero)           511         727   (límite + 127, igual)',
    'última imagen de selección (1P auto)   +66         +66   tras la 2ª elección',
    'última imagen de selección (1P manual) +67         +67',
    'última imagen de selección (VS)        +114        +114 (espera 112)',
    'mover cursor: pulsación -> imagen      1 cuadro    1 cuadro',
    'después: s05b pasa directamente al combate (sin mánagers/entrada/VS)',
    'elegir: pulsación -> elección          1 cuadro    1 cuadro (parpadeo visible f1 en 1P, f3 en 2P)']
open('/workspace/wwf_sgdk/out/s05b_tabla_fotogramas.txt','w').write('\n'.join(L)+'\n')
print('\n'.join(L[:12]))
