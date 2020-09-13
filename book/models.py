"""book models.py"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Book(models.Model):
    """Book class"""
    name = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='books')
    in_use_by = models.OneToOneField(to=User,
                                     on_delete=models.CASCADE,
                                     related_name='current_book_user')
    since_given = models.DateTimeField(default=timezone.now)
    since_back = models.DateTimeField(default=timezone.now)
