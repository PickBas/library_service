"""user_profile forms.py"""
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.http import HttpRequest

from library_service import settings
from user_profile.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """ProfileUpdateForm class. Used for updating user profile"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Profile
        fields = ('birth',)
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'birth': 'Дата рождения',
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
        self.fields['invite_key'] = forms.CharField(max_length=15,
                                                    required=False,
                                                    label='Секретный ключ')
        self.fields['first_name'] = forms.CharField(max_length=50,
                                                    required=True,
                                                    label='Имя',
                                                    widget=forms.TextInput(
                                                        attrs={'placeholder': 'First name'}
                                                    ))
        self.fields['last_name'] = forms.CharField(max_length=50,
                                                   required=True,
                                                   label='Фамилия',
                                                   widget=forms.TextInput(
                                                       attrs={'placeholder': 'Last name'}
                                                   ))
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Пароль (еще раз)'

        self.fields.move_to_end('password1')
        self.fields.move_to_end('password2')
        self.fields.move_to_end('invite_key')

    def save(self, request: HttpRequest) -> None:
        """
        Saving new user

        :param request: HttpRequest
        """

        invite_key = self.cleaned_data.get('invite_key')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        user = super().save(request)

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile = Profile(user=user)

        if invite_key == settings.LIBRARIAN_KEY:
            profile.is_librarian = True
        else:
            profile.is_student = True

        profile.save()
        return user
