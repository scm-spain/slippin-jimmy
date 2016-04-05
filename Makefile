PROJECT=slippinj
MY_CURR_DIR=$(shell pwd)
MY_PYTHON_PATH=$(shell echo ${PYTHONPATH})
PIP=pip

install-develop: clean
	$(PIP) install -e $(MY_CURR_DIR)

install-user: clean
	python setup.py install --user

install: clean
	python setup.py install

uninstall-user:
	$(PIP) uninstall $(PROJECT)

uninstall:
	$(PIP) uninstall $(PROJECT)

test: clean
	export PYTHONPATH=$(MY_PYTHON_PATH):$(MY_CURR_DIR)/src; py.test -vv --cache-clear --cov-report term --cov=$(PROJECT) tests/$(PROJECT)

clean:
	rm -rf build dist $(PROJECT).egg-info docs-api tmp .cache
	find . -name "*.pyc" -exec rm -rf {} \;

publish: clean
	python setup.py sdist
	twine upload dist/*
