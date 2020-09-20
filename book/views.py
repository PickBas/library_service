"""book views.py"""
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View

from book.models import Book
from book.forms import UploadBookForm


class BookListPageView(View):
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

        self.context['books'] = Book.objects.all()

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
            book = Book(file=request.FILES['file'],
                        in_use_by=None,
                        name=book_form.cleaned_data.get('name'))
            book.save()
            return redirect(reverse('books_list_page'))

        return self.get(request)


class BookPageView(View):
    """BookPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'book/book_main_page.html'
        self.context = {}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        """

        current_book = get_object_or_404(Book, id=kwargs['pk'])

        self.context['page_name'] = current_book.name
        self.context['current_book'] = current_book

        return render(request, self.template_name, self.context)
