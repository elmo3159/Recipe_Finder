import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Import ingredients from a CSV file and delete existing data'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # 既存のデータを削除
        Ingredient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted existing data from Ingredient table'))

        # CSVファイルからデータを読み込み、データベースに保存
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Ingredient.objects.create(name=row['name'])
                self.stdout.write(self.style.SUCCESS(f"Imported ingredient: {row['name']}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported ingredients from CSV file'))
