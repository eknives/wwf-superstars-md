import sys,struct; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
W=np.array(struct.unpack('>%dH'%(80*68),open('../res/bgb_map.bin','rb').read())).reshape(68,80)
T=open('../res/bgb_tiles.bin','rb').read()
c=Core('WWF_SGDK_s03.bin',{b'genesis_plus_gx_region_detect':b'pal'}); c.run(60); c.run(300,pad0=('LEFT',)); c.run(30)
v=bytes(c.vram_bytes()[:65536]); B=np.array(struct.unpack('>2048H',v[0xE000:0xF000])).reshape(32,64)
sx,sy=-32,120; c0=(sx+32)>>3; r0=(sy+8+16)>>3
bad=[]
for r in range(r0,r0+31):
  for cc in range(c0,c0+33):
    e=W[r,cc]; m=B[r&31,cc&63]
    if e&0xfff==0:
      if m&0x7ff: bad.append((r,cc,'expect0',hex(m)))
      continue
    slot=m&0x7ff; data=v[slot*32:slot*32+32]; want=T[((e&0xfff)-1)*32:(e&0xfff)*32]
    if data!=want: bad.append((r,cc,hex(e),hex(m)))
import collections; print(len(bad), collections.Counter(b[0] for b in bad), collections.Counter(b[1] for b in bad))
