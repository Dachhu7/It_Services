from django import forms
from django.contrib.auth.models import User
from .models import Service, Subscription

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'payment_terms', 'price', 'package', 'tax', 'image', 'active']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['address']