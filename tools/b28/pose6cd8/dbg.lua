local mem=manager.machine.devices[":maincpu"].spaces["program"]
local A={bx=0xff00ae,climb=0xff036a,sx=0xff0370,wpS=0xff03a6,mv=0xff03aa,pinS=0xff03c2,tagT=0xff0930,eb1=0xff0932,wxS=0xff5d3c,wcS=0xff5d46,humW=0xff5d58,rn=0xff5d72,rv1=0xff5d74,kd1=0xff5d7a}
emu.register_frame_done(function() if manager.machine.screens[":megadriv"] then end end)
local g=0
emu.register_frame_done(function() g=g+1 if g>=1236 and g<=1244 then local s=tostring(g) for k,a in pairs(A) do s=s.." "..k.."="..mem:read_u16(a) end print(s) end end)
