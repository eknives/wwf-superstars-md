#!/bin/bash
# uso: mame95.sh rom.bin script.lua [sistema]   (sistema: genesis = NTSC, megadriv = PAL)
# Variables: MAME (ejecutable MAME 0.276), ROMPATH (BIOS/ROMs propias), SHOTS (carpeta de capturas)
MAME=${MAME:-mame}; ROMPATH=${ROMPATH:-$HOME/mame/roms}; SHOTS=${SHOTS:-./shots}
export SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
mkdir -p /tmp/nv95 /tmp/cfg95 "$SHOTS"
"$MAME" ${3:-genesis} -cart "$1" -rompath "$ROMPATH" -video none -sound none -nothrottle -skip_gameinfo -window -autoboot_script "$2" -nvram_directory /tmp/nv95 -cfg_directory /tmp/cfg95 -snapshot_directory "$SHOTS"
