tui = require 'arcantui'

local function redraw(wnd)
	wnd:erase()
	wnd:write_to(0, 0, "hello readline")
end

-- different kinds of readline configurations for more advanced prompts
-- and editing controls
local opts =
{
	{
		prompt = {"split ", "into ", "multiple>"}
	},
	{
		anchor = -2,
		rows = 2,
		margin_left = 10,
		margin_right = 10,
		multiline = true,
		prompt = "position+props, meta+enter to set> ",
		verify = function(self, prefix, msg, suggest)
			if (suggest) then
				self:suggest({"hi", "there", "potato"})
			end
			return true
		end,
	},
	{
		cancellable = true,
		mask_character = "*",
		prompt = "password>"
	},
	{
		prompt = {
			"formatting ",
			tui.attr({bold = true, fc = tui.colors.alert}),
			"with  ",
			tui.attr({fr = 255, fg = 127, fb = 64, br = 0, bg = 0, bb = 127}),
			"multiples: >"
		},
		verify =
		function(self, prefix, line)
			print("I am in verify, run autocomplete")
			if not string.find(line, " hi$") then
				self:autocomplete(" hi")
			else
				self:autocomplete("")
			end
			return true
		end,
	},
	{
		prompt = "only alphanum >",
		filter =
		function(self, ch, len)
			return string.match(ch, "%w") ~= nil
		end
	}
}

wnd = tui.open("hi", "", {handlers = {resized = redraw, recolor = redraw}})

local lineind = 1
local handler
handler =
function(self, msg)
	print("readline-got:", msg)
	if opts[lineind] then
		local rl = wnd:readline(handler, opts[lineind])
		rl:set_prompt(opts[lineind].prompt)
		lineind = lineind + 1
	else
		wnd:close()
	end
end

local rl = wnd:readline(handler, {})
rl:set_history({"these", "are", "echoes", "of", "the", "past"})
rl:set_prompt("a simple one")

-- the alive part of the loop matters as we invoke :close from a handler
while (wnd:process() and wnd:alive()) do
	wnd:refresh()
end

print("no more lines to read")
