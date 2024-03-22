# from datetime import datetime
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.core.cache import cache
# from django.views.decorators.cache import cache_page

from .forms import ProductForm
from .models import Product, Category, Subscription
from .filters import ProductFilter


# Create your views here.
class ProductsList(ListView):
    model = Product  # Указываем модель, объекты которой мы будем выводить
    ordering = 'name'  # Поле, которое будет использоваться для сортировки объектов
    # queryset = Product.objects.filter(price__lt=300)
    template_name = 'products.html'  # Указываем имя шаблона, в котором будут все инструкции как показать
    context_object_name = 'products'  # Это имя списка, в котором будут лежать все объекты.
    paginate_by = 5  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Product  # Модель всё та же, но мы хотим получать информацию по отдельному товару
    template_name = 'product.html'  # Используем другой шаблон — product.html
    context_object_name = 'product'  # Название объекта, в котором будет выбранный пользователем продукт

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs['pk']}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs['pk']}', obj)
        return obj

# def create_product(request):  # заменяем данную функцию на класс для использования объектов
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/products/')
#     return render(request, 'product_create.html', {'form': form})


class ProductCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # raise_exception = True  # добавляем вывод ошибки на страницу для не авторизованных пользователей
    permission_required = ('market.add_product',)  # добавляем доступ на добавление
    form_class = ProductForm  # Указываем нашу разработанную форму
    model = Product  # модель товаров
    template_name = 'product_create.html'  # и новый шаблон, в котором используется форма.


# Добавляем представление для изменения товара.
class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('market.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_create.html'


# Представление удаляющее товар.
class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('market.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user,
                                        category=category, ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(request,
                  'subscriptions.html',
                  {'categories': categories_with_subscriptions}, )
