.PHONY: install
export PREFIX ?= /usr

install:
	install -m 0755 rtl2dot.py "$(DESTDIR)$(PREFIX)/bin"
