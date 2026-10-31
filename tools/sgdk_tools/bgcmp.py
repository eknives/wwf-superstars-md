import numpy as np,sys,collections
from PIL import Image
tag=sys.argv[1]; N=['centre','left','right','top','bottom','leftdown','rightup']
# anim mask in world coords -> screen per position
q=np.frombuffer(open('../res/anim.bin','rb').read(),'>u2'); AM=np.zeros((68*8,80*8),bool); i=0
while i<len(q):
  c0,r0,n=q[i],q[i+1],q[i+2]; AM[r0*8:r0*8+64,c0*8:c0*8+64]=True; i+=3+n*64
cams={'centre':(128,120),'left':(-32,120),'right':(336,120),'top':(128,-8),'bottom':(128,184),'leftdown':(-32,273),'rightup':(320,-8)}
pairs=collections.Counter(); tot=0; bad=0; rows=[]; per=[]
for n in N:
  arc=np.array(Image.open('bg_%s.png'%n).convert('RGB'))[8:232].astype(int)
  md=np.array(Image.open('../out/%s_ntsc-u_%s.png'%(tag,n)).convert('RGB'))[:224].astype(int)
  sx,sy=cams[n]; am=AM[sy+16+16:sy+16+16+224, sx+32:sx+32+256]
  m=np.zeros((224,256),bool); m[48:200]=True; m&=~am
  d=np.abs(arc-md).max(2)>40
  per.append((n,round(100*(d&m).sum()/m.sum(),2)))
  for y,x in zip(*np.nonzero(m)): pairs[(tuple(arc[y,x]),tuple(md[y,x]))]+=1
  vis=md.astype(np.uint8).copy(); vis[d&m]=[255,0,255]; vis[~m]//=3
  rows.append(np.concatenate([arc.astype(np.uint8),np.zeros((224,4,3),np.uint8),md.astype(np.uint8),np.zeros((224,4,3),np.uint8),vis],1))
Image.fromarray(np.concatenate(rows[:4],0)).save('../out/%s_vs_mamebg_1.png'%tag)
Image.fromarray(np.concatenate(rows[4:],0)).save('../out/%s_vs_mamebg_2.png'%tag)
print('diff% per position (bg only, crowd-anim cells excluded):',per)
byc=collections.defaultdict(collections.Counter)
for (a,b),v in pairs.items(): byc[a][b]+=v
T=sum(pairs.values()); E=0
out=[]
for a,cnt in byc.items():
  b,v=cnt.most_common(1)[0]; s=sum(cnt.values()); e=max(abs(a[k]-b[k]) for k in range(3)); E+=e*s
  out.append((s,a,b,e,round(100*v/s)))
out.sort(reverse=True)
print('weighted mean max-channel error',round(E/T,1))
for s,a,b,e,f in out[:40]: print('%6d px  arcade %-15s -> MD %-15s err %3d (%d%% consistent)'%(s,a,b,e,f))
