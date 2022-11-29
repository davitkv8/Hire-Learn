from django.contrib import admin
from users.models import HashTag, Image


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ("hashTag", )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image", )