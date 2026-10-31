import pickle,numpy as np
states,blk,imgs,uses=pickle.load(open('world_states.pkl','rb'))
AX0,AY0,AW,AH=-2,-1,40,34
def base_entry(tx,ty):
    s=states.get((tx,ty))
    if s: return s[0]
    bx,by=tx//4,ty//4
    if (bx,by) in blk: return blk[(bx,by)][0][(ty-by*4)*4+(tx-bx*4)]
    return None
def world_rgb():
    img=np.zeros((AH*16,AW*16,3),np.int16)-1
    for ty in range(AY0,AY0+AH):
        for tx in range(AX0,AX0+AW):
            e=base_entry(tx,ty)
            if e is not None: img[(ty-AY0)*16:(ty-AY0)*16+16,(tx-AX0)*16:(tx-AX0)*16+16]=imgs[e]
    return img
