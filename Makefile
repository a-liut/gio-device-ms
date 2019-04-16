.PHONY: deps test run

deps:
	pip install -e .

test:
	python -m pytest -vv --setup-show

cov:
	python -m pytest --cov-report term-missing --cov=gfndevice

run:
	export FLASK_APP=gfndevice && \
	export FLASK_ENV=development && \
	flask run