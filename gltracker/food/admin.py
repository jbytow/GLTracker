from django.contrib import admin
from .models import FoodItem
from .models import Meal

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Meal)
