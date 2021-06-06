local function
redraw(wnd)
	wnd:write_to(1, 1, "hello world")
end

tui = require 'arcantui'

wnd = tui.open("hi", "", {handlers = {resized = redraw}})
redraw(wnd)

while (wnd:process()) do
	wnd:refresh()
end
