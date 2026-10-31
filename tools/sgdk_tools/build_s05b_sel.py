# s05b: assets de la pantalla de seleccion (plano B estatico 32x28, cursores 1P/2P 8x9 tiles en plano A)
import numpy as np, pickle, struct
exec(open('tools/selq.py').read().split("if __name__")[0])
R=pickle.load(open('/tmp/selq.pkl','rb')); tp,pals,assign=R['tp'],R['pals'],R['assign']
nbg=[0]*4; bgent={}
for k in range(6):
    p=assign[k]; bgent[k]=(p,1+(15-[sum(1 for kk in range(6) if assign[kk]==pp) for pp in range(4)][p])+nbg[p]); nbg[p]+=1
# palette words
md=lambda c:(int(c[2])<<9)|(int(c[1])<<5)|(int(c[0])<<1)
cram=[0]*64
for p in range(4):
    for j,c in enumerate(pals[p]): cram[p*16+1+j]=md(rgb[c])
for k,(p,i) in bgent.items(): cram[p*16+i]=md(AZ)
tiles=[];tix={};mp=[]
for t in range(NT):
    ty,tx=divmod(t,32); p=tp[t]; sl=(slice(ty*8,ty*8+8),slice(tx*8,tx*8+8))
    kk=np.vectorize(ci.get)(K[sl]); b=bgcell[sl]
    j=D[kk][:,:,pals[p]].argmin(2)+1
    for k in range(6): j[b==k]=bgent[k][1]
    key_=j.astype(np.uint8).tobytes()
    if key_ not in tix: tix[key_]=len(tiles); tiles.append(j)
    mp.append((p<<13)|tix[key_])
print('tiles',len(tiles))
def tb(j): return bytes((int(j[y,x])<<4)|int(j[y,x+1]) for y in range(8) for x in range(0,8,2))
open('res/sel_tiles.bin','wb').write(b''.join(tb(j) for j in tiles))
open('res/sel_map.bin','wb').write(b''.join(struct.pack('>H',v) for v in mp))
open('res/sel_pal.bin','wb').write(b''.join(struct.pack('>H',v) for v in cram))
# cursores: bloque 8x9 tiles con origen en la celda (arcade px)
org={'Savage':(16,32),'Hogan':(96,16),'Warrior':(176,32),'Honky':(16,128),'Duggan':(96,144),'BigBoss':(176,128)}
p3=pals[3]; cur=[]
for pl in ('1P','2P'):
    acc=None
    for n,(x0,y0) in org.items():
        m,img=o2[(pl,n)]; blk_m=m[y0:y0+72,x0:x0+64]; blk=img[y0:y0+72,x0:x0+64]
        if acc is None or blk_m.sum()>acc[0].sum(): acc=(blk_m,blk)
    bm,bi=acc
    J=np.zeros((72,64),int); bad=0
    for y,x in zip(*np.nonzero(bm)):
        c=ci.get(int(key(q(bi[y,x].astype(int)))))
        if c not in p3: bad+=1; continue
        J[y,x]=1+p3.index(c)
    print(pl,'pix',bm.sum(),'fuera de paleta',bad)
    cur+= [J[ty*8:ty*8+8,tx*8:tx*8+8] for ty in range(9) for tx in range(8)]
open('res/sel_cur.bin','wb').write(b''.join(tb(j) for j in cur))
with open('src/sel.h','w') as f:
    f.write('// generado por tools/build_s05b_sel.py\n#define SEL_NT %d\n'%len(tiles))
    f.write('static const u8 selBgPal[6]={%s};\n'%','.join(str(bgent[k][0]*16+bgent[k][1]) for k in range(6)))
    f.write('// celdas: 0 Savage 1 Hogan 2 Warrior (arriba) 3 Honky 4 Duggan 5 BigBoss (abajo); origen del cursor en tiles MD (x,y)\n')
    f.write('static const u8 selCurX[6]={%s};\nstatic const u8 selCurY[6]={%s};\n'%(','.join(str(org[n][0]//8) for n in names),','.join(str(org[n][1]//8-1) for n in names)))
print(names, bgent)
