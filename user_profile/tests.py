"""user_profile tests.py"""
import os
from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from library_service.settings import BASE_DIR, LIBRARIAN_KEY
from user_profile.forms import UserUpdateForm, ProfileUpdateForm
from user_profile.models import Profile

LIBRARIAN_USERNAME = 'SecondUserTestLibrarian'
STUDENT_USERNAME = 'FirstUserTestStudent'


def create_user(username: str, email: str) -> User:
    """
    Creating user

    :param username: str
    :param email: str
    :returns: User
    """

    student_different = User.objects.create(username=username,
                                            email=email,
                                            password='asdf123!')
    student_different_profile = Profile(user=student_different, is_student=True)
    student_different_profile.save()
    student_different.save()

    return student_different


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
            'login': STUDENT_USERNAME,
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
            'login': STUDENT_USERNAME,
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

    def test_registering_librarian(self) -> None:
        """Testing registration for librarians"""

        data_to_send = {
            'email': 'test@email.com',
            'username': 'testLibrarianRegistration',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'password1': 'asdf123!',
            'password2': 'asdf123!',
            'invite_key': LIBRARIAN_KEY
        }

        response = self.client.post(reverse('account_signup'),
                                    data=data_to_send, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)

        librarian_item = User.objects.get(username='testLibrarianRegistration')
        self.assertTrue(librarian_item.is_staff)

    def test_registering_with_existent_credentials(self) -> None:
        """Testing if
            a user is allowed to register with the same credentials twice"""

        data_to_send = {
            'email': 'FirstUserTest@FirstUserTest.FirstUserTest',
            'username': STUDENT_USERNAME,
            'password1': 'asdf123!',
            'password2': 'asdf123!',
        }

        response = self.client.post(reverse('account_signup'),
                                    data=data_to_send, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertNotIn(('/', 302), response.redirect_chain)


class PasswordChangingTest(TestCase):
    """class PasswordChangingTest"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        self.client_student = Client()
        self.client_librarian = Client()

        self.current_user_student = User.objects.get(username=STUDENT_USERNAME)
        self.current_user_librarian = User.objects.get(username=LIBRARIAN_USERNAME)

        self.client_student.force_login(user=self.current_user_student)
        self.client_librarian.force_login(user=self.current_user_librarian)

        super().setUp()

    def test_student_password_update(self) -> None:
        """Testing if a student can change his password"""

        data = {
            'oldpassword': 'asdf123!',
            'password1': 'qwer123!',
            'password2': 'qwer123!'
        }

        response = self.client_student.post(reverse("account_change_password"), data)
        self.assertEqual(302, response.status_code)

        data = {
            'login': self.current_user_student.username,
            'password': 'qwer123!',
            'remember': 'false'
        }

        response = self.client.post(reverse('account_login'),
                                    data=data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)


class ProfileEditTest(TestCase):
    """class ProfileEditTest"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up ProfileEditTest"""

        super().setUp()
        self.client = Client()
        self.current_user = User.objects.get(username=STUDENT_USERNAME)
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

    def test_changing_data_page_loads(self) -> None:
        """Testing if the page loads"""

        response = self.client.get(reverse('update_profile_info'))

        self.assertEqual(200, response.status_code)

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
        self.assertEqual(User.objects.get(username=STUDENT_USERNAME).last_name,
                         form_user_update_data['last_name'])

    def test_avatar_upload_page_loads(self) -> None:
        """Testing if the page loads"""

        response = self.client.get(reverse('update_profile_avatar'))

        self.assertEqual(200, response.status_code)

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


class ProfileMainPageTestCase(TestCase):
    """ProfileMainPageTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up ProfileEditTest"""

        super().setUp()
        self.client_student = Client()
        self.client_librarian = Client()

        self.current_user_librarian = User.objects.get(username=LIBRARIAN_USERNAME)
        self.current_user_student = User.objects.get(username=STUDENT_USERNAME)

        self.client_librarian.force_login(user=self.current_user_librarian)
        self.client_student.force_login(user=self.current_user_student)

    def test_own_student_profile_page_loads(self) -> None:
        """Testing if the student's profile main page loads"""

        self.current_user = User.objects.get(username=STUDENT_USERNAME)
        self.client.force_login(user=self.current_user)

        response = self.client.get(reverse('profile_main_page',
                                           kwargs={'pk': self.current_user.id}))

        self.assertEqual(200, response.status_code)

    def test_own_librarian_profile_page_loads(self) -> None:
        """Testing if the librarian's profile main page loads"""

        self.current_user = User.objects.get(username=LIBRARIAN_USERNAME)
        self.client.force_login(user=self.current_user)

        response = self.client.get(reverse('profile_main_page',
                                           kwargs={'pk': self.current_user.id}))

        self.assertEqual(200, response.status_code)

    def test_different_student_page_loads_student(self) -> None:
        """Testing if student is allowed to load different students page"""

        student_different = create_user(username='testDifferentStudentFromStudent',
                                             email='testDifferentStudentFromStudent@gmail.com')

        client_student_different = Client()
        client_student_different.force_login(user=student_different)
        response = client_student_different.get(reverse('profile_main_page',
                                                        kwargs={'pk': student_different.id}))
        self.assertEqual(200, response.status_code)




class LibrarianStatsTestCase(TestCase):
    """LibrarianStatsTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up ProfileEditTest"""

        super().setUp()

        self.client_librarian = Client()
        self.current_librarian = User.objects.get(username=LIBRARIAN_USERNAME)
        self.client_librarian.force_login(user=self.current_librarian)

        self.client_student = Client()
        self.client_student.force_login(
            User.objects.get(username=STUDENT_USERNAME)
        )

    def test_librarian_stats_page_loads_for_librarian(self) -> None:
        """Testing if the page loads for librarians"""

        response = self.client_librarian.get(
            reverse('librarian_stats_page', kwargs={'pk': self.current_librarian.id})
        )

        self.assertEqual(200, response.status_code)

    def test_librarian_stats_page_loads_for_student(self) -> None:
        """Testing if the page does not load for students"""

        response = self.client_student.get(
            reverse('librarian_stats_page', kwargs={'pk': self.current_librarian.id})
        )

        self.assertEqual(403, response.status_code)
