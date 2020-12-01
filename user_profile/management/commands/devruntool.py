"""
Management utility to create users for dev.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import Profile


class Command(BaseCommand):
    help = 'Creating test users'

    def handle(self, *args, **options):

        user_item = User.objects.create_user('librarian', 'librarian@librarian.librarian', 'asdf123!', first_name='librarian', last_name='librarian')

        user_item2 = User.objects.create_user('first_student', 'first_student@first_student.first_student', 'asdf123!', first_name='first_student', last_name='first_student')

        profile_item = Profile(user=user_item, is_librarian=True)
        profile_item2 = Profile(user=user_item2, is_student=True)

        profile_item2.save()
        user_item2.save()
        profile_item.save()
        user_item.save()
