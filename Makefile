# SGDK 2.11 + m68k-elf-gcc 13.1.0. Ver docs/COMPILAR.md.
# Uso: make GDK=/ruta/a/sgdk   (con m68k-elf-* y java 17 en el PATH)
GDK ?= $(error Define GDK=/ruta/a/SGDK-2.11)
include $(GDK)/makefile.gen
