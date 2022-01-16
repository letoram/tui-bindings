--
-- similar to the popen example, but using data callbacks and chaining
-- two commands together into a pipeline instead
--
local tui = require 'arcantui'
wnd = tui.open("popen", "", {handlers = {}})

local _, stdout, _, p1pid = wnd:popen("find /", "r")
local _, out, _, p2pid = wnd:popen("rev", stdout, "r")

local function track_children()
	if p1pid then
		local status, code = wnd:pwait(p1pid)
		if not status then
			print("find process over", code)
			p1pid = nil
		end
	end

	if p2pid then
		local status, code = wnd:pwait(p2pid)
		if not status then
			print("find process over", code)
			p2pid = nil
		end
	end
end

-- when there is no more data to be read, propagate that so we break out
local reading = true
out:data_handler(
function(oob)
	local line
	line, reading = out:read()
	if line then
		print(line)
	end
	return true
end)

-- the alive part of the loop matters as we invoke :close from a handler
while (wnd:process() and wnd:alive() and reading) do
	wnd:refresh()
	track_children()
end

wnd:close()
