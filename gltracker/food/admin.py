from django.contrib import admin
from .models import FoodItem, Meal, MealItem

# Register your models here.
admin.site.register(FoodItem)


class MealItemInline(admin.TabularInline):
    model = MealItem


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    inlines = [MealItemInline]
    list_display = ('name', 'user', 'get_total_kcal')  # Add 'get_total_kcal' to list_display

    def get_total_kcal(self, obj):
        # Get value 'total_kcal' for Meal Object
        total_kcal = obj.calculate_total_macros()['total_kcal']
        return total_kcal

    get_total_kcal.short_description = 'Total Kcal'  # Field Description


@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    pass


