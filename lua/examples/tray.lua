-- one tray icon and one 'statusbar'
tui = require 'arcantui'

local function
redraw(wnd)
	wnd:write_to(0, 0, "tray-statusbar embed")
	wnd:write_to(0, 1, "if the WM supports it, this should be hidden")
end

local function redraw_tray()
	wnd:write_to(0, 0, "hi there")
end

local function
setup_traywnd(paren, wnd)
	if not wnd then
		print("rejected traywnd request")
	end

	print("tray allocated")
	wnd:set_handlers({resized = redraw_tray})
end

wnd = tui.open("tray-test", "", {handlers = {resized = redraw}})
redraw(wnd)
wnd:new_window("dock", setup_traywnd)

while (wnd:process()) do
	wnd:refresh()
end
