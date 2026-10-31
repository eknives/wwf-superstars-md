# s04c vs MAME 0.276: post climb, frame by frame (logic position/height, camera, shown pose, drawn anchor)
import sys,collections; sys.argv=[sys.argv[0]]
exec(open('/workspace/wwf_sgdk/tools/edge4b.py').read().split("if __name__")[0].replace("WWF_SGDK_s04b.bin",__import__("os").environ.get("ROMV","WWF_SGDK_s04c.bin")))
sys.path.insert(0,'/workspace/wwf_sgdk/rec4'); from load import dec
_ns={}; exec(open('/workspace/wwf_sgdk/rec5/an8.py').read(),_ns); T9=_ns['T']
exec(open('/workspace/wwf_sgdk/tools/build_s04c_spr.py').read().split("def bitmap(g):")[0].split("# ---- pair_table")[0])
# pose id table from ROM build order
import pickle
order_ids={}
src=open('/workspace/wwf_sgdk/tools/build_s04c_spr.py').read()
PROBES=[('U',646,330),('U',648,330),('UL',700,330),('UL',700,373),('U',888,330),('U',890,330),('UR',840,330),('UR',840,373)]
def msig(r):
    return tuple(sorted((s['code'],s['fx'],s['h']) for s in dec(r['spr']) if s['bank']==0))
def zof(r): return r['o'][0x14]<<8|r['o'][0x15]
def run(d,x0,y0,par=1,yp=0,shots=()):
    global PARK
    PARK=[(x0,y0),(600,120),(880,120),(1000,120),(760,110)]
    c=Core(ROM,{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(60)
    for _ in range(200):
        for k,(x,y) in enumerate(PARK): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        poke(c,SYM['oxf'],0); poke(c,SYM['oyf'],0); c.run(1)
    poke(c,TICK,par); poke(c,YT,yp)
    out=[]; im={}
    for f in range(480):
        for k,(x,y) in enumerate(PARK[1:],1): poke(c,OX+2*k,x); poke(c,OY+2*k,y)
        c.run(1,pad0=tuple(M[ch] for ch in d) if f<220 else ())
        camx=peek(c,SYM['camx'])+0x200; camy=0x200-peek(c,SYM['camy'])
        out.append(dict(x=peek(c,OX),y=peek(c,OY),z=peek(c,SYM['z0']),cx=camx,cy=camy,pose=peek(c,SYM['curPose']),
                        ax=peek(c,SYM['dox'])-camx, ay=camy-peek(c,SYM['doy'])-(peek(c,SYM['dz0'])-187)))
        if f in shots: im[f]=np.array(c.image().convert('RGB'))[:224]
    return out,im
def mame(d,x0,y0):
    tr=T9['m%s_%d_%d'%(d,x0,y0)]; tr={r['pt']:r for r in tr}
    out=[]
    for f in range(480):
        r=tr.get(120+f); p=tr.get(119+f)
        if r is None: break
        out.append(dict(x=r['x'],y=r['y'],z=zof(r),cx=r['cx'],cy=r['cy'],sig=msig(r),ax=p['x']-r['cx'],ay=r['cy']-p['y']-(zof(p)-187)))
    return out
if __name__=='__main__':
    sigpose={}
    tot=collections.Counter(); rows=[]
    for d,x0,y0 in PROBES:
        m=mame(d,x0,y0)
        best=None
        for par in (0,1):
          for yp in (0,1):
            s,_=run(d,x0,y0,par,yp)
            e=1000*sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m,s))+sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
            if best is None or e<best[0]: best=(e,par,yp,s)
        e,par,yp,s=best
        # pose consistency: each MAME sprite signature must map to exactly one s04c pose id
        for a,b in zip(m,s): sigpose.setdefault(a['sig'],collections.Counter())[b['pose']]+=1
        ep=sum((a['x'],a['y'],a['z'])!=(b['x'],b['y'],b['z']) for a,b in zip(m,s))
        ec=sum((a['cx'],a['cy'])!=(b['cx'],b['cy']) for a,b in zip(m,s))
        ea=sum((a['ax'],a['ay'])!=(b['ax'],b['ay']) for a,b in zip(m,s))
        first=next((i for i,(a,b) in enumerate(zip(m,s)) if (a['x'],a['y'],a['z'],a['cx'],a['cy'])!=(b['x'],b['y'],b['z'],b['cx'],b['cy'])),None)
        trig_m=next((i for i,a in enumerate(m) if a['y']==377),None); trig_s=next((i for i,b in enumerate(s) if b['y']==377),None)
        print('%-3s from (%d,%d): frames %d  pos/z diff %d  cam diff %d  drawn-anchor diff %d  first diff %s  climb@ MAME %s s04c %s'%(d,x0,y0,len(m),ep,ec,ea,first,trig_m,trig_s))
        rows.append((d,x0,y0,m,s))
    amb={k:v for k,v in sigpose.items() if len(v)>1}
    print('MAME sprite poses',len(sigpose),'ambiguous (MAME pose shown with >1 s04c pose):',len(amb))
    for k,v in list(amb.items())[:6]: print('  ',k[:2],dict(v))
    pickle.dump(rows,open('/tmp/climb_rows.pkl','wb'))
