.PHONY: all
all: lint/ruff test lint

help:
	@inv help-make

#
# Tests
#
.PHONY: test test-with-sqla-warnings test-with-coverage test-with-typeguard

## Run tests
test:
	pytest


#
# Lint
#
.PHONY: lint/ruff lint hadolint audit

##
lint/ruff:
	ruff src tests

## Lint source code and check typing
lint:
	ruff src tests/test*.py
	# flake8 src tests/test*.py
	lint-imports
	vulture --min-confidence 80 src
	mypy --show-error-codes tests
	pyright
	# deptry .
	# TODO later
	# make hadolint
	# mypy --show-error-codes --check-untyped-defs tests src
	# pyright tests
	# mypy --show-error-codes src
	# mypy --check-untyped-defs --show-error-codes src
	# python -m pyanalyze --config-file pyproject.toml src

hadolint:
	docker container run --rm -i \
		hadolint/hadolint hadolint --ignore DL3008 --ignore DL3059 -t style - < docker/Dockerfile

## Run security audit
audit:
	pip-audit
	safety check


#
# Rest
#

## Run (dev) server
run:
	honcho -f Procfile.dev start

## Run server under gunicorn
run-gunicorn:
	gunicorn -b 127.0.0.1:5000 -w1 'app.main:create_app()'

## Cleanup repository
clean:
	adt clean

## Format source code
format:
	black --target-version py310 src tests *.py
	isort src tests *.py

#
# Dependencies
#
.PHONY: update-deps

## Update dependencies
update-deps:
	pip install -qU pip setuptools wheel
	poetry update

poetry.lock: pyproject.toml
	poetry update

#
# Deploy to Nua
#
deploy:
	inv nua-deploy
	# nua deploy
