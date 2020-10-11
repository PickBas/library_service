"""book forms.py"""
from django import forms
from django.contrib.auth.models import User

from book.models import Book


class UploadBookForm(forms.Form):
    """UploadBookForm form"""

    name = forms.CharField(max_length=100,
                           label='Название')

    info = forms.CharField(max_length=500,
                           label='Информация о книге',
                           widget=forms.Textarea())


class EditBookForm(forms.ModelForm):
    """EditBookForm form"""

    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Book
        fields = ('name', 'info')
        widgets = {
            'info': forms.Textarea(),
        }
        labels = {
            'name': 'Название',
            'info': 'Информация о книге',
        }


class GiveBookForm(forms.Form):
    """GiveBookForm class"""

    student = forms.ModelChoiceField(label='Ученик',
                                     queryset=User.objects.filter(profile__is_student=True))

    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.fields['student'].choices = [(stud.pk,
                                           stud.profile.get_full_name())
                                          for stud in User.objects.filter(profile__is_student=True)]

    date_back = forms.DateTimeField(label='Дата возврата',
                                    widget=forms.DateInput(attrs={'type': 'date'}))
