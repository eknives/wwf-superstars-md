# worst line: 4 wrestlers + referee side by side at the same depth; count sprites / pixels per scanline from the real SAT
exec(open('/workspace/wwf_sgdk/tools/walk4.py').read().split("def run(")[0])
import struct
c=Core('/workspace/wwf_sgdk/out/WWF_SGDK_s04.bin',{b"genesis_plus_gx_region_detect":b"ntsc-u"}); c.run(60)
cam=peek(c,A_CAMX)+0x200
import sys
YY=int(sys.argv[1]) if len(sys.argv)>1 else 320
xs=[cam+20+k*46 for k in range(5)]
for k in range(5): poke(c,OX+2*k,xs[k]); poke(c,OY+2*k,YY)
c.run(2); poke(c,OX+4,xs[2]); 
for k in range(5): poke(c,OX+2*k,xs[k]); poke(c,OY+2*k,YY)
c.run(1); v=c.vram_bytes()
cnt=np.zeros(224,int); px=np.zeros(224,int); i=0; n=0
while True:
    e=struct.unpack('>4H',v[0xD800+8*i:0xD808+8*i]); y=e[0]-128; h=((e[1]>>8)&3)+1; w=((e[1]>>10)&3)+1
    for yy in range(max(0,y),min(224,y+8*h)): cnt[yy]+=1; px[yy]+=8*w
    n+=1; i=e[1]&0x7f
    if i==0: break
print('sprites in SAT',n,'max per line',cnt.max(),'at',int(cnt.argmax()),'max px per line',px.max(),'at',int(px.argmax()))
c.shot('/workspace/wwf_sgdk/out/s04_worstline.png')
