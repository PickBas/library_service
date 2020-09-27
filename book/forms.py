"""book forms.py"""
from django import forms
from django.contrib.auth.models import User


class UploadBookForm(forms.Form):
    """UploadBookForm form"""

    name = forms.CharField(max_length=100,
                           label='Название')

    info = forms.CharField(max_length=500,
                           label='Информация о книге',
                           widget=forms.Textarea())


class GiveBookForm(forms.Form):
    """GiveBookForm class"""

    STUDENTS = ()

    for student in User.objects.filter(profile__is_student=True):
        STUDENTS += ((student.id, student.profile.get_full_name()),)

    student = forms.ChoiceField(label='Ученик', choices=STUDENTS)
    date_back = forms.DateTimeField(label='Дата возврата', widget=forms.DateInput(attrs={'type': 'date'}))
