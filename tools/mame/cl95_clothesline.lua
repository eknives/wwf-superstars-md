local A={}
for l in io.lines(os.getenv('SYM')) do
 local a,n=l:match('^e0(ff%x+) [bBdD] ([%w_.]+)$')
 if a and n then local base=n:match('^(%w+)');if base then A[base]=tonumber(a,16)end end
end
local mem=manager.machine.devices[':maincpu'].spaces['program']
local mode=os.getenv('MODE88')or'DR';local who=mode:sub(1,1)=='W'and 1 or 0;local dir=mode:sub(2,2)=='L'and-1 or 1
local out=''..(os.getenv('CLD'))..''..mode
local csv=io.open(out..'.csv','w');csv:write('frame,arc,clock,clstep,cltime,rn,rnk,hit,x,y,z,pose,art,vx,vy,vz,vpose,fs,held,mv,mk,alt,loop,vblank,aflip,vflip,aload,vload\n')
local OFF={rn=52,rnk=54,rnW=58,mv=74,mk=76,pAlt=82}
local function g(n,i)if OFF[n]then return mem:read_u16(A.fd+100*who+OFF[n])end return mem:read_u16(A[n]+2*(i or 0))end
local function w(n,v,i)mem:write_u16(A[n]+2*(i or 0),v)end
local function q(o,off,v)mem:write_u16(A.fd+o*100+off,v)end
local K={};for _,p in pairs(manager.machine.ioport.ports)do for n,v in pairs(p.fields)do K[n]=v end end
local f=0;local shot={};local tapped=false;local hold=os.getenv('HOLD87')=='1'
local function snap(tag)
 if not shot[tag]then shot[tag]=true;manager.machine.screens[':megadriv']:snapshot(''..(os.getenv('CLD'))..''..mode..'_'..tag..'.png');print('SHOT',tag,f)end
end

local function file(p)local f=assert(io.open(p,'rb'));local b=f:read('a');f:close();return b end
local ST=file('/workspace/b95/res/spr_tab.bin');local TT=file('/workspace/b95/res/spr_tiles.bin')
local function word(s,a)return s:byte(a+1)*256+s:byte(a+2)end
local VR=emu.item(manager.machine.devices[':gen_vdp'].items['0/m_vram'])
local CR=emu.item(manager.machine.devices[':gen_vdp'].items['0/m_cram'])
local SP=file('/workspace/b95/res/spr_pal.bin')
local checked={};local loaderrors=0
local function checktiles(i)
 local pose=g('dLoaded',i);if pose<821 or pose>842 or checked[pose]then return end
 local off=pose*126;local t0=word(ST,off+2);local nt=word(ST,off+4);local slot=i==0 and 1016 or 1672
 local errors=0
 for j=0,nt*32-2,2 do if VR:read(slot*16+j//2)~=word(TT,t0*32+j)then errors=errors+1 end end
 local pe=0;for n=0,15 do if CR:read(32+n)~=word(SP,n*2)then pe=pe+1 end end
 checked[pose]=true;loaderrors=loaderrors+errors+pe;print('TILECHECK',pose,nt,errors,'PALETTE_ERRORS',pe)
end

emu.register_frame_done(function()
 F=(F or 0)+1
 for _,v in pairs(K)do v:set_value(0)end
 HELD=HELD or {}
 if F>=60 and F<=63 then K['P1 Start']:set_value(1) end
 if g('selPhase89')==2 then local sf=g('selFrame89');for _,t in ipairs({{20,'P1 A'},{40,'P1 Left'},{60,'P1 A'}}) do if sf>=t[1] and not HELD[t[1]] then HELD[t[1]]=F+2 end; if HELD[t[1]] and F<=HELD[t[1]] then K[t[2]]:set_value(1) end end end
 if g('selPhase89')~=4 then return end
 f=(f==0 and 61 or f)+1
 if f==62 then
  w('ctl',who)
  q(who,0,dir==1 and 700 or 830);q(who,2,300)
  q(1-who,0,mode=='DT'and 825 or(dir==1 and 790 or 740));q(1-who,2,(mode=='DM'or mode=='DRM'or mode=='WRM')and 320 or 300)
 end
 local dk=dir==1 and 'P1 Right'or'P1 Left'
 if f>=65 and f<=68 then K['P1 A']:set_value(1);K['P1 B']:set_value(1);K[dk]:set_value(1)end
 if f>=70 and f<=100 then K[dk]:set_value(1)end
 if f>=78 and f<=80 then K['P1 A']:set_value(1)end
 if f==240 then q(who,0,720);q(who,2,300);q(1-who,0,820);q(1-who,2,300);w('vh',0,1-who);w('fs',0,1-who)end
 if f>=260 and (f<=263 or(hold and f<350))then K['P1 A']:set_value(1)end
 if not hold and f>270 and g('mk')>=10 and g('mv')==1 and not tapped then K['P1 A']:set_value(1);tapped=true;print('TAP',f)end
 if f>=60 then
 local names={'arcTick','arcClock','clStep','clTimer','rn','rnk','rnW'};local vals={f}
 for _,n in ipairs(names)do vals[#vals+1]=g(n,(n=='clStep'or n=='clTimer')and who or nil)end
 for _,n in ipairs({'dX','dY','dZ','dLog','dPose'})do vals[#vals+1]=g(n,who)end
 for _,n in ipairs({'dX','dY','dZ','dLog','fs','clHeld'})do vals[#vals+1]=g(n,1-who)end
 for _,n in ipairs({'mv','mk','pAlt'})do vals[#vals+1]=g(n)end
 vals[#vals+1]=mem:read_u16(A.fd+who*100+70);vals[#vals+1]=mem:read_u32(A.vtimer)
 for _,n in ipairs({'dFlip','dLoaded'})do vals[#vals+1]=g(n,who);vals[#vals+1]=g(n,1-who)end
 csv:write(table.concat(vals,',')..'\n')
 if f<220 then
 checktiles(0);checktiles(1)
 manager.machine.screens[':megadriv']:snapshot(string.format(''..(os.getenv('CLD'))..'md_%s_%03d.png',mode,f))
 if g('rn')==3 and g('clStep',who)==1 then snap('contact')end
 if g('clHeld',1-who)==2 then snap('catch')end
 if g('fs',1-who)==5 then snap('flight')end
 if g('fs',1-who)==6 then snap('bounce')end
 if g('fs',1-who)==7 then snap('land')end
 end
 end
 if f==205 then print('TOTAL_TILE_ERRORS',loaderrors);csv:close();manager.machine:exit()end
end)
