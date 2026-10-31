#!/bin/sh
# Semi-automatic build: verify your own wwfsstar ROM set, extract assets, build with SGDK.
# Usage: ./build.sh /path/to/wwfsstar.zip   (needs python3, unzip, SGDK in $GDK, m68k-elf toolchain)
set -e
ZIP="$1"; [ -f "$ZIP" ] || { echo "usage: $0 wwfsstar.zip"; exit 1; }
mkdir -p roms build
unzip -o -q "$ZIP" -d roms
# 1) verify: compare CRC32 against the MAME wwfsstar set (fill roms.crc from MAME: mame -listxml wwfsstar)
if [ -f roms.crc ]; then
  python3 - <<'P'
import zlib,sys,os
bad=0
for l in open('roms.crc'):
    n,c=l.split(); p=os.path.join('roms',n)
    if not os.path.exists(p): print('MISSING',n); bad=1; continue
    v='%08x'%(zlib.crc32(open(p,'rb').read())&0xffffffff)
    print(('OK ' if v==c.lower() else 'BAD'),n,v); bad|=v!=c.lower()
sys.exit(bad)
P
else echo "WARNING: roms.crc not found, skipping verification"; fi
# 2) extract graphics/sound/data tables from YOUR ROM into res/ and src/ (generated, git-ignored)
#    The individual extractor scripts live in tools/; see README "Status".
for t in tools/extract_*.py; do [ -f "$t" ] && python3 "$t" roms res src; done
[ -f src/main.c ] || { echo "src/main.c not generated yet - see README (WIP)"; exit 2; }
# 3) SGDK build
make GDK="${GDK:?set GDK to your SGDK path}" -f "$GDK/makefile.gen" release
echo "Done: out/rom.bin"
