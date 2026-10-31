MS=1150 UE=1195 ME=1226 AB=1228 END=3400 SH={1226,1236,1270}
local f=0
local io=manager.machine.ioport.ports
local pad
for k,p in pairs(io) do for n,fl in pairs(p.fields) do if n=="P1 Left" then pad=p end end end
local function fld(n) return pad.fields[n] end
local mem=manager.machine.devices[":maincpu"].spaces["program"]

emu.register_frame_done(function() f=f+1
 local L=(f>=MS and f<ME)
 fld("P1 Left"):set_value(L and 1 or 0); fld("P1 Up"):set_value((f>=MS and f<UE) and 1 or 0)
 fld("P1 A"):set_value((f>=AB and f<AB+3) and 1 or 0)
 if false then print(f, mem:read_u8(0xff5d9e), mem:read_u8(0xff5d9f), mem:read_i16(0xff0044), mem:read_i16(0xff0012), mem:read_i16(0xff0014), mem:read_i16(0xff0016), mem:read_u8(0xff08c0), mem:read_i16(0xff03b8), mem:read_i16(0xff03ac), mem:read_i16(0xff03ba), mem:read_i16(0xff03ae), mem:read_i16(0xff03bc), mem:read_i16(0xff03b0)) end
 for _,s in ipairs(SH) do if f==s then manager.machine.video:snapshot() end end
 if f==1400 then mem:write_i16(0xff0012,20) end
 if f==END then manager.machine:exit() end end)
local mem=manager.machine.devices[":maincpu"].spaces["program"]
local A={"mv2",0xff5d5a,"cool2",0xff0042,"rv1",0xff5d74,"mv",0xff03aa,"sp1",0xff039c,"kd1",0xff5d7a,"cTag",0xff08c0}
local g=0 local last=""
emu.register_frame_done(function() g=g+1 if g>=1250 and g<=2200 then local s="" for i=1,#A,2 do s=s.." "..A[i].."="..mem:read_u16(A[i+1]) end if s~=last then print(g..s) last=s end end end)
