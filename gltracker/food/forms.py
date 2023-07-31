from django import forms
from .models import FoodItem, Meal, MealItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        exclude = ['user']


class MealItemForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['food_item', 'quantity']


MealItemFormSet = forms.inlineformset_factory(Meal, MealItem, form=MealItemForm, extra=1, can_delete=True)


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'image']

    def __init__(self, user=None, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        meal = super(MealForm, self).save(commit=False)
        if self.user:
            meal.user = self.user
        if commit:
            meal.save()
        return meal