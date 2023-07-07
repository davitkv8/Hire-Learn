import os
import django
from django.core.management import call_command
from django.conf import settings

print_separate_line = lambda: print("-" * 50)

# configure django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HNL.settings")
django.setup()

from users.models import *

call_command("makemigrations", interactive=False)
call_command("migrate", interactive=False)

for i in settings.INSTALLED_APPS:
    if ".apps." in i:
        i = i.split(".")[0]
        try:
            call_command("makemigrations", i, interactive=False)
            call_command("migrate", app_label=i, interactive=False)
        except django.core.management.base.CommandError:
            print(i, "Does not have migrations")


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

print("ALL PROCESSES ENDED SUCCESSFULLY!")
