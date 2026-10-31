from rend import *
D='/workspace/wwf/port_35/'
pal=cram(open(D+'ring_cram.bin','rb').read())
T=tiles(open(D+'rope_tiles.bin','rb').read())
segs=[(0x441,15),(0x78A,6),(0x7A1,31),(0x4AC,20)]
m={};k=0
for b,n in segs:
    for i in range(n): m[b+i]=k;k+=1
M=list(struct.unpack('>1792H',open(D+'rope_map.bin','rb').read()))
full=[0]*4096; bad=0
for i,v in enumerate(M):
    if v:
        t=v&0x7ff
        if t not in m: bad+=1; continue
        full[18*64+i]=(v&0xF800)|(m[t]+1)
T2=np.concatenate([np.zeros((1,8,8),np.uint8),T])
print('bad',bad)
render(full,64,64,T2,pal).save('ropes_plane.png')
# overlay on ring
N=struct.unpack('>4096H',open(D+'ring_names.bin','rb').read())
R=tiles(open(D+'ring_tiles.bin','rb').read())
a=np.array(render(N,64,64,R,pal)); b=np.array(render(full,64,64,T2,pal)); msk=b.sum(2)>0
a[msk]=[255,0,255]; Image.fromarray(a).save('ropes_over.png')
