tui = require 'arcantui'

wnd = tui.open("hi", "", {handlers = {}})

local env = wnd:getenv()
local _, stdout, _, pid = wnd:popen("find /tmp", "r", wnd:getenv())

if not pid then
	print("popen fail")
end

local _, alive =
stdout:data_handler(
function(_)
	local nr, ok = stdout:read()
	print(nr)
	return ok
end)

stdout:lf_strip(true)
while (wnd:process()) do
	wnd:refresh()
end
