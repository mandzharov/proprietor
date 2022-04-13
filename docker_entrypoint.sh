#!/bin/bash

apt update && apt upgrade -y
apt install git
git clone https://github.com/mandzharov/proprietor.git
cd proprietor
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata sample_data_fixture.json
gunicorn proprietor.wsgi --bind 0.0.0.0:8001 --workers 3