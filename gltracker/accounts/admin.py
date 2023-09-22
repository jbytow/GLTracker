from django.contrib import admin
from .models import Profile, WeightRecord, FoodDailyRequirements, FoodLog

# Register your models here.
admin.site.register(Profile)
admin.site.register(WeightRecord)
admin.site.register(FoodDailyRequirements)
admin.site.register(FoodLog)
