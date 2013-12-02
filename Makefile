
.PHONY : clean default check check-1 check-2

default : OperatingSystemSourceListing.pdf DependencyGraph.pdf CC65Version.lst OriginalVersion.pdf CC65Version.dump OriginalVersion.dump

###############################################################################

check : check-1 check-2

check-1 : CC65Version.dump OriginalVersion.dump
	@echo "========== Compare dump files from two paths - they must be identical."
	@if cmp -s CC65Version.dump OriginalVersion.dump ; then echo "identical -- all ok" ; else echo -e "\n***** ERROR: DUMPS NOT IDENTICAL *****\n" ; fi

check-2 : CC65Version.dump
	@echo "========== Check that the CC65 dump file corresponds to the ROM file ..."
	@./CheckDumpAgainstROM.py

###############################################################################

AlmostCC65Version.s : RootVersion.lst
	./MakeVersion.py --version=cc65 < $< > $@

CC65Version.s : AlmostCC65Version.s CC65Version.patch
	patch -p1 AlmostCC65Version.s CC65Version.patch -o CC65Version.s

CC65Version.o CC65Version.lst : CC65Version.s
	ca65 --listing CC65Version.lst --list-bytes 99 CC65Version.s

CC65Version.dump : CC65Version.lst
	./ListToDump.py --version=cc65 < $< > $@

###############################################################################

OriginalVersion.lst : RootVersion.lst
	./MakeVersion.py --version=original < $< > $@

OriginalVersion.dump : OriginalVersion.lst
	./ListToDump.py --version=original < $< > $@

OriginalVersion.ps : OriginalVersion.lst
	enscript --landscape --no-header --font Courier8.5 OriginalVersion.lst -o OriginalVersion.ps

OriginalVersion.pdf : OriginalVersion.ps
	ps2pdf OriginalVersion.ps OriginalVersion.pdf

###############################################################################

DependencyGraph.pdf : DependencyGraph.dot
	dot -Tpdf DependencyGraph.dot -o DependencyGraph.pdf

OperatingSystemSourceListing.pdf OperatingSystemSourceListing.aux OperatingSystemSourceListing.log : OperatingSystemSourceListing.tex DependencyGraph.pdf
	pdflatex OperatingSystemSourceListing.tex
	pdflatex OperatingSystemSourceListing.tex

###############################################################################

clean :
	${RM} *~
	${RM} OperatingSystemSourceListing.pdf OperatingSystemSourceListing.aux OperatingSystemSourceListing.log DependencyGraph.pdf
	${RM} OriginalVersion.lst OriginalVersion.dump OriginalVersion.ps OriginalVersion.pdf
	${RM} AlmostCC65Version.s CC65Version.s CC65Version.o CC65Version.bin CC65Version.lst CC65Version.dump
