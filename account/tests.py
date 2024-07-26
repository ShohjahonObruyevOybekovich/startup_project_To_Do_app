# myapp/management/commands/test_cache.py

from django.core.cache import cache
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test cache functionality'

    def handle(self, *args, **kwargs):
        test_key = 'test_key'
        test_value = 'test_value'
        cache.set(test_key, test_value, timeout=300)
        cached_value = cache.get(test_key)
        self.stdout.write(self.style.SUCCESS(f'Cached value: {cached_value}'))
