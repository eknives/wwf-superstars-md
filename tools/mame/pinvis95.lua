-- b93 MD: Warrior (slot1, ctl1) cubre a Duggan (slot0) tumbado. vface 1 = arcade ori0, vface 0 = ori1.
local A={};for l in io.lines((os.getenv('SYM') or '/workspace/b94/out/symbol.txt')..'')do local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$');if a then local b=n:match('^(%w+)');if b then A[b]=tonumber(a,16)end end end
local m=manager.machine.devices[':maincpu'].spaces['program'];local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local function g(n,i)return m:read_u16(assert(A[n],n)+2*(i or 0))end
local function w(n,v,i)m:write_u16(assert(A[n],n)+2*(i or 0),v&65535)end
local function q(f,o,v)m:write_u16(A.fd+100*f+o,v&65535)end
local function fq(f,o)return m:read_u16(A.fd+100*f+o)end
local function s(v)return v>=32768 and v-65536 or v end
local cases={{'W_o0_x760',760,0,1},{'W_o1_x760',760,1,1},{'D_o0_x760',760,0,0},{'D_o1_x760',760,1,0},{'W_o0_x680',680,0,1},{'W_o1_x860',860,1,1}}
local f=0;local ci=1;local k=0;local held={};local seen={};local S
local log=assert(io.open('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b94')..'_pin_frames.csv','w'));log:write('case,k,pnS,pnK,ax,ay,az,aflip,apose,vx,vflip,vlyo,vdx,adx,ady,adz,pnX,pnM\n')
emu.register_frame_done(function()
 f=f+1;for _,v in pairs(K)do v:set_value(0)end
 if f>=60 and f<=63 then held['P1 Start']=63 end
 if g('selPhase89')==2 then local sf=g('selFrame89');for _,t in ipairs({{20,'P1 A'},{40,'P1 Left'},{60,'P1 A'}})do if sf>=t[1] and not seen[t[1]] then seen[t[1]]=true;held[t[2]]=f+2 end end end
 if g('selPhase89')==4 then
  k=k+1;local c=cases[ci];local X=c[2];local o=c[3];local at=c[4];local vi=1-at;local ax=o==0 and X-16 or X+16
  if k<=80 then
   w('ctl',at);w('follow',0);w('gr',0);w('pnS',0);w('tr',0,0);w('tr',0,1);w('fs',0,0);w('fs',0,1)
   for who=0,1 do for off=0,98,2 do q(who,off,0)end
    q(who,0,who==vi and X or ax);q(who,2,300);q(who,8,187);q(who,16,0xffff)
    w('energy90',48,who);w('kvPhase90',0,who);w('groundSeen90',1,who);w('ground90',22,who)
    w('vh',who==vi and 3 or 0,who);w('vk',30,who);w('vface',who==vi and (o==0 and 1 or 0) or 0,who);w('koF',who==vi and 1 or 0,who);w('vlast',180,who);w('vjolt',0,who)
   end
   w('pnN',0,0);w('pnN',0,1);S=nil
  end
  if k>=81 and k<=84 then held['P1 B']=f end
  if k>80 then
   log:write(table.concat({c[1],k,g('pnS'),g('pnK'),s(fq(at,0)),s(fq(at,2)),s(fq(at,8)),g('dFlip',at),g('dPose',at),s(fq(vi,0)),g('dFlip',vi),s(g('dLyo',vi)),s(g('dX',vi)),s(g('dX',at)),s(g('dY',at)),s(g('dZ',at)),s(g('pnX')),s(g('pnM'))},',')..'\n')
   if g('pnS')==1 and not S then S=k end
   if S and k==S+3 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b94')..'_'..c[1]..'_04_p513.png')end
   if S and k==S+8 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b94')..'_'..c[1]..'_02_aprox.png')end
   if S and k==S+60 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b94')..'_'..c[1]..'_01_cubriendo.png')end
   if k==81 then print('CAM',c[1],s(g('camx')),s(g('camy'))) end
   if k==81 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b94')..'_'..c[1]..'_00_posicion.png')end
  end
  if k==150 then log:flush() end
  if k>=170 then ci=ci+1;k=0;if ci>#cases then log:close();manager.machine:exit();return end end
 end
 for n,u in pairs(held)do if f<=u then K[n]:set_value(1)else held[n]=nil end end
end)
