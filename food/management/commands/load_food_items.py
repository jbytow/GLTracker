import csv

from django.core.management.base import BaseCommand
from food.models import FoodItem

from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = 'Loads food items from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                try:
                    kcal = Decimal(row['kcal'])
                    proteins = Decimal(row['proteins'])
                    carbohydrates = Decimal(row['carbohydrates'])
                    fats = Decimal(row['fats'])
                    glycemic_index = Decimal(row['glycemic_index'])
                    glycemic_load = Decimal(row['glycemic_load'])
                except (InvalidOperation, KeyError) as e:
                    error_message = f"Error processing product: {name}. Reason: {str(e)}"
                    raise ValueError(error_message)

                # Create new FoodItem object and save to the database
                food_item = FoodItem(
                    name=name,
                    kcal=kcal,
                    proteins=proteins,
                    carbohydrates=carbohydrates,
                    fats=fats,
                    glycemic_index=glycemic_index,
                    glycemic_load=glycemic_load,
                    user_id=None
                )
                food_item.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded food items from CSV'))
