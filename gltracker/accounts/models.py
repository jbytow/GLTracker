from django.db import models
from django.contrib.auth.models import User


from food.models import Meal, FoodItem


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    height = models.IntegerField(null=True)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)


class WeightRecord(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.entry_date}"


class FoodDailyRequirements(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calories = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    proteins = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Daily Requirements for {self.user.username}"


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField(FoodItem, blank=True, through='FoodLogFoodItem')
    meals = models.ManyToManyField(Meal, blank=True, through='FoodLogMeal')
    date = models.DateField()

    def calculate_total_macros_log(self):
        total_kcal = 0
        total_carbohydrates = 0
        total_fats = 0
        total_proteins = 0




    def __str__(self):
        return f"{self.user.username}'s Food Log - {self.date}"


class FoodLogFoodItem(models.Model):
    food_log = models.ForeignKey(FoodLog, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class FoodLogMeal(models.Model):
    food_log = models.ForeignKey(FoodLog, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


