tui = require 'arcantui'

local function
redraw(wnd)
	local hattr = tui.attr({underline_alt = true})

	local l = tui.attr({border_left = true, fg = 255})
	local r = tui.attr({border_right = true, fg = 255})
	local tl = tui.attr({border_left = true, border_top = true, fg = 255})
	local tr = tui.attr({border_right = true, border_top = true, fg = 255})
	local t = tui.attr({border_top = true, fg = 255})
	local d = tui.attr({border_down = true, fg = 255})
	local dl = tui.attr({border_left = true, border_down = true, fg = 255})
	local dr = tui.attr({border_right = true, border_down = true, fg = 255})

	wnd:write_to(0, 0, " ", tl)
	wnd:write_to(1, 0, "           ", t)
	wnd:write(" ", tr)
	wnd:write_to(0, 1, " ", l)
	wnd:write_to(1, 1, "hello world", hattr)
	wnd:write(" ", r)
	wnd:write_to(0, 2, " ", dl)
	wnd:write_to(1, 2, "           ", d)
	wnd:write(" ", dr)
end

wnd = tui.open("hi", "", {handlers = {resized = redraw}})
redraw(wnd)

while (wnd:process()) do
	wnd:refresh()
end
