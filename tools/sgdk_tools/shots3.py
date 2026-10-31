import sys; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
from PIL import Image
import numpy as np
def s16(r,a): v=r[a]<<8|r[a+1]; return v-65536 if v>32767 else v
A=dict(camx=int(sys.argv[1],16)&0xffff, camy=int(sys.argv[2],16)&0xffff, dma=int(sys.argv[3],16)&0xffff, vc=int(sys.argv[4],16)&0xffff, pk=int(sys.argv[5],16)&0xffff)
seqs=[('centre',[]),('left',[(300,('LEFT',))]),('right',[(400,('RIGHT',))]),('top',[(300,('UP',))]),('bottom',[(300,('DOWN',))]),('leftdown',[(300,('LEFT','DOWN'))]),('rightup',[(400,('RIGHT','UP'))])]
for reg in ('ntsc-u','pal'):
  for name,sq in seqs:
    c=Core('WWF_SGDK_s03.bin',{b'genesis_plus_gx_region_detect':reg.encode()}); c.run(60)
    for n,p in sq: c.run(n,pad0=p)
    c.run(30); r=c.ram_bytes(); c.shot('s03_%s_%s.png'%(reg,name))
    print(reg,name,'cam',s16(r,A['camx']),s16(r,A['camy']),'dmaMax',(r[A['dma']]<<24|r[A['dma']+1]<<16|r[A['dma']+2]<<8|r[A['dma']+3]),'vcMax',r[A['vc']]<<8|r[A['vc']+1],'poolPeak',r[A['pk']]<<8|r[A['pk']+1])
