from django.urls import path

import accounts.views

urlpatterns = [

    path('register/', accounts.views.register_page, name='register'),
    path('login/', accounts.views.login_page, name='login'),
]