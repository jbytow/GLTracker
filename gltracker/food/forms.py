from django import forms
from .models import FoodItem, MealItem, Meal


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        exclude = ['user']


class MealItemForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['food_item', 'quantity']


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


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['food_item', 'quantity']


class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Recipe name"}))

    class Meta:
        model = Meal
        fields = ['name', 'image']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # django-crispy-forms
            for field in self.fields:
                new_data = {
                    "placeholder": f'Meal{str(field)}',
                    "class": 'form-control'
                }
                self.fields[str(field)].widget.attrs.update(
                    new_data
                )
