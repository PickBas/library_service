"""book tests.py"""
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from book.forms import GiveBookForm

IDS = {
    'librarian_id': 1,
    'student_id': 2
}


class LibraryViewTest(TestCase):
    """LibraryViewTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(id=IDS['librarian_id'])
        self.client.force_login(user=self.current_user)

    def test_page_loads(self) -> None:
        """Testing if library page loads"""

        response = self.client.get(reverse("index_page"))
        self.assertEquals(200, response.status_code)


class BookTest(TestCase):
    """BookTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(id=IDS['librarian_id'])
        self.client.force_login(user=self.current_user)

    def test_add_book_page_loads(self) -> None:
        """Testing if add_book_to_lib page loads"""

        response = self.client.get(reverse('add_book_to_lib'))
        self.assertEquals(200, response.status_code)

    def test_book_upload(self) -> None:
        """Testing if it is possible to upload a book"""

        data = {
            'name': 'test',
            'info': 'info about the book'
        }

        response = self.client.post(reverse('add_book_to_lib'), data)
        self.assertEquals(302, response.status_code)


class StudentsListTestCase(TestCase):
    """StudentsListTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(id=IDS['librarian_id'])
        self.client.force_login(user=self.current_user)

    def test_student_list_page_loads(self) -> None:
        """Testing if the students list page loads"""

        response = self.client.get(reverse('all_students_page'))

        self.assertEquals(200, response.status_code)


class GiveBookTestCase(TestCase):
    """GiveBookTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(id=IDS['librarian_id'])
        self.client.force_login(user=self.current_user)

    def test_book_giving(self) -> None:
        """Testing if a librarian can give a book to a student"""

        data = {
            'name': 'test',
            'info': 'info about the book'
        }

        self.client.post(reverse('add_book_to_lib'), data)

        data = {
            'student': User.objects.get(id=IDS['student_id']),
            'date_back': datetime.today()
        }

        response = self.client.post(reverse('give_book_page', kwargs={'pk': 2}),
                                    data)

        self.assertEquals(302, response.status_code)
