from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.forms import authenticate
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .models import Profile


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
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

        context = {'form': form}
        return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}

        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')
