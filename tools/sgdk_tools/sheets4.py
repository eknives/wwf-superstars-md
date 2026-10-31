import sys; sys.argv=['x']; exec(open('/workspace/wwf_sgdk/tools/walk4.py').read().split("WANT=set(range")[0])
sys.path.insert(0,'/workspace/wwf_sgdk/tools'); from sheet4 import sheet
mame=lambda p:np.array(Image.open(p).convert('RGB'))[8:232]
# 1) lineup t=200 (all 5 at arcade lineup positions, same camera 0x280/0x180)
c=Core('/workspace/wwf_sgdk/out/WWF_SGDK_s04.bin',{b'genesis_plus_gx_region_detect':b'ntsc-u'})
for i in range(80):
    c.run(1)
    if peek(c,A_CAMX)==128 and i>20: pass
FN=frames('/workspace/wwf_sgdk/rec4/nofg/rec.bin')
MC={w(FN[t],0x1c002a)-0x200:t for t in range(210,189,-1)}
c=Core('/workspace/wwf_sgdk/out/WWF_SGDK_s04.bin',{b'genesis_plus_gx_region_detect':b'ntsc-u'})
for i in range(120):
    c.run(1); cx=peek(c,A_CAMX)
    if i>30 and cx in MC: break
tm=MC[cx]; setobj(c,FN[tm],range(5)); c.run(1); s4=np.array(c.image().convert('RGB'))[:224]; print('cam after',peek(c,A_CAMX)); print('s04 camx',cx,'MAME t',tm)
rows=[('Presentación\nt=%d\ncam x=0x%x y=0x180\n(4 luchadores\n+ árbitro)'%(tm,w(FN[tm],0x1c002a)),mame('/workspace/wwf_sgdk/rec4/nofg/f%04d.png'%tm),s4)]
# 2) P1 walking, same inputs, others at MAME positions
WANT={320,420,520,550,570,610}
pos,shots=run(1,0,0)
lab={320:"Andando dcha.",420:"Andando arriba",520:'Diagonal arr.-dcha.',550:'Diagonal abj.-izq.',570:'Diagonal arr.-izq.',610:'Parado (idle)'}
for t in sorted(WANT):
    rows.append(('%s\nt=%d\nP1 x=%d y=%d\ncam x=0x%x\n(rivales: MAME\nIA moviéndose;\ns04 en idle)'%(lab[t],t,w(F[t],0x1c010c),w(F[t],0x1c0110),w(F[t],0x1c002a)),mame('/workspace/wwf_sgdk/rec4/walk/f%04d.png'%t) if t%10==0 else None,shots[t]))
rows=[r for r in rows if r[1] is not None]
print(len(rows))
st=sheet(rows[:4],'/workspace/wwf_sgdk/out/s04_vs_mame_1.png'); print(st)
if len(rows)>4: print(sheet(rows[4:],'/workspace/wwf_sgdk/out/s04_vs_mame_2.png'))
