"""book models.py"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Book(models.Model):
    """Book class"""

    name = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    in_use_by = models.OneToOneField(to=User,
                                     on_delete=models.CASCADE,
                                     related_name='current_book_user',
                                     null=True)

    read_history = models.ManyToManyField(User)

    since_given = models.DateTimeField(default=timezone.now)
    since_back = models.DateTimeField(default=timezone.now)
    upload_time = models.DateTimeField(default=timezone.now)
