from django.urls import path
from .views import StartView, index, ProductListView, ProductCreateView
app_name = 'app'
urlpatterns = [
    path('', index, name='base'),
    path('start/', StartView.as_view(), name='start'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/create', ProductCreateView.as_view(), name='create'),
]
