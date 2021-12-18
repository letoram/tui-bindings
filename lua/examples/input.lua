tui = require 'arcantui'

local msg = ""
local wnd

local offset = 1

-- see query_label below
local labels =
{
	{"TEST", "A custom input for testing", tui.keys.A, tui.modifiers.SHIFT, "A"}
}

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

-- this can be called at any time to figure out if you export any custom
-- inputs. returns name, description (matching country, language if possible)
-- and if the input is analog or digital.
--
-- the matching 'name' will be sent to the label or alabel (analog)
-- above when the user wants to trigger it. These should be kept modest
-- in length, ~at most 100 or so but really 5-10 makes more UI sense.
--
-- querying will stop at the first index that returns nil, otherwise the
-- expected returns are:
-- 'label', 'description', default_key (or 0), default_modifier (or 0)
-- and 'v-sym' (single utf8 encoded codepoint for icon identifier.
--
-- Only the 'label' is obligatory in this case.
--
	query_label =
		function(self, index, country, language)
			if labels[index] then
				return unpack(labels[index])
			end
		end,

-- key input that resolve to a 'translated' input, [str] is a single
-- utf8 encoded unicode codepoint. If return is false the input will
-- be re-injected as an on_key (below)
	utf8 =
		function(self, str)
			self:write(str)
			return true
		end,

-- clipboard block of text
	paste =
		function(self, message)
			self:write(message)
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

wnd:set_flags(tui.flags.mouse);
assert(wnd, "tui:open failed")

while (wnd:process()) do
	wnd:refresh()
end
