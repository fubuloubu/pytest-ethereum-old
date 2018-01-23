install:
	python setup.py install

test:
	py.test example/

clean:
ifneq ($(shell git clean -xdn), )
	@git clean -xdn
	@read -p "Do you wish to continue? [y/N] " yn; \
	 case $$yn in [Yy]* ) git clean -xdf;; esac
endif
