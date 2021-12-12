LIBNAME= luaarcantui
ROCKSPEC= $(shell find . -name $(LIBNAME)-*-*.rockspec)

all: install

install:
	luarocks-5.1 make --local $(ROCKSPEC)

.PHONY: all install
