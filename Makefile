deps:
	pip install -e .

run:
	export FLASK_APP=gfndevice && \
	export FLASK_ENV=development && \
	flask run