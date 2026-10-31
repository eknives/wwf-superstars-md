# Desensamblado recursivo (capstone) del programa 68000 de WWF Superstars (set wwfsstarj, 24ac-0_j-1.34/24ad-0_j-1.35)
import capstone,struct,re,json
a=open('/workspace/wwf/rom/24ac-0_j-1.34','rb').read();b=open('/workspace/wwf/rom/24ad-0_j-1.35','rb').read()
rom=bytes(x for p in zip(a,b) for x in p); open('tools/prog.bin','wb').write(rom)
md=capstone.Cs(capstone.CS_ARCH_M68K,capstone.CS_MODE_M68K_000)
vec={i:struct.unpack('>I',rom[i*4:i*4+4])[0] for i in range(64)}
ins={};ents={};todo=[]
def add(t,why):
    if t is None or t>=0x40000 or t%2 or t<0x400:return
    if t not in ents: ents[t]=why
    todo.append(t)
for i,v in vec.items():
    if i>=1: add(v,'vector%d'%i)
import re as _r
for l in open('arc.dis'):
    m=_r.match(r'([0-9a-f]{6}) (jsr|bsr\S*)\s+\$([0-9a-f]+)',l)
    if m:
        t=int(m.group(3),16)
        if t<0x40000 and t%2==0 and t>=0x400 and t not in ents: ents[t]='semilla_lineal@'+m.group(1); todo.append(t)
LIN=[(int(l[:6],16),l[7:].strip()) for l in open('arc.dis') if _r.match(r'[0-9a-f]{6} ',l)]
for k,(p,txt) in enumerate(LIN):
    m=_r.match(r'lea\.l \$([0-9a-f]+)\.l, (a\d)',txt)
    if not m:continue
    base=int(m.group(1),16);reg=m.group(2)
    if base>=0x40000:continue
    w=[t for _,t in LIN[k+1:k+9]]
    ptr=None
    for j,t in enumerate(w):
        m2=_r.match(r'movea\.l \('+reg+r', d\d\.w\), (a\d)',t)
        if m2:
            r2=m2.group(1)
            if any(x in('jsr ('+r2+')','jmp ('+r2+')') for x in w[j+1:j+5]): ptr=1
            break
        if t.startswith(('rts','bra')):break
    if ptr:
        t=base
        for c in range(96):
            v=struct.unpack('>I',rom[t:t+4])[0]
            if v<0x400 or v>=0x40000 or v%2:break
            if v not in ents: ents[v]='tabla_ptr_lineal@%06x'%p; todo.append(v)
            t+=4
def tgt(op):
    m=re.fullmatch(r'\$([0-9a-f]+)(\.[wl])?',op.strip());return int(m.group(1),16) if m else None
def dis1(pc):
    try:return next(md.disasm(rom[pc:pc+10],pc))
    except StopIteration:return None
def flood():
    while todo:
        pc=todo.pop()
        while pc<0x40000 and pc not in ins:
            i=dis1(pc)
            if not i:break
            ins[pc]=(i.size,i.mnemonic,i.op_str)
            mn=i.mnemonic
            if (mn[0] in 'bj' or mn.startswith('db')) and not mn.startswith(('bset','bclr','btst','bchg')):
                t=tgt(i.op_str.split(',')[-1])
                if t is not None:
                    if mn.startswith(('jsr','bsr')): add(t,'call')
                    else: todo.append(t) if t<0x40000 else None
            if mn in('rts','rte','rtr') or mn.startswith(('bra','jmp')):break
            pc+=i.size
def prev(q):
    for d in (2,4,6,8,10):
        if q-d in ins and q-d+ins[q-d][0]==q:return q-d
seenT=set()
while True:
    flood();n=len(ents)
    for p in list(ins):
        sz,mn,op=ins[p]
        if mn=='lea.l' and p not in seenT:
            base=tgt(op.split(',')[0]); reg=op.split(',')[-1].strip()
            if base is None or base>=0x40000:continue
            # mirar 8 instrucciones siguientes
            q=p;kind=None
            for k in range(8):
                q=q+ins[q][0]
                if q not in ins:break
                m2,o2=ins[q][1],ins[q][2]
                if m2 in('jsr','jmp') and o2.startswith('('+reg+','):kind='bra';break
                if m2=='movea.l' and o2.startswith('('+reg+','):kind='ptr';break
                if m2 in('rts','bra.w','bra.b','bra.s'):break
            if not kind:continue
            seenT.add(p)
            t=base;cnt=0
            if kind=='bra':
                while cnt<128:
                    i=dis1(t)
                    if not i or not i.mnemonic.startswith(('bra','jmp')):break
                    add(tgt(i.op_str),'tabla_bra@%06x'%p);t+=i.size;cnt+=1
            else:
                # punteros: solo si el puntero cargado se llama luego (jsr (aX))
                r2=ins[q][2].split(',')[-1].strip();called=False;qq=q
                for k in range(6):
                    qq=qq+ins[qq][0]
                    if qq not in ins:break
                    if ins[qq][1] in('jsr','jmp') and ins[qq][2]=='('+r2+')':called=True;break
                if called:
                    while cnt<128:
                        v=struct.unpack('>I',rom[t:t+4])[0]
                        if v<0x400 or v>=0x40000 or v%2:break
                        add(v,'tabla_ptr@%06x'%p);t+=4;cnt+=1
    flood()
    if len(ents)==n and not todo:break
json.dump({'ins':ins,'ents':ents},open('tools/rdis.json','w'))
print('instrucciones',len(ins),'bytes codigo',sum(v[0] for v in ins.values()),'entradas',len(ents))
with open('arc_rec.dis','w') as f:
    for k in sorted(ins):
        if k in ents: f.write('\n; ---- rutina %06x (%s)\n'%(k,ents[k]))
        f.write('%06x %s %s\n'%(k,ins[k][1],ins[k][2]))
