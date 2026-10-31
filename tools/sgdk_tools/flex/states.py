exec(open('/workspace/wwf_sgdk/tools/flex/base.py').read())
TS=load('/workspace/wwf_sgdk/rec5/traj42b.txt')[0]
CR=[(8,24),(8,25),(9,24),(9,25),(10,24),(10,25),(11,24),(11,25)]+[(r,c) for r in range(12,19) for c in (25,26)]+[(12,24)]+[(r,c) for r in range(19,22) for c in (26,27)]
CL=[(r,31-c) for r,c in CR]
OFF=[3,33,49,61,69,75,79,83]
def mask(cells):
    M=np.zeros((512,512),bool)
    for r,c in cells: M[r*16:r*16+16,c*16:c*16+16]=True
    return M
