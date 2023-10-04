from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory

from .models import FoodItem, Meal, MealItem
from .forms import FoodItemForm, MealItemForm, MealForm


@login_required()
def fooditem_list(request):
    public_items = FoodItem.objects.filter(user=None)  # Default, database fooditems
    user_items = FoodItem.objects.filter(user=request.user, is_active=True)  # User fooditems

    context = {
        'public_items': public_items,
        'user_items': user_items,
    }

    return render(request, 'fooditem_list.html', context)


@login_required
def fooditem_add(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            fooditem = form.save(commit=False)
            fooditem.user = request.user
            fooditem.save()

            messages.success(request, 'Food item has been added!')

            return redirect('fooditem_add')
    else:
        form = FoodItemForm()
    return render(request, 'add_fooditem.html', {'form': form})


def fooditem_delete(request, food_item_id):   # doesn't really delete but change record to inactive
    food_item = get_object_or_404(FoodItem, id=food_item_id)

    if request.method == 'POST':
        food_item.is_active = False
        food_item.save()
        return redirect('fooditem_list')

    return redirect('fooditem_list')


@login_required()
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
def meal_details(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.user != meal.user:
        return HttpResponseForbidden("You do not have permission to view this meal.")

    meal_macros = meal.calculate_total_macros_meal()

    meal_items = meal.mealitem_set.all()

    message = request.session.pop('message', None)

    return render(request, 'meal_details.html', {
        'meal': meal,
        'meal_macros': meal_macros,
        'meal_items': meal_items,
        'message': message})


@login_required()
def meal_create_update(request, id=None):
    if id:
        obj = get_object_or_404(Meal, id=id, user=request.user)
    else:
        obj = None

    form = MealForm(request.POST or None, request.FILES or None, instance=obj)
    MealItemFormset = modelformset_factory(
        MealItem,
        form=MealItemForm,
        extra=0,
        can_delete=True,
    )

    if obj:
        qs = obj.mealitem_set.all()
    else:
        qs = MealItem.objects.none()

    formset = MealItemFormset(request.POST or None, form_kwargs={'user': request.user}, queryset=qs)

    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }

    if request.method == 'POST':
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            parent.user = request.user
            parent.save()
            for form in formset:
                child = form.save(commit=False)
                child.meal = parent
                child.save()

            for deleted_form in formset.deleted_forms:
                if deleted_form.instance.pk is not None:
                    deleted_form.instance.delete()

            request.session['message'] = 'Data Saved'

            return redirect('meal_details', meal_id=parent.id)

    return render(request, "add_update_meal.html", context)


@login_required()
def meal_delete(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)

    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')

    return redirect('meal_list')
