"""
    AclBundle urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_itineraries, name='get_itineraries'),
    path('details/<int:itinerary_id>', views.get_itinerary, name='get_itinerary'),
    path('update/title/<int:itinerary_id>', views.update_itinerary_title, name='update_itinerary_title'),
    path('update', views.update_itinerary_steps, name='update_itinerary_steps'),
    path('create', views.create_itinerary, name='get_create_itinerary'),
    path('delete/<int:itinerary_id>', views.delete_itinerary, name='delete_itinerary')
]