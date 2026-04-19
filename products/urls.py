from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('check-stock/', views.async_check_stock, name='check_stock'),
]