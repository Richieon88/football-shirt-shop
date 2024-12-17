from django import forms
from .models import NewsletterSubscriber

class NewsletterSignupForm(forms.ModelForm):
    email = forms.EmailField(
        label="Your Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
