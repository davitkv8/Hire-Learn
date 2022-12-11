import os
import django
from django.core.management import call_command

print_separate_line = lambda: print("-" * 50)


# configure django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HNL.settings")
django.setup()

call_command("makemigrations", interactive=False)
call_command("migrate", interactive=False)

from users.models import UserStatus
from django.contrib.auth.models import User
from users.models import *


for username in ["davit"]:

    try:
        user = User(username=username)
        user.set_password("123")
        user.is_superuser = True
        user.is_staff = True
        user.save()
    except django.db.utils.IntegrityError:
        print(f"User {username} already exists")


platforms_we_support = sorted(Platform.platform_choices)

for platform in platforms_we_support:
    Platform.objects.get_or_create(platform=platform[0])


# for user_status in ["teacher", "student"]:
#     UserStatus.objects.update_or_create(
#             userStatus=user_status,
#             defaults={
#                 "userStatus": user_status,
#             }
#         )

print("ALL PROCESSES ENDED SUCCESSFULLY")
