"""
    Language urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_languages, name='get_languages'),
    path('details/<int:language_id>', views.get_language, name='get_language'),
    path('add', views.add_language, name='add_language'),
    path('update', views.update_language, name='update_language'),
    path('delete/<int:language_id>', views.delete_language, name='delete_language')
]
