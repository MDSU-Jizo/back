"""
    User urls
"""
from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile', views.get_profile, name='profile'),
    path('', views.get_users, name='users'),
    path('details/<int:user_id>', views.get_user, name='get_user'),
    path('update/<int:user_id>', views.update_profile, name='update_profile'),
    path('update/password/<int:user_id>', views.update_password, name='update_password'),
    path('update/language/<int:user_id>', views.change_language, name='change_language'),
    path('delete/<int:user_id>', views.delete_profile, name='delete_profile'),
]