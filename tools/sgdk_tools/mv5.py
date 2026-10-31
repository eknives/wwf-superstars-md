import sys,collections; sys.path.insert(0,'/workspace/wwf_sgdk/rec4'); from load import dec
def load(fn,fn2):
    T=collections.defaultdict(dict)
    for l in open(fn):
        f=l.split(); T[f[0]][int(f[1])]=dict(pt=int(f[1]),x=int(f[2]),y=int(f[3]),cx=int(f[4]),cy=int(f[5]),o=bytes.fromhex(f[6]),spr=bytes.fromhex(f[7]))
    for l in open(fn2):
        f=l.split(); r=T[f[0]][int(f[1])]; r['x2']=int(f[2]); r['y2']=int(f[3]); r['o2']=bytes.fromhex(f[4])
    return T
def z(o): return o[0x14]<<8|o[0x15]
def grp(tr,t,bank):
    # sprites of frame t drawn with positions of t-1 (arcade sprite lag)
    r=tr[t]; p=tr[t-1]
    if bank==0: ox,oy,oz=p['x'],p['y'],z(p['o'])
    else: ox,oy,oz=p['x2'],p['y2'],z(p['o2'])
    ax=ox-r['cx']; ay=r['cy']-oy-(oz-187)
    g=[dict(x,x=x['x']-ax,y=x['y']-ay) for x in dec(r['spr']) if x['bank']==bank]
    return g, tuple(sorted((x['code'],x['x'],x['y'],x['fx'],x['fy'],x['h']) for x in g))
