from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput

from .models import Profile, WeightRecord, FoodDailyRequirements


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height', 'target_weight']


class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['entry_date', 'weight']
        widgets = {
            'entry_date': DateInput(attrs={'type': 'date'}),
        }


class DailyRequirementsForm(forms.ModelForm):
    class Meta:
        model = FoodDailyRequirements  # Zmiana modelu na FoodDailyRequirements
        fields = ['calories', 'carbohydrates', 'fats', 'proteins']