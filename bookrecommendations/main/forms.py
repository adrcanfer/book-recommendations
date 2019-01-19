from django import forms

class searchForm(forms.Form):
    query = forms.CharField(max_length=50)
