from django.db import models
from django.contrib.auth.models import User


class TimeGraph(models.Model):
    timeGraph = models.JSONField("Time Graph", null=True, blank=False)

    def __str__(self):
        return f"Time Graph ID : {self.pk}"


class Relationship(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='receiver')
    agreed_days = models.JSONField("Agreed Days", null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} | {self.receiver} | {self.is_confirmed}"
