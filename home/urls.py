from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("newsletter/signup/", views.newsletter_signup, name="newsletter_signup"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(extra_context={"next": "/"}),
        name="account_login",
    ),
    path("logout/", views.custom_logout, name="account_logout"),
    path("logout/confirm/", views.logout_confirm, name="logout_confirm"),
]
