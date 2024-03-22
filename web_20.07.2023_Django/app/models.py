from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=15)
    author_name = models.CharField(max_length=15)

    def __str__(self):
        return f'Book name: {self.name},\nAuthor: {self.author_name}'
