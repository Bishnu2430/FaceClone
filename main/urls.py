from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('post/<int:post_id>/like/', views.like_toggle, name='like_toggle'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
