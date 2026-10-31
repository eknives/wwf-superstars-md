import sys,struct; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
import numpy as np
W0=np.array(struct.unpack('>%dH'%(80*68),open('../res/bgb_map.bin','rb').read())).reshape(68,80)
T=open('../res/bgb_tiles.bin','rb').read()
sym={l.split()[-1]:int(l.split()[0],16) for l in open('symbol.txt') if len(l.split())==3}
c=Core('WWF_SGDK_s03.bin',{b'genesis_plus_gx_region_detect':b'pal'}); c.run(60)
def chk():
  r=c.ram_bytes(); rx0=struct.unpack('>h',bytes(r[(sym['rx0']&0xffff):][:2]))[0]; ry0=struct.unpack('>h',bytes(r[(sym['ry0']&0xffff):][:2]))[0]
  v=bytes(c.vram_bytes()[:65536]); B=np.array(struct.unpack('>2048H',v[0xE000:0xF000])).reshape(32,64)
  bad=[]
  for rr in range(ry0,ry0+31):
    for cc in range(rx0,rx0+33):
      e=W0[rr,cc] if 0<=rr<68 and 0<=cc<80 else 0; m=B[rr&31,cc&63]
      if e&0xfff==0: continue
      slot=m&0x7ff
      if v[slot*32:slot*32+32]!=T[((e&0xfff)-1)*32:(e&0xfff)*32]: bad.append((rr,cc))
  return rx0,ry0,bad

A=set(); p=open('../res/anim.bin','rb').read(); q=np.frombuffer(p,'>u2'); i=0
while i<len(q):
  c0,r0,n=q[i],q[i+1],q[i+2]; A|={(r0+j,c0+k) for j in range(8) for k in range(8)}; i+=3+n*64
h=[set(),set()]
for f in range(400):
  c.run(1,pad0=('LEFT',)); rx0,ry0,bad=chk(); s=set(bad)-A
  if s&h[0]&h[1]: print(f,rx0,ry0,sorted(s&h[0]&h[1])[:8]); break
  h=[h[1],s]
