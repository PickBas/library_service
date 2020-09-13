"""user_profile models.py"""
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Profile(models.Model):
    """Profile class"""

    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        (None, 'Не указано')
    )

    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='user')
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_sys_admin = models.BooleanField(default=False)

    base_image = models.ImageField(upload_to='avatars/', default='avatars/0.png')
    image = models.ImageField(upload_to='avatars/', default='avatars/0.png')

    birth = models.DateField(null=True)
    show_email = models.BooleanField(default=False)


@receiver(user_signed_up)
def create_user_profile(**kwargs: dict) -> None:
    """Creating user profile after registration"""
    profile = Profile(user=kwargs['user'])
    profile.save()
