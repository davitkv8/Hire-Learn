#!/bin/sh


wait-for-it -t 30 -s postgres:5432

echo `ls -ltr`

python main.py

python manage.py runserver 0.0.0.0:8000