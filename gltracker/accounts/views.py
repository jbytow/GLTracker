from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Profile, WeightRecord, FoodLog, FoodLogFoodItem, FoodLogMeal
from .forms import CreateUserForm, ProfileForm, WeightLogForm, \
    FoodDailyRequirementsForm, FoodLogFoodItemForm, FoodLogMealForm


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                Profile.objects.create(
                    user=user,
                    name=user.username,
                )

                messages.success(request, 'Account was successfully created')
                return redirect('login')
        else:
            form = CreateUserForm()

        context = {'form': form}
        return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required()
def profile_page(request):
    try:
        profile = Profile.objects.get(user=request.user)
        target_weight = profile.target_weight
    except Profile.DoesNotExist:
        profile = None
        target_weight = None

    if request.method == 'POST':
        weight_log_form = WeightLogForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=profile)

        if weight_log_form.is_valid():
            weight_log = weight_log_form.save(commit=False)
            weight_log.profile = Profile.objects.get(user=request.user)
            weight_log.save()
            return redirect('profile')

        if profile_form.is_valid():
            user_profile = profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')

    else:
        weight_log_form = WeightLogForm()
        profile_form = ProfileForm(instance=profile)

    user_weight_log = WeightRecord.objects.filter(profile__user=request.user).order_by('-entry_date')

    if user_weight_log:
        latest_weight = float(user_weight_log[0].weight)    # changed number to float for later conversion to m from cm
        height = profile.height
        bmi = round(latest_weight / ((height/100) ** 2), 2)
    else:
        bmi = None

    serialized_data = [{'weight': record.weight, 'entry_date': record.entry_date.strftime('%Y-%m-%d')} for record in
                       user_weight_log]

    paginator = Paginator(user_weight_log, 10)

    page = request.GET.get('page')

    try:
        user_weight_log = paginator.page(page)
    except PageNotAnInteger:
        user_weight_log = paginator.page(1)
    except EmptyPage:
        user_weight_log = paginator.page(paginator.num_pages)

    return render(request, 'profile.html', {
        'user_weight_log': user_weight_log,
        'height': height,
        'latest_weight': latest_weight,
        'bmi': bmi,
        'target_weight': target_weight,
        'weight_log_form': weight_log_form,
        'profile_form': profile_form,
        'weight_data': serialized_data
    })


@login_required()
def weight_delete(request, weight_id):
    weight = get_object_or_404(WeightRecord, id=weight_id)

    if request.method == 'POST':
        weight.delete()
        return redirect('profile')

    return redirect('profile')


@login_required
def food_log(request):
    # Pobierz wszystkie dzienniki żywieniowe użytkownika, posortowane od najnowszego do najstarszego.
    food_logs = FoodLog.objects.filter(user=request.user).order_by('-date')

    # Paginacja: Wybierz stronę i ilość elementów na stronę
    page = request.GET.get('page')
    items_per_page = 10

    # Oblicz daty na podstawie których będziemy wykonywać paginację
    dates = [food_log.date for food_log in food_logs]
    num_pages = len(dates) // items_per_page + (1 if len(dates) % items_per_page > 0 else 0)

    # Jeśli użytkownik nie wybrał konkretnej strony, przekieruj go na pierwszą stronę
    if not page:
        return redirect('food-log', page=1)

    try:
        page = int(page)
    except ValueError:
        page = 1

    if page < 1:
        page = 1
    elif page > num_pages:
        page = num_pages

    # Wybierz daty dla danej strony
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    # Sprawdź, czy end_idx nie przekracza długości listy dates
    if end_idx > len(dates):
        end_idx = len(dates)

    displayed_dates = dates[start_idx:end_idx]

    # Jeśli użytkownik nie ma dziennika żywieniowego na daną datę, stwórz go automatycznie
    for date in displayed_dates:
        if not FoodLog.objects.filter(user=request.user, date=date).exists():
            food_log = FoodLog.objects.create(user=request.user, date=date)

    # Pobierz dzienniki żywieniowe na podstawie daty dla danej strony
    food_logs = FoodLog.objects.filter(user=request.user, date__in=displayed_dates).order_by('-date')



    # Oblicz całkowite makroskładniki dla aktualnego dziennika żywieniowego
    current_food_log = None  # Zainicjuj zmienną current_food_log jako None

    # Sprawdź, czy displayed_dates nie jest puste
    if displayed_dates:
        current_food_log = FoodLog.objects.filter(user=request.user, date=displayed_dates[0]).first()

    # Oblicz całkowite makroskładniki dla aktualnego dziennika żywieniowego, jeśli istnieje
    if current_food_log:
        total_macros = current_food_log.calculate_total_macros_log()
    else:
        total_macros = {}

    # Obsługa formularzy
    if request.method == 'POST':
        food_log_food_item_form = FoodLogFoodItemForm(request.POST)
        food_log_meal_form = FoodLogMealForm(request.POST)

        if food_log_food_item_form.is_valid():
            # Utwórz instancję FoodLogFoodItem z datą FoodLog i zapisz
            food_log_food_item = food_log_food_item_form.save(commit=False)
            food_log_food_item.food_log = current_food_log  # Przypisz odpowiednie FoodLog
            food_log_food_item.save()
            messages.success(request, 'Food items added successfully.')
            return redirect('food-log')

        if food_log_meal_form.is_valid():
            # Utwórz instancję FoodLogMeal z datą FoodLog i zapisz
            food_log_meal = food_log_meal_form.save(commit=False)
            food_log_meal.food_log = current_food_log  # Przypisz odpowiednie FoodLog
            food_log_meal.save()
            messages.success(request, 'Meals added successfully.')
            return redirect('food-log')
    else:
        food_log_food_item_form = FoodLogFoodItemForm()
        food_log_meal_form = FoodLogMealForm()

    return render(request, 'food_log.html', {
        'food_logs': food_logs,
        'food_log_food_item_form': food_log_food_item_form,
        'food_log_meal_form': food_log_meal_form,
        'total_macros': total_macros,
        'page': page,
        'num_pages': num_pages,
    })