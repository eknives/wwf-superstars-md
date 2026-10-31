import sys;sys.path.insert(0,'tools');from render_obj import *
from PIL import Image,ImageDraw
import os
def npose(bank):
    tb=L(0x6cd8+bank*4);n=0
    while True:
        p=L(tb+n*4)
        if not(0x20000<=p<0x40000) or (n and tb+n*4>=min(L(tb+k*4) for k in range(n))): break
        n+=1
    return n
def sheet(bank,poses,out,palfix=None):
    tiles=[]
    for p in poses:
        try:
            log=[];pcs=frame(bank,p,log)
            if not pcs or len(pcs)>80: continue
            d=L(L(L(0x6cd8+bank*4)+p*4)+4);pal=palfix if palfix is not None else (P[d]>>4)&7
            render(pcs,pal,'/tmp/_s.png');tiles.append((p,Image.open('/tmp/_s.png').copy(),pal))
        except Exception as e: pass
    cols=8;W=max(t[1].width for t in tiles)+8;H=max(t[1].height for t in tiles)+20
    rows=(len(tiles)+cols-1)//cols;im=Image.new('RGBA',(cols*W,rows*H),(50,50,80,255));d=ImageDraw.Draw(im)
    for i,(p,t,pal) in enumerate(tiles):
        x=(i%cols)*W;y=(i//cols)*H;im.paste(t,(x+4,y+H-4-t.height),t);d.text((x+3,y+2),f'{p:#x} p{pal}',fill='white')
    im.save(out);return len(tiles)
