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
ADMIN_USERNAME = 'ThirdUserAdmin'


def create_user(username: str, email: str, is_librarian=False) -> User:
    """
    Creating user

    :param username: str
    :param email: str
    :returns: User
    """

    student_different = User.objects.create(username=username,
                                            email=email,
                                            password='asdf123!',
                                            is_staff=is_librarian)
    student_different_profile = Profile(user=student_different,
                                        is_student=(not is_librarian),
                                        is_librarian=is_librarian)
    student_different_profile.save()
    student_different.save()

    return student_different


class AbsTestCase(TestCase):
    """AbsTestCase class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        self.client_student = Client()
        self.client_librarian = Client()
        self.client_admin = Client()

        self.current_user_student = User.objects.get(username=STUDENT_USERNAME)
        self.current_user_librarian = User.objects.get(username=LIBRARIAN_USERNAME)
        self.current_user_admin = User.objects.get(username=ADMIN_USERNAME)

        self.client_student.force_login(user=self.current_user_student)
        self.client_librarian.force_login(user=self.current_user_librarian)
        self.client_admin.force_login(user=self.current_user_admin)

        super().setUp()


class LoginTest(AbsTestCase):
    """LoginTest class"""

    fixtures = ['test_db.json']

    def setUp(self) -> None:
        """Setting up the TestCase"""

        self.client = Client()
        super().setUp()

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


class RegistrationTest(AbsTestCase):
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


class PasswordChangingTest(AbsTestCase):
    """class PasswordChangingTest"""

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


class ProfileEditTest(AbsTestCase):
    """class ProfileEditTest"""

    def test_forms(self) -> None:
        """
        Testing forms validation

        :returns: None
        """

        f_user_update_data = {'first_name': 'test', 'last_name': 'usertest'}
        user_update_form = UserUpdateForm(f_user_update_data, instance=self.current_user_student)
        self.assertTrue(user_update_form.is_valid())

        f_profile_data = {
            'birth': datetime.now()
        }
        profile_update_form = ProfileUpdateForm(f_profile_data, instance=self.current_user_student.profile)
        self.assertTrue(profile_update_form.is_valid())

    def test_changing_data_page_loads(self) -> None:
        """Testing if the page loads"""

        response = self.client_student.get(reverse('update_profile_info'))

        self.assertEqual(200, response.status_code)

    def test_changing_data(self) -> None:
        """Testing if it's possible to change the profile data"""

        form_user_update_data = {'first_name': 'test', 'last_name': 'usertest'}

        response = self.client_student.post(reverse('update_profile_info'), {
            **form_user_update_data,
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(User.objects.get(username=STUDENT_USERNAME).last_name,
                         form_user_update_data['last_name'])

    def test_avatar_upload_page_loads(self) -> None:
        """Testing if the page loads"""

        response = self.client_student.get(reverse('update_profile_avatar'))

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
        response = self.client_student.post(reverse('update_profile_avatar'), {
            **to_send_image,
            **to_send_cropper,

        })

        self.assertEqual(response.status_code, 302)


class ProfileMainPageTestCase(AbsTestCase):
    """ProfileMainPageTestCase class"""

    def test_own_student_profile_page_loads(self) -> None:
        """Testing if the student's profile main page loads"""

        self.current_user = User.objects.get(username=STUDENT_USERNAME)
        self.client.force_login(user=self.current_user)

        response = self.client.get(reverse('profile_main_page',
                                           kwargs={'pk': self.current_user.id}))

        self.assertEqual(200, response.status_code)

    def test_different_student_page_loads_student(self) -> None:
        """Testing if student is allowed to load different students page"""

        student_different = create_user(username='testDifferentStudentFromStudent',
                                        email='testDifferentStudentFromStudent@gmail.com')
        response = self.client_student.get(reverse('profile_main_page',
                                                   kwargs={'pk': student_different.id}))
        self.assertEqual(403, response.status_code)

    def test_own_librarian_profile_page_loads(self) -> None:
        """Testing if the librarian's profile main page loads"""

        response = self.client_librarian.get(reverse('profile_main_page',
                                                     kwargs={'pk': self.current_user_librarian.id}))
        self.assertEqual(200, response.status_code)

    def test_different_librarian_page_loads_student(self) -> None:
        """Testing if librarian is allowed to load different librarian's page"""

        librarian_different = create_user(username='testDifferentLibrarianFromStudent',
                                          email='testDifferentLibrarianFromStudent@gmail.com',
                                          is_librarian=True)
        response = self.client_librarian.get(reverse('profile_main_page',
                                                     kwargs={'pk': librarian_different.id}))
        self.assertEqual(403, response.status_code)

    def test_pages_load_for_admin(self) -> None:
        """Testing if admin is allowed to see admin, librarian and student pages"""

        response_student_page = self.client_admin.get(reverse('profile_main_page',
                                                              kwargs={'pk': self.current_user_student.id}))
        response_librarian_page = self.client_admin.get(reverse('profile_main_page',
                                                                kwargs={'pk': self.current_user_librarian.id}))
        response_admin_page = self.client_admin.get(reverse('profile_main_page',
                                                            kwargs={'pk': self.current_user_admin.id}))
        self.assertEqual(200, response_student_page.status_code)
        self.assertEqual(200, response_librarian_page.status_code)
        self.assertEqual(200, response_admin_page.status_code)


class LibrarianStatsTestCase(AbsTestCase):
    """LibrarianStatsTestCase class"""

    def test_librarian_stats_page_loads_for_librarian(self) -> None:
        """Testing if the page loads for librarians"""

        response = self.client_librarian.get(
            reverse('librarian_stats_page', kwargs={'pk': self.current_user_librarian.id})
        )

        self.assertEqual(200, response.status_code)

    def test_librarian_stats_page_loads_for_student(self) -> None:
        """Testing if the page does not load for students"""

        response = self.client_student.get(
            reverse('librarian_stats_page', kwargs={'pk': self.current_user_librarian.id})
        )

        self.assertEqual(403, response.status_code)
