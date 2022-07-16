"""user_profile views.py"""
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from book.models import BookInfo
from core.forms import CropAvatarForm
from user_profile.forms import UpdateAvatarForm, ProfileUpdateForm, UserUpdateForm


class ProfilePageView(View):
    """ProfilePageView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/profile_main_page.html'
        self.context = {}
        self.current_user = None
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request.

        :param request: HttpRequest
        :param kwargs: dict (pk)
        :returns: render
        :raises: Http404
        """

        if not User.objects.filter(id=kwargs['pk']).exists():
            raise Http404()
        self.current_user = User.objects.get(id=kwargs['pk'])
        self.check_permission(request_user=request.user)
        self.context['current_user'] = self.current_user
        self.context['page_name'] = self.current_user.username
        return render(request, self.template_name, self.context)

    def check_permission(self, request_user: User) -> None:
        """
        Check if request user is allowed to see the page

        :param request_user: User
        """

        if request_user.profile.is_student and request_user != self.current_user:
            raise PermissionDenied()
        if self.current_user.profile.is_librarian and request_user.profile.is_librarian\
                and request_user != self.current_user:
            raise PermissionDenied()
        if self.current_user.is_superuser and not request_user.is_superuser:
            raise PermissionDenied()


class ProfileUpdateView(View):
    """ProfileUpdateView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/update_profile.html'
        self.context = {'page_name': 'Profile edit'}
        self.current_profile = None
        self.previous_birth = None
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :returns: render
        """

        self.context['user_form'] = UserUpdateForm(instance=request.user)
        self.context['profile_form'] = ProfileUpdateForm(instance=request.user.profile)
        self.previous_birth = request.user.profile.birth
        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest) -> redirect:
        """
        Processing POST request

        :param request: HttpRequest
        :returns: redirect
        """

        self.current_profile = request.user.profile
        self.previous_birth = request.user.profile.birth
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         instance=self.current_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            self.validate_birth()
            return redirect(reverse('profile_main_page', kwargs={'pk': request.user.id}))
        return self.get(request)

    def validate_birth(self):
        """Validating date of birth from ProfileUpdateForm"""

        if self.current_profile.birth is None:
            self.current_profile.birth = self.previous_birth
            self.current_profile.save()


class AvatarUpdateView(View):
    """AvatarUpdateView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/update_avatar.html'
        self.context = {'page_name': 'Change photo'}
        self.current_user = None
        self.x_axis = 0.0
        self.y_axis = 0.0
        self.width = 0.0
        self.height = 0.0
        super().__init__(**kwargs)

    def get(self, request: HttpRequest) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :returns: render
        """

        self.context['avatar_form'] = UpdateAvatarForm()
        self.context['crop_form'] = CropAvatarForm()
        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest) -> redirect:
        """
        Cropping and saving user avatar

        :param request: request
        :returns: redirect
        """

        avatar_form = UpdateAvatarForm(request.POST, request.FILES,
                                       instance=request.user.profile)
        crop_form = CropAvatarForm(request.POST)
        self.current_user = request.user
        if crop_form.is_valid() and avatar_form.is_valid():
            avatar_form.save()
            self.get_size(request)
            self.save_avatar(self.get_image_resized(self.open_image(request)))
            return redirect(reverse('profile_main_page', kwargs={'pk': request.user.id}))

    def get_image_resized(self, image: Image) -> Image:
        """
        Getting image resized

        :param image:
        :return:
        """

        cropped_image = image.crop((self.x_axis, self.y_axis,
                                    self.width + self.x_axis, self.height + self.y_axis))
        return cropped_image.resize((256, 256), Image.ANTIALIAS)

    def open_image(self, request: HttpRequest) -> Image:
        """
        Opening image from request

        :param request: HttpRequest
        :returns: Image
        """

        if request.FILES.get('base_image'):
            image = Image.open(request.FILES.get('base_image'))
        else:
            image = Image.open(self.current_user.profile.base_image)
        return image

    def get_size(self, request: HttpRequest):
        """
        Getting size of an image from request

        :param request: HttpRequest
        """

        self.x_axis = float(request.POST.get('x'))
        self.y_axis = float(request.POST.get('y'))
        self.width = float(request.POST.get('width'))
        self.height = float(request.POST.get('height'))

    def save_avatar(self, resized_image: Image):
        """
        Saving avatar

        :param resized_image: Image
        """

        input_output = BytesIO()
        try:
            resized_image.save(input_output, 'JPEG', quality=100)
            self.current_user.profile.image.save('image_{}.jpg'.format(self.current_user.id),
                                                 ContentFile(input_output.getvalue()),
                                                 save=False)
            self.current_user.profile.save()
        except OSError:
            resized_image.save(input_output, 'PNG', quality=100)
            self.current_user.profile.image.save('image_{}.png'.format(self.current_user.id),
                                                 ContentFile(input_output.getvalue()),
                                                 save=False)
            self.current_user.profile.save()


class LibrarianStatsView(View):
    """LibrarianStatsView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/librarian_stats.html'
        self.context = {}
        self.since_date = datetime
        self.to_date = datetime
        super().__init__(**kwargs)

    def get(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing GET request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        :raises: 403
        """

        current_librarian = User.objects.get(id=kwargs['pk'])
        if request.user.profile.is_student:
            raise PermissionDenied()
        self.context['page_name'] = 'Statistics ' + current_librarian.username
        self.context['books'] = BookInfo.objects.filter(librarian=current_librarian)
        self.context['current_librarian'] = current_librarian
        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, **kwargs: dict) -> render:
        """
        Processing POST request

        :param request: HttpRequest
        :param kwargs: pk
        :returns: render
        :raises: 403, 404
        """

        template_name = 'library/librarian_stats_table.html'
        if request.user.profile.is_student:
            raise PermissionDenied()
        self.get_dates_from_request(request)
        current_librarian = User.objects.get(id=kwargs['pk'])
        self.context['books'] = BookInfo.objects.filter(
            librarian=current_librarian,
            date_giving_book__range=[request.POST.get(key='since_date'),
                                     request.POST.get(key='to_date')])
        return render(request, template_name, self.context)

    def get_dates_from_request(self, request: HttpRequest):
        """
        Getting dates from HttpRequest

        :param request: HttpRequest
        """

        try:
            self.since_date = datetime.strptime(request.POST.get('since_date'), '%Y-%m-%d')
            self.to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')
        except ValueError as invalid_dates:
            raise Http404() from invalid_dates
        if not self.since_date and not self.to_date or \
                self.since_date > self.to_date:
            raise Http404()
