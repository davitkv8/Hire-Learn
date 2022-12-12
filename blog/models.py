from django.db import models
from users.models import Image, HashTag
from django.contrib.auth.models import User
from django.utils.timezone import now


class TimeGraph(models.Model):
    timeGraph = models.JSONField("Time Graph", null=True, blank=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="userTable")

    def __str__(self):
        return f"Time Graph of {self.user}"


class Post(models.Model):
    title = models.CharField(blank=False, null=False, max_length=6000)
    description = models.TextField(blank=False, null=False, max_length=6000)

    hashTags = models.ManyToManyField(HashTag)
    postImage = models.ForeignKey(Image, null=True,
                                  default="default_post_image.jpg", on_delete=models.SET_NULL
                                  )

    last_updated_at = models.DateTimeField(editable=False,
                                           auto_now=True)

    record_creation_datetime = models.DateTimeField(editable=True,
                                                    auto_now=True)

    likes = models.IntegerField(default=0)

    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField(null=False, max_length=3000)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.comment}"


class File(models.Model):
    file = models.FileField(upload_to='user_files')
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.file}"
