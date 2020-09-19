"""user_profile tests.py"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from user_profile.forms import UserUpdateForm, ProfileUpdateForm


class LoginTest(TestCase):
    """LoginTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        self.client = Client()
        super(LoginTest, self).setUp()

    def test_page_loads(self) -> None:
        """Testing if login page loads"""

        response = self.client.get(reverse("account_login"))
        self.assertEquals(200, response.status_code)

    def test_login_with_wrong_credentials(self) -> None:
        """Testing if
            it is possible to login with wrong credentials"""

        data_to_send = {
            'login': 'FirstUserTestStudent',
            'password': 'asdf1233!',
            'remember': 'false'
        }

        response = self.client.post(reverse('account_login'),
                                    data=data_to_send)
        self.assertEquals(200, response.status_code)

    def test_login_with_valid_credentials(self) -> None:
        """Testing if
            it is possible to login with valid credentials"""

        data_to_send = {
            'login': 'FirstUserTestStudent',
            'password': 'asdf123!',
            'remember': 'false'
        }

        response = self.client.post(reverse('account_login'),
                                    data=data_to_send, follow=True)
        self.assertEquals(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)


class RegistrationTest(TestCase):
    """RegistrationTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        self.client = Client()
        super(RegistrationTest, self).setUp()

    def test_signup_page_loads(self) -> None:
        """Testing if sign up page loads"""

        response = self.client.get(reverse('account_signup'))
        self.assertEquals(200, response.status_code)

    def test_registering(self) -> None:
        """Testing if it is possible to register"""

        data_to_send = {
            'email': 'test@email.com',
            'username': 'test',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'password1': 'asdf123!',
            'password2': 'asdf123!',
        }

        response = self.client.post(reverse('account_signup'),
                                    data=data_to_send, follow=True)
        self.assertEquals(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)

    def test_registering_with_existent_credentials(self) -> None:
        """Testing if
            a user is allowed to register with the same credentials twice"""

        data_to_send = {
            'email': 'FirstUserTest@FirstUserTest.FirstUserTest',
            'username': 'FirstUserTestStudent',
            'password1': 'asdf123!',
            'password2': 'asdf123!',
        }

        response = self.client.post(reverse('account_signup'),
                                    data=data_to_send, follow=True)
        self.assertEquals(200, response.status_code)
        self.assertNotIn(('/', 302), response.redirect_chain)


class ProfileEditTest(TestCase):
    """class ProfileEditTest"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up ProfileEditTest"""
        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(id=1)
        self.client.force_login(user=self.current_user)

    def test_forms(self) -> None:
        """
        Testing forms validation

        :returns: None
        """

        f_user_update_data = {'first_name': 'test', 'last_name': 'usertest'}
        user_update_form = UserUpdateForm(f_user_update_data, instance=self.current_user)
        self.assertTrue(user_update_form.is_valid())

        f_profile_data = {
            'show_email': True
        }
        profile_update_form = ProfileUpdateForm(f_profile_data, instance=self.current_user.profile)
        self.assertTrue(profile_update_form.is_valid())

    def test_changing_data(self) -> None:
        """
        Testing if it's possible to change the profile data

        :returns: None
        """

        form_user_update_data = {'first_name': 'test', 'last_name': 'usertest'}
        form_profile_data = {
            'show_email': True
        }

        response = self.client.post(reverse('update_profile_info'), {
                                        **form_user_update_data,
                                        **form_profile_data,
                                    })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(id=1).profile.show_email, form_profile_data['show_email'])
        self.assertEqual(User.objects.get(id=1).last_name, form_user_update_data['last_name'])
