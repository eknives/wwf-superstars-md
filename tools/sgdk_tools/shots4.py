import sys; sys.path.insert(0,'/workspace/chiki/tools'); from lr import *
c=Core('WWF_SGDK_s04.bin',{b'genesis_plus_gx_region_detect':b'ntsc-u'}); c.run(120); c.shot('s04_boot.png')
for n,p,tag in ((40,('RIGHT',),'r'),(9,('RIGHT',),'r2'),(60,('UP',),'u'),(60,('LEFT','DOWN'),'ld'),(60,('DOWN',),'d')):
    c.run(n,pad0=p); c.shot('s04_%s.png'%tag)
