#!/bin/sh

python manage.py showmigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
gunicorn  --bind :8000 --workers 2 satellite.wsgi
exec "$@"
