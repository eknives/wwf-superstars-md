import struct,wave
r=open('/tmp/z/24a9-0.46','rb').read()+open('/tmp/z/24j8-0.45','rb').read()
st=[16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552]
ix=[-1,-1,-1,-1,2,4,6,8]
def dec(a,b):
  s=0;i=0;o=[]
  for byte in r[a:b+1]:
    for n in (byte>>4,byte&15):
      d=st[i];v=d>>3
      if n&1:v+=d>>2
      if n&2:v+=d>>1
      if n&4:v+=d
      s=s-v if n&8 else s+v; s=max(-2048,min(2047,s)); i=max(0,min(48,i+ix[n&7])); o.append(s)
  return o
import sys
for n in range(1,0x40):
  e=r[n*8:n*8+8];a=int.from_bytes(e[0:3],'big')&0x3ffff;b=int.from_bytes(e[3:6],'big')&0x3ffff
  if not a or b<=a: continue
  o=dec(a,b);w=wave.open('oki/s%02x.wav'%n,'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000)
  w.writeframes(b''.join(struct.pack('<h',x*16) for x in o));w.close()
  import math
  q=len(o)//4 or 1; env=[ (sum(x*x for x in o[k*q:(k+1)*q])/q)**.5 for k in range(4)]
  zc=sum(1 for k in range(1,len(o)) if (o[k-1]<0)!=(o[k]<0))/(len(o)/8000)/2
  print('%02x %06x-%06x %.2fs env %s zc~%dHz'%(n,a,b,len(o)/8000,[int(x) for x in env],zc))
