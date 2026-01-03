from django.db import models

class Week(models.Model):
    week_number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200, default="Jikoni Journals – 30-Day Dinner Meal Plan")
    compiled_by = models.CharField(max_length=100, default="Charity Mutisya")
    shopping_list = models.TextField(help_text="Comma-separated list of shopping items for the week.")

    def __str__(self):
        return f"Week {self.week_number}"

class Recipe(models.Model):
    week = models.ForeignKey(Week, related_name='recipes', on_delete=models.CASCADE)
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True, null=True)
    ingredients = models.TextField(help_text="List each ingredient on a new line.")
    method = models.TextField(help_text="List each step on a new line.")

    class Meta:
        ordering = ['week__week_number', 'day']

    def __str__(self):
        return f"Week {self.week.week_number}, Day {self.day}: {self.title}"
