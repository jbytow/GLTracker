from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput

from .models import Profile, WeightRecord, FoodDailyRequirements, FoodLogFoodItem, FoodLogMeal


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


class FoodDailyRequirementsForm(forms.ModelForm):
    class Meta:
        model = FoodDailyRequirements
        fields = ['calories', 'carbohydrates', 'fats', 'proteins']


class DateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        initial_date = kwargs.pop('initial_date', None)
        super().__init__(*args, **kwargs)
        if initial_date:
            self.fields['date'].initial = initial_date


class FoodLogFoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodLogFoodItem
        fields = ['food_item', 'quantity']


class FoodLogMealForm(forms.ModelForm):
    class Meta:
        model = FoodLogMeal
        fields = ['meal', 'quantity']
