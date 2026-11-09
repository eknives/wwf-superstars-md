-- b95: velocidad de carrera (px/s) y ritmo de poses, Warrior y Duggan, NTSC/PAL (sistema por argumento de MAME)
local A={};for l in io.lines(os.getenv('SYM'))do local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$');if a then local b=n:match('^([%w_]+)');if b then A[b]=tonumber(a,16)end end end
local m=manager.machine.devices[':maincpu'].spaces['program'];local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local scr=manager.machine.screens[':megadriv']
local function g(n,i)return m:read_u16(assert(A[n],n)+2*(i or 0))end
local function w(n,v,i)m:write_u16(assert(A[n],n)+2*(i or 0),v&65535)end
local function q(f,o,v)m:write_u16(A.fd+100*f+o,v&65535)end
local function fq(f,o)return m:read_u16(A.fd+100*f+o)end
local function s(v)return v>=32768 and v-65536 or v end
local TAG=os.getenv('TAG') or 'b95'
-- {nombre, luchador controlado, x0, dir}
local cases={{'W_sale_izq',1,660,-1},{'W_sale_der',1,880,1},{'D_sale_izq',0,660,-1},{'D_sale_der',0,880,1}}
local f=0;local ci=1;local k=0;local held={};local seen={};local loops=0
local log=assert(io.open('/workspace/b95/shots95/md/'..TAG..'_salir.csv','w'));log:write('case,k,t,loops,ox,oxf,oy,rn,rnk,pose,sx\n')
tap=m:install_write_tap(A.arcLast,A.arcLast+3,'lp',function(o,d,mk) if o==A.arcLast then loops=loops+1 end end)
emu.register_frame_done(function()
 f=f+1;for _,v in pairs(K)do v:set_value(0)end
 if f>=60 and f<=63 then held['P1 Start']=63 end
 if g('selPhase89')==2 then local sf=g('selFrame89');for _,t in ipairs({{20,'P1 A'},{40,'P1 Left'},{60,'P1 A'}})do if sf>=t[1] and not seen[t[1]] then seen[t[1]]=true;held[t[2]]=f+2 end end end
 if g('selPhase89')==4 then
  k=k+1;local c=cases[ci];local me=c[2];local ot=1-me
  if k<=40 then
   w('ctl',me);w('follow',0);w('gr',0);w('pnS',0);w('tr',0,0);w('tr',0,1);w('fs',0,0);w('fs',0,1)
   for who=0,1 do for off=0,98,2 do q(who,off,0)end
    q(who,0,who==me and c[3] or 768);q(who,2,who==me and 300 or 240);q(who,8,187);q(who,16,0xffff)
    w('energy90',48,who);w('vh',0,who);w('vk',0,who);w('koF',0,who);w('vface',0,who)
   end
   w('pnN',0,0);w('pnN',0,1)
  end
  if k>=50 and k<=200 then K[c[4]>0 and 'P1 Right' or 'P1 Left']:set_value(1) end
  if k>40 then
   log:write(table.concat({c[1],k,string.format('%.6f',manager.machine.time:as_double()),loops,s(fq(me,0)),0,s(fq(me,2)),fq(me,52),fq(me,54),g('dPose',me),g('dSx',me)},',')..'\n')
   if k==150 then scr:snapshot('/workspace/b95/shots95/md/'..TAG..'_salir_'..c[1]..'.png') end
  end
  if k>=240 then ci=ci+1;k=0;if ci>#cases then log:close();manager.machine:exit();return end end
 end
 for n,u in pairs(held)do if f<=u then K[n]:set_value(1)else held[n]=nil end end
end)
