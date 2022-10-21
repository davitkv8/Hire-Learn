from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class UserImage(models.Model):
    userImage = models.ImageField(blank=False, null=True,
                                  default='default.png', upload_to='teacher_profile_images')


class HashTag(models.Model):
    hashTag = models.CharField(max_length=55)

    def __repr__(self):
        return f"{self.hashTag}"


class Subject(models.Model):
    subject = models.CharField(max_length=55)

    def __repr__(self):
        return f"{self.subject}"


class UserStatus(models.Model):
    userStatus = models.CharField(max_length=55, choices=(
        ('student', 'student'),
        ('lecturer', 'lecturer')
    ))
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.userStatus}"


class UserProfile(models.Model):
    description = models.TextField(blank=False, null=True, max_length=6000)
    hashtags = models.ManyToManyField(HashTag)
    image = models.OneToOneField(UserImage, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.user.username}"


class TeachersProfile(UserProfile):
    birth_date = models.DateField(blank=False, null=False)
    full_name = models.CharField(blank=False, null=False, max_length=55)
    lecture_price = models.PositiveIntegerField(blank=False, null=False, validators=[MaxValueValidator(10000)])
    platform_choices = (
        ('', ''),
        ('Google Meet', 'Google Meet'),
        ('Microsoft Teams', 'Microsoft Teams'),
        ('Zoom', 'Zoom'),
        ('Facebook Messenger', 'Facebook Messenger'),
        ('Other', 'Other')
    )
    platform = models.CharField(blank=False, null=False, max_length=55, choices=platform_choices)

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL,
                                blank=False, null=True, max_length=55, default='')

    def __str__(self):
        return f"{self.full_name}'s Profile."

    # def get_description(self):
    #     return self.description[:300]
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


