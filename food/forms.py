from django import forms
from django.db.models import Q, Case, When, Value, IntegerField
from .models import FoodItem, MealItem, Meal


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        exclude = ['user', 'is_active']
        labels = {
            'kcal': 'Kcal (in 100g)',
            'carbohydrates': 'Carbohydrates (in 100g)',
            'fats': 'Fats (in 100g)',
            'proteins': 'Proteins (in 100g)',
            'glycemic_load': 'Glycemic Load (in 100g)'
        }
        widgets = {
            'glycemic_load': forms.NumberInput(attrs={
                'placeholder': "If no value is provided, it will be calculated automatically: "
                               "GL = GI x carbohydrates / 100"}),
        }


class MealItemForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['food_item', 'quantity']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food_item'].queryset = (
            FoodItem.objects.filter(Q(user=user, is_active=True) | Q(user__isnull=True))
            .annotate(
                sort_order=Case(
                    When(user__isnull=True, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
            .order_by('sort_order', 'name')
        )
        self.fields['food_item'].empty_label = None


class MealForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Recipe name"}))

    class Meta:
        model = Meal
        fields = ['name', 'image', 'description']

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
