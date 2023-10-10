from django.urls import path

import accounts.views

urlpatterns = [

    path('register/', accounts.views.register_page, name='register'),
    path('activate/<uidb64>/<token>', accounts.views.activate, name='activate'),
    path('login/', accounts.views.login_page, name='login'),
    path('logout/', accounts.views.logout_user, name='logout'),
    path('profile/', accounts.views.profile_page, name='profile'),
    path('profile/password-change', accounts.views.password_change, name='password_change'),
    path('profile/password-reset', accounts.views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>', accounts.views.passwordResetConfirm, name='password_reset_confirm'),
    path('profile/delete/<int:weight_id>/', accounts.views.weight_delete, name='weight_delete'),
    path('food-log/', accounts.views.food_log, name='food_log'),
    path('food-log/delete-item/<int:item_id>/', accounts.views.food_log_item_delete, name='food_log_item_delete'),
]