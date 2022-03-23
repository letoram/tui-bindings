local kill_target = -1
local ticks = 200
local dwnd, root

local function
redraw(wnd)
	wnd:write_to(1, 1, "hello world")
end

local function
tick(wnd)
	ticks = ticks - 1
	if dwnd then
		dwnd:hint(root, {
			anchor_row = math.random(1, 20),
			anchor_col = math.random(1, 20)
		})
	end

	if ticks == 100 then
		print("killing child")
		if kill_target > 0 then
			wnd:psignal(kill_target, "kill")
		end

	elseif ticks == 0 then
		print("shutting down")
		wnd:close()
	end
end

tui = require 'arcantui'

root = tui.open("hi", "", {handlers = {resized = redraw, tick = tick}})
redraw(root)

root:new_window("handover",
	function(wnd, new)
		if not new then
			print("handover not permitted")
			return
		end
		local _, _, _, pid = wnd:phandover("/usr/bin/afsrv_terminal", "")
		kill_target = pid
		dwnd = new
		print("handed over to", pid, new)
	end
)

while (root:process() and root:alive()) do
	root:refresh()
end
