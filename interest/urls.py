"""
    Favorite urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_interests, name='get_interests'),
    path('details/<int:interest_id>', views.get_interest, name='get_interest'),
    path('add', views.add_interest, name='add_interest'),
    path('update', views.update_interest, name='update_interest'),
    path('delete/<int:interest_id>', views.delete_interest, name='delete_interest')
]
