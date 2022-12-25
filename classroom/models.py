from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import datetime


class TimeGraph(models.Model):
    """
        To understand how this JSONField stores data, please check template_days_data.json
        "0:00-1:00":"false", "1:00-2:00":"true", "2:00-3:00":"User John Smith"
        here, false means that user has blocked this timegraph that he is not taking requests for these times.
        For example : {
            monday: {"0:00-1:00":"false", "1:00-2:00":"true"}
        }
        means that, this teacher has not free time on monday in this range "0:00-1:00",
        but on "1:00-2:00" he is able to take requests.

        "2:00-3:00" at this time, he has already booked lessons from user John Smith
    """

    timeGraph = models.JSONField("Time Graph", null=True, blank=False)
    record_creation_datetime = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"Time Graph ID : {self.pk}"


class Relationship(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='receiver')
    agreed_days = models.JSONField("Agreed Days", null=True)
    is_confirmed = models.BooleanField(default=False)
    record_creation_datetime = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):

        if self.is_confirmed is True:
            self.record_creation_datetime = datetime.now()

        super(Relationship, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} | {self.receiver} | {self.is_confirmed}"


class Feedback(models.Model):

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=False)
    textFeedback = models.TextField(max_length=200, null=False)

    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name="feedback_sender")

    receiver = models.ForeignKey(User, null=False, on_delete=models.CASCADE,
                                 related_name="feedback_receiver")

    record_creation_datetime = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver} score : {self.rating}"