from django import forms

from webapp.models import File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['author', 'created_at', 'access']


class AuthFileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['created_at','author']

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')
