tui = require 'arcantui'
local root

local tbl = {}
for i=1,65536 do
	tbl[i] = string.char(i % 255);
end
local bufferstr = table.concat(tbl, "")

local function setup_bufferwnd(parent, wnd)
	if not wnd then
		print("failed to allocate new window")
		return
	end

	wnd:bufferview(bufferstr,
	function()
		print("buffer over")
		wnd:close()
	end)
end

root = tui.open("hi", "", {
handlers = {
	key =
	function(self, sub, keysym, code, mods)
		if keysym == tui.keys.F1 then
			root:new_window("tui", setup_bufferwnd)
		elseif keysym == tui.keys.F2 then
			root:close()
		end
	end
}})

root:write("press F1 to request a new window, F2 to close")
root:refresh()

while (root:process() and root:alive()) do
	root:refresh()
end

print("over")
