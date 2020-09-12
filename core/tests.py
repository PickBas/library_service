"""core tests.py"""

from django.test import TestCase, Client


class IndexViewTestCase(TestCase):
    """IndexViewTestCase class"""
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')

    def test_page(self):
        """Testing if page loads"""
        self.assertEqual(self.response.status_code, 200)
