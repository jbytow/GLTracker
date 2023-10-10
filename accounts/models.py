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
    calories = models.IntegerField(default=0)
    carbohydrates = models.IntegerField(default=0)
    fats = models.IntegerField(default=0)
    proteins = models.IntegerField(default=0)

    def __str__(self):
        return f"Daily Requirements for {self.user.username}"


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField(FoodItem, blank=True, through='FoodLogFoodItem')
    meals = models.ManyToManyField(Meal, blank=True, through='FoodLogMeal')
    date = models.DateField()

    def calculate_total_macros_log(self):
        log_total_kcal = 0
        log_total_carbohydrates = 0
        log_total_fats = 0
        log_total_proteins = 0
        log_total_glycemic_load = 0
        log_total_quantity = 0

        # Calories and macronutrients from FoodLogFoodItem - divided by 100 as FoodItems have values per 100g
        for food_log_food_item in self.foodlogfooditem_set.all():
            food_item = food_log_food_item.food_item
            quantity = food_log_food_item.quantity
            log_total_kcal += round(food_item.kcal * quantity/100)
            log_total_carbohydrates += round(food_item.carbohydrates * quantity/100)
            log_total_fats += round(food_item.fats * quantity/100)
            log_total_proteins += round(food_item.proteins * quantity/100)
            log_total_glycemic_load += round(food_item.glycemic_load * quantity / 100)
            log_total_quantity += quantity

        # Calories and macronutrients from FoodLogMeal - divided by 100 as Meals have values per 100g
        for food_log_meal in self.foodlogmeal_set.all():
            meal = food_log_meal.meal
            meal_macros = meal.calculate_total_macros_meal()
            quantity = food_log_meal.quantity
            log_total_kcal += round(meal_macros['total_kcal_per_100g'] * quantity/100)
            log_total_carbohydrates += round(meal_macros['total_carbohydrates_per_100g'] * quantity/100)
            log_total_fats += round(meal_macros['total_fats_per_100g'] * quantity/100)
            log_total_proteins += round(meal_macros['total_proteins_per_100g'] * quantity/100)
            log_total_glycemic_load += round(meal_macros['total_glycemic_load_per_100g'] * quantity / 100)
            log_total_quantity += quantity

        return {
            'log_total_kcal': log_total_kcal,
            'log_total_carbohydrates': log_total_carbohydrates,
            'log_total_fats': log_total_fats,
            'log_total_proteins': log_total_proteins,
            'log_total_glycemic_load': log_total_glycemic_load,
            'log_total_quantity': log_total_quantity

        }

    def __str__(self):
        return f"{self.user.username}'s Food Log - {self.date}"


class FoodLogFoodItem(models.Model):
    food_log = models.ForeignKey(FoodLog, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_name(self):
        return self.food_item.name

    def get_calories(self):
        return round(float(self.quantity / 100) * float(self.food_item.kcal))

    def get_carbohydrates(self):
        return round(float(self.quantity / 100) * float(self.food_item.carbohydrates))

    def get_fats(self):
        return round(float(self.quantity / 100) * float(self.food_item.fats))

    def get_proteins(self):
        return round(float(self.quantity / 100) * float(self.food_item.proteins))

    def get_glycemic_load(self):
        return round(float(self.quantity / 100) * float(self.food_item.glycemic_load))


class FoodLogMeal(models.Model):
    food_log = models.ForeignKey(FoodLog, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_name(self):
        return self.meal.name

    def get_calories(self):
        macros = self.meal.calculate_total_macros_meal()
        return round(float(self.quantity / 100) * float(macros['total_kcal_per_100g']))

    def get_carbohydrates(self):
        macros = self.meal.calculate_total_macros_meal()
        return round(float(self.quantity / 100) * float(macros['total_carbohydrates_per_100g']))

    def get_fats(self):
        macros = self.meal.calculate_total_macros_meal()
        return round(float(self.quantity / 100) * float(macros['total_fats_per_100g']))

    def get_proteins(self):
        macros = self.meal.calculate_total_macros_meal()
        return round(float(self.quantity / 100) * float(macros['total_proteins_per_100g']))

    def get_glycemic_load(self):
        macros = self.meal.calculate_total_macros_meal()
        return round(float(self.quantity / 100) * float(macros['total_glycemic_load_per_100g']))
