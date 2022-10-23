LIBNAME= luaarcantui
ROCKSPEC= $(shell find . -name $(LIBNAME)-*-*.rockspec)

all: install

install:
	luarocks make --local $(ROCKSPEC)

.PHONY: all install
