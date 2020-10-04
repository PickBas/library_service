"""book views.py"""
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from book.models import Book
from book.forms import UploadBookForm, GiveBookForm


class StudentsPageView(View):
    """StudentsPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/students.html'
        self.context = {'page_name': 'Ученики'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing get request

        :param request: HttpRequest
        :return: render
        """

        all_users = User.objects.filter(profile__is_student=True)
        self.context['all_users'] = all_users

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

        book_form = UploadBookForm(request.POST)

        if book_form.is_valid():
            book = Book(in_use_by=None,
                        name=book_form.cleaned_data.get('name'),
                        info=book_form.cleaned_data.get('info'))
            book.save()
            return redirect(reverse('index_page'))

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

    def post(self, request: HttpRequest, **kwargs: dict):
        """
        Processing POST request. Giving a book back.

        :param request: HttpRequest
        :param kwargs: pk
        :returns: redirect
        """

        current_book = get_object_or_404(Book, id=kwargs['pk'])

        from_student = current_book.in_use_by

        from_student.profile.books_in_use.remove(current_book)

        if current_book.when_should_be_back > timezone.now() and \
                current_book not in from_student.profile.overdue_books.all():
            from_student.profile.overdue_books.add(current_book)

        from_student.save()

        current_book.in_use_by = None
        current_book.when_should_be_back = timezone.now()
        current_book.since_back = timezone.now()

        if from_student not in current_book.read_history.all():
            current_book.read_history.add(from_student)

        current_book.save()

        return redirect(reverse('book_page', kwargs={'pk': current_book.id}))


class GiveBookPageView(View):
    """GiveBookPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/give_a_book.html'
        self.context = {'page_name': 'Выписывание книги'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        :raises: 403, 404
        """

        if request.user.profile.is_student:
            raise PermissionDenied()

        current_book = get_object_or_404(Book, id=kwargs['pk'])
        students = User.objects.filter(profile__is_student=True)

        self.context['current_book'] = current_book
        self.context['students'] = students
        self.context['book_form'] = GiveBookForm()

        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, **kwargs: dict):
        """
        Processing POST request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: redirect, render
        :raises: 403, 404
        """

        if request.user.profile.is_student:
            raise PermissionDenied()

        current_book = get_object_or_404(Book, id=kwargs['pk'])

        librarian = request.user
        book_form = GiveBookForm(request.POST)

        if book_form.is_valid():
            current_book.when_should_be_back = book_form.cleaned_data.get('date_back')

            to_student = User.objects.get(id=book_form.cleaned_data.get('student'))
            to_student.profile.books_in_use.add(current_book)

            to_student.save()

            current_book.read_history.add(to_student)
            current_book.in_use_by = to_student
            current_book.save()

            librarian.profile.given_books_all_times.add(current_book)
            librarian.save()

            return redirect(reverse('index_page'))

        return self.get(request)
