exec(open('/workspace/wwf_sgdk/tools/edge4b.py').read().split("if __name__")[0])
sys.path.insert(0,'/workspace/wwf_sgdk/tools'); from sheet4 import sheet
T7=collections.defaultdict(list)
for l in open('/workspace/wwf_sgdk/rec5/traj7.txt'):
    n,pt,x,y,cx,cy,_=l.split(); T7[n].append((int(x),int(y),int(cx),int(cy)))
PARK7=[(768,300),(540,430),(560,420),(580,440),(600,420)]
cases=[('U','Cuerda superior\n(subiendo)',60,'p6','c_U',T,1),('D','Cuerda inferior\n(bajando)',52,'p6','c_D',T,0),('L','Cuerda lateral izq.',101,'p6','c_L',T,0),('R','Cuerda lateral dcha.',103,'p6','c_R',T,0),
       ('UL','Esquina sup.-izq.\n(último frame antes\nde trepar al poste)',106,'p6','c_UL',T,0),('UR','Esquina sup.-dcha.\n(último frame antes\nde trepar al poste)',108,'p6','c_UR',T,0),
       ('DL','Esquina inf.-izq.\n(último frame antes\nde la acción de esquina)',130,'p6','c_DL',T,0),('DR','Esquina inf.-dcha.\n(último frame antes\nde salir por la esquina)',None,'p7','h_DR2',T7,0)]
rows=[]; tab=[]
for d,lab,k,pd,name,TT,yp in cases:
    global PARK
    PARK=PARK7 if pd=='p7' else [(768,300),(600,120),(880,120),(1000,120),(760,110)]
    m=TT[name][120:]
    tr,_=probe(d,1,yp)
    if k is None: k=next(i for i in range(len(m)) if m[i][:2]!=tr[i][:2])-1
    tr,im=probe(d,1,yp,shots=(k,))
    a=np.array(Image.open('/workspace/wwf_sgdk/rec5/%s/%s_%03d.png'%(pd,name,120+k)).convert('RGB'))[8:232]
    b=im[k]
    dd=(np.abs(a.astype(int)-b.astype(int)).max(2)>40); dd[:48]=False; dd[200:]=False
    rows.append(('%s\nframe %d\nMAME P1 (%d,%d)\ns04b P1 (%d,%d)\ncam MAME %x/%x\ncam s04b %x/%x'%(lab,k,m[k][0],m[k][1],tr[k][0],tr[k][1],m[k][2],m[k][3],tr[k][2],tr[k][3]),a,b))
    tab.append((d,m[k][:2],tr[k][:2],m[k][2:],tr[k][2:]))
    print(d,k,'MAME',m[k],'s04b',tr[k])
sheet(rows[:4],'/workspace/wwf_sgdk/out/s04b_bordes_1.png',cols=('MAME (original)','s04b (Mega Drive)'))
sheet(rows[4:],'/workspace/wwf_sgdk/out/s04b_bordes_2.png',cols=('MAME (original)','s04b (Mega Drive)'))
