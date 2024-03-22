from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache

from resources import POSITIONS


# Create your models here.
class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'
    nobody = 'NB'

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default="nobody")
    labor_contract = models.IntegerField()

    def get_last_name(self):
        last_name = self.full_name.split()
        if len(last_name) >= 1:
            return last_name[0]
        else:
            return None


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)],)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[MinValueValidator(0.0)],)
    composition = models.TextField(default="Ingredients not specified")

    def __str__(self):
        return f'{self.name.title()}: {self.description[:15]}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class Category(models.Model):   # Категория, к которой будет привязываться товар
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions')


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    @property
    def get_duration(self):
        now = datetime.now()
        if self.complete and self.time_out:
            return (self.time_out - self.time_in).total_seconds()
        else:
            return (now - self.time_in).total_seconds()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self._amount
