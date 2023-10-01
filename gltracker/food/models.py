from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

import os


class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    kcal = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    proteins = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    glycemic_index = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    glycemic_load = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.glycemic_load is None:
            self.glycemic_load = self.calculate_glycemic_load()
        super().save(*args, **kwargs)

    def calculate_glycemic_load(self):
        # Glycemic load calculation logic
        glycemic_load = self.carbohydrates * self.glycemic_index / 100
        return glycemic_load

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


def meal_default_image():
    return 'images/mealdefault.png'


def meal_image_upload_to(instance, filename):
    path = os.path.join('meal_images', instance.name, filename)
    return path


class Meal(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=meal_image_upload_to, blank=True, null=True)
    meal_items = models.ManyToManyField('FoodItem', through='MealItem', related_name='meals')

    def calculate_total_macros_meal(self):
        total_kcal = 0
        total_carbohydrates = 0
        total_fats = 0
        total_proteins = 0
        total_glycemic_load = 0
        total_glycemic_index = 0
        total_weight = 0
        weighted_glycemic_index = 0

        meal_items = self.mealitem_set.all()
        for meal_item in meal_items:
            quantity = meal_item.quantity
            food_item = meal_item.food_item
            total_weight += quantity

            total_kcal += food_item.kcal * quantity/100
            total_carbohydrates += food_item.carbohydrates * quantity/100
            total_fats += food_item.fats * quantity/100
            total_proteins += food_item.proteins * quantity/100
            total_glycemic_load += food_item.glycemic_load * quantity/100
            total_glycemic_index += food_item.glycemic_index/100
            weighted_glycemic_index += food_item.glycemic_index * quantity/100

        if total_weight != 0:
            total_kcal_per_100g = round((total_kcal / total_weight*100), 2)
            total_carbohydrates_per_100g = round((total_carbohydrates / total_weight*100), 2)
            total_fats_per_100g = round((total_fats / total_weight*100), 2)
            total_proteins_per_100g = round((total_proteins / total_weight*100), 2)
            total_glycemic_load_per_100g = round((total_glycemic_load / total_weight*100), 2)
            average_glycemic_index = round(weighted_glycemic_index / total_weight*100, 2)
        else:
            total_kcal_per_100g = 0
            total_carbohydrates_per_100g = 0
            total_fats_per_100g = 0
            total_proteins_per_100g = 0
            total_glycemic_load_per_100g = 0
            average_glycemic_index = 0

        return {
            'total_kcal': total_kcal,
            'total_carbohydrates': total_carbohydrates,
            'total_fats': total_fats,
            'total_proteins': total_proteins,
            'total_glycemic_load': total_glycemic_load,
            'total_kcal_per_100g': total_kcal_per_100g,
            'total_carbohydrates_per_100g': total_carbohydrates_per_100g,
            'total_fats_per_100g': total_fats_per_100g,
            'total_proteins_per_100g': total_proteins_per_100g,
            'total_glycemic_load_per_100g': total_glycemic_load_per_100g,
            'average_glycemic_index': average_glycemic_index
        }

    def __str__(self):
        return self.name


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} - {self.meal.name}"