from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import FoodItem, Meal
from .forms import FoodItemForm


def index(request):
    return render(request, "index.html")


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
