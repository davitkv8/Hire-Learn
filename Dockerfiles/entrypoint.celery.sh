#!/bin/sh

# wait for django proj to start
wait-for-it -t 30 -s hnl__app:8000

celery -A HNL worker -l INFO
