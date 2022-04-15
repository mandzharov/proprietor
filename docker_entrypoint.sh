#!/bin/bash

python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata sample_data.json
gunicorn proprietor.wsgi --bind 0.0.0.0:8000
