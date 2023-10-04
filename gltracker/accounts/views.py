from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .forms import DateForm

from datetime import datetime

from .models import Profile, WeightRecord, FoodLog, FoodDailyRequirements, FoodLogMeal, FoodLogFoodItem
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

    # Handling the FoodDailyRequirementsForm
    try:
        daily_requirements_instance = FoodDailyRequirements.objects.get(user=request.user)
    except FoodDailyRequirements.DoesNotExist:
        daily_requirements_instance = None

    if 'submit_daily_requirements' in request.POST:
        daily_requirements_form = FoodDailyRequirementsForm(request.POST, instance=daily_requirements_instance)
        if daily_requirements_form.is_valid():
            daily_requirements = daily_requirements_form.save(commit=False)
            daily_requirements.user = request.user
            daily_requirements.save()
            return redirect('food_log')
    else:
        daily_requirements_form = FoodDailyRequirementsForm(instance=daily_requirements_instance)

    today = timezone.now().date()  # Get today's date

    # By default, set selected_date to today's date
    selected_date = today

    # If the selected date is stored in the session, set selected_date from the session
    if 'selected_date' in request.session:
        selected_date_str = request.session['selected_date']
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    # If the date form is submitted, update selected_date
    if 'submit_date' in request.POST:
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            selected_date = date_form.cleaned_data['date']
            request.session['selected_date'] = selected_date.strftime('%Y-%m-%d')  # save in session
            return redirect('food_log')
    else:
        date_form = DateForm(initial={'date': selected_date})  # Set the form with the selected date

    # Fetch or create FoodLog for the selected date
    food_log, created = FoodLog.objects.get_or_create(user=request.user, date=selected_date)

    # Calculate macronutrients
    total_macros = food_log.calculate_total_macros_log()

    # Fetch all FoodLogFoodItem and FoodLogMeal objects related to the food_log
    food_log_fooditems = FoodLogFoodItem.objects.filter(food_log=food_log)
    food_log_meals = FoodLogMeal.objects.filter(food_log=food_log)
    food_log_items = list(food_log_fooditems) + list(food_log_meals)
    food_log_items.sort(key=lambda x: x.id, reverse=True)

    # Handling the FoodItem form submission
    if 'submit_fooditem' in request.POST:
        fooditem_form = FoodLogFoodItemForm(request.POST, user=request.user)
        if fooditem_form.is_valid():
            food_item = fooditem_form.save(commit=False)
            food_item.food_log = food_log
            food_item.save()
            return redirect('food_log')
    else:
        fooditem_form = FoodLogFoodItemForm(user=request.user)

    # Handling the Meal form submission
    if 'submit_meal' in request.POST:
        meal_form = FoodLogMealForm(request.POST, user=request.user)
        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.food_log = food_log
            meal.save()
            return redirect('food_log')
    else:
        meal_form = FoodLogMealForm(user=request.user)

    return render(request, 'food_log.html',
                  {'daily_requirements_form': daily_requirements_form,
                   'date_form': date_form,
                   'selected_date': selected_date,
                   'food_log_items': food_log_items,
                   'total_macros': total_macros,
                   'fooditem_form': fooditem_form,
                   'meal_form': meal_form})


def food_log_item_delete(request, item_id):
    # Depending on whether the object is a FoodLogFoodItem or FoodLogMeal, you will need to apply the appropriate logic.
    try:
        item = FoodLogFoodItem.objects.get(pk=item_id)
    except FoodLogFoodItem.DoesNotExist:
        item = FoodLogMeal.objects.get(pk=item_id)

    item.delete()
    return redirect('food_log')

