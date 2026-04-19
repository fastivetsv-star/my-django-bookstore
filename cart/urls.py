from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
]