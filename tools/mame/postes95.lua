-- Investigacion b95: ritmo del bucle principal b94 (iteraciones/refresco) y carrera.
local A={};for l in io.lines(os.getenv('SYM') or '/workspace/b94/out/symbol.txt')do local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$');if a then local b=n:match('^(%w+)');if b then A[b]=tonumber(a,16)end end end
local m=manager.machine.devices[':maincpu'].spaces['program'];local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local scr=manager.machine.screens[':megadriv']
local function g(n,i)return m:read_u16(assert(A[n],n)+2*(i or 0))end
local function w(n,v,i)m:write_u16(assert(A[n],n)+2*(i or 0),v&65535)end
local function q(f,o,v)m:write_u16(A.fd+100*f+o,v&65535)end
local function fq(f,o)return m:read_u16(A.fd+100*f+o)end
local function s(v)return v>=32768 and v-65536 or v end
local TAG=os.getenv('TAG') or 'b94'
local cases={{'quieto_centro',768,300,820,300,{}},{'quieto_poste_sup_izq',652,366,720,330,{}},{'quieto_poste_sup_der',881,366,820,330,{}},{'quieto_cuerda_sup_centro',768,366,820,330,{}},{'quieto_poste_inf_izq',628,236,700,260,{}},{'quieto_poste_inf_der',905,236,840,260,{}},{'andar_sup_hacia_izq',830,366,900,300,{'P1 Left'}},{'andar_sup_hacia_der',706,366,640,300,{'P1 Right'}},{'andar_inf_hacia_izq',830,236,900,300,{'P1 Left'}},{'andar_inf_hacia_der',706,236,640,300,{'P1 Right'}},{'andar_centro_der',680,300,900,400,{'P1 Right'}}}
local f=0;local ci=1;local k=0;local held={};local seen={};local loops=0;local startv={}
local log=assert(io.open('/workspace/b95/shots95/md/'..TAG..'_postes.csv','w'));log:write('case,k,frame,loops,busymax,polls,vd,vc,wch,caZone,ox,oy,rn,rnk,pose,nsat,camx,camy\n')
local vd=0;local vc=0;local wch=0;local lastv=-1;local tS=0;local busy=0;local polls=0;local waitStart=nil;local busyMax=0
local function now()return manager.machine.time:as_double()end
tap=m:install_write_tap(A.arcLast,A.arcLast+3,'lp',function(o,d,mk) if o==A.arcLast then loops=loops+1;tS=now();waitStart=nil end end)
tap3=m:install_write_tap(0xc00000,0xc00003,'vd',function(o,d,mk) vd=vd+1 end)
tap4=m:install_write_tap(0xc00004,0xc00007,'vc',function(o,d,mk) vc=vc+1 end)
tap5=m:install_write_tap(A.W,A.W+88*68*2-1,'wm',function(o,d,mk) wch=wch+1 end)
tap2=m:install_read_tap(0xc00004,0xc00007,'vs',function(o,d,mk) polls=polls+1;if not waitStart then waitStart=now();local b=(waitStart-tS)*59.92;if b>busyMax then busyMax=b end end return d end)
emu.register_frame_done(function()
 f=f+1;for _,v in pairs(K)do v:set_value(0)end
 if f>=60 and f<=63 then held['P1 Start']=63 end
 if g('selPhase89')==2 then local sf=g('selFrame89');for _,t in ipairs({{20,'P1 A'},{40,'P1 Left'},{60,'P1 A'}})do if sf>=t[1] and not seen[t[1]] then seen[t[1]]=true;held[t[2]]=f+2 end end end
 if g('selPhase89')==4 then
  k=k+1;local c=cases[ci]
  if k<=40 then
   w('ctl',1);w('follow',0);w('gr',0);w('pnS',0);w('tr',0,0);w('tr',0,1);w('fs',0,0);w('fs',0,1)
   for who=0,1 do for off=0,98,2 do q(who,off,0)end
    q(who,0,who==1 and c[2] or c[4]);q(who,2,who==1 and c[3] or c[5]);q(who,8,187);q(who,16,0xffff)
    w('energy90',48,who);w('vh',0,who);w('vk',0,who);w('koF',0,who);w('vface',0,who)
   end
   w('pnN',0,0);w('pnN',0,1)
  end
  if k>=50 and k<=330 then for _,b in ipairs(c[6]) do K[b]:set_value(1) end end
  if k>40 then
   log:write(table.concat({c[1],k,f,loops,string.format('%.3f',busyMax),polls,vd,vc,wch,g('caZone'),s(fq(1,0)),s(fq(1,2)),fq(1,52),fq(1,54),g('dPose',1),g('nsat'),s(g('camx')),s(g('camy'))},',')..'\n')
   busyMax=0;polls=0;vd=0;vc=0;wch=0
   if k==200 then scr:snapshot('/workspace/b95/shots95/md/'..TAG..'_'..c[1]..'.png') end
  end
  if k>=340 then ci=ci+1;k=0;if ci>#cases then log:close();manager.machine:exit();return end end
 end
 for n,u in pairs(held)do if f<=u then K[n]:set_value(1)else held[n]=nil end end
end)
