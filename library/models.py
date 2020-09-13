"""library models.py"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from book.models import Book


class Library(models.Model):
    """Library class"""
    name = models.CharField(max_length=100, blank=None)
    given_books_all_times_count = models.IntegerField(default=0)
    given_books_at_the_moment = models.IntegerField(default=0)
    books = models.ManyToManyField(Book, related_name='books')
    librarians = models.ManyToManyField(User, related_name='librarians')

    def give_book_to_student(self,
                             student: User,
                             librarian: User,
                             book_id: int) -> None:
        """Student borrows a book"""

        book = Book.objects.get(id=book_id)

        self.given_books_all_times_count += 1
        self.given_books_at_the_moment += 1

        student.profile.books_in_use.add(book)
        librarian.profile.given_books_all_times.add(book)

        self.books.remove(book)

        student.save()
        librarian.save()
        self.save()

        book.in_use_by = student
        book.since_given = timezone.now
        book.save()

    def get_book_back(self, student: User, book_id: int) -> None:
        """Student gives the book back"""

        if not self.given_books_at_the_moment:
            return

        book = Book.objects.get(id=book_id)
        self.given_books_at_the_moment -= 1

        self.books.add(book)
        self.save()

        student.profile.books_in_use.remove(book)
        student.save()

        book.in_use_by = None
        book.since_given = None
        book.since_back = timezone.now
        book.save()




