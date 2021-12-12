project('arcantui', 'c', default_options : ['c_std=c11'])
shmif = dependency('arcan-shmif-tui')

foreach ver : ['1', '2', '3', '4']
    lua = dependency('lua5.' + ver, required: false)
    if lua.found()
        luadir = 'lib/lua/5.' + ver
        break
    endif
endforeach

if not lua.found()
    error('no supported lua version found (5.1, 5.2, 5.3, 5.4)')
endif

thread = dependency('threads')
cc = meson.get_compiler('c')
math = cc.find_library('m', required : false)
shared_library('arcantui', 'tui_lua.c', install : true, install_dir: luadir, name_prefix: '', dependencies : [shmif, math, thread, lua])
