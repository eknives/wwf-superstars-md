local mem=manager.machine.devices[":maincpu"].spaces["program"]
local A={"mv2",0xff5d5a,"cool2",0xff0042,"rv1",0xff5d74,"mv",0xff03aa,"sp1",0xff039c,"kd1",0xff5d7a,"cTag",0xff08c0}
local g=0 local last=""
emu.register_frame_done(function() g=g+1 if g>=1250 and g<=2200 then local s="" for i=1,#A,2 do s=s.." "..A[i].."="..mem:read_u16(A[i+1]) end if s~=last then print(g..s) last=s end end end)
