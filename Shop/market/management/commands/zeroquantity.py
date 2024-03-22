from django.core.management.base import BaseCommand  # CommandError
from market.models import Product


class Command(BaseCommand):
    help = 'Данная команда обнуляет колчество всех товаров'
    # missing_args_message = 'Недостаточно аргументов'
    # requires_migrations_checks = True  # напоминать ли о миграциях.
    #
    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.quantity = 0
            product.save()

            self.stdout.write(self.style.SUCCESS(f'Обнуление количества {product.name} выполнено'))
