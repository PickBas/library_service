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
        self.context['current_user'] = self.current_user
        self.context['page_name'] = self.current_user.username

        return render(request, self.template_name, self.context)


class ProfileUpdateView(View):
    """ProfileUpdateView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/update_profile.html'
        self.context = {'page_name': 'Редактирование профиля'}
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
        :param kwargs: dict
        :returns: redirect
        """

        self.previous_birth = request.user.profile.birth

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user)

        self.current_profile = request.user.profile

        self.current_profile.show_email = request.POST.get('show_email') is not None

        profile_form = ProfileUpdateForm(request.POST,
                                         instance=self.current_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            if self.current_profile.birth is None:
                self.current_profile.birth = self.previous_birth
                self.current_profile.save()

            return redirect(reverse('profile_main_page', kwargs={'pk': request.user.id}))

        return self.get(request)


class AvatarUpdateView(View):
    """AvatarUpdateView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'profile/update_avatar.html'
        self.context = {'page_name': 'Смена фото'}
        self.current_user = None
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

    def post(self, request: HttpRequest):
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

            x_axis = float(request.POST.get('x'))
            y_axis = float(request.POST.get('y'))
            width = float(request.POST.get('width'))
            height = float(request.POST.get('height'))

            if request.FILES.get('base_image'):
                image = Image.open(request.FILES.get('base_image'))
            else:
                image = Image.open(self.current_user.profile.base_image)

            cropped_image = image.crop((x_axis, y_axis, width + x_axis, height + y_axis))
            resized_image = cropped_image.resize((256, 256), Image.ANTIALIAS)

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

            return redirect(reverse('profile_main_page', kwargs={'pk': request.user.id}))


class LibrarianStatsView(View):
    """LibrarianStatsView class"""

    def __init__(self, **kwargs: dict):
        self.template_name = 'library/librarian_stats.html'
        self.context = {}
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

        self.context['page_name'] = 'Статистика ' + current_librarian.username
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

        try:
            datetime.strptime(request.POST.get('since_date'), '%Y-%m-%d')
            datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')
        except ValueError:
            raise Http404()

        if request.user.profile.is_student:
            raise PermissionDenied()

        if not request.POST.get('since_date') and not request.POST.get('to_date') or \
                request.POST.get(key='since_date') > request.POST.get(key='to_date'):
            raise Http404()

        current_librarian = User.objects.get(id=kwargs['pk'])
        self.context['books'] = BookInfo.objects.filter(
            librarian=current_librarian,
            date_giving_book__range=[request.POST.get(key='since_date'),
                                     request.POST.get(key='to_date')])

        return render(request, template_name, self.context)
