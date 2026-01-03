from django.contrib import admin
from .models import MapPin

@admin.register(MapPin)
class MapPinAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'pin_type', 'staple_dish', 'latitude', 'longitude')
    list_filter = ('pin_type', 'region')
    search_fields = ('name', 'description', 'region', 'staple_dish')
    filter_horizontal = ('recipes',)