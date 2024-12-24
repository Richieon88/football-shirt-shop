from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import NewsletterSignupForm, ProfileUpdateForm
from .models import NewsletterSubscriber
from shirts.models import Shirt

# Create your views here.


def index(request):
    """A view to return the index page"""
    featured_shirts = Shirt.objects.filter(featured=True)  # Query featured shirts
    context = {
        "featured_shirts": featured_shirts,
    }
    return render(request, "home/index.html", context)


def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                form.save()
                send_mail(
                    "Welcome to Our Newsletter!",
                    "Thank you for subscribing to our newsletter. Stay tuned for updates and offers!",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Thank you for subscribing to our newsletter!",
                    extra_tags="newsletter",
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "This email is already subscribed.",
                    extra_tags="newsletter",
                )
            return redirect("home:index")  # Redirect to homepage
    else:
        form = NewsletterSignupForm()

    return render(request, "home/newsletter_signup.html", {"form": form})


@login_required
def profile(request):
    """A view to display and update the user's profile."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("home:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "home/profile.html", {"form": form})


def custom_login(request, *args, **kwargs):
    """Custom login view to add feedback messages."""
    response = login(request, *args, **kwargs)
    messages.success(request, "Welcome back, {}!".format(request.user.username))
    return response


def custom_logout(request):
    """Custom logout view to add feedback messages and redirect to logout confirmation."""
    if request.method == "POST":
        username = request.user.username if request.user.is_authenticated else "Guest"
        logout(request)
        messages.success(request, f"Goodbye, {username}. You have been logged out.")
        return redirect("home:index")
    return redirect("account_logout")


def logout_confirm(request):
    """Render logout confirmation page."""
    return render(request, "account/logout_confirm.html")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Allow: /",
        "Sitemap: https://8000-richieon88-footballshir-f5ra4hucbpk.ws.codeinstitute-ide.net/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
