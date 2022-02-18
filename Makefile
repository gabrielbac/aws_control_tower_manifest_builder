.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black venv
.DEFAULT_GOAL := help
VENV = venv
VERSION := $(shell git describe --tags --abbrev=0 | sed -Ee 's/^v|-.*//')

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

venv: 
	test -d $(VENV) || python3 -m $(VENV) $(VENV)
	. $(VENV)/bin/activate
	pip install --upgrade -r requirements_dev.txt

run: ## runs script locally and opens the manifest file
	. $(VENV)/bin/activate
	python aws_control_tower_manifest_builder/aws_control_tower_manifest_builder.py
	@if command -v code; then \
		code output_manifest/manifest.yaml; \
	else \
		@cat output_manifest/manifest.yaml; \
	fi 

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	rm -rf $(VENV)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 ./src ./test --ignore=E501,W503
lint/black: ## check style with black
	black --check src tests
lint/pylint:
	pylint --disable=E0101,R1710,W0511 src/aws_control_tower_manifest_builder

lint: lint/flake8 lint/pylint lint/black ## check style

test: ## run tests quickly with the default Python
	PYTHONPATH=./aws_control_tower_manifest_builder python -m pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source aws_control_tower_manifest_builder -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/aws_control_tower_manifest_builder.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ aws_control_tower_manifest_builder
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	pip uninstall -y aws_control_tower_manifest_builder
	python setup.py install

local-dist: ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

local-install: ## install the package to the venv
	pip uninstall -y aws_control_tower_manifest_builder
	python setup.py install

make local-test:
	aws_control_tower_manifest_builder --input-cf tests/sample_templates \
	--input-scp tests/sample_scp \
	--output tests/output_manifest

SEMVER_TYPES := major minor patch
BUMP_TARGETS := $(addprefix bump-,$(SEMVER_TYPES))
.PHONY: $(BUMP_TARGETS)
$(BUMP_TARGETS): 
	$(eval bump_type := $(strip $(word 2,$(subst -, ,$@))))
	bumpversion --verbose --current-version $(VERSION) $(bump_type) setup.py
    #$(eval f := $(words $(shell a="$(SEMVER_TYPES)";echo $${a/$(bump_type)*/$(bump_type)} )))
    #@echo -n v
    #@echo $(VERSION) | awk -F. -v OFS=. -v f=$(f) '{ $$f++ } 1'
	