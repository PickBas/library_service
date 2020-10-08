"""user_profile tests.py"""
import os
from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from library_service.settings import BASE_DIR
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
        self.assertEqual(200, response.status_code)

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
        self.assertEqual(200, response.status_code)

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
        self.assertEqual(200, response.status_code)
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
        self.assertEqual(200, response.status_code)

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
        self.assertEqual(200, response.status_code)
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
        self.assertEqual(200, response.status_code)
        self.assertNotIn(('/', 302), response.redirect_chain)


class ProfileEditTest(TestCase):
    """class ProfileEditTest"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up ProfileEditTest"""
        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(username='FirstUserTestStudent')
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
            'birth': datetime.now()
        }
        profile_update_form = ProfileUpdateForm(f_profile_data, instance=self.current_user.profile)
        self.assertTrue(profile_update_form.is_valid())

    def test_changing_data(self) -> None:
        """
        Testing if it's possible to change the profile data

        :returns: None
        """

        form_user_update_data = {'first_name': 'test', 'last_name': 'usertest'}

        response = self.client.post(reverse('update_profile_info'), {
            **form_user_update_data,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username='FirstUserTestStudent').last_name,
                         form_user_update_data['last_name'])

    def test_avatar_upload(self) -> None:
        """Testing if it's possible to upload an avatar"""

        x_position = 0
        y_position = 0
        width = 1915
        height = 1915

        photo = Image.open(os.path.join(BASE_DIR, 'media/avatars/0.jpg'))

        to_send_image = {
            'base_image': photo,
        }

        to_send_cropper = {
            'x': x_position,
            'y': y_position,
            'width': width,
            'height': height,
        }

        response = self.client.post(reverse('update_profile_avatar'), {
            **to_send_image,
            **to_send_cropper,

        })

        self.assertEqual(response.status_code, 302)
