from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from classroom.models import *


class Image(models.Model):
    image = models.ImageField(blank=False, null=True,
                              default='default.png', upload_to='teacher_profile_images')

    def __repr__(self):
        return f"{self.image}"

    def __str__(self):
        return f"Path on localhost : {self.image.url}"


class HashTag(models.Model):

    hashTag = models.CharField(max_length=55)
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    def __repr__(self):
        return f"{self.hashTag}"

    def __str__(self):
        return self.hashTag


class Title(models.Model):
    title = models.CharField(max_length=55)

    def __repr__(self):
        return f"{self.title}"

    def __str__(self):
        return self.title


class UserStatus(models.Model):
    userStatus = models.CharField(max_length=55, choices=(
        ('student', 'student'),
        ('teacher', 'teacher')
    ))

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.userStatus}"


class Platform(models.Model):
    platform_choices = (
        ('', ''),
        ('Google Meet', 'Google Meet'),
        ('Microsoft Teams', 'Microsoft Teams'),
        ('Zoom', 'Zoom'),
        ('Facebook Messenger', 'Facebook Messenger'),
        ('Other', 'Other')
    )
    platform = models.CharField(blank=False, null=False, max_length=55, choices=platform_choices)

    def __repr__(self):
        return f"{self.platform}"

    def __str__(self):
        return self.platform


class BasicAbstractProfile(models.Model):
    description = models.TextField(blank=False, null=True, max_length=6000)
    hashTag = models.ManyToManyField(HashTag)
    image = models.OneToOneField(Image, on_delete=models.SET_NULL, null=True)
    timeGraph = models.OneToOneField(TimeGraph, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    record_creation_datetime = models.DateTimeField(editable=True, auto_now=True)

    user_status = models.ForeignKey(UserStatus, editable=False, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.user_status = self.user.userstatus
        super().save(*args, **kwargs)

    def get_description(self):
        return self.description[:300]

    def __repr__(self):
        return f"{self.user.username}"


class StudentProfile(BasicAbstractProfile):
    def __repr__(self):
        return f"{self.user.username}"


class TeacherProfile(BasicAbstractProfile):
    birth_date = models.DateField(blank=False, null=False)
    full_name = models.CharField(blank=False, null=False, max_length=55)
    lecture_price = models.FloatField(
        blank=False, null=False, validators=[MaxValueValidator(10000)]
    )

    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              blank=False, null=True, max_length=55, default='')

    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL,
                                 blank=False, null=True, max_length=55)

    def __str__(self):
        return f"{self.full_name}'s Profile."

    #
    # def get_friends(self):
    #     return self.friends.all()
    #
    # def get_friends_number(self):
    #     return self.friends.all().count()
    #
    # def get_feedbacks_number(self):
    #     return self.feedback.all().count()
    #
    # def feedback_rating(self):
    #     sum_rating = 0
    #     all_feedbacks = self.feedback.all()
    #     if self.get_feedbacks_number() == 0:
    #         return 0
    #     for feedback in all_feedbacks:
    #         sum_rating += feedback.rating
    #     return round(sum_rating/self.get_feedbacks_number(), 1)


STATUS_CHOICES = (
        ('send', 'send'),
        ('Approve', 'Approve')
    )


class Relationship(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.sender} | {self.receiver} | {self.status}"
