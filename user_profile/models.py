"""user_profile models.py"""
from django.contrib.auth.models import User
from django.db import models

from book.models import Book


class Profile(models.Model):
    """Profile class"""

    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        (None, 'Не указано')
    )

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_sys_admin = models.BooleanField(default=False)

    base_image = models.ImageField(upload_to='avatars/', default='avatars/0.jpg')
    image = models.ImageField(upload_to='avatars/', default='avatars/0.jpg')

    birth = models.DateField(null=True)
    show_email = models.BooleanField(default=False)

    given_books_all_times = models.ManyToManyField(Book, related_name='given_books')

    books_in_use = models.ManyToManyField(Book, related_name='books_in_use')

    def get_profile_name(self) -> str:
        """
        Getting full name of a user

        :returns: str
        """

        if not self.user.first_name and not self.user.last_name:
            return self.user.username

        if self.user.first_name and self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name\
                   + ' (' + self.user.username + ')'

        if self.user.first_name:
            return self.user.first_name + ' (' + self.user.username + ')'

        return self.user.last_name + ' (' + self.user.username + ')'
