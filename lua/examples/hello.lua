tui = require 'arcantui'
wnd = tui.open("hi", "")
wnd:write_to(1, 1, "hello world")

while true do
	print(wnd:process())
	wnd:refresh()
end
