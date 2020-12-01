"""book tests.py"""

from django.contrib.auth.models import User
from django.db import models
from django.test import Client
from django.urls import reverse

from book.models import Book
from user_profile.tests import AbsTestCase

LIBRARIAN_USERNAME = 'SecondUserTestLibrarian'
STUDENT_USERNAME = 'FirstUserTestStudent'
ADMIN_USERNAME = 'ThirdUserAdmin'


class LibraryViewTest(AbsTestCase):
    """LibraryViewTest class"""

    def test_page_loads(self) -> None:
        """Testing if library page loads"""

        response = self.client_librarian.get(reverse("index_page"))
        self.assertEqual(200, response.status_code)


class BookPageTestCase(AbsTestCase):
    """BookPageTestCase class"""

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        data = {
            'name': 'testBookPage',
            'info': 'info about the book'
        }

        self.client_librarian.post(reverse('add_book_post'), data)
        self.current_book = Book.objects.get(name='testBookPage')

    def test_book_page_loads_librarian(self) -> None:
        """Testing if book_page loads for a librarian"""

        response = self.client_librarian.get(reverse('book_page',
                                                     kwargs={'pk': self.current_book.id}))

        self.assertEqual(200, response.status_code)

    def test_book_page_loads_student(self) -> None:
        """Testing if book_page loads for a student"""

        client = Client()
        client.force_login(user=User.objects.get(username=STUDENT_USERNAME))

        response = client.get(reverse('book_page', kwargs={'pk': self.current_book.id}))

        self.assertEqual(200, response.status_code)


class UploadBookTestCase(AbsTestCase):
    """UploadBookTestCase class"""

    def test_book_upload(self) -> None:
        """Testing if it is possible to upload a book"""

        data = {
            'name': 'test',
            'info': 'info about the book'
        }

        response = self.client_librarian.post(reverse('add_book_post'), data)
        self.assertEqual(200, response.status_code)

    def test_book_upload_student(self) -> None:
        """Testing if it is possible to upload a book for a student"""

        data = {
            'name': 'test',
            'info': 'info about the book'
        }

        response = self.client_student.post(reverse('add_book_post'), data)
        self.assertEqual(403, response.status_code)


class StudentsListTestCase(AbsTestCase):
    """StudentsListTestCase class"""

    def test_student_list_page_loads(self) -> None:
        """Testing if the students list page loads"""

        response = self.client_librarian.get(reverse('all_students_page'))

        self.assertEqual(200, response.status_code)

    def test_student_list_page_loads_for_students(self) -> None:
        """Testing if the students list page loads"""

        response = self.client_student.get(reverse('all_students_page'))
        self.assertEqual(403, response.status_code)


class LibrariansListTestCase(AbsTestCase):
    """LibrariansListTestCase class"""

    def test_student_list_page_loads(self) -> None:
        """Testing if the librarians list page loads"""

        response = self.client_student.get(reverse('all_librarians_page'))
        self.assertEqual(403, response.status_code)

    def test_student_list_page_loads_for_students(self) -> None:
        """Testing if the students list page loads"""

        response = self.client_student.get(reverse('all_students_page'))
        self.assertEqual(403, response.status_code)

    def test_student_list_page_loads_for_admins(self) -> None:
        """Testing if the students list page loads"""

        response = self.client_admin.get(reverse('all_students_page'))
        self.assertEqual(200, response.status_code)


class GiveBookTestCase(AbsTestCase):
    """GiveBookTestCase class"""

    def setUp(self):
        """Setting up the TestCase"""

        super().setUp()

        data = {
            'name': 'TestBookGivingBook',
            'info': 'info about the book2'
        }

        self.client_librarian.post(reverse('add_book_post'), data)
        self.current_book = Book.objects.get(name='TestBookGivingBook')

    def test_book_giving(self) -> None:
        """Testing if it's possible to give a book"""

        data = {
            'student_id': str(self.current_user_student.id),
            'to_date': '2021-01-01'
        }

        response = self.client_librarian.post(reverse('give_book_post',
                                                      kwargs={'pk': self.current_book.id}),
                                              data)
        self.assertEqual(200, response.status_code)


class UpdateBookTestCase(AbsTestCase):
    """UpdateBookTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        data = {
            'name': 'testUpdateBook',
            'info': 'info about the book'
        }

        self.client_librarian.post(reverse('add_book_post'), data)
        self.current_book = Book.objects.get(name='testUpdateBook')

    def test_update_book_page_loads(self) -> None:
        """Testing if edit_book_page loads"""

        response = self.client_librarian.get(reverse('edit_book_page',
                                                     kwargs={'pk': self.current_book.id}))
        self.assertEqual(200, response.status_code)

    def test_update_page_loads_for_students(self) -> None:
        """Testing if edit_book_page raises 404 for students"""

        response = self.client_student.get(reverse('edit_book_page',
                                                   kwargs={'pk': self.current_book.id}))
        self.assertEqual(404, response.status_code)

    def test_update_book(self) -> None:
        """Testing if it's possible to edit the book's information"""

        data = {
            'name': 'testUpdateBook',
            'info': 'updated information'
        }

        response = self.client_librarian.post(reverse('edit_book_page',
                                                      kwargs={'pk': self.current_book.id}),
                                              data)

        book = Book.objects.get(id=self.current_book.id)

        self.assertEqual(302, response.status_code)
        self.assertEqual('updated information', book.info)

    def test_update_book_from_student(self) -> None:
        """Testing if it's possible to edit a book for a student"""

        data = {
            'name': 'testUpdateBook',
            'info': 'updated information'
        }

        response = self.client_student.post(reverse('edit_book_page',
                                                    kwargs={'pk': self.current_book.id}),
                                            data)
        self.assertEqual(404, response.status_code)


class DeletionBookTestCase(AbsTestCase):
    """DeletionBookTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        data = {
            'name': 'testBookDeletion',
            'info': 'info about the book'
        }

        self.client_librarian.post(reverse('add_book_post'), data)
        self.current_book = Book.objects.get(name='testBookDeletion')

    def test_book_deletion_librarian(self) -> None:
        """Testing if it's possible to delete a book for a librarian"""

        response = self.client_librarian.get(reverse('delete_book',
                                                     kwargs={'pk': self.current_book.id}))

        self.assertEqual(302, response.status_code)

        with self.assertRaises(models.ObjectDoesNotExist):
            Book.objects.get(id=self.current_book.id)

    def test_book_deletion_student(self) -> None:
        """Testing if it's possible to delete a book for a student"""

        response = self.client_student.get(reverse('delete_book',
                                                   kwargs={'pk': self.current_book.id}))

        self.assertEqual(403, response.status_code)
