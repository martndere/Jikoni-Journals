from django.contrib import admin
from .models import Week, Recipe

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('week_number', 'title', 'compiled_by')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'week', 'day')
    list_filter = ('week',)
    search_fields = ('title', 'notes')
