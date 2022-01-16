--
-- testing using popen and non-blocking I/O
--
-- there are multiple ways of using the io streams that come from popen,
-- with the more UI friendly being to arm data handler callbacks.
--

local tui = require 'arcantui'
wnd = tui.open("popen", "", {handlers = {}})

local env = wnd:getenv()

print("in directory", wnd:chdir())
print("going up", wnd:chdir(".."))
print("going bad", wnd:chdir("does not exist"))

wnd:close()
