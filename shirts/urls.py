from django.urls import path
from . import views

app_name = 'shirts'
urlpatterns = [
    path('', views.shirts_list, name='shirt_list'),
    path('<int:pk>/', views.shirt_detail, name='shirt_detail'),
]