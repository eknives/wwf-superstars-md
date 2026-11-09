-- b93 MD: Warrior (slot1, ctl1) cubre a Duggan (slot0) tumbado. vface 1 = arcade ori0, vface 0 = ori1.
local A={};for l in io.lines((os.getenv('SYM') or '/workspace/b94/out/symbol.txt')..'')do local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$');if a then local b=n:match('^(%w+)');if b then A[b]=tonumber(a,16)end end end
local m=manager.machine.devices[':maincpu'].spaces['program'];local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local function g(n,i)return m:read_u16(assert(A[n],n)+2*(i or 0))end
local function w(n,v,i)m:write_u16(assert(A[n],n)+2*(i or 0),v&65535)end
local function q(f,o,v)m:write_u16(A.fd+100*f+o,v&65535)end
local function fq(f,o)return m:read_u16(A.fd+100*f+o)end
local function s(v)return v>=32768 and v-65536 or v end
local cases={{'W_o0',760,0,1,0},{'W_o1',760,1,1,0},{'D_o0',760,0,0,0},{'D_o1',760,1,0,0},{'W_o0_cuenta3',760,0,1,1}}
local f=0;local ci=1;local k=0;local held={};local seen={};local S,K2,K3
local log=assert(io.open(''..(os.getenv('OUT') or '/workspace/b95/shots95/md/zafar.csv')..'','w'));log:write('case,k,pnS,pnK,ax,ay,az,aflip,apose,vx,vflip,vlyo,vdx,adx,ady,adz,pnX,pnM,vy,vz,vpose,winK,resetReq,fsA,pnN,alyo,fsv,az2,rf0,rf1\n')
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
   w('pnN',0,0);w('pnN',0,1);if c[5]==1 then w('pnN',1,vi) end;S=nil;K2=nil
  end
  if k>=81 and k<=84 then held['P1 B']=f end
  if k>80 then
   log:write(table.concat({c[1],k,g('pnS'),g('pnK'),s(fq(at,0)),s(fq(at,2)),s(fq(at,8)),g('dFlip',at),g('dPose',at),s(fq(vi,0)),g('dFlip',vi),s(g('dLyo',vi)),s(g('dX',vi)),s(g('dX',at)),s(g('dY',at)),s(g('dZ',at)),s(g('pnX')),s(g('pnM')),s(fq(vi,2)),s(fq(vi,8)),g('dPose',vi),g('winK'),g('resetReq'),g('fs',at),g('pnN',vi),s(g('dLyo',at)),g('fs',at),s(fq(at,8)),g('rFall',0),g('rFall',1)},',')..'\n')
   if g('pnS')==1 and not S then S=k end
   local T=(os.getenv('TAG') or 'b94')
   if g('pnS')==2 and g('pnK')==20 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b95')..'_zafar_'..c[1]..'_zafar.png')end
   if g('pnS')==0 and S and not K2 then K2=k end
   for _,dd in ipairs({10,20,40}) do if K2 and k==K2+dd then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b95')..'_zafar_'..c[1]..'_t'..(20+dd)..'.png') end end
   if K2 and k==K2+12 then manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b95')..'_zafar_'..c[1]..'_despues.png')end
   if g('pnS')==3 and not K3 then K3=k;manager.machine.screens[':megadriv']:snapshot('/workspace/b95/shots95/md/'..(os.getenv('TAG') or 'b95')..'_zafar_'..c[1]..'_cuenta3.png')end
  end
  if k==150 then log:flush() end
  if k>=(c[5]==1 and 520 or 420) then ci=ci+1;k=0;if ci>#cases then log:close();manager.machine:exit();return end end
 end
 for n,u in pairs(held)do if f<=u then K[n]:set_value(1)else held[n]=nil end end
end)
