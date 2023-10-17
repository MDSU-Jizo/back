from django.contrib import admin
from .models import Itinerary


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    """
        Display data as tables in Dashboard admin
    """
    list_display = ("id", "country", "starting_city", "ending_city", "user")
