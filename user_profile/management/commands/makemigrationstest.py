"""
Management utility to create fixtures for tests.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import os

from user_profile.models import Profile


class Command(BaseCommand):
    help = 'Custom migrations creating'

    def handle(self, *args, **options):
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")

        user_item = User.objects.create_user('FirstUserTestStudent', 'FirstUserTest@FirstUserTest.FirstUserTest', 'asdf123!')

        user_item2 = User.objects.create_user('SecondUserTestLibrarian', 'SecondUserTest@SecondUserTest.SecondUserTest', 'asdf123!')

        profile_item = Profile(user=user_item, is_student=True)
        profile_item2 = Profile(user=user_item2, is_librarian=True)

        profile_item2.save()
        user_item2.save()
        profile_item.save()
        user_item.save()
        os.system(
            "python manage.py dumpdata --indent 2 --exclude=contenttypes --exclude=auth.permission > fixtures/test_db.json")