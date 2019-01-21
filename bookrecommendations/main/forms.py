from django import forms
from main.models import User
from django.core.exceptions import ValidationError


class searchForm(forms.Form):
    buscar = forms.CharField(max_length=50)


class idForm(forms.Form):
    userId = forms.IntegerField()


class loginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(loginForm, self).clean()
        user = User.objects.filter(username=cleaned_data['username'], password=cleaned_data['password'])
        if user.count() != 1:
            raise ValidationError('Nombre de usuario y/o contraseña incorrectos')
        return cleaned_data


class registerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        return cleaned_data

class ratingForm(forms.Form):
    bookId = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    rating = forms.IntegerField(max_value=10, min_value=0, required=True)
