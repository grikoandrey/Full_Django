from django.shortcuts import render
from .models import Book


# Create your views here.
def index(request):
    book1 = Book(name='Django book', author_name='Dronov')
    # book_get = Book.objects.get(id=1)
    return render(request, 'index.html', context={'book': book1})
