#!/bin/sh
if [ -e db.sqlite3 ]
then
    echo "Starting..."
else
    echo "Initializing..."
    python manage.py makemigrations
    python manage.py migrate
    python manage.py creatersakey
	python manage.py createsuperuser --noinput
    echo "Initialization complete! Starting..."
fi

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn oidc_server.wsgi:application -w 2 -b :8000