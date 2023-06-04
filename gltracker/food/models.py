from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    kcal = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    proteins = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    glycemic_index = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    glycemic_load = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def calculate_total_macros(self):
        total_kcal = 0
        total_carbohydrates = 0
        total_fats = 0
        total_protein = 0
        total_glycemic_load = 0
        total_glycemic_index = 0

        meal_items = self.mealitem_set.all()
        for meal_item in meal_items:
            quantity = meal_item.quantity
            food_item = meal_item.food_item
            total_kcal += food_item.kcal * quantity/100
            total_carbohydrates += food_item.carbohydrates * quantity/100
            total_fats += food_item.fats * quantity/100
            total_protein += food_item.protein * quantity/100
            total_glycemic_load += food_item.glycemic_load * quantity/100
            total_glycemic_index += food_item.glycemic_index * quantity/100

        num_items = meal_items.count()
        average_glycemic_index = total_glycemic_index / num_items if num_items > 0 else 0

        return {
            'total_kcal': total_kcal,
            'total_carbohydrates': total_carbohydrates,
            'total_fats': total_fats,
            'total_protein': total_protein,
            'total_glycemic_load': total_glycemic_load,
            'average_glycemic_index': average_glycemic_index
        }

    def __str__(self):
        return self.name


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} - {self.meal.name}"