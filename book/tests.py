"""book tests.py"""

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from book.models import Book


class LibraryViewTest(TestCase):
    """LibraryViewTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(username='SecondUserTestLibrarian')
        self.client.force_login(user=self.current_user)

    def test_page_loads(self) -> None:
        """Testing if library page loads"""

        response = self.client.get(reverse("index_page"))
        self.assertEqual(200, response.status_code)


class BookTest(TestCase):
    """BookTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(username='SecondUserTestLibrarian')
        self.client.force_login(user=self.current_user)

    def test_add_book_page_loads(self) -> None:
        """Testing if add_book_to_lib page loads"""

        response = self.client.get(reverse('add_book_to_lib'))
        self.assertEqual(200, response.status_code)

    def test_book_upload(self) -> None:
        """Testing if it is possible to upload a book"""

        data = {
            'name': 'test',
            'info': 'info about the book'
        }

        response = self.client.post(reverse('add_book_to_lib'), data)
        self.assertEqual(302, response.status_code)


class StudentsListTestCase(TestCase):
    """StudentsListTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(username='SecondUserTestLibrarian')
        self.client.force_login(user=self.current_user)

    def test_student_list_page_loads(self) -> None:
        """Testing if the students list page loads"""

        response = self.client.get(reverse('all_students_page'))

        self.assertEqual(200, response.status_code)


class GiveBookTestCase(TestCase):
    """GiveBookTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(username='SecondUserTestLibrarian')
        self.client.force_login(user=self.current_user)

    def test_book_giving_page_loads(self) -> None:
        """Testing page load"""

        data = {
            'name': 'test2',
            'info': 'info about the book2'
        }

        self.client.post(reverse('add_book_to_lib'), data)

        current_book = Book.objects.get(name='test2')

        response = self.client.get(reverse('give_book_page', kwargs={'pk': current_book.id}))

        self.assertEqual(200, response.status_code)


class UpdateBookTestCase(TestCase):
    """UpdateBookTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(username='SecondUserTestLibrarian')
        self.client.force_login(user=self.current_user)

        data = {
            'name': 'testUpdateBook',
            'info': 'info about the book'
        }

        self.client.post(reverse('add_book_to_lib'), data)
        self.current_book = Book.objects.get(name='testUpdateBook')

    def test_update_book_page_loads(self) -> None:
        """Testing if edit_book_page loads"""

        response = self.client.get(reverse('edit_book_page',
                                           kwargs={'pk': self.current_book.id}))
        self.assertEqual(200, response.status_code)

    def test_update_page_loads_for_students(self) -> None:
        """Testing if edit_book_page raises 404 for students"""

        client = Client()
        client.force_login(user=User.objects.get(username='FirstUserTestStudent'))

        response = client.get(reverse('edit_book_page',
                                      kwargs={'pk': self.current_book.id}))
        self.assertEqual(404, response.status_code)

    def test_update_book(self) -> None:
        """Testing if it's possible to edit the book's information"""

        data = {
            'name': 'testUpdateBook',
            'info': 'updated information'
        }

        response = self.client.post(reverse('edit_book_page',
                                            kwargs={'pk': self.current_book.id}),
                                    data)

        book = Book.objects.get(id=self.current_book.id)

        self.assertEqual(302, response.status_code)
        self.assertEqual('updated information', book.info)

    def test_update_book_from_student(self) -> None:
        """Testing if it's possible to edit a book for a student"""

        client = Client()
        client.force_login(user=User.objects.get(username='FirstUserTestStudent'))

        data = {
            'name': 'testUpdateBook',
            'info': 'updated information'
        }

        response = client.post(reverse('edit_book_page',
                                       kwargs={'pk': self.current_book.id}),
                               data)
        self.assertEqual(404, response.status_code)
