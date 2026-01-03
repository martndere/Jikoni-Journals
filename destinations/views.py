from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MapPin
from django.shortcuts import get_object_or_404


def recipes_for_pin(request, pk):
    """
    Returns an HTML partial (rendered template) containing recipes linked to a MapPin.
    Intended to be requested by HTMX and swapped into a target container.
    """
    pin = get_object_or_404(MapPin, pk=pk)
    recipes = pin.recipes.all()
    return render(request, 'destinations/partials/recipes_list.html', {'pin': pin, 'recipes': recipes})

def map_view(request):
    """
    Renders the main map page. The actual pin data will be fetched
    by a separate view to keep things clean.
    """
    return render(request, 'destinations/map_page.html')

def map_pins_api(request):
    """
    An API-like view that returns all map pin locations as JSON, including regional dishes.
    """
    pins = MapPin.objects.all().values('id', 'name', 'description', 'latitude', 'longitude', 'pin_type', 'region', 'staple_dish')
    return JsonResponse(list(pins), safe=False)
