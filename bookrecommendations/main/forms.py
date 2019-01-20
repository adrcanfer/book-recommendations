from django import forms


class searchForm(forms.Form):
    query = forms.CharField(max_length=50)


class idForm(forms.Form):
    userId = forms.IntegerField()
