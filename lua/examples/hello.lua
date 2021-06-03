tui = require 'arcantui'
wnd = tui.open("hi", "")
wnd:write_to(1, 1, "hello world")

while (wnd:process()) do
	wnd:refresh()
end
