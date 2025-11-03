from django import forms

class serch(forms.Form):
    category = forms.CharField(widget=forms.TextInput, required=False)
    tags = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=200, required=False)