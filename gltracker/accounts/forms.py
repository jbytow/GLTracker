from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput
from django.db.models import Q

from datetime import date
from django_select2.forms import ModelSelect2Widget
from captcha.fields import ReCaptchaField

from .models import Profile, WeightRecord, FoodDailyRequirements, FoodLogFoodItem, FoodLogMeal, FoodItem, Meal


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This e-mail address is already used.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height', 'target_weight']


class SetPasswordForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()


class WeightLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeightLogForm, self).__init__(*args, **kwargs)
        self.fields['entry_date'].initial = date.today()

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
        labels = {'calories': False,
                  'carbohydrates': False,
                  'fats': False,
                  'proteins': False}


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
        labels = {'food_item': False,
                  'quantity': False,
                  }

        widgets = {
            'food_item': ModelSelect2Widget(
                model=FoodItem,
                search_fields=['name__icontains'],
                dependent_fields={'user': 'user'},
                max_results=500,
                attrs={
                    'data-minimum-input-length': 0,
                    'data-placeholder': 'Select food to add to the food log',
                },
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super(FoodLogFoodItemForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['food_item'].queryset = FoodItem.objects.filter(Q(user=user, is_active=True) | Q(user__isnull=True))


class FoodLogMealForm(forms.ModelForm):
    class Meta:
        model = FoodLogMeal
        fields = ['meal', 'quantity']
        labels = {'meal': False,
                  'quantity': False,
                  }

        widgets = {
            'meal': ModelSelect2Widget(
                model=Meal,
                search_fields=['name__icontains'],
                dependent_fields={'user': 'user'},
                max_results=500,
                attrs={
                    'data-minimum-input-length': 0,
                    'data-placeholder': 'Select meal to add to the food log',
                },
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super(FoodLogMealForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['meal'].queryset = Meal.objects.filter(user=user).order_by('name')
