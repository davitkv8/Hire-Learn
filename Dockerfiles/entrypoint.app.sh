#!/bin/sh


wait-for-it -t 30 -s postgres:5432

python startup_script.py

python manage.py runserver 0.0.0.0:8000