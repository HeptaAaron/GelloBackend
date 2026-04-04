PYTHON=python3.12
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

help:
	@echo "make setup    - create venv + install deps + download models"
	@echo "make run      - run django server"
	@echo "make migrate  - run migrations"
	@echo "make shell    - django shell"
	@echo "make clean    - remove venv"

check-python:
	@$(PYTHON) -c "import sys; exit(0) if sys.version_info[:2]==(3,12) else exit(1)" || (echo "Python 3.12 required"; exit 1)

setup: check-python
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PY) DjangoBackend/scripts/download_models.py

run:
	$(PY) manage.py runserver

migrate:
	$(PY) manage.py makemigrations
	$(PY) manage.py migrate

shell:
	$(PY) manage.py shell

clean:
	rm -rf $(VENV)