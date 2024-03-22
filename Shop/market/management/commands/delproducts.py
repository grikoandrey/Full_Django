from django.core.management.base import BaseCommand  # CommandError
from market.models import Product


class Command(BaseCommand):
    help = 'Осторожно! Данная команда удаляет все товары'

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all products? y/n')  # спрашиваем
        answer = input()  # считываем подтверждение

        if answer == 'y':  # в случае подтверждения действительно удаляем все товары
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully wiped products!'))
            return

        self.stdout.write(self.style.ERROR('Access denied'))
