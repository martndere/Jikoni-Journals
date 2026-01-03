from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_resolved')
    list_filter = ('is_resolved', 'submitted_at')
    search_fields = ('name', 'email', 'message')
