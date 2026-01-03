from django.core.management.base import BaseCommand
from destinations.models import MapPin
from mealplans.models import Recipe

class Command(BaseCommand):
    help = 'Auto-link recipes to MapPins based on matching region or staple_dish keywords in recipe title/ingredients/method.'

    def handle(self, *args, **options):
        pins = MapPin.objects.all()
        linked_count = 0
        for pin in pins:
            keywords = []
            if pin.region:
                keywords.append(pin.region.lower())
            if pin.staple_dish:
                keywords.extend([w.strip().lower() for w in pin.staple_dish.split() if w.strip()])

            if not keywords:
                self.stdout.write(f"Skipping pin {pin} (no region/staple_dish)")
                continue

            # search recipes for any keyword in title, ingredients, method
            for recipe in Recipe.objects.all():
                hay = ' '.join([str(recipe.title), str(recipe.ingredients or ''), str(recipe.method or '')]).lower()
                if any(k in hay for k in keywords):
                    if recipe not in pin.recipes.all():
                        pin.recipes.add(recipe)
                        linked_count += 1
                        self.stdout.write(f"Linked recipe '{recipe}' to pin '{pin}'")

        self.stdout.write(self.style.SUCCESS(f"Auto-link complete. Total links added: {linked_count}"))
