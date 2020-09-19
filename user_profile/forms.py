"""user_profile forms.py"""

from django import forms
from django.contrib.auth.models import User

from user_profile.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """ProfileUpdateForm class. Used for updating user profile"""

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

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
