from __future__ import absolute_import, unicode_literals

import datetime
import os

from celery import Celery
from celery.signals import worker_process_init, worker_ready

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HNL.celery_settings')

app = Celery('HNL')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.now = datetime.datetime.utcnow


@worker_ready.connect
def run_init_task(sender=None, **kwargs):
    pass


app.autodiscover_tasks()
