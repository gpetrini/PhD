PREFIX = /home/gpetrini/
INSTALLDIR = $(PREFIX)/kirq
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/man

.PHONY: dist
dist: VERSION = $(shell suf --version|head -n1|sed 's/suf //')
dist: SRCDIR = dist/kirq
dist:
	pyinstaller -y /usr/local/bin/kirq
	cp Makefile $(SRCDIR)/
	mkdir -p $(SRCDIR)/man/man1/
	cp ~/dev/qca/acq/doc/README $(SRCDIR)
	pandoc -s -t plain --toc < ~/dev/qca/acq/doc/FAQ.pandoc > $(SRCDIR)/FAQ
	pandoc -s -t man < ~/dev/qca/acq/doc/kirq.pandoc > $(SRCDIR)/man/man1/kirq.1
	tar -C dist -cvvjf kirq-$(VERSION)-linux.tar.bz2 kirq

.PHONY: install
install:
	cp -r ./ $(INSTALLDIR)
	ln -s $(INSTALLDIR)/kirq $(BINDIR)
	mkdir -p $(MANDIR)/man1
	cp $(INSTALLDIR)/man/man1/kirq.1 $(MANDIR)/man1/kirq.1

.PHONY: uninstall
uninstall:
	rm $(BINDIR)/kirq
	rm -r $(INSTALLDIR)
	rm $(MANDIR)/man1/kirq.1

