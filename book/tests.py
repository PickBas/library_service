"""book tests.py"""
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse


class LibraryViewTest(TestCase):
    """LibraryViewTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(id=1)
        self.client.force_login(user=self.current_user)

    def test_page_loads(self) -> None:
        """Testing if library page loads"""

        response = self.client.get(reverse("books_list_page"))
        self.assertEquals(200, response.status_code)


class BookTest(TestCase):
    """BookTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        super().setUp()

        self.client = Client()
        self.current_user = User.objects.get(id=2)
        self.client.force_login(user=self.current_user)

    def test_add_book_page_loads(self) -> None:
        """Testing if add_book_to_lib page loads"""

        response = self.client.get(reverse('add_book_to_lib'))
        self.assertEquals(200, response.status_code)

    def test_book_upload(self) -> None:
        """Testing if it is possible to upload a book"""

        data = {
            'name': 'test',
            'file': SimpleUploadedFile('test.pdf', b'test')
        }

        response = self.client.post(reverse('add_book_to_lib'), data)
        self.assertEquals(302, response.status_code)
