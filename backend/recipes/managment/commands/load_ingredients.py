import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из data/ingredients.json'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка тегов...')
        tags_data = [
            {'name': 'Завтрак', 'slug': 'breakfast'},
            {'name': 'Обед', 'slug': 'lunch'},
            {'name': 'Ужин', 'slug': 'dinner'},
        ]
        for tag in tags_data:
            Tag.objects.get_or_create(**tag)

        path = os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {path}'))
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            ingredients = [
                Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                ) for item in data
            ]
            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            f'Загрузка завершена! Ингредиентов в базе: {Ingredient.objects.count()}'
        ))
