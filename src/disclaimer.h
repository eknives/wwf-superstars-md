/* pre-completa: power-on disclaimer. REPLACES the arcade copyright screen (MAME: fg text shown frames 7..263 = 256 frames,
   pale cyan 0xCCFFEE on black, not skippable, arcade fg font codes = ASCII - 0x20, uppercase only, ',' = code 0x07).
   Text: edit DISC_TXT only (word-wrapped at runtime to the arcade's 26-column text width, '\n' = blank line). */
static const char DISC_TXT[] =
 "This is a free, non-commercial fan project, made with no profit motive. This is an AI-assisted port. It must not be sold or distributed for profit.\n"
 "All trademarks, characters, names, graphics, music and sound belong to their respective owners. This project is not affiliated with or endorsed by them.\n"
 "Dedicated with gratitude to everyone who appeared in, or took part directly or indirectly in, the making of this game, and in loving memory of those who are no longer with us.";
#define DISC_FRAMES 256   /* arcade copyright screen duration */
#define DISC_COL0 3       /* arcade text column */
#define DISC_W 26
#define DISC_T 16         /* VRAM tile base for the 64 font glyphs */
static void discLine(const char *s, u16 n, u16 y)
{ for (u16 i = 0; i < n; i++) { u8 ch = s[i]; if (ch >= 'a' && ch <= 'z') ch -= 32; u16 code = (ch == ',') ? 0x07 : (ch >= 0x20 && ch < 0x60) ? ch - 0x20 : 0;
    VDP_setTileMapXY(BG_A, TILE_ATTR_FULL(PAL0, 1, 0, 0, DISC_T + code), DISC_COL0 + (DISC_W - n) / 2 + i, y); } }
static void disclaimer(void)
{   VDP_setScreenWidth256(); PAL_setColor(0, 0); PAL_setColor(15, 0xEEC);
    VDP_clearPlane(BG_A, TRUE); VDP_clearPlane(BG_B, TRUE);
    VDP_loadTileData((const u32*) arc_font, DISC_T, 64, CPU);
    /* count lines first to centre vertically */
    u16 y, pass;
    for (pass = 0; pass < 2; pass++) {
      u16 nl = 0; const char *p = DISC_TXT; y = 0;
      if (pass) { y = 0; }
      static u16 y0; if (pass == 1) y = y0;
      while (*p) { if (*p == '\n') { p++; y++; nl++; continue; }
        while (*p == ' ') p++;
        u16 n = 0, br = 0; while (p[n] && p[n] != '\n' && n < DISC_W) { if (p[n] == ' ') br = n; n++; }
        if (p[n] && p[n] != '\n' && p[n] != ' ' && br) n = br;
        if (pass) discLine(p, n, y); p += n; y++; nl++; }
      if (!pass) y0 = (28 - nl) / 2; }
    for (u16 t = 0; t < DISC_FRAMES; t++) SYS_doVBlankProcess();
    VDP_clearPlane(BG_A, TRUE); }
