package = "luaarcantui"
version = "1.0-0"
source = {
    url = "https://github.com/letoram/tui-bindings.git",
		tag = "",
    file = ""
}
description = {
    summary = "luaarcantui is a text UI library for the Arcan Desktop Engine",
    detailed = [[
        luaarcantui is a wrapper of libarcan-tui for lua.
    ]],
    license = "BSD-3-clause",
    homepage = "https://github.com/letoram/tui-bindings"
}
dependencies = {
    "lua >= 5.1"
}
build = {
    type = "builtin",
    modules = {
        arcantui = {
            sources = { "tui_lua.c", "nbio.c", "tui_popen.c" },
            libraries = { "arcan_tui" },
-- no way to just use pkg-tool?
            libdirs = {"/usr/local/lib", "/usr/lib"},
						incdirs = {
							"/usr/include/arcan/shmif",
							"/usr/local/include/arcan/shmif",
							"/usr/include/arcan",
							"/usr/local/include/arcan"
						}
        }
    },
}

