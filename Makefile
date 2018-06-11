install:
	pip install -e .

test: clean
	py.test tests/

# Verify our example project
.PHONY: example
example: install
	py.test --package-file example/contracts.json example/

upload: test example
	python setup.py sdist
	twine upload dist/*

# Checks dry run, then prompts to execute
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf pytest_ethereum.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
