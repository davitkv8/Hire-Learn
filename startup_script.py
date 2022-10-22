import os
import django
from users.models import UserStatus

print_separate_line = lambda: print("-" * 50)


# configure django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()


for user_status in ["teacher", "student"]:
    UserStatus.objects.update_or_create(
            userStatus=user_status,
            defaults={
                "userStatus": user_status,
            }
        )
