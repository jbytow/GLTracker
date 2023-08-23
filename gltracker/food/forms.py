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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food_item'].queryset = FoodItem.objects.filter(user=user) | FoodItem.objects.filter(user=None)


class MealForm(forms.ModelForm):
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
