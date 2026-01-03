from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tour_date', 'guests', 'is_paid', 'amount_due', 'created_at')
    list_filter = ('tour_date', 'is_paid', 'created_at')
    search_fields = ('name', 'email')