from django import forms


class Create_Form(forms.Form):
    title = forms.CharField(label="Enter Title", max_length=100)
    tags = forms.CharField(label="Tag", max_length=50)
    text = forms.CharField(label="Text", max_length=5000,widget=forms.Textarea())

    