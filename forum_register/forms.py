from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100,required=True)
    password = forms.CharField(label="Password", max_length=100,required=True,widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", max_length=100,required=True,widget=forms.PasswordInput)
    key = forms.CharField(label="key", max_length=256,required=True)
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100,required=True)
    password = forms.CharField(label="Password", max_length=100,required=True,widget=forms.PasswordInput)
