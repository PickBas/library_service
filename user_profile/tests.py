"""user_profile tests.py"""
from django.test import TestCase, Client
from django.urls import reverse


class LoginTest(TestCase):
    """LoginTest class"""

    def setUp(self) -> None:
        self.client = Client()

    def test_page_loads(self) -> None:
        """Testing if login page loads"""
        response = self.client.get(reverse("account_login"))
        self.assertEquals(200, response.status_code)
