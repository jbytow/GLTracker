from django.urls import path

import food.views

urlpatterns = [

    path('fooditem_add/', food.views.fooditem_add, name='fooditem_add'),
    path('fooditem_list/', food.views.fooditem_list, name='fooditem_list'),
    path('fooditem/delete/<int:food_item_id>/', food.views.fooditem_delete, name='fooditem_delete'),
    path('meals/', food.views.meal_list, name='meal_list'),
    path('meals/<int:meal_id>', food.views.meal_details, name='meal_details'),
    path('meals/add/', food.views.meal_create_update, name='add_meal'),
    path('meals/<int:id>/edit/', food.views.meal_create_update, name='edit_meal'),

]