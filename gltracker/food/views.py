from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.http import HttpResponseForbidden
from django.forms import formset_factory, modelformset_factory

from .models import FoodItem, Meal, MealItem
from .forms import FoodItemForm, MealItemForm, MealForm, RecipeForm, RecipeIngredientForm


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
def add_meal(request, id=None):
    MealItemFormSet = formset_factory(MealItemForm, extra=1)

    if request.method == 'POST':
        form = MealForm(request.user, request.POST, request.FILES)
        formset = MealItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            meal = form.save()
            for form in formset:
                meal_item = form.save(commit=False)
                meal_item.meal = meal
                meal_item.save()

            return redirect('meal_list')

    else:
        form = MealForm(user=request.user)
        formset = MealItemFormSet()

    return render(request, 'add_update_meal.html', {'form': form, 'formset': formset})


def recipe_update_view(request, id=None):
    obj = get_object_or_404(Meal, id=id, user=request.user)
    RecipeIngredientFormset = modelformset_factory(MealItem, form=RecipeIngredientForm, extra=0)
    qs = obj.mealitem_set.all()
    form = RecipeForm(request.POST or None, instance = obj)
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save()
        #formset.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = 'Data saved.'
    return render(request, "add_update_meal.html", context)

