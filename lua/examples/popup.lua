tui = require 'arcantui'
local root
local popup_active

local function setup_popup(parent, new)
	if not wnd then
		print("failed to allocate new window")
		return
	end

	popup_active = wnd
	wnd:hint(parent, {min_rows = 10, anchor_x = 5, anchor_y = 5})
	wnd:set_handlers({resized =
	function(self, col, rows)
		for i=1,rows do
			self:write_to(0, i-1, "line " .. tostring(i))
		end
	end})
end

root = tui.open("hi", "", {
handlers = {
	key =
	function(self, sub, keysym, code, mods)
		if keysym == tui.keys.F1 then
			root:new_window("popup", setup_popup)
		elseif keysym == tui.keys.F2 then
			if popup_active then
				popup_active:close()
				popup_active = nil
			end
		end
	end,
	resized = function(wnd)
		wnd:write_to(0, 0, "press F1 to trigger popup, F2 to close")
	end,
}})

root:refresh()

while (root:process() and root:alive()) do
	root:refresh()
end

print("over")
