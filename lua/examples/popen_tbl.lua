--
-- Testing using popen and non-blocking I/O with table append.
--
-- This has a lower syscall and processing overhead akin to the callback
-- form, but useful when the contents need to be buffered rather than
-- in-stream processed.
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

local tbl = {}

local function flush()
	local ret = false
	_, ret = stdout:read(tbl)
	return ret
end

-- the alive part of the loop matters as we invoke :close from a handler
while (wnd:process() and wnd:alive()) do
	wnd:refresh()

-- Read buffered (set arg 1 to true for non-buffered)
	flush()
	print(#tbl)

-- It is also possible for the process to have terminated with data still
-- in the pipe, hence the second flush call.
	local status, code = wnd:pwait(pid)
	if not status then
		print("flushing")
		while flush() do
		end
		print(#tbl)
		print("exited with code", code)
		break
	end
end

print("results:")
for i,v in ipairs(tbl) do
	print(i, v)
end

wnd:close()
