
/* b24: referee count-out (arcade 0xd7d8 state 3 when either wrestler has $19==1 or action 4; 0xdee4/e016). MAME C2085: first count
   46 f after P1 $19=1, then every 64 f, BCD 1..20. Voices 0xe0a8: 17..20 -> 0x40..0x43 (1..3 skipped in state 3). At 20 every
   wrestler outside loses (both outside = double count-out): cntLose bit0 P1, bit1 Warrior. */
static u16 cntLose;
static void cntStep(void)
{   const u16 out = sx || wO;
    if (cntV >= 20) { cntEnd++; if (cntEnd == 130) { dma((void*) (cnt_glyph + 20 * 512), CNT_T * 32, 512, 2); cntShow = 2; } return; }
    if (!out || pinS) { cntS = 0; cntV = 0; cntShow = 0; return; }
    if (!cntS) { cntS = 1; cntT = 0; cntV = 0; }
    if (++cntT >= (cntV ? 64 : 46))
    {   cntT = 0; cntV++; dma((void*) (cnt_glyph + (u32) (cntV - 1) * 512), CNT_T * 32, 256, 2); cntShow = 1;
        if (cntV >= 17) snd(0x40 + cntV - 17);
        if (cntV == 20) cntLose = (sx ? 1 : 0) | (wO ? 2 : 0); }
}
static s16 wLog(void) { return (wO == 2) ? oy[2] + 59 : oy[2]; }   /* outside: oy holds y + (z 128 - 187), baked like the track */
static void wWalk(s16 tx, s16 ty, u16 *np2)
{   const s16 hx = (tx > ox[2]) ? 1 : (tx < ox[2]) ? -1 : 0, hy = (ty > wLog()) ? 1 : (ty < wLog()) ? -1 : 0;
    static u16 tk, ph;
    if (++tk & 1) { const s16 sp = (hx && hy) ? 2 : 3; s16 X = ox[2] + hx * sp, Y = oy[2] + hy * sp; const s16 tY = ty - ((wO == 2) ? 59 : 0);
        if ((hx > 0 && X > tx) || (hx < 0 && X < tx)) X = tx;
        if ((hy > 0 && Y > tY) || (hy < 0 && Y < tY)) Y = tY;
        if (wO == 2) { if (X < SX_OUTL) X = SX_OUTL; if (X > SX_OUTR) X = SX_OUTR; if (Y + 59 > SX_YOUT) Y = SX_YOUT - 59; }
        else { if (Y < RING_Y0) Y = RING_Y0; if (Y > RING_Y1) Y = RING_Y1; const s16 e = ((u16) (Y - RING_Y0)) / 6; if (X < RING_XL + e) X = RING_XL + e; if (X > RING_XR - e) X = RING_XR - e; }
        ox[2] = X; oy[2] = Y; }
    if (hx || hy) { *np2 = ((const u8*) move_seq)[mvOff[10] + (ph & 31)]; ph++; } else *np2 = 6;
}
static u16 aiOut(u16 *np2)
{   if (humW || hum2 || cpuOff) return 0;
    if (cntV >= 20) { *np2 = 6; return 1; }
    if (!sx && !wO) { wDec = 0; return 0; }
    if (wO == 1 || wO == 3)
    {   const u16 o = (wO == 1) ? WOX_O : WOE_O, n = (wO == 1) ? WOX_N : WOE_N, j = (wOk >= n) ? n - 1 : wOk;
        const s16 *q = spT(o + j), *q0 = spT(o + ((j > 2) ? j - 2 : 0));
        ox[2] = wOX0 + wOM * q[1]; oy[2] = wOY0 + q[2]; *np2 = q0[0]; p2face = (wO == 1) ? (wOM < 0) : (wOM > 0);
        if (++wOk >= n) { if (wO == 1) wO = 2; else { wO = 0; wDec = 3; } }
        return 1; }
    if (mv == 3 || rv || wpS || wcS || wxS || mv2) return 0;
    const u16 left = ox[2] < (RING_XL + RING_XR) / 2;
    if (wO == 2)
    {   if (cntV >= 10 || !sx)   /* 0x1AED4 threshold 0x0F BCD (count 10); MAME C2078: back in at 0x11 once idle */
        {   s16 ty = wLog(); if (ty < SX_YIN0) ty = SX_YIN0; if (ty > SX_YIN1) ty = SX_YIN1;
            const s16 e = ((u16) (ty - RING_Y0)) / 6, tx = left ? RING_XL + e - 73 : RING_XR - e + 73;
            wWalk(tx, ty, np2);
            if (ox[2] == tx && wLog() == ty) { wO = 3; wOk = 0; wOX0 = ox[2]; wOY0 = ty; wOM = left ? 1 : -1; }   /* recorded on the left going right */
            return 1; }
        /* brawl outside: approach P1 and use the normal strike (outside move choice SIN CONFIRMAR) */
        const s16 tx = ox[0] + ((ox[0] > ox[2]) ? -40 : 40);
        if (abs(ox[2] - tx) <= 4 && abs(wLog() - oy[0]) <= 4) { p2face = ox[0] > ox[2]; if (!cool2) { mv2 = 1; mk2 = 0; cool2 = 40; return 0; } cool2--; *np2 = 6; return 1; }
        wWalk(tx, oy[0], np2); p2face = ox[0] > ox[2]; return 1; }
    /* inside, P1 outside: 0x1907C each frame until decided; re-roll while P1 is knocked down / flying */
    if (!wDec) { if (cntV >= 10) wDec = 3; else if (!kd1) wDec = (((random() >> 1) & 15) >= 8) ? 3 : 4; }
    if (wDec == 4 && cntV >= 10) wDec = 3;
    if (wDec != 4) { wWalk(720, wLog(), np2); p2face = ox[0] > ox[2]; return 1; }
    {   const u16 pl = ox[0] < (RING_XL + RING_XR) / 2; s16 ty = oy[0]; if (ty < SX_YMIN) ty = SX_YMIN; if (ty > RING_Y1 - 1) ty = RING_Y1 - 1;
        const s16 e = ((u16) (ty - RING_Y0)) / 6, tx = pl ? RING_XL + e : RING_XR - e;
        wWalk(tx, ty, np2); p2face = !pl;
        if (ox[2] == tx && oy[2] == ty) { wO = 1; wOk = 0; wOX0 = ox[2]; wOY0 = oy[2]; wOM = pl ? 1 : -1; }   /* track recorded leaving left */
        return 1; }
}
