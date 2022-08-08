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
	poetry run flake8 page_loader

lint-test:
	poetry run flake8 tests/test_page_loader.py

test:
	poetry run pytest -vv

test-cov:
	poetry run pytest --cov=page_loader

test-cov-xml:
	poetry run pytest --cov=page_loader --cov-report xml tests/

test-cov-html:
	poetry run pytest --cov=page_loader --cov-report html tests/

.PHONY: install test lint selfcheck check build
