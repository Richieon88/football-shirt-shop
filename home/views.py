from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSignupForm
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
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.warning(request, "This email is already subscribed.")
            return redirect('home:index')  # Redirect to homepage
    else:
        form = NewsletterSignupForm()

    return render(request, 'home/newsletter_signup.html', {'form': form})