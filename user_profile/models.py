"""user_profile models.py"""
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


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

    base_image = models.ImageField(upload_to='avatars/', default='avatars/0.png')
    image = models.ImageField(upload_to='avatars/', default='avatars/0.png')

    birth = models.DateField(null=True)
    show_email = models.BooleanField(default=False)

    roles = models.ManyToManyField(Role)


@receiver(user_signed_up)
def create_user_profile(**kwargs: dict) -> None:
    """Creating user profile after registration"""
    profile = Profile(user=kwargs['user'])
    profile.save()
