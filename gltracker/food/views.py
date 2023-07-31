from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.http import HttpResponseForbidden

import logging

from .models import FoodItem, Meal
from .forms import FoodItemForm, MealForm, MealItemFormSet


def index(request):
    return render(request, "index.html")


@login_required()
def fooditem_list(request):
    public_items = FoodItem.objects.filter(user=None)  # Default, database fooditems
    user_items = FoodItem.objects.filter(user=request.user)  # User fooditems

    context = {
        'public_items': public_items,
        'user_items': user_items,
    }

    return render(request, 'fooditem_list.html', context)


@login_required
def add_fooditem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            fooditem = form.save(commit=False)
            fooditem.user = request.user
            fooditem.save()
            return redirect('fooditem_list')
    else:
        form = FoodItemForm()
    return render(request, 'add_fooditem.html', {'form': form})


class FoodItemDeleteView(View):
    def post(self, request, food_item_id):
        food_item = get_object_or_404(FoodItem, id=food_item_id)
        food_item.delete()
        return redirect('fooditem_list')


def meal_list(request):
    meals = Meal.objects.filter(user=request.user)

    paginator = Paginator(meals, 4)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'meal_list.html', {'meals': meals, 'pages': pages})


@login_required()
def meal_details_view(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.user != meal.user:
        return HttpResponseForbidden("You do not have permission to view this meal.")

    meal_details = meal.calculate_total_macros()

    return render(request, 'meal_details.html', {'meal': meal, 'meal_details': meal_details})


@login_required()
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.user, request.POST, request.FILES)
        formset = MealItemFormSet(request.POST, instance=Meal())

        if form.is_valid() and formset.is_valid():
            meal = form.save()
            formset.instance = meal
            formset.save()

            return redirect('meal_list')

    else:
        form = MealForm(user=request.user)
        formset = MealItemFormSet(instance=Meal())

    return render(request, 'add_meal.html', {'form': form, 'formset': formset})

