from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm


def index(request):
    return render(request, "index.html")


def fooditem_list(request):
    food_items = FoodItem.objects.all()
    return render(request, 'fooditem_list.html', {'food_items': food_items})


@login_required
def add_fooditem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            fooditem = form.save(commit=False)
            fooditem.user = request.user
            fooditem.save()
            return redirect('my_food_items')
    else:
        form = FoodItemForm()
    return render(request, 'add_fooditem.html', {'form': form})


@login_required
def my_food_items(request):
    food_items = FoodItem.objects.filter(user=request.user)
    return render(request, 'my_food_items.html', {'food_items': food_items})