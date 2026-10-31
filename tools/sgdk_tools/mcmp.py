import numpy as np,glob
from PIL import Image
N=['centre','left','right','top','bottom','leftdown','rightup']
rows=[]; rep=[]
for n in N:
  st=np.stack([np.array(Image.open(f).convert('RGB')) for f in sorted(glob.glob('m_%s_*.png'%n))]).astype(int)
  arc=np.median(st,0).astype(np.uint8)
  md=np.array(Image.open('../out/s03b_ntsc-u_%s.png'%n).convert('RGB'))[:224].astype(int)
  ys=np.r_[48:200]; best=None
  for dy in range(0,17):
    for dx in range(-4,5):
      a=arc[ys+dy][:,max(0,dx):256+min(0,dx)].astype(int); b=md[ys][:,max(0,-dx):256+min(0,-dx)]
      e=np.abs(a-b).max(2).mean()
      if best is None or e<best[0]: best=(e,dy,dx)
  e,dy,dx=best
  a=arc[dy:dy+224].astype(int); d=np.abs(a-md).max(2)>40
  m=np.zeros((224,256),bool); m[48:200]=True
  # unstable arcade pixels (sprites moving / crowd anim) across the 15 frames
  unst=(np.abs(st-st[0:1]).max(3)>0).any(0)[dy:dy+224]
  dd=d&m; dst=dd&~unst
  rep.append((n,dy,dx,round(100*dd.sum()/m.sum(),2),round(100*dst.sum()/m.sum(),2)))
  vis=md.astype(np.uint8).copy(); vis[dd]=[255,0,255]
  rows.append(np.concatenate([a.astype(np.uint8),np.zeros((224,4,3),np.uint8),md.astype(np.uint8),np.zeros((224,4,3),np.uint8),vis],1))
  Image.fromarray(np.concatenate(rows[-1:],0)).save('../out/s03b_vs_mame_%s.png'%n)
Image.fromarray(np.concatenate(rows[:4],0)).save('../out/s03b_vs_mame_1.png')
Image.fromarray(np.concatenate(rows[4:],0)).save('../out/s03b_vs_mame_2.png')
for r in rep: print('%-9s dy %2d dx %2d diff%% %5.2f  diff%% excl. moving/anim %5.2f'%r)
