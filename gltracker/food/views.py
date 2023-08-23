from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory

from .models import FoodItem, Meal, MealItem
from .forms import FoodItemForm, MealItemForm, MealForm


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
def meal_details_view(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.user != meal.user:
        return HttpResponseForbidden("You do not have permission to view this meal.")

    meal_details = meal.calculate_total_macros()

    return render(request, 'meal_details.html', {'meal': meal, 'meal_details': meal_details})


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
        qs_user = obj.mealitem_set.filter(user=request.user)
        qs_list = obj.mealitem_set.filter(user=None)
    else:
        qs_user = MealItem.objects.none()
        qs_list = MealItem.objects.none()

    formset = MealItemFormset(request.POST or None, form_kwargs={'user': request.user}, queryset=qs_user | qs_list)

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

            context['message'] = 'Data saved.'

    return render(request, "add_update_meal.html", context)