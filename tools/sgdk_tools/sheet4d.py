import os,sys
exec(open('/workspace/wwf_sgdk/tools/pix4d.py').read().split("\nif __name__")[0])
exec(open('/workspace/wwf_sgdk/tools/sheet4.py').read().split("\nif __name__")[0])
SEL=[('U',648,330,'izq.'),('UR',840,373,'der.')]
MO=[('Aproximación (andar)',-20),('Inicio de la subida (A)',4),('Subida (C)',20),('En el poste (F)',80),('Bajada (E)',302),('Tras bajar',360)]
out=[]
for d,x0,y0,lado in SEL:
    m=mame(d,x0,y0); tr=next(i for i,a in enumerate(m) if a['y']==377)-1
    bb=None
    for par in (0,1):
        for yp in (0,1):
            s,_=run(d,x0,y0,par,yp)
            e=1000*sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m,s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
            if bb is None or e<bb[0]: bb=(e,par,yp)
    _,par,yp=bb
    cand=[tr+k+j for _,k in MO for j in range(8)]
    s,im=run(d,x0,y0,par,yp,shots=cand)
    tr9={r['pt']:r for r in T9['m%s_%d_%d'%(d,x0,y0)]}
    for lab,k in MO:
        for j in range(8):
            f=tr+k+j; A=np.array(Image.open('/workspace/wwf_sgdk/rec5/p9/m%s_%d_%d_%03d.png'%(d,x0,y0,120+f)).convert('RGB'))[8:232]
            mk=mask_of(tr9[119+f])[16:240]; B=im[f]
            bgm=np.zeros_like(mk); bgm[60:200:3,8:248:3]=True; bgm&=~mk
            ga=best(A,B,bgm,4)[1:]; sp=best(A,B,mk,12)[1:]
            if ga==(0,0): break
        print(d,x0,y0,lab,f,'fondo',ga,'sprite',sp)
        out.append(('%s\n%s (%d,%d), poste %s\nfot. %d  sprite dx,dy=%d,%d'%(lab,d,x0,y0,lado,f,sp[0],sp[1]),A,B))
for i in range(2):
    st=sheet(out[i*6:i*6+6],'/workspace/wwf_sgdk/out/s04d_poste_%s.png'%('izq','der')[i],cols=('MAME (original)','s04d (Mega Drive)','Diferencias'))
    print(['%.1f'%x for x in st])
# ---- Diferencias: MAME colours mapped to MD colours (LUT from the aligned image), compared only around P1 (MAME sprite box +12 px)
def binary_dilation(m,iterations=1):
    ys,xs=np.nonzero(m); z=np.zeros_like(m)
    if len(ys): z[max(0,ys.min()-iterations):ys.max()+iterations+1,max(0,xs.min()-iterations):xs.max()+iterations+1]=True
    return z
from PIL import ImageDraw,ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
def lut_map(A,B):
    ka=(A[...,0].astype(int)<<16)|(A[...,1].astype(int)<<8)|A[...,2]; kb=(B[...,0].astype(int)<<16)|(B[...,1].astype(int)<<8)|B[...,2]
    import collections; c=collections.defaultdict(collections.Counter)
    for a,b in zip(ka.ravel(),kb.ravel()): c[a][b]+=1
    L={a:v.most_common(1)[0][0] for a,v in c.items()}
    return np.vectorize(L.get)(ka)==kb
S=2; W=256*S; H=224*S; LW=230
for i in range(2):
    R=out[i*6:i*6+6]
    im=Image.new('RGB',(LW+3*(W+8),28+len(R)*(H+8)),(32,32,32)); dr=ImageDraw.Draw(im)
    for c,t in enumerate(('MAME (original)','s04d (Mega Drive)','Diferencias (magenta = desviación)')): dr.text((LW+c*(W+8)+8,6),t,font=F,fill=(255,255,0))
    for k,(lab,A,B) in enumerate(R):
        f=int(lab.split('fot. ')[1].split()[0]); d,x0,y0=SEL[i][:3]
        tr9={r['pt']:r for r in T9['m%s_%d_%d'%(d,x0,y0)]}; mk=mask_of(tr9[119+f])[16:240]
        zone=binary_dilation(mk,iterations=12)
        bad=(~lut_map(A,B))&zone
        v=(B//3).astype(np.uint8); v[zone]=B[zone]; v[bad]=[255,0,255]
        y=28+k*(H+8)
        for c,x in enumerate((A,B,v)): im.paste(Image.fromarray(x.astype(np.uint8)).resize((W,H),Image.NEAREST),(LW+c*(W+8),y))
        dr.multiline_text((6,y+6),lab+'\n\npíxeles desviados: %d\n(zona: luchador ±12 px)'%bad.sum(),font=F,fill=(255,255,255))
        print(lab.split('\n')[0],d,f,'desviados',bad.sum())
    im.save('/workspace/wwf_sgdk/out/s04d_poste_%s.png'%('izq','der')[i])
