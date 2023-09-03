from django.urls import path

import accounts.views

urlpatterns = [

    path('register/', accounts.views.register_page, name='register'),
    path('login/', accounts.views.login_page, name='login'),
    path('logout/', accounts.views.logout_user, name='logout'),
    path('profile/', accounts.views.profile_page, name='profile'),
]