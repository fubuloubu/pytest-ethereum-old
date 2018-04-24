install:
	pip install -e .


# Verify our example project
.PHONY: example
example:
	py.test --assets-file example/contracts.json example/

upload: clean install
	python setup.py sdist
	twine upload dist/*

# Checks dry run, then prompts to execute
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf pytest_ethereum.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
