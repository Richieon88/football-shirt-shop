from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import NewsletterSignupForm, ProfileUpdateForm
from .models import NewsletterSubscriber

# Create your views here.

def index(request):
    """ A view to return the index page"""
    return render(request, 'home/index.html')

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                form.save()
                # Send welcome email
                send_mail(
                    'Welcome to Our Newsletter!',
                    'Thank you for subscribing to our newsletter. Stay tuned for updates and offers!',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.warning(request, "This email is already subscribed.")
            return redirect('home:index')  # Redirect to homepage
    else:
        form = NewsletterSignupForm()

    return render(request, 'home/newsletter_signup.html', {'form': form})

@login_required
def profile(request):
    """A view to display and update the user's profile."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'home/profile.html', {'form': form})