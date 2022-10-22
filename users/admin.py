from django.contrib import admin
from users.models import HashTag

@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ("hashTag", )

