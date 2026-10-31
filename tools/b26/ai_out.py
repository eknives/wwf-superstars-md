# s64: paso 5 — Warrior 0x22 / 0x33 / 0x31 + Duggan victim.
# 1) Dedupa tiles exactos del base s63 (libera ~221 KB).
# 2) Extrae tracks MAME p56/p57 (L2_N2, R2w, c4).
import sys, struct, hashlib, shutil, os
src = open('/workspace/wwf_sgdk/s34/_base_s33/build_s24_spr.py').read().split('\n')
ns = {}; exec('\n'.join(src[:30] + src[176:203]), ns)
sys.path.insert(0, '/workspace/wwf_sgdk/tools'); import mv5

B = '/workspace/wwf_sgdk/s64/base_res/'
R = '/workspace/b24/res/'

tab = bytearray(open(R + 'spr_tab.bin', 'rb').read()); tiles = bytearray(open(R + 'spr_tiles.bin', 'rb').read()); NP0 = len(tab)//126
# rebuild exist map
exist = {}
for i in range(NP0):
    nPcs, t0, nT = struct.unpack_from('>HHH', tab, i * 126)
    if nT == 0: continue
    h = hashlib.md5(bytes(tiles[t0 * 32:(t0 + nT) * 32])).hexdigest()
    exist[(nPcs, nT, h)] = i

out = bytearray(open(R + 'sp_trk.bin', 'rb').read())
ids = {}; newN = 0; reuseN = 0; maxt = [0, 0]

def pid(g, sig, bank):
    global tab, tiles, newN, reuseN
    if (bank, sig) in ids: return ids[(bank, sig)]
    img, x0, y0 = ns['bitmap'](g); idx, _ = ns['remap'](img, bank); H, W = idx.shape; pcs = []
    for by in range(0, H, 32):
        for bx in range(0, W, 32):
            raw = img[by:by + 32, bx:bx + 32]
            if not raw.any(): continue
            blk = idx[by:by + 32, bx:bx + 32]
            rows = [r for r in range(0, blk.shape[0], 8) if raw[r:r + 8].any()]
            cols = [c for c in range(0, blk.shape[1], 8) if raw[:, c:c + 8].any()]
            pc = blk[rows[0]:rows[-1] + 8, cols[0]:cols[-1] + 8]; hc, wc = pc.shape[0] // 8, pc.shape[1] // 8
            tl = b''.join(ns['enc'](pc[r * 8:r * 8 + 8, c * 8:c * 8 + 8]) for c in range(wc) for r in range(hc))
            pcs.append((x0 + bx + cols[0], y0 + by + rows[0], wc, hc, tl, 2))
    assert len(pcs) <= 12, len(pcs)
    nT = sum(p[2] * p[3] for p in pcs); payload = b''.join(p[4] for p in pcs)
    h = hashlib.md5(payload).hexdigest(); key = (len(pcs), nT, h)
    if key in exist:
        reuseN += 1; ids[(bank, sig)] = exist[key]; return exist[key]
    newN += 1; maxt[1 if bank else 0] = max(maxt[1 if bank else 0], nT)
    t0 = len(tiles) // 32; tab += struct.pack('>HHH', len(pcs), t0, nT); off = 0
    for dx, dy, wc, hc, tl, line in pcs:
        tab += struct.pack('>hhHHH', dx, dy, ((wc - 1) << 2) | (hc - 1), line, off); off += wc * hc; tiles.extend(tl)
    tab += b'\0' * 10 * (12 - len(pcs))
    ids[(bank, sig)] = len(tab) // 126 - 1; exist[key] = ids[(bank, sig)]; return ids[(bank, sig)]

def emit_pair(tr, t0, e_atk, e_vic, atk_who, hit_t, bake_z=True):
    """Warrior atk (bank 2) + Duggan vic (bank 0). Returns o1(vic),n1,o2(atk),n2,k_dmg_from_vic0,hdx."""
    # o1 = victim (P1/Duggan), o2 = attacker (P2/Warrior) — W1E / S0C style, vic=1
    r0 = tr[t0]
    # victim track
    o1 = len(out) // 8; last = None
    x0v = r0['x'] if atk_who == 2 else r0['x2']
    y0v = r0['y'] if atk_who == 2 else r0['y2']
    for t in range(t0, e_vic + 1):
        who = 0 if atk_who == 2 else 2
        g, sig = mv5.grp(tr, t, who)
        p_ = pid(g, sig, who) if g else last; last = p_
        r = tr[t]; oo = r['o'] if who == 0 else r['o2']
        x = r['x'] if who == 0 else r['x2']; y = r['y'] if who == 0 else r['y2']
        z = mv5.z(oo); zh = (z - 187) if bake_z else 0
        dx = x - x0v; dy = (y - y0v) - zh
        out.extend(struct.pack('>4h', p_, dx, dy, oo[0x2d]))
    n1 = e_vic - t0 + 1
    # attacker track
    o2 = len(out) // 8; last = None
    x0a = r0['x2'] if atk_who == 2 else r0['x']
    y0a = r0['y2'] if atk_who == 2 else r0['y']
    for t in range(t0, e_atk + 1):
        who = atk_who
        g, sig = mv5.grp(tr, t, who)
        p_ = pid(g, sig, who) if g else last; last = p_
        r = tr[t]; oo = r['o2'] if who == 2 else r['o']
        x = r['x2'] if who == 2 else r['x']; y = r['y2'] if who == 2 else r['y']
        z = mv5.z(oo); zh = (z - 187) if bake_z else 0
        dx = x - x0a; dy = (y - y0a) - zh
        out.extend(struct.pack('>4h', p_, dx, dy, oo[0x2d]))
    n2 = e_atk - t0 + 1
    kd = hit_t - t0
    # hdx at hit: for vic=1 damage path uses sk1; geometry unused when k2==0
    rh = tr[hit_t]
    if atk_who == 2:
        hdx = rh['x'] - rh['x2']  # vic - atk
    else:
        hdx = rh['x2'] - rh['x']
    return o1, n1, o2, n2, kd, hdx


# s67: Warrior CPU rope exit / re-entry (MAME wwfsstar 0.139, /tmp/s23/ai g2.lua NM=C2078b MF=2078, P1 walk-out (630,330)+Left; Warrior pinned (770,240) pt<60 only)
T = mv5.load('/tmp/s23/ai/traj_C2078b.txt','/tmp/s23/ai/traj_C2078bb.txt')['C2078b']
def trk2(t0,e):
    o=len(out)//8; last=None; r0=T[t0]
    for k in range(t0+1,e+1):
        g,sig=mv5.grp(T,k,2); p_=pid(g,sig,2) if g else last; last=p_
        r=T[k]; oo=r['o2']; zh=mv5.z(oo)-187
        out.extend(struct.pack('>4h',p_ if p_ is not None else 0,r['x2']-r0['x2'],r['y2']-r0['y2']+zh,oo[0x2d]))
    return o
for k in (185,186,248,250,877,878,931,932,934): r=T[k]; print(k,r['x2'],r['y2'],mv5.z(r['o2']),'%02x'%r['o2'][0x2d],r['o2'][0x19])
h=''
for nm,t0,e in (('WOX',185,248),('WOE',877,932)):
    a=trk2(t0,e); r=T[t0]; h+=f'#define {nm}_O {a}\n#define {nm}_N {e-t0}\n#define {nm}_X0 {r["x2"]}\n#define {nm}_Y0 {r["y2"]}\n'
    r1=T[e]; h+=f'#define {nm}_X1 {r1["x2"]}\n#define {nm}_Y1 {r1["y2"]}\n'
h+=f'#define NPOSE_AIO {len(tab)//126}\n'
open(R+'spr_tab.bin','wb').write(tab); open(R+'spr_tiles.bin','wb').write(tiles); open(R+'sp_trk.bin','wb').write(out)
open(R+'gm67.h','w').write(h); print(h,'new',newN,'reuse',reuseN)
