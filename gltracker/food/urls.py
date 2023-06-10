from django.urls import path

import food.views

urlpatterns = [

    path('add_fooditem/', food.views.add_fooditem, name='add_fooditem'),
]