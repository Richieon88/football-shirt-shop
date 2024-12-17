from django.contrib import admin
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
]
