from django.urls import path
from . import views

app_name = 'shirts'
urlpatterns = [
    path('', views.shirts_list, name='shirt_list'),
    path('<int:pk>/', views.shirt_detail, name='shirt_detail'),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
    path('<int:pk>/edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('<int:pk>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]