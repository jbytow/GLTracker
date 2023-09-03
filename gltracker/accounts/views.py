from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, WeightLogForm
from .models import Profile, Weight


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


def profile_page(request):
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_log = form.save(commit=False)
            weight_log.profile = request.user.profile
            weight_log.save()
    else:
        form = WeightLogForm()

    user_weight_log = Weight.objects.filter(profile__user=request.user)

    return render(request, 'profile.html', {
        'user_weight_log': user_weight_log,
        'form': form,
    })