--
-- testing using popen and non-blocking I/O
--
-- there are multiple ways of using the io streams that come from popen,
-- with the more UI friendly being to arm data handler callbacks.
--

local tui = require 'arcantui'
wnd = tui.open("popen", "", {handlers = {}})

local env = wnd:getenv()

local _, stdout, _, pid = wnd:popen("find /tmp", "r", env)

if not pid then
	print("popen failed")
	wnd:destroy()
	return
end

local function flush()
-- There is a lot of nuance here - with this setup the source may actually
-- saturate us and re-introduce blocking behaviour even though stdout is set as
-- non-blocking. The other form to :read() takes a callback and leaves the
-- heuristic of interleaving/multiplexing I/O to wnd:process.
	local line = stdout:read()

	while line do
		print(line)
		line = stdout:read()
	end
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
		flush()
		print("exited with code", code)
		break
	end
end

wnd:close()
