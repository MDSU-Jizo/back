"""
    Type urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_types, name='get_types'),
    path('details/<int:type_id>', views.get_type, name='get_type'),
    path('add', views.add_type, name='add_type'),
    path('update', views.update_type, name='update_type'),
    path('delete/<int:type_id>', views.delete_type, name='delete_type')
]