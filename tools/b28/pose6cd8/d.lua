emu.register_frame_done(function() for k,p in pairs(manager.machine.ioport.ports) do for n,_ in pairs(p.fields) do print(k,n) end end manager.machine:exit() end)
