--
-- test case that first writes a number of lines, tries to read
-- them back and compare, then increase the count and width and
-- repeats until forcibly terminated.
--
tui = require 'arcantui'
wnd = tui.open("hi", "", {handlers = {}})
wnd:funlink("test.out")
nbio = wnd:fopen("test.out", "w")
if not nbio then
	error("couldn't open test.out for writing")
end

function schedule_write(n, m, tbl)
	local function on_complete(ok)
		print("pass ", n, m, "completed")
		nbio:close()
		schedule_read(n, m, tbl)
	end

	if tbl then
		local out = {}
		for i=1,n do
			local str = string.rep((i-1) % 10, m) .. "\n"
			table.insert(out, str)
		end
		if not nbio:write(out, on_complete) then
			error("fail on tbl-write " .. tostring(m))
		end
	else
		for i=1,n do
			local str = string.rep((i-1) % 10, m) .. "\n"
			if not nbio:write(str, on_complete) then
				error("fail on " .. tostring(i) .. " : " .. tostring(m))
			end
		end
	end
end

schedule_write(123, 10)

function schedule_read(n, m, tbl)
	nbio = wnd:fopen("test.out", "r")
	nbio:lf_strip(true)

	local dset = {}
	nbio:data_handler(
	function()
		_, alive = nbio:read(dset)
		if not alive then
			print("dset over")
			if #dset ~= n then
				for i,v in ipairs(dset) do
					print(i, v)
				end
				error(string.format("count mismatch expected: %d got: %d", n, #dset))
			end
			print("next iter")
			wnd:funlink("test.out")
			nbio:close()
			nbio = wnd:fopen("test.out", "w")
			schedule_write(n+1, m+1, not tbl)
		end
		return true
	end)
end

while (wnd:process()) do
	wnd:refresh()
end
