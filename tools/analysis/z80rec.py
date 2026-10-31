from z80dis import z80
import re,sys
d=open('/tmp/z/24ab-0.12','rb').read()
seen={};todo=[0,0x38,0x66,0x18f];ents=set(todo)
while todo:
  a=todo.pop()
  while a<len(d) and a not in seen:
    i=z80.decode(d[a:a+4],a); t=z80.disasm(i); seen[a]=(t,i.len)
    m=re.search(r'(CALL|JP|JR|DJNZ)\b.*?(0x[0-9a-f]+)',t)
    if m and '(' not in t.split()[-1]:
      tg=int(m.group(2),16)
      if m.group(1)=='CALL': ents.add(tg)
      todo.append(tg)
    if t in ('RET','RETN','RETI') or t.startswith('JP (') or re.match(r'(JP|JR) 0x',t): break
    a+=i.len
with open('/tmp/z80.lst','w') as f:
  for a in sorted(seen):
    if a in ents: f.write('; ---- %04x\n'%a)
    f.write('%04x %s\n'%(a,seen[a][0]))
print(len(seen),sum(v[1] for v in seen.values()),len(ents))
