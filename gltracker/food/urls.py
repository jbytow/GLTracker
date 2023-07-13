from django.urls import path

import food.views

urlpatterns = [

    path('add_fooditem/', food.views.add_fooditem, name='add_fooditem'),
    path('fooditem_list/', food.views.fooditem_list, name='fooditem_list'),
    path('food_item/delete/<int:food_item_id>/', food.views.FoodItemDeleteView.as_view(), name='delete_food_item'),
    path('meals/', food.views.meal_list, name='meal_list'),

]