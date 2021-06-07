-- This example covers the three major kinds of blob transfers:
--
--  state blobs (for store/restoring application state)
--  immediate bchunks (for universal open/save)
--  passive bchunks for drag-drop/user initiated open/save
--
-- The complication with this is that tui has soft-realtime requirements,
-- blocking on I/O operations is a poor user experience and we don't want to
-- pull in other large asynchronous I/O libraries like libuv, which makes this
-- whole procedure much more difficult.
--
local tui = require 'arcantui'
local wnd

local function
redraw(wnd)
	wnd:erase()
end

-- The first is 'state' which is some kind of serializable blob.
--
-- The 'blob' usertable here is by default our own abstraction that we
-- can attach to wnd and have it be part of wnd:process(). If that is
-- not desired and the normal lua file API is to be used, blob:lua_file()
-- can be used. This returns the same object wrapped as a lua file,
-- and the source blob is closed.
--
local function
state_in(self, blob)
	wnd:write_to(1, 0, "got state deserialize")
	blob.data_handler(
	function(buffer, last)
		print("read:", buffer)
	end)
end

-- this can use both the callback form or the 'you provide the buffer,
-- the backend will do the transfers and send progress notification
local function
state_out(self, blob)
	wnd:erase()
	wnd:write_to(1, 0, "got state serialize")
	blob:data_handler("this is a simple state blob, nothing to see here")
end

local function
bchunk_in(self, blob, id)
	wnd:erase()
	wnd:write_to(1, 0, "load from blob for " .. id)
end

-- id will match one of the extensions provided in the announcement
-- below, but could also be anything if the '*' mask was used in
-- announce/request_io
local function
bchunk_out(self, blob, id)
	wnd:erase()
	wnd:write_to(1, 0, "save into blob for " .. id)
end

-- In contrast to 'announce' below, here we say that we would like to
-- load (F1) or store (F2) immediately. It is still a hint, there is
-- no obligation for the user to act.
local function
keyinput(self, sub, keysym, code, mods)
	if keysym == tui.keys.F1 then
		wnd:write_to(0, 0, "reqesting to load a file of 'tmp' extension")
		wnd:request_io("tmp")
	elseif keysym == tui.keys.F2 then
		wnd:write_to(0, 0, "reqesting to save a file 'tmp' extension")
		wnd:request_io(nil, "tmp")
	end
end

wnd = tui.open("state", "", {
	handlers = {
		state_in = deserialize,
		state_out = serialize,
		bchunk_in = bchunk_in,
		bchunk_out = bchunk_out,
		key = keyinput
	}
})

-- Announce that we are capable of loading 'html' and 'txt' extensions
-- and saving 'txt'. This is only a hint, when / how the user does this
-- is not up to us.
wnd:announce_io("html;txt", "txt")
wnd:state_size(4096)

while (wnd:process()) do
	wnd:refresh()
end
