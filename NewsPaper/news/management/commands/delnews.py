from django.core.management.base import BaseCommand  # CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Осторожно! Данная команда удалит все новости выбранной категории'

    def handle(self, *args, **options):
        # self.stdout.readable()
        category_code = input('Select a category to delete posts(POL/EDU/SPR/MUS): ').encode('utf-8').decode('utf-8')
        try:
            category = Category.objects.get(category=category_code)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('Category does not exist. Try again.'))
            return

        answer = input(f'Do you really want to delete all posts in {category.get_category_display()}? (Y/N): ')

        if answer == 'y':  # в случае подтверждения действительно удаляем все товары
            Post.objects.filter(post_category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully wiped posts in {category.get_category_display()}!'))
            return

        self.stdout.write(self.style.ERROR('Access denied'))
