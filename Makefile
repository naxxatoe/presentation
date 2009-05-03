SOURCE=README douf00.spec
TESTSOURCE=test-slides/
PYSOURCE=pysrc/
ALLSOURCE=$(SOURCE) $(TESTSOURCE) $(PYSOURCE)
TAR=tar

test:
	./pysrc/douf00 ./test-slides

dist: ./dist/douf00.tar.gz ./dist/douf00.tar.bz2

dist_tmp: $(ALLSOURCE)
	test -d $@ || mkdir $@
	cp -Rv $^ dist_tmp

dist/douf00.tar.gz: dist_tmp
	$(TAR) cvzf $@ --transform="s/dist_tmp/douf00/" $^

dist/douf00.tar.bz2: dist_tmp
	$(TAR) cvjf $@ --transform="s/dist_tmp/douf00/" $^

clean:
	test ! -e dist/douf00.tar.gz || rm dist/douf00.tar.gz
	test ! -e dist/douf00.tar.bz2 || rm dist/douf00.tar.bz2
	test ! -d dist_tmp || rm -rf dist_tmp
	for file in pysrc/*.pyc; do \
	(test -z "${file}" || test ! -e "${file}" || rm "${file}"); \
	done
