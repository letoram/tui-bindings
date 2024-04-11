tui = require 'arcantui'
wnd = tui.open("mm", "", {handlers = {}})
local next = wnd:utf8_step("åhå", 1, 1)
next = wnd:utf8_step("åhå", next)
next = wnd:utf8_step("åhå", next)
