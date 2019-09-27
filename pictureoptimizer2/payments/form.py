from django import forms

class SubscribeForm(forms.Form):
    cardNumber= forms.CharField(max_length=100)
    cardExpiry= forms.CharField(max_length=100)
    email= forms.EmailField()
    cardCVC=forms.CharField(max_length=100)
    cardSecurityCode=forms.CharField(max_length=100)
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    company=forms.CharField(max_length=100)
    address=forms.CharField(max_length=100)
    postalCode=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    country=forms.CharField(max_length=100)

