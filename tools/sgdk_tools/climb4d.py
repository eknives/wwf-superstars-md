# s04d vs MAME 0.276 frame by frame, input schedules (rec5 traj11/traj12)
import sys,os,collections; sys.argv=[sys.argv[0]]
os.environ.setdefault('ROMV','WWF_SGDK_s04d.bin')
exec(open('/workspace/wwf_sgdk/tools/climb4c.py').read().split("\nif __name__")[0])
TT={}
for fn in ('traj11.txt','traj12.txt'):
    _n={}; exec(open('/workspace/wwf_sgdk/rec5/an8.py').read().replace('traj9.txt',fn),_n); TT.update(_n['T'])
PR={'dD50':(648,330,[("U",0,50),("D",50,110)]),'dD80':(648,330,[("U",0,50),("D",80,140)]),'dD120':(648,330,[("U",0,60),("D",120,180)]),
    'dL120':(648,330,[("U",0,60),("L",120,180)]),'dRD120':(888,330,[("U",0,60),("D",120,180)]),
    'cDL':(660,260,[("DL",0,220)]),'bL2':(618,250,[("D",0,220)]),'bL4':(640,229,[("DL",0,220)]),'bL1':(640,229,[("L",0,220)]),
    'bU120':(660,260,[("DL",0,60),("U",120,180)]),'bU50':(660,260,[("DL",0,50),("U",50,110)]),'bD120':(660,260,[("DL",0,60),("D",120,180)])}
def pad(sg,f):
    g=''
    for d,a,b in sg:
        if a<=f<b: g=d
    return tuple(M[ch] for ch in g)
def run2(x0,y0,sg,par,yp,shots=()):
    PARK=[(x0,y0),(600,120),(880,120),(1000,120),(760,110)]
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
    for _ in range(200):
        for k,(x,y) in enumerate(PARK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        poke(c,SYM['oxf'],0); poke(c,SYM['oyf'],0); c.run(1)
    poke(c,TICK,par); poke(c,YT,yp); out=[]; im={}
    for f in range(480):
        for k,(x,y) in enumerate(PARK[1:],1): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        c.run(1,pad0=pad(sg,f))
        camx=peek(c,SYM['camx'])+0x200; camy=0x200-peek(c,SYM['camy'])
        out.append(dict(x=peek(c,OX),y=peek(c,OY),z=peek(c,SYM['z0']),cx=camx,cy=camy,pose=peek(c,SYM['curPose'])))
        if f in shots: im[f]=np.array(c.image().convert('RGB'))[:224]
    return out,im
def mame2(n):
    tr={r['pt']:r for r in TT[n]}; out=[]
    for f in range(480):
        r=tr.get(120+f)
        if r is None: break
        out.append(dict(x=r['x'],y=r['y'],z=zof(r),cx=r['cx'],cy=r['cy'],sig=msig(r)))
    return out
def best2(n,lim=480):
    x0,y0,sg=PR[n]; m=mame2(n); bb=None
    for par in (0,1):
        for yp in (0,1):
            s,_=run2(x0,y0,sg,par,yp)
            e=1000*sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m[:lim],s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m[:lim],s))
            if bb is None or e<bb[0]: bb=(e,par,yp,s)
    return m,bb
if __name__=='__main__':
    rows={}
    for n in (sys.argv_names if hasattr(sys,'argv_names') else PR):
        m,(e,par,yp,s)=best2(n)
        ep=[f for f,(a,b) in enumerate(zip(m,s)) if (a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z'])]
        ec=sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
        print('%-7s pos/z diff %3d  cam diff %3d  first pos diff %s'%(n,len(ep),ec,ep[:1]))
        if ep: f=ep[0]; print('        M',[(m[i]['x'],m[i]['y'],m[i]['z']) for i in range(f-1,f+3)],'S',[(s[i]['x'],s[i]['y'],s[i]['z']) for i in range(f-1,f+3)])
        rows[n]=(m,s,par,yp)
    pickle.dump(rows,open('/tmp/climb4d_rows.pkl','wb'))
