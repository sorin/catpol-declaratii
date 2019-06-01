venv-force:
	pip3 install virtualenv && rm -rf ./venv && virtualenv --python=python3.7 ./venv

install-requirements:
	./venv/bin/pip3 install -r requirements.txt -r requirements-dev.txt

install-requirements-force: venv-force install-requirements

run: 
	(export DJANGO_SETTINGS_MODULE=project_template.settings.dev && ./venv/bin/python3 manage.py runserver)

local-env-bash:
	(bash -c 'source ./venv/bin/activate; bash --init-file  ~/.bash_profile')

cleandb:
	rm -f project_template/migrations/*
	rm -f db.sqlite3

installdb: cleandb
	(export DJANGO_SETTINGS_MODULE=project_template.settings.dev && ./venv/bin/python manage.py makemigrations)
	(export DJANGO_SETTINGS_MODULE=project_template.settings.dev && ./venv/bin/python manage.py migrate --run-syncdb)

setup: install-requirements-force installdb
