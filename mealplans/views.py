from django.shortcuts import render
from .models import Week, Recipe

def recipe_detail(request, recipe_id):
    """
    Fetches a single recipe by its ID to be displayed in a modal or partial view.
    This view is designed to be called by an HTMX request.
    """
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'mealplans/partials/recipe_detail.html', {'recipe': recipe})

def meal_plan_list(request):
    # Existing logic for weeks (assuming it filters for meals or you want to keep it as is)
    weeks = Week.objects.prefetch_related('recipes').all().order_by('week_number')
    
    # New logic: Fetch Drinks and Snacks
    drinks = Recipe.objects.filter(category='drink')
    snacks = Recipe.objects.filter(category='snack')

    return render(request, 'mealplans/meal_plan_page.html', {
        'weeks': weeks,
        'drinks': drinks,
        'snacks': snacks,
    })