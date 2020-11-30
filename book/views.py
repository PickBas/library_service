"""book views.py"""
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from book.forms import EditBookForm
from book.models import Book, BookInfo


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

        if request.user.profile.is_student:
            raise PermissionDenied()

        all_users = User.objects.filter(profile__is_student=True)
        self.context['all_users'] = all_users

        return render(request, self.template_name, self.context)


class LibrariansPageView(View):
    """LibrariansPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/librarians.html'
        self.context = {'page_name': 'Библиотекари'}
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing get request

        :param request: HttpRequest
        :return: render
        """

        if not request.user.is_superuser:
            raise PermissionDenied()

        all_users = User.objects.filter(profile__is_librarian=True)
        self.context['all_users'] = all_users

        return render(request, self.template_name, self.context)


class AddBookView(View):
    """AddBookView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/table_of_books.html'
        self.name = ''
        self.info = ''
        self.context = {}
        super().__init__(**kwargs)

    def post(self, request: HttpRequest) -> render:
        """
        Processing POST request

        :param request: HttpRequest
        :returns: redirect
        :raises: 403, 404
        """

        self.name = request.POST.get('name')
        self.info = request.POST.get('info')

        self.validate_request(request)

        Book(in_use_by=None,
             name=request.POST.get('name'),
             info=request.POST.get('name')).save()

        self.context['books'] = Book.objects.all()
        self.context['page_name'] = 'Список книг'

        return render(request, self.template_name, self.context)

    def validate_request(self, request: HttpRequest):
        """
        Validating POST request
        :param request: HttpRequest
        """

        if not request.user.profile.is_librarian:
            raise PermissionDenied()
        if not self.name or not self.info:
            raise Http404()


class BookPageView(View):
    """BookPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'book/book_main_page.html'
        self.context = {}
        self.current_book = None
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
        self.context['students'] = User.objects.filter(profile__is_student=True)

        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, **kwargs: dict):
        """
        Processing POST request
            Retrieving a book

        :param request: HttpRequest
        :param kwargs: pk
        :returns: redirect
        """

        self.current_book = get_object_or_404(Book, id=kwargs['pk'])

        from_student = self.current_book.in_use_by

        from_student.profile.books_in_use.remove(self.current_book)

        if self.current_book.when_should_be_back < timezone.now() and \
                self.current_book not in from_student.profile.overdue_books.all():
            from_student.profile.overdue_books.add(self.current_book)

        if self.current_book.when_should_be_back >= timezone.now() and \
                self.current_book in from_student.profile.overdue_books.all():
            from_student.profile.overdue_books.remove(self.current_book)

        from_student.save()

        self.current_book.in_use_by = None
        self.current_book.when_should_be_back = timezone.now()
        self.current_book.since_back = timezone.now()

        if from_student not in self.current_book.read_history.all():
            self.current_book.read_history.add(from_student)

        self.current_book.save()

        return redirect(reverse('book_page', kwargs={'pk': self.current_book.id}))


class GiveBookView(View):
    """GiveBookView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'book/book_main_page_data.html'
        self.context = {}
        self.current_book = None
        self.librarian = None
        self.student = None
        super().__init__(**kwargs)

    def post(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing POST request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        :raises: 403, 404
        """

        self.current_book = get_object_or_404(Book, id=kwargs['pk'])
        self.student = get_object_or_404(User, id=request.POST.get('student_id'))
        self.librarian = request.user

        self.validate_post_request(request)

        self.current_book.when_should_be_back = request.POST.get('to_date')
        self.student.profile.books_in_use.add(self.current_book)
        self.student.save()

        if self.student not in self.current_book.read_history.all():
            self.current_book.read_history.add(self.student)

        self.current_book.in_use_by = self.student
        self.current_book.save()
        self.save_book_info(datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d'))

        if self.current_book not in self.librarian.profile.given_books_all_times.all():
            self.librarian.profile.given_books_all_times.add(self.current_book)
            self.librarian.save()

        self.fill_context()

        return render(request, self.template_name, self.context)

    def save_book_info(self, date: datetime):
        """Saving information about book giving"""

        BookInfo.objects.create(
            book=self.current_book,
            librarian=self.librarian,
            student=self.student,
            date_term=(abs((date - datetime.today()).days))
        ).save()

    def fill_context(self):
        """Filling context"""

        self.context['students'] = User.objects.filter(profile__is_student=True)
        self.context['page_name'] = self.current_book.name
        self.context['current_book'] = self.current_book

    def validate_post_request(self, request: HttpRequest):
        """
        Validating POST request.

        :param request: HttpRequest
        :raises: 404, 403
        """

        if request.user.profile.is_student:
            raise PermissionDenied()
        if self.current_book in self.student.profile.books_in_use.all():
            raise Http404()
        if datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d') <= datetime.now():
            raise Http404()


class EditBookPageView(View):
    """EditBookPageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'book/edit_book.html'
        self.context = {'page_name': 'Редактирование книги'}
        self.current_book = None
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        :raises: 404
        """

        if not request.user.profile.is_librarian:
            raise Http404()

        self.current_book = Book.objects.get(id=kwargs['pk'])
        book_edit_form = EditBookForm(instance=self.current_book)

        self.context['current_book'] = self.current_book
        self.context['form'] = book_edit_form

        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, **kwargs: dict):
        """
        Processing POST request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render, redirect
        :raises: 404
        """

        if not request.user.profile.is_librarian:
            raise Http404()

        self.current_book = Book.objects.get(id=kwargs['pk'])
        book_edit_form = EditBookForm(request.POST, instance=self.current_book)

        if book_edit_form.is_valid():

            if not len(book_edit_form.cleaned_data.get('name')) > 0 \
                    and not len(book_edit_form.cleaned_data.get('info')) > 0:
                return redirect(reverse('book_page', kwargs={'pk': self.current_book.id}))

            self.current_book.name = book_edit_form.cleaned_data.get('name')
            self.current_book.info = book_edit_form.cleaned_data.get('info')

            self.current_book.save()
            return redirect(reverse('book_page', kwargs={'pk': self.current_book.id}))

        return self.get(request, **kwargs)


class DeleteBookView(View):
    """DeleteBookView class"""

    def __init__(self, **kwargs: dict):
        self.current_book = None
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> redirect:
        """
        Processing GET request. Deleting a book

        :param request: HttpRequest
        :param kwargs: pk
        :returns: redirect
        :raises: 403
        """

        if not request.user.profile.is_librarian:
            raise PermissionDenied()

        self.current_book = Book.objects.get(id=kwargs['pk'])

        if self.current_book.in_use_by is not None:
            raise Http404()

        self.current_book.delete()
        return redirect(reverse('index_page'))
