from django.urls import path
from . import views

urlpatterns = [
    path('', views.shirt_list, name='shirt_list'),
]