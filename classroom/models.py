from django.db import models
from django.contrib.auth.models import User


class TimeGraph(models.Model):
    timeGraph = models.JSONField("Time Graph", null=True, blank=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="userTable")

    def __str__(self):
        return f"Time Graph of {self.user}"
