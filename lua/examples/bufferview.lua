tui = require 'arcantui'

wnd = tui.open("hi", "", {handlers = {}})

local tbl = {}

for i=1,65536 do
	tbl[i] = string.char(i % 255);
end

wnd:bufferview(table.concat(tbl, ""),
function(done)
	print("done - edited?", done ~= nil)
	wnd:close()
end, {}
)

while (wnd:process()) do
	wnd:refresh()
end
