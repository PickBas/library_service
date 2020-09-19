"""user_profile forms.py"""
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest

from user_profile.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """ProfileUpdateForm class. Used for updating user profile"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Profile
        fields = ('birth', 'show_email')
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'birth': 'Дата рождения',
            'show_email': 'Отображать почту',
        }


class UserUpdateForm(forms.ModelForm):
    """Form for changing first and last name of user"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }


class UpdateAvatarForm(forms.ModelForm):
    """Form for updating user avatar"""
    base_image = forms.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ('base_image',)


class CustomSignupForm(SignupForm):
    """CustomSignupForm class"""

    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.fields['invite_key'] = forms.CharField(max_length=15, required=False)

    def save(self, request: HttpRequest) -> None:
        """
        Saving new user

        :param request: HttpRequest
        """

        user = super().save(request)
        profile = Profile(user=user)
        profile.save()
        return user
