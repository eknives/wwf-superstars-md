-- b95: frames perdidos hacia los 4 postes (diagonal, como inv95/diag.lua) + integridad del fondo (BG_B vs W/ROM)
local A={};for l in io.lines(os.getenv('SYM'))do local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$');if a then local b=n:match('^([%w_]+)');if b then A[b]=tonumber(a,16)end end end
local RA={};for l in io.lines(os.getenv('SYM'))do local a,n=l:match('^(%x+) [TtRr] ([%w_]+)$');if a then RA[n]=tonumber(a,16)end end
local m=manager.machine.devices[':maincpu'].spaces['program']
local function vset(a) m:write_u16(0xC00004,0x8F02);m:write_u16(0xC00004,a&0x3FFF);m:write_u16(0xC00004,(a>>14)&3) end
local function vrd() return m:read_u16(0xC00000) end
local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local scr=manager.machine.screens[':megadriv']
local function g(n,i)return m:read_u16(assert(A[n],n)+2*(i or 0))end
local function w(n,v,i)m:write_u16(assert(A[n],n)+2*(i or 0),v&65535)end
local function q(f,o,v)m:write_u16(A.fd+100*f+o,v&65535)end
local function fq(f,o)return m:read_u16(A.fd+100*f+o)end
local function s(v)return v>=32768 and v-65536 or v end
local TAG=os.getenv('TAG') or 'b95';local OUTD=os.getenv('OUTD') or '/workspace/b95/shots95/md/'
local MW,VW,VH,NB49,NCA=88,33,29,3540,608
local cases={{'diag_a_poste_sup_izq',768,300,820,300,{'P1 Left','P1 Up'}},{'diag_a_poste_sup_der',768,300,700,300,{'P1 Right','P1 Up'}},{'diag_a_poste_inf_izq',768,300,820,300,{'P1 Left','P1 Down'}},{'diag_a_poste_inf_der',768,300,700,300,{'P1 Right','P1 Down'}},{'carrera_der_centro',650,300,768,240,{'P1 Right'},true}}
local f=0;local ci=1;local k=0;local held={};local seen={};local loops=0
local log=assert(io.open(OUTD..TAG..'_post.csv','w'));log:write('case,k,frame,loops,busymax,ox,oy,camx,camy,cx,cy,tx,ty,bad,chk,zero,visok\n')
local tS=0;local waitStart=nil;local busyMax=0;local bad=0;local chk=0;local zero=0;local visok=1;local nl=0;local active=false;local badlog=0
local function now()return manager.machine.time:as_double()end
local function src(id) if id<=NB49 then return RA.t_bin+(id-1)*32 elseif id<=NB49+NCA then return RA.ca_tiles+(id-NB49-1)*32 else return RA.ex_tiles+(id-NB49-NCA-1)*32 end end
local function cell(r,c)
 local e=m:read_u16(A.W+2*(r*MW+c));local id=e&0x1FFF;local bgb=g('bgb_addr')
 vset(bgb+2*((r&31)*64+(c&63)));local pe=vrd();chk=chk+1
 if id==0 then if pe~=0 then bad=bad+1 end return end
 if pe==0 then zero=zero+1 return end
 local at=((e&0x8000)>>2)|((e&0x6000)>>2)
 if (pe&0xF800)~=at then bad=bad+1;return end
 local sl=pe&0x7FF;local sa=src(id)
 vset(sl*32) for i=0,30,2 do if vrd()~=m:read_u16(sa+i) then bad=bad+1;if badlog<20 then badlog=badlog+1;print(string.format('BAD %s k%d r%d c%d id%d slot%d',cases[ci][1],k,r,c,id,sl)) end return end end
end
local function check()
 local tx,ty=s(g('tx')),s(g('ty'));nl=nl+1
 local full=(nl%16==0)
 for r=ty,ty+VH-1 do if full then for c=tx,tx+VW-1 do cell(r,c) end else cell(r,tx);cell(r,tx+VW-1) end end
 if not full then for c=tx+1,tx+VW-2 do cell(ty,c);cell(ty+VH-1,c) end end
 local cx,cy=s(g('cx')),s(g('cy'))
 if (cx>>3)<tx or ((cx+255)>>3)>tx+VW-1 or (cy>>3)<ty or ((cy+223)>>3)>ty+VH-1 then visok=0 end
end
tap=m:install_write_tap(A.arcLast,A.arcLast+3,'lp',function(o,d,mk) if o==A.arcLast then loops=loops+1;tS=now();waitStart=nil;if active then check() end end end)
tap2=m:install_read_tap(0xc00004,0xc00007,'vs',function(o,d,mk) if not waitStart then waitStart=now();local b=(waitStart-tS)*scr.frame_number/ math.max(manager.machine.time:as_double(),1e-6);end return d end)
emu.register_frame_done(function()
 f=f+1;for _,v in pairs(K)do v:set_value(0)end
 if f>=60 and f<=63 then held['P1 Start']=63 end
 if g('selPhase89')==2 then local sf=g('selFrame89');for _,t in ipairs({{20,'P1 A'},{40,'P1 Left'},{60,'P1 A'}})do if sf>=t[1] and not seen[t[1]] then seen[t[1]]=true;held[t[2]]=f+2 end end end
 if g('selPhase89')==4 then
  k=k+1;local c=cases[ci]
  if k<=40 then
   active=false
   w('ctl',1);w('follow',1);w('gr',0);w('pnS',0);w('tr',0,0);w('tr',0,1);w('fs',0,0);w('fs',0,1)
   for who=0,1 do for off=0,98,2 do q(who,off,0)end
    q(who,0,who==1 and c[2] or c[4]);q(who,2,who==1 and c[3] or c[5]);q(who,8,187);q(who,16,0xffff)
    w('energy90',48,who);w('vh',0,who);w('vk',0,who);w('koF',0,who);w('vface',0,who)
   end
   w('pnN',0,0);w('pnN',0,1)
  end
  if k>40 then active=true end
  if k>=50 and k<=630 then for _,b in ipairs(c[6]) do K[b]:set_value(1) end; if c[7] and (k==52 or k==53) then K['P1 A']:set_value(1);K['P1 B']:set_value(1) end end
  if k>40 then
   log:write(table.concat({c[1],k,f,loops,0,s(fq(1,0)),s(fq(1,2)),s(g('camx')),s(g('camy')),s(g('cx')),s(g('cy')),s(g('tx')),s(g('ty')),bad,chk,zero,visok},',')..'\n')
   if k==300 or k==600 then scr:snapshot(OUTD..TAG..'_'..c[1]..'_k'..k..'.png') end
  end
  if k>=640 then ci=ci+1;k=0;bad=0;chk=0;zero=0;visok=1;if ci>#cases then log:close();manager.machine:exit();return end end
 end
 for n,u in pairs(held)do if f<=u then K[n]:set_value(1)else held[n]=nil end end
end)
