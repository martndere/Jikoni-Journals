from django.shortcuts import render
from .models import Week, Recipe

def meal_plan_list(request):
    """
    Fetches all weeks and their related recipes to display on the main meal plan page.
    Using prefetch_related to optimize the database query.
    """
    weeks = Week.objects.prefetch_related('recipes').all().order_by('week_number')
    return render(request, 'mealplans/meal_plan_page.html', {'weeks': weeks})

def recipe_detail(request, recipe_id):
    """
    Fetches a single recipe by its ID to be displayed in a modal or partial view.
    This view is designed to be called by an HTMX request.
    """
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'mealplans/partials/recipe_detail.html', {'recipe': recipe})
