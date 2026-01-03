from django.db import models
from mealplans.models import Recipe

class MapPin(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pin_type = models.CharField(max_length=50, help_text="e.g., 'Restaurant', 'Tourist Spot', 'Cooking Class'")
    region = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'Kiambu', 'Mombasa', 'Nakuru'")
    staple_dish = models.CharField(max_length=255, blank=True, null=True, help_text="Cultural or staple food of this region, e.g., 'Potato Salad', 'Coastal Seafood'")
    # Optional link to recipes from the mealplans app
    recipes = models.ManyToManyField(Recipe, blank=True, related_name='map_pins', help_text='Related recipes for this region')

    def __str__(self):
        return self.name
