install:
	python setup.py install


# Verify our example project
test:
	py.test example/


# Checks dry run, then prompts to execute
clean:
ifneq ($(shell git clean -xdn), )
	@git clean -xdn
	@read -p "Do you wish to continue? [y/N] " yn; \
	 case $$yn in [Yy]* ) git clean -xdf;; esac
else
	@echo "Nothing to clean!"
endif
