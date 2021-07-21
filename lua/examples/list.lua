-- This example covers the use of the 'listview' window
-- state. When :set_list is called, the active set of handlers is taken over
-- by a builtin implementation that behaves like a normal listview style
-- component, calling a closure function when an item has been selected or the
-- user has chosen to cancel/quit.

local list =
{
	{
		label = "Hi",
		shortcut = "h"
	},
	{
		label = "There",
		shortcut = "t"
	}
}

tui = require 'arcantui'
wnd = tui.open("listview", "", {handlers = {}})
wnd:set_list(list,
function(ind)
	if ind and list[ind] then
	else
	end
	wnd:close()
end
)

while (wnd:process()) do
end

