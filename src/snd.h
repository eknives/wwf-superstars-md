/* pre-completa: sound = old WWF v29 Z80 driver (/workspace/wwf/snd): arcade YM2151 song logs converted to YM2612 (6 FM, extra 2
   channels -> PSG) + OKI phrases as 4-bit DPCM mixed on the DAC (4 voices). Commands = arcade sound command ids (0x01..0x67,0xFE,0xFF),
   sent through the 16-byte mailbox at Z80 0x1FE0 (write idx 0x1FF0). Song/PCM data blob appended at ROM 0x398000 (tools/addsnd.py). */
#define ZRAM ((volatile u8*) 0xA00000)
static void sndInit(void) { Z80_loadCustomDriver((const u8*) z80drv, 0x1800); }
static u16 sndMute;   /* MUSIC HOOK: set to 1 to silence everything (sndQ drops commands) */
static void snd(u8 c)
{   if (sndMute) return;
    const bool t = Z80_getAndRequestBus(TRUE);
    u8 w = ZRAM[0x1FF0] & 15; ZRAM[0x1FE0 + w] = c; ZRAM[0x1FF0] = (w + 1) & 15;
    if (!t) Z80_releaseBus(); }
/* MUSIC HOOK: all music goes through sndMusic (arcade song ids 0x01..0x17), effects through snd */
static u8 sndCur;
static void sndMusic(u8 s) { if (s != sndCur) { sndCur = s; snd(s); } }
