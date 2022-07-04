install:
	poetry install

force-inst:
	python3 -m pip install --force-reinstall

page-loader:
	poetry run page-loader

build:
	poetry build

publish:
	poetry publish --dry-run --username ' ' --password ' '

package-inst:
	python3 -m pip install --user dist/*.whl

patch:
	poetry install
	poetry build
	poetry publish --dry-run --username ' ' --password ' '

lint:
	poetry run flake8 pageloader

test:
	poetry run pytest -vv

test-cov:
	poetry run pytest --cov=pageloader

test-cov-xml:
	poetry run pytest --cov=pageloader --cov-report xml tests/

test-cov-html:
	poetry run pytest --cov=pageloader --cov-report html tests/

.PHONY: install test lint selfcheck check build
