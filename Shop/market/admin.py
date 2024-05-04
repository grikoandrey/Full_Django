from django.contrib import admin
from .models import Category, Product


# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_quantity(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из
    # них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы
    # выделили галочками.
    queryset.update(quantity=0)


nullfy_quantity.short_description = 'Обнулить товары'  # описание для более понятного представления в админ-панели
# задаётся, как будто это объект


class ProductAdmin(admin.ModelAdmin):  # новый класс для представления товаров в админке
    list_display = ('name', 'description', 'quantity', 'price', 'on_stock')
    list_filter = ('price', 'quantity', 'name')  # добавляем примитивные фильтры в админ
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_quantity]  # добавляем действия в список


#    list_display — это список со всеми полями, которые будут в таблице с товарами
#    list_display = [field.name for field in Product._meta.get_fields()]  # генерируем список всех полей для отображения


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # ProductAdmin
