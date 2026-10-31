# s05 vs MAME 0.276 (1P vs 2P, P1 Duggan, P2 Warrior idle): strikes and lock-up, frame by frame
import os,sys,pickle; sys.argv=[sys.argv[0]]
exec(open('/workspace/wwf_sgdk/tools/edge4b.py').read().split("if __name__")[0].replace("WWF_SGDK_s04b.bin",os.environ.get("ROMV","WWF_SGDK_s05.bin")))
sys.path.insert(0,'/workspace/wwf_sgdk/tools'); import mv5
M.update({'1':'A','2':'B'})
T=mv5.load('/workspace/wwf_sgdk/rec5/traj23.txt','/workspace/wwf_sgdk/rec5/traj23b.txt')
PR={'pA':(760,300,800,300,[('1',0,3)],90),'pB':(760,300,800,300,[('2',0,3)],90),'pA0':(760,300,860,300,[('1',0,3)],90),
    'pB0':(760,300,860,300,[('2',0,3)],110),'lk':(740,300,820,300,[('R',0,60)],300)}
def pad(sg,f):
    g=''
    for d,a,b in sg:
        if a<=f<b: g=d
    return tuple(M[ch] for ch in g)
def run(n,par,yp,shots=()):
    x0,y0,x2,y2,sg,N=PR[n]; PK=[(x0,y0),(600,120),(x2,y2),(1000,120),(760,110)]
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
    for _ in range(200):
        for k,(x,y) in enumerate(PK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        poke(c,SYM['oxf'],0); poke(c,SYM['oyf'],0); c.run(1)
    poke(c,TICK,par); poke(c,YT,yp); out=[]; im={}
    for f in range(N):
        for k in (1,3,4): poke(c,OX+2*k,PK[k][0]); poke(c,OY+2*k,PK[k][1])
        c.run(1,pad0=pad(sg,f))
        out.append(dict(x=peek(c,OX),y=peek(c,OY),x2=peek(c,OX+4),y2=peek(c,OY+4),cx=peek(c,SYM['camx'])+0x200,cy=0x200-peek(c,SYM['camy']),
                        p1=peek(c,SYM['curPose']),p2=peek(c,SYM['curPose']+4)))
        if f in shots: im[f]=np.array(c.image().convert('RGB'))[:224]
    return out,im
def mame(n):
    tr=T[n]; return [dict(x=tr[120+f]['x'],y=tr[120+f]['y'],x2=tr[120+f]['x2'],y2=tr[120+f]['y2'],cx=tr[120+f]['cx'],cy=tr[120+f]['cy']) for f in range(PR[n][5]) if 120+f in tr]
def best(n):
    m=mame(n); bb=None
    for par in (0,1):
        for yp in (0,1):
            s,_=run(n,par,yp)
            e=1000*sum((a['x'],a['y'],a['x2'],a['y2'])!=(b['x'],b['y'],b['x2'],b['y2']) for a,b in zip(m,s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
            if bb is None or e<bb[0]: bb=(e,par,yp,s)
    return m,bb
if __name__=='__main__':
    rows={}
    for n in PR:
        m,(e,par,yp,s)=best(n)
        ep=[f for f,(a,b) in enumerate(zip(m,s)) if (a['x'],a['y'],a['x2'],a['y2'])!=(b['x'],b['y'],b['x2'],b['y2'])]
        ec=sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
        print('%-4s pos diff %3d  cam diff %3d  first %s'%(n,len(ep),ec,ep[:1]))
        if ep: f=ep[0]; print('   M',[(m[i]['x'],m[i]['y'],m[i]['x2'],m[i]['y2']) for i in range(max(0,f-1),f+3)],'S',[(s[i]['x'],s[i]['y'],s[i]['x2'],s[i]['y2']) for i in range(max(0,f-1),f+3)])
        rows[n]=(m,s,par,yp)
    pickle.dump(rows,open('/tmp/mv5_rows.pkl','wb'))
