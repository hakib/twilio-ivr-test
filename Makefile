all:

lint:
	venv/bin/flake8 ivr/
	venv/bin/mypy --no-error-summary ivr/

pipcheck:
	venv/bin/python -m pip check

PYTHON := venv/bin/python -X dev -Werror

test:
	$(PYTHON) ivr/manage.py check
	$(PYTHON) -m pytest ivr/

check: lint pipcheck test

coverage:
	coverage erase
	coverage run -m pytest ivr/
	coverage html

init:
	test -d venv/bin || python3 -m venv venv
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install -r requirements.txt
	venv/bin/python -m pip install -r requirements-dev.txt

runserver:
	$(PYTHON) ivr/manage.py runserver 127.0.0.1:8000

makemigrations:
	$(PYTHON) ivr/manage.py makemigrations

createsuperuser:
	$(PYTHON) ivr/manage.py createsuperuser

makemessages:
	cd ivr && ../$(PYTHON) manage.py makemessages --no-obsolete --no-location

compilemessages:
	cd ivr && ../$(PYTHON) manage.py compilemessages

migrate:
	$(PYTHON) ivr/manage.py migrate

setup: init migrate check
