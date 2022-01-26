-- This is mainly a test case for dealing with larger lists

local list = {}

for i=1,1000 do
	table.insert(list, {label = tostring(i), hidden = (i % 10) == 0})
end

local lh
tui = require 'arcantui'

-- handler that dynamically updates the second item
wnd = tui.open("listview", "", {handlers = {}})

local function listview_select(ind)
	if not ind then
		wnd:close()
		return
	end
	lh = wnd:listview(list, listview_select)
end
lh = wnd:listview(list, listview_select)

while (wnd:process()) do
	wnd:refresh()
end
