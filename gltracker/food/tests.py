from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import FoodItem, Meal, MealItem
from .forms import FoodItemForm, MealForm, MealItemForm

from decimal import Decimal


class FoodItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.food = FoodItem.objects.create(name="Test Food", user=self.user)

    def test_fooditem_creation(self):
        self.assertTrue(isinstance(self.food, FoodItem))
        self.assertEqual(self.food.__str__(), "Test Food")

    def test_calculate_glycemic_load(self):
        self.food.carbohydrates = 100
        self.food.glycemic_index = 50
        self.food.save()
        self.assertEqual(self.food.calculate_glycemic_load(), 50)


class MealModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.food = FoodItem.objects.create(
            name="Test Food",
            user=self.user,
            kcal=200,
            carbohydrates=50,
            fats=10,
            proteins=20,
            glycemic_index=70
        )
        self.meal = Meal.objects.create(name="Test Meal", user=self.user)
        self.meal_item = MealItem.objects.create(meal=self.meal, food_item=self.food, quantity=2)

    def test_meal_creation(self):
        self.assertTrue(isinstance(self.meal, Meal))
        self.assertEqual(self.meal.__str__(), "Test Meal")

    def test_calculate_total_macros_meal(self):
        macros = self.meal.calculate_total_macros_meal()

        expected_kcal = Decimal(2/100 * self.food.kcal).quantize(Decimal('0.00'))
        self.assertEqual(macros['total_kcal'].quantize(Decimal('0.00')), expected_kcal)

        expected_carbs = Decimal(2/100 * self.food.carbohydrates).quantize(Decimal('0.00'))
        self.assertEqual(macros['total_carbohydrates'].quantize(Decimal('0.00')), expected_carbs)

        expected_fats = Decimal(2/100 * self.food.fats).quantize(Decimal('0.00'))
        self.assertEqual(macros['total_fats'].quantize(Decimal('0.00')), expected_fats)

        expected_proteins = Decimal(2/100 * self.food.proteins).quantize(Decimal('0.00'))
        self.assertEqual(macros['total_proteins'].quantize(Decimal('0.00')), expected_proteins)

        expected_glycemic_load = Decimal(2/100 * self.food.calculate_glycemic_load()).quantize(Decimal('0.00'))
        self.assertEqual(macros['total_glycemic_load'].quantize(Decimal('0.00')), expected_glycemic_load)


class MealItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.food = FoodItem.objects.create(name="Test Food", user=self.user)
        self.meal = Meal.objects.create(name="Test Meal", user=self.user)
        self.meal_item = MealItem.objects.create(meal=self.meal, food_item=self.food, quantity=2)

    def test_mealitem_creation(self):
        self.assertTrue(isinstance(self.meal_item, MealItem))
        self.assertEqual(self.meal_item.__str__(), "Test Food - Test Meal")


class FoodAppModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.food1 = FoodItem.objects.create(name="Rice", kcal=100, carbohydrates=20, user=self.user)
        self.food2 = FoodItem.objects.create(name="Chicken", kcal=150, proteins=25, user=self.user)

        self.meal = Meal.objects.create(name="Lunch", user=self.user)
        MealItem.objects.create(meal=self.meal, food_item=self.food1, quantity=100)
        MealItem.objects.create(meal=self.meal, food_item=self.food2, quantity=50)

    def test_fooditem_creation(self):
        self.assertEqual(self.food1.name, "Rice")
        self.assertEqual(self.food1.kcal, 100)
        self.assertEqual(self.food1.carbohydrates, 20)

    def test_meal_creation(self):
        self.assertEqual(self.meal.name, "Lunch")
        self.assertEqual(self.meal.user, self.user)

    def test_mealitem_creation(self):
        meal_item = MealItem.objects.get(food_item=self.food1)
        self.assertEqual(meal_item.quantity, 100)
        self.assertEqual(meal_item.meal.name, "Lunch")

    def test_glycemic_load_calculation(self):
        self.assertEqual(self.food1.calculate_glycemic_load(), 0)

        self.food1.glycemic_index = 70
        self.food1.save()
        self.assertEqual(self.food1.calculate_glycemic_load(), 14)  # 20 * 70 / 100 = 14

    def test_meal_macros_calculation(self):
        macros = self.meal.calculate_total_macros_meal()
        expected_kcal = (100 * self.food1.kcal + 50 * self.food2.kcal) / 100
        self.assertEqual(macros['total_kcal'], expected_kcal)
        expected_proteins = (50 * self.food2.proteins) / 100
        self.assertEqual(macros['total_proteins'], expected_proteins)


class FoodItemViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.food_item = FoodItem.objects.create(name='Apple', user=self.user, is_active=True)

    def test_fooditem_list_view(self):
        response = self.client.get(reverse('fooditem_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')
        self.assertTemplateUsed(response, 'fooditem_list.html')

    def test_fooditem_add_view_POST_valid_data(self):
        data = {'name': 'Banana',
                'kcal': '92',
                'carbohydrates': '22',
                'fats': '0.2',
                'proteins': '1',
                'glycemic_index': '50',
                }
        response = self.client.post(reverse('fooditem_add'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FoodItem.objects.filter(name='Banana').exists())

    def test_fooditem_delete_view_POST(self):
        response = self.client.post(reverse('fooditem_delete', args=[self.food_item.id]))
        self.assertEqual(response.status_code, 302)
        self.food_item.refresh_from_db()
        self.assertFalse(self.food_item.is_active)


class MealViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.meal = Meal.objects.create(name='Lunch', user=self.user)

    def test_meal_list_view(self):
        response = self.client.get(reverse('meal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lunch')
        self.assertTemplateUsed(response, 'meal_list.html')

    def test_meal_details_view_ownership(self):
        another_user = User.objects.create_user(username='anotheruser', password='testpass')
        another_meal = Meal.objects.create(name='Another Lunch', user=another_user)
        response = self.client.get(reverse('meal_details', args=[another_meal.id]))
        self.assertEqual(response.status_code, 403)

    def test_meal_delete_view_POST(self):
        response = self.client.post(reverse('meal_delete', args=[self.meal.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Meal.DoesNotExist):
            self.meal.refresh_from_db()