import sys; sys.path.insert(0,'/workspace/wwf_sgdk/tools'); import mv5, numpy as np
Tt=np.load('/workspace/wwf/port_35/sprtiles.npy')
T42=mv5.load('/workspace/wwf_sgdk/rec5/traj42.txt','/workspace/wwf_sgdk/rec5/traj42c.txt')
def sprimg(r,banks=(4,),codes=None):
    Mk=np.zeros((272,288+128),np.uint8)
    for s in mv5.dec(r['spr']):
        if s['bank'] not in banks: continue
        if codes and not codes(s): continue
        for part in range(s['h']//16):
            t=Tt[s['code']+part]
            if s['fx']: t=t[:,::-1]
            if s['fy']: t=t[::-1]
            yy=s['y']+16+(part*16 if not s['fy'] else (s['h']//16-1-part)*16); xx=(s['x']-512 if s['x']>=384 else s['x'])+16+64
            if 0<=yy<=256 and 0<=xx<=272+128:
                reg=Mk[yy:yy+16,xx:xx+16]; m=t>0; reg[m]=t[m]
    return Mk[16:256,16+64:272+64] if False else Mk[16:256,16:272+128]
R0=np.load('/workspace/wwf_sgdk/tools/ropeidx.npy'); I=np.load('/workspace/wwf_sgdk/tools/bgidx.npy')
def toworld(r,S):
    ys,xs=np.nonzero(S); X=(xs-64+r['cx']-512)%512; Y=(ys+512-r['cy'])%512; return X,Y,S[ys,xs]
