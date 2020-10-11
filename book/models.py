"""book models.py"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Book(models.Model):
    """Book class"""

    name = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    in_use_by = models.ForeignKey(to=User,
                                  on_delete=models.CASCADE,
                                  related_name='current_book_user',
                                  null=True)

    read_history = models.ManyToManyField(User)

    since_given = models.DateTimeField(default=timezone.now)
    since_back = models.DateTimeField(default=timezone.now)
    upload_time = models.DateTimeField(default=timezone.now)
    when_should_be_back = models.DateTimeField(default=timezone.now)


class BookInfo(models.Model):
    """BookInfo class. Used for getting statistics of librarians"""

    book = models.ForeignKey(to=Book,
                                  on_delete=models.CASCADE,
                                  related_name='given_book',
                                  null=True)
    librarian = models.ForeignKey(to=User,
                                  on_delete=models.CASCADE,
                                  related_name='librarian_who_gave_the_book',
                                  null=True)

    student = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,
                                related_name='student_who_received_the_book',
                                null=True)

    date_giving_book = models.DateTimeField(default=timezone.now)
    date_term = models.IntegerField(default=0)
