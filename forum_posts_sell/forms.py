from django import forms


class Create_Form(forms.Form):
    title = forms.CharField(label="Enter Title", max_length=100)
    tags = forms.CharField(
        label="Tag",
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Separate tags with commas'
        })
    )
    text = forms.CharField(label="Text", max_length=5000, widget=forms.Textarea())
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2, initial=0.00)
    item = forms.CharField(label="Selled Item", max_length=5000, widget=forms.Textarea())

class Opinion(forms.Form):
    rate = forms.IntegerField(label="Rate", min_value=1, max_value=5)

class serch_Form(forms.Form):
    title = forms.CharField(label="Title", max_length=100, required=False)
    tag = forms.CharField(label="Tag", max_length=50, required=False)
    min_price = forms.DecimalField(label="Min Price", max_digits=10, decimal_places=2, initial=0.00, required=False)
    max_price = forms.DecimalField(label="Max Price", max_digits=10, decimal_places=2, initial=0.00, required=False)
    author = forms.CharField(label="Author", max_length=100, required=False)
