tui = require 'arcantui'

local msg = ""
local wnd

local offset = 1

local function draw()
-- erase,
-- cursor to ..
end

local function add_str(str)
	msg = msg .. str
	draw()
end

-- note that most events only trigger on rising edge (press)
wnd =
tui.open("input", "", {
	handlers =
	{

-- return state determines if the input will be consumed and continue
-- on as a key event (see below)
	label =
		function(self, label)
			print("label", label)
			return false
		end,

-- these can be both relative and absolute, but will only be forwarded
-- if the window is in mouse forward mode
	mouse_motion =
		function(self, relative, x, y, mods)
			print("mouse", relative, x, y, mods)
		end,

-- these will always be in absolute space, but only forwarded if the
-- window is in mouse forward mode
	mouse_button =
		function(self, x, y, index, active, mods)
			print("mouse button", x, y, index, active, mods)
		end,

-- key input that resolve to a 'translated' input, [str] is a single
-- utf8 encoded unicode codepoint. If return is false the input will
-- be re-injected as an on_key (below)
	utf8 =
		function(self, str)
			add_str(str)
			return false
		end,

-- clipboard block of text
	paste =
		function(self, message)
			add_str(message)
		end,

-- This should be avoided and instead use label if possible, it is when
-- the input model is complex (like emacs level) where mod+key mod+key2
-- like sequences need to be interpreted.
	key =
		function(self, sub, keysym, code, mods)
			print(sub, keysym, code, mods, tui.keys[keysym])
		end
	}
}
)

assert(wnd, "tui:open failed")
print(tui, tui.keys, tui.flags)
for k,v in pairs(tui) do print(k,v); end

while (wnd:process()) do
	wnd:refresh()
end
