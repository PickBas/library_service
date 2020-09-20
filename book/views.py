"""book views.py"""
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from book.models import Book
from book.forms import UploadBookForm


class BooksPageView(View):
    """BooksPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/books_list.html'
        self.context = {'page_name': 'Список книг в библиотеке'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :returns: render
        """

        return render(request, self.template_name, self.context)


class AddBookPageView(View):
    """AddBookPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/add_book_to_lib.html'
        self.context = {'page_name': 'Добавление книги'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :returns: render
        :raises: 403
        """

        if not request.user.profile.is_librarian:
            raise PermissionDenied()

        self.context['form'] = UploadBookForm()

        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest):
        """
        Processing POST request

        :param request: HttpRequest
        :returns: redirect
        :raises: 403
        """

        if not request.user.profile.is_librarian:
            raise PermissionDenied()

        book_form = UploadBookForm(request.POST, request.FILES)

        if book_form.is_valid():
            book = Book(file=book_form.cleaned_data.get('file'))
            book.save()
            return redirect(reverse('books_list_page'))

        print(request.FILES)
        return self.get(request)