import os
import django

print_separate_line = lambda: print("-" * 50)


# configure django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HNL.settings")
django.setup()

from users.models import UserStatus
from django.contrib.auth.models import User


for username in ["davit"]:

    try:
        user = User(username=username)
        user.set_password("123")
        user.is_superuser = True
        user.is_staff = True
        user.save()
    except django.db.utils.IntegrityError:
        print(f"User {username} already exists")


# for user_status in ["teacher", "student"]:
#     UserStatus.objects.update_or_create(
#             userStatus=user_status,
#             defaults={
#                 "userStatus": user_status,
#             }
#         )

print("ALL PROCESSES ENDED SUCCESSFULLY")
