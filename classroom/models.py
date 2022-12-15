from django.db import models
from django.contrib.auth.models import User


class TimeGraph(models.Model):
    timeGraph = models.JSONField("Time Graph", null=True, blank=False)

    def __str__(self):
        return f"Time Graph ID : {self.pk}"
