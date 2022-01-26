-- This example covers the use of the 'listview' window
--
-- state. When :set_list is called, the active set of handlers is taken over
-- by a builtin implementation that behaves like a normal listview style
-- component, calling a closure function when an item has been selected or the
-- user has chosen to cancel/quit.
--
local list =
{
	{
		label = "This",
		shortcut = "t"
	},
	{
		label = "os.time",
		cur = os.time(),
		tick = 0
	},
	{
		label = "separator",
		separator = true
	},
	{
		label = "could be toggled",
		checked = true,
	},
	{
		label = "heading",
		itemlabel = true
	},
	{
		label = "cantseethis",
		hidden = true
	},
	{
		label = "no touching",
		passive = true
	},
	{
		label = "subgroup",
		shortcut = "l",
		indent = 1,
		has_sub = true
	},
	{
		label = "flip_hidden",
		flip = true
	}
}

local lh
tui = require 'arcantui'

-- handler that dynamically updates the second item
wnd = tui.open("listview", "", {handlers = {
	tick = function()
		local now = os.time()
		if list[2].cur ~= now then
			list[2].cur = now
			list[2].tick = 0
		else
			list[2].tick = list[2].tick + 1
		end

		list[2].label = tostring(os.time()) .. "." .. tostring(list[2].tick)
		lh:update(2, list[2])
	end
}})

local function listview_select(ind)
	if not ind then
		wnd:close()
		return
	end
	if list[ind].checked ~= nil then
		list[ind].checked = not list[ind].checked
	end
	if list[ind].flip then
		for _,v in ipairs(list) do
			if not v.flip then
				v.hidden = not v.hidden
			end
		end
	end

	lh = wnd:listview(list, listview_select)
end

lh = wnd:listview(list, listview_select)
print("lh is", lh)

while (wnd:process()) do
	wnd:refresh()
end
