exec(open('/workspace/wwf_sgdk/tools/edge4b.py').read().split("if __name__")[0].replace("WWF_SGDK_s04b.bin","WWF_SGDK_s04c.bin"))
exec(open('/workspace/wwf_sgdk/rec5/an.py').read().split("if __name__")[0].replace("traj3.txt","/workspace/wwf_sgdk/rec5/traj3.txt").replace("for l in open('/workspace/wwf_sgdk/rec5/traj3.txt'):\n    n,pt,x,y=l.split()","for l in open('/workspace/wwf_sgdk/rec5/traj3.txt'):\n    n,pt,x,y=l.split()[:4]"))
c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
for k,(x,y) in enumerate(PARK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
c.run(1)
import pickle
bad=[];n=0
probes=[('L',768,y,'fL_%d'%y) for y in range(229,374)]+[('R',768,y,'fR_%d'%y) for y in range(229,374)]+[('U',x,300,'fU_%d'%x) for x in range(640,897,8)]+[('D',x,300,'fD_%d'%x) for x in range(640,897,8)]
for d,x,y,name in probes:
    poke(c,SYM['climb'],0); poke(c,SYM['z0'],187); poke(c,OX,x); poke(c,OY,y); poke(c,SYM['oxf'],0); poke(c,SYM['oyf'],0)
    for f in range(150):
        for k,(px,py) in enumerate(PARK[1:],1): poke(c,OX+2*k,px); poke(c,OY+2*k,py)
        c.run(1,pad0=tuple(M[ch] for ch in d))
    got=(peek(c,OX),peek(c,OY)); want=res[name][0]; n+=1
    if name.startswith('fD') and tuple(want)[1]==224: want=(want[0],229)
    if got!=tuple(want): bad.append((name,want,got))
print('probes',n,'mismatch',len(bad)); print([b for b in bad if not b[0].startswith('fU')][:30]); print([b for b in bad if b[0].startswith('fU')])
