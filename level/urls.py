"""
    Level urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_levels, name='get_levels'),
    path('details/<int:level_id>', views.get_level, name='get_level'),
    path('add', views.add_level, name='add_level'),
    path('update', views.update_level, name='update_level'),
    path('delete/<int:level_id>', views.delete_level, name='delete_level')
]
