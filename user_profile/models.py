"""user_profile models.py"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class Role(models.Model):
    """Role class"""
    STUDENT = 1
    LIBRARIAN = 2
    SUPERVISOR = 3
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (LIBRARIAN, 'teacher'),
        (SUPERVISOR, 'supervisor'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    """User class"""
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role)


class Profile(models.Model):
    """Profile class"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)

# @receiver(user_signed_up)
# def create_user_profile(**kwargs) -> None:
#     """Creating user profile after registration"""
#     profile = Profile(user=kwargs['user'])
#
#     if Profile.objects.filter(custom_url=kwargs['user'].username).exists():
#         profile.custom_url =\
#             kwargs['user'].username + \
#             str(len(Profile.objects.filter(
#                 custom_url=kwargs['user'].username)) + 1)
#
#     else:
#         profile.custom_url = kwargs['user'].username
#
#     profile.save()
