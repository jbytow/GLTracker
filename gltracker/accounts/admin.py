from django.contrib import admin
from .models import Profile, WeightRecord, FoodDailyRequirements, FoodLogFoodItem, FoodLogMeal, FoodLog

# Register your models here.
admin.site.register(Profile)
admin.site.register(WeightRecord)
admin.site.register(FoodDailyRequirements)


class FoodLogFoodItemInline(admin.TabularInline):
    model = FoodLogFoodItem


class FoodLogMealInline(admin.TabularInline):
    model = FoodLogMeal


@admin.register(FoodLog)
class MealAdmin(admin.ModelAdmin):
    inlines = [FoodLogMealInline, FoodLogFoodItemInline]
