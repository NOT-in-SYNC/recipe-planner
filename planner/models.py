from django.db import models

class Recipe(models.Model):
    # CORRECTED: No "models.Column" wrapper needed here
    title = models.CharField(max_length=200)
    description = models.TextField()
    prep_time_minutes = models.PositiveIntegerField() 

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    # Link ingredient to a recipe
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return f"{self.quantity} {self.name}"