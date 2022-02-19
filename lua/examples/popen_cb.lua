--
-- Testing using popen and non-blocking I/O with callback flushing.
--
-- The use for that over spinning on reads until fail is fewer system
-- calls per line and easier eof propagation.
--
local tui = require 'arcantui'
wnd = tui.open("popen", "", {handlers = {}})

local env = wnd:getenv()

local _, stdout, _, pid = wnd:popen("find /tmp", "r", env)
stdout:lf_strip(true);

if not pid then
	print("popen failed")
	wnd:destroy()
	return
end

local function flush()
	local ret = false
	local _, alive =
	stdout:read(
		function(line, eof)
			print(line)
			ret = eof
		end
	)
	return ret or not alive
end

-- the alive part of the loop matters as we invoke :close from a handler
while (wnd:process() and wnd:alive()) do
	wnd:refresh()

-- Read buffered (set arg 1 to true for non-buffered)
	flush()

-- It is also possible for the process to have terminated with data still
-- in the pipe, hence the second flush call.
	local status, code = wnd:pwait(pid)
	if not status then
		while not flush() do
		end
		print("exited with code", code)
		break
	end
end

wnd:close()
