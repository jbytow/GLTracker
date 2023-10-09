from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages import get_messages

from datetime import date
from unittest.mock import patch

from .models import Profile, WeightRecord, FoodDailyRequirements, FoodLog, FoodLogFoodItem, FoodLogMeal
from food.models import Meal, FoodItem


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, name='Test User', height=170, target_weight=65.5)
        self.assertEqual(profile.name, 'Test User')


class WeightRecordTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, name='Test User')

    def test_weight_record(self):
        weight_record = WeightRecord.objects.create(profile=self.profile, weight=70.5, entry_date='2022-09-28')
        self.assertEqual(str(weight_record), 'testuser - 2022-09-28')


class FoodDailyRequirementsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')

    def test_food_daily_requirements(self):
        food_daily_req = FoodDailyRequirements.objects.create(user=self.user, calories=2000, carbohydrates=250, fats=70, proteins=50)
        self.assertEqual(str(food_daily_req), 'Daily Requirements for testuser')


class FoodLogTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.food_item = FoodItem.objects.create(name='Test Food', kcal=100, carbohydrates=20, fats=5, proteins=10)
        self.meal = Meal.objects.create(name='Test Meal', user=self.user)

    def test_food_log(self):
        food_log = FoodLog.objects.create(user=self.user, date='2022-09-28')
        food_log.foods.add(self.food_item)
        food_log.meals.add(self.meal)
        self.assertEqual(str(food_log), "testuser's Food Log - 2022-09-28")


class FoodLogFoodItemTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.food_log = FoodLog.objects.create(user=self.user, date='2022-09-28')
        self.food_item = FoodItem.objects.create(name='Test Food', kcal=100, carbohydrates=20, fats=5, proteins=10)

    def test_food_log_food_item(self):
        food_log_item = FoodLogFoodItem.objects.create(food_log=self.food_log, food_item=self.food_item, quantity=150)
        self.assertEqual(food_log_item.get_name(), 'Test Food')
        self.assertEqual(food_log_item.get_calories(), 150)


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='password', email='test@email.com')
        self.profile = Profile.objects.create(user=self.user, name='testuser')

    def test_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_password_change_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'password',
            'new_password1': 'NewComplexP@ssw0rd!',
            'new_password2': 'NewComplexP@ssw0rd!'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your password has been changed')

    def test_weight_delete_view(self):
        weight = WeightRecord.objects.create(profile=self.profile, weight=70, entry_date=date.today())
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('weight_delete', args=[weight.id]))
        self.assertEqual(response.status_code, 302)  # redirection to profile
        self.assertFalse(WeightRecord.objects.filter(pk=weight.id).exists())  # Check if weight record was deleted


class UserFoodLogViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='password', email='test@email.com')

    def test_food_log_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('food_log'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_log.html')

    def test_food_log_item_delete_view(self):
        food_log = FoodLog.objects.create(user=self.user, date='2023-09-27')

        food_item = FoodItem.objects.create(
            name="test food",
            kcal=100,
            carbohydrates=10,
            fats=10,
            proteins=10,
            glycemic_index=50
        )

        food_log_item = FoodLogFoodItem.objects.create(
            food_log=food_log,
            food_item=food_item,
            quantity=100
        )

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('food_log_item_delete', args=[food_log_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FoodLogFoodItem.objects.filter(
            pk=food_log_item.id).exists())


