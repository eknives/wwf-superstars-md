import os; os.environ.setdefault('ROMV','WWF_SGDK_s04e.bin')
exec(open('/workspace/wwf_sgdk/tools/rope4e.py').read().split("\nif __name__")[0])
import collections
from PIL import ImageDraw,ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
def zone_of(mk,d=12):
    ys,xs=np.nonzero(mk); z=np.zeros_like(mk)
    if len(ys): z[max(0,ys.min()-d):ys.max()+d+1,max(0,xs.min()-d):xs.max()+d+1]=True
    return z
# geometry check: MAME P1 silhouette (sprite RAM + tiles) vs MD P1 silhouette (pixels in the wrestler palettes 2-3 only)
import struct as _st
_cr=[int(x) for x in _st.unpack('>32H',open('/workspace/wwf_sgdk/res/pal.bin','rb').read()[:64])]
_pk=pickle.load(open('/workspace/wwf_sgdk/tools/s04_poses.pkl','rb')); _L2,_L3=_pk[1],_pk[2]
def _t(w): return ((w>>1)&7,(w>>5)&7,(w>>9)&7)
BGC={_t(w) for w in _cr}; SPC={_t(w) for w in list(_L2[1:])+list(_L3[1:])}
def md_sil(B):
    q=np.rint(B.astype(float)/36.43).astype(int); tq=[tuple(v) for v in q.reshape(-1,3)]
    sp=np.array([t in SPC and t not in BGC for t in tq]).reshape(B.shape[:2]); amb=np.array([t in SPC and t in BGC for t in tq]).reshape(B.shape[:2])
    return sp,amb
def dev(A,B,mk,z=None):
    # a pixel deviates when one image shows P1 there and the other clearly shows something else (ropes/posts in front count as "something else" in both)
    sp,amb=md_sil(B)
    ka=(A[...,0].astype(int)<<16)|(A[...,1].astype(int)<<8)|A[...,2]
    ring=~mk if z is None else (z&~mk)
    bgcol=set(np.unique(ka[ring]).tolist())
    inbg=np.isin(ka,list(bgcol))
    maS=mk&~inbg; maAmb=mk&inbg
    return (sp&~maS&~maAmb)|(maS&~sp&~amb)
res=measure_cases()
S=2; W=256*S; H=224*S; LW=300
for part,(i0,i1) in enumerate(((0,5),(5,9))):
    R=res[i0:i1]
    im=Image.new('RGB',(LW+3*(W+8),28+len(R)*(H+8)),(32,32,32)); dr=ImageDraw.Draw(im)
    for c,t in enumerate(('MAME (original)','s04e (Mega Drive)','Diferencias (magenta = desviación)')): dr.text((LW+c*(W+8)+8,6),t,font=F,fill=(255,255,0))
    for k,(n,lab,f,ga,sp,pm,ps,A,B,mk) in enumerate(R):
        z=zone_of(mk); z[:40]=False   # HUD band excluded
        bad=dev(A,B,mk,z)&z
        v=(B//3).astype(np.uint8); v[z]=B[z]; v[bad]=[255,0,255]
        y=28+k*(H+8)
        for c,x in enumerate((A,B,v)): im.paste(Image.fromarray(x.astype(np.uint8)).resize((W,H),Image.NEAREST),(LW+c*(W+8),y))
        txt=lab.replace(': ',':\n').replace(' (','\n(')
        dr.multiline_text((6,y+6),'%s\n\nprueba %s, fot. %d\nMAME %s\ns04e %s\nfondo dx,dy=%d,%d\nluchador dx,dy=%d,%d\npíxeles desviados: %d\n(silueta MAME vs s04e,\nzona luchador ±12 px)'%(txt,n,f,pm,ps,ga[0],ga[1],sp[0],sp[1],bad.sum()),font=F,fill=(255,255,255))
        print(lab,'fot',f,'luchador',sp,'desviados',bad.sum())
    im.save('/workspace/wwf_sgdk/out/s04e_hoja_%d.png'%(part+1))
# frame table
rows={}
with open('/workspace/wwf_sgdk/out/s04e_tabla_posiciones.txt','w') as T_:
    T_.write('s04e vs MAME 0.276, NTSC, por fotograma (x,y,z lógicos; camX,camY; * = difiere)\n')
    names={'rWD':'Poste delantero der.: ABAJO-DER. desde (880,229), luego ABAJO','rD':'Poste delantero der.: ABAJO en (913,229)','x912':'Cuerda delantera: ABAJO en (912,229) (no sube: umbral x>=913)',
           'rU50':'Bajada con dirección contraria: ARRIBA en fot. 50 (subiendo), poste delantero der.','rU120':'Bajada con dirección contraria: ARRIBA en fot. 120, poste delantero der.'}
    for n in names:
        lim={'rU50':168,'rU120':166,'x912':120}.get(n,480)   # MAME leaves through the ropes after this (not ported)
        m,(e,par,yp,s)=best2(n,lim)
        nd=0; T_.write('\n== %s (%s) ==%s\nfot  MAME x,y,z  cam   | s04e x,y,z  cam\n'%(n,names[n],'  [comparado hasta fot. %d: después el luchador apoyado en el borde del ring interviene en MAME (lógica de juego, no portada)]'%lim if lim<len(m) else ''))
        for f in range(min(lim,len(m))):
            a=m[f]; b=s[f]; ka=(a['x'],a['y'],a['z'],a['cx'],a['cy']); kb=(b['x'],b['y'],b['z'],b['cx'],b['cy']); nd+=ka[:3]!=kb[:3]
            T_.write('%3d  %d,%d,%d  %d,%d | %d,%d,%d  %d,%d %s\n'%((f,)+ka+kb+('*' if ka!=kb else '',)))
        print(n,'pos diff',nd,'de',min(lim,len(m)))
