from django import forms
from .models import NewsletterSubscriber
from django.contrib.auth.models import User


class NewsletterSignupForm(forms.ModelForm):
    email = forms.EmailField(
        label="Your Email Address",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
